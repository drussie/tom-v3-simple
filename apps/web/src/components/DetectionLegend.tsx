export function DetectionLegend() {
  return (
    <div className="detection-legend" aria-label="Detection overlay legend">
      <span>
        <i className="legend-swatch ball" />
        ball
      </span>
      <span>
        <i className="legend-swatch player" />
        player
      </span>
      <span>
        <i className="legend-swatch selected" />
        selected
      </span>
    </div>
  );
}
