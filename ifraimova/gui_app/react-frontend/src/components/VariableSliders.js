const VariableSliders = ({
  dimension,
  sliderValues,
  setSliderValues,
  selectedVars,
  functionBounds,
}) => {
  return (
    <div className="panel-section">
      <h3>Variable Values</h3>
      {Array.from({ length: dimension }, (_, i) => (
        <div key={i} className="slider-group">
          <label>
            x{i}:{" "}
            <span className="slider-value">{sliderValues[i]?.toFixed(2)}</span>
          </label>
          <input
            type="range"
            min={functionBounds[0]}
            max={functionBounds[1]}
            step="0.1"
            value={sliderValues[i] || 0}
            onChange={(e) =>
              setSliderValues({
                ...sliderValues,
                [i]: parseFloat(e.target.value),
              })
            }
            disabled={selectedVars.includes(i)}
          />
        </div>
      ))}
    </div>
  );
};

export default VariableSliders;
