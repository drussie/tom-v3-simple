"use client";

import type { ReactNode } from "react";
import { useEffect, useMemo, useRef, useState } from "react";

import { getApiBaseUrl } from "../lib/api";
import {
  currentTimeSecondsToFrame,
  currentTimeSecondsToTimestampMs,
  formatReplayTime
} from "../lib/replayTime";
import type { ReplayInfo, ReplayPlaybackState } from "../lib/types";

interface ReplayVideoPlayerProps {
  replayInfo: ReplayInfo;
  children?: ReactNode;
  onPlaybackStateChange?: (state: ReplayPlaybackState) => void;
}

export function ReplayVideoPlayer({
  replayInfo,
  children,
  onPlaybackStateChange
}: ReplayVideoPlayerProps) {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const animationFrameRef = useRef<number | null>(null);
  const [currentTimeSeconds, setCurrentTimeSeconds] = useState(0);
  const [durationSeconds, setDurationSeconds] = useState(
    replayInfo.duration_ms !== null ? replayInfo.duration_ms / 1000 : 0
  );

  const videoSource = useMemo(() => {
    if (replayInfo.video_url.startsWith("http")) {
      return replayInfo.video_url;
    }
    return `${getApiBaseUrl()}${replayInfo.video_url}`;
  }, [replayInfo.video_url]);

  useEffect(() => {
    const video = videoRef.current;
    if (video === null) {
      return;
    }

    const update = () => {
      const nextCurrentTimeSeconds = video.currentTime;
      const nextDurationSeconds = Number.isFinite(video.duration)
        ? video.duration
        : durationSeconds;
      setCurrentTimeSeconds(nextCurrentTimeSeconds);
      onPlaybackStateChange?.({
        currentTimeSeconds: nextCurrentTimeSeconds,
        timestampMs: currentTimeSecondsToTimestampMs(nextCurrentTimeSeconds),
        frameNumber: currentTimeSecondsToFrame(
          nextCurrentTimeSeconds,
          replayInfo.fps,
          replayInfo.frame_count
        ),
        durationSeconds: nextDurationSeconds
      });
    };
    const updateDuration = () => {
      if (Number.isFinite(video.duration)) {
        setDurationSeconds(video.duration);
      }
    };
    const tick = () => {
      update();
      animationFrameRef.current = window.requestAnimationFrame(tick);
    };
    const startTicking = () => {
      if (animationFrameRef.current === null) {
        animationFrameRef.current = window.requestAnimationFrame(tick);
      }
    };
    const stopTicking = () => {
      if (animationFrameRef.current !== null) {
        window.cancelAnimationFrame(animationFrameRef.current);
        animationFrameRef.current = null;
      }
      update();
    };

    video.addEventListener("loadedmetadata", updateDuration);
    video.addEventListener("timeupdate", update);
    video.addEventListener("play", startTicking);
    video.addEventListener("pause", stopTicking);
    video.addEventListener("ended", stopTicking);

    update();
    updateDuration();

    return () => {
      stopTicking();
      video.removeEventListener("loadedmetadata", updateDuration);
      video.removeEventListener("timeupdate", update);
      video.removeEventListener("play", startTicking);
      video.removeEventListener("pause", stopTicking);
      video.removeEventListener("ended", stopTicking);
    };
  }, [durationSeconds, onPlaybackStateChange, replayInfo.fps, replayInfo.frame_count]);

  const timestampMs = currentTimeSecondsToTimestampMs(currentTimeSeconds);
  const frameNumber = currentTimeSecondsToFrame(
    currentTimeSeconds,
    replayInfo.fps,
    replayInfo.frame_count
  );
  const progress =
    durationSeconds > 0 ? Math.max(0, Math.min(currentTimeSeconds / durationSeconds, 1)) : 0;

  return (
    <section className="panel replay-video-panel">
      <div className="panel-header">
        <h2>Video Replay</h2>
        <span className="mini-pill">nearest frame from media metadata</span>
      </div>
      <div className="panel-body replay-video-body">
        <div
          className="replay-video-frame"
          style={{
            aspectRatio:
              replayInfo.width !== null && replayInfo.height !== null
                ? `${replayInfo.width} / ${replayInfo.height}`
                : "16 / 9"
          }}
        >
          <video
            ref={videoRef}
            className="replay-video"
            controls
            preload="metadata"
            src={videoSource}
          />
          {children}
        </div>

        <div className="replay-telemetry-grid">
          <TelemetryCell label="time" value={formatReplayTime(currentTimeSeconds)} />
          <TelemetryCell label="timestamp_ms" value={timestampMs.toString()} />
          <TelemetryCell label="frame" value={frameNumber.toString()} />
          <TelemetryCell label="fps" value={replayInfo.fps?.toString() ?? "n/a"} />
          <TelemetryCell label="frame_count" value={replayInfo.frame_count?.toString() ?? "n/a"} />
        </div>

        <div className="replay-timeline-shell" aria-label="Replay timeline shell">
          <div className="replay-timeline-track">
            <div className="replay-timeline-progress" style={{ width: `${progress * 100}%` }} />
          </div>
          <div className="meta-line">
            <span>{formatReplayTime(currentTimeSeconds)}</span>
            <span>{formatReplayTime(durationSeconds)}</span>
          </div>
        </div>
      </div>
    </section>
  );
}

function TelemetryCell({ label, value }: { label: string; value: string }) {
  return (
    <div className="media-cell">
      <strong>{label}</strong>
      <span>{value}</span>
    </div>
  );
}
