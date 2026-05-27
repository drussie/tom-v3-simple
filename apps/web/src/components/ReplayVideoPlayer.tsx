"use client";

import type { ReactNode } from "react";
import { useEffect, useMemo, useRef, useState } from "react";

import { getApiBaseUrl } from "../lib/api";
import {
  currentTimeSecondsToFrame,
  currentTimeSecondsToTimestampMs,
  formatReplayTime
} from "../lib/replayTime";
import type { ReplayInfo, ReplayPlaybackState, ReplaySeekRequest } from "../lib/types";

interface ReplayVideoPlayerProps {
  replayInfo: ReplayInfo;
  children?: ReactNode;
  onPlaybackStateChange?: (state: ReplayPlaybackState) => void;
  seekRequest?: ReplaySeekRequest | null;
  streamLiveEdgeMs?: number | null;
  streamProxyMode?: boolean;
  onSeekPastLiveEdge?: () => void;
}

export function ReplayVideoPlayer({
  replayInfo,
  children,
  onPlaybackStateChange,
  seekRequest = null,
  streamLiveEdgeMs = null,
  streamProxyMode = false,
  onSeekPastLiveEdge
}: ReplayVideoPlayerProps) {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const animationFrameRef = useRef<number | null>(null);
  const streamLiveEdgeRef = useRef<number | null>(streamLiveEdgeMs);
  const streamProxyModeRef = useRef(streamProxyMode);
  const onSeekPastLiveEdgeRef = useRef(onSeekPastLiveEdge);
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
    streamLiveEdgeRef.current = streamLiveEdgeMs;
    streamProxyModeRef.current = streamProxyMode;
    onSeekPastLiveEdgeRef.current = onSeekPastLiveEdge;
  }, [onSeekPastLiveEdge, streamLiveEdgeMs, streamProxyMode]);

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
        durationSeconds: nextDurationSeconds,
        paused: video.paused
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
    const clampSeekToLiveEdge = () => {
      const liveEdgeMs = streamLiveEdgeRef.current;
      if (!streamProxyModeRef.current || liveEdgeMs === null) {
        return;
      }
      const liveEdgeSeconds = liveEdgeMs / 1000;
      if (video.currentTime > liveEdgeSeconds + 0.05) {
        video.currentTime = liveEdgeSeconds;
        onSeekPastLiveEdgeRef.current?.();
      }
    };

    video.addEventListener("loadedmetadata", updateDuration);
    video.addEventListener("timeupdate", update);
    video.addEventListener("play", startTicking);
    video.addEventListener("pause", stopTicking);
    video.addEventListener("ended", stopTicking);
    video.addEventListener("seeking", clampSeekToLiveEdge);

    update();
    updateDuration();

    return () => {
      stopTicking();
      video.removeEventListener("loadedmetadata", updateDuration);
      video.removeEventListener("timeupdate", update);
      video.removeEventListener("play", startTicking);
      video.removeEventListener("pause", stopTicking);
      video.removeEventListener("ended", stopTicking);
      video.removeEventListener("seeking", clampSeekToLiveEdge);
    };
  }, [
    durationSeconds,
    onPlaybackStateChange,
    replayInfo.fps,
    replayInfo.frame_count
  ]);

  useEffect(() => {
    const video = videoRef.current;
    if (video === null || seekRequest === null) {
      return;
    }
    const requestedTimestampMs =
      streamProxyMode && streamLiveEdgeMs !== null
        ? Math.min(seekRequest.timestampMs, streamLiveEdgeMs)
        : seekRequest.timestampMs;
    const nextTimeSeconds = Math.max(0, requestedTimestampMs / 1000);
    if (Math.abs(video.currentTime - nextTimeSeconds) > 0.01) {
      video.currentTime = nextTimeSeconds;
    }
  }, [seekRequest, streamLiveEdgeMs, streamProxyMode]);

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
          {streamProxyMode ? (
            <TelemetryCell
              label="live_edge_ms"
              value={streamLiveEdgeMs !== null ? Math.round(streamLiveEdgeMs).toString() : "n/a"}
            />
          ) : null}
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
