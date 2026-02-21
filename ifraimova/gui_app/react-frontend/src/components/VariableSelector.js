const VariableSelector = ({ dimension, selectedVars, onVarToggle }) => {
  return (
    <div className="panel-section">
      <h3>📊 Variables for Visualization</h3>
      <p className="hint">Select exactly 2 variables</p>
      <div className="checkbox-list">
        {Array.from({ length: dimension }, (_, i) => (
          <label key={i} className="checkbox-label">
            <input
              type="checkbox"
              checked={selectedVars.includes(i)}
              onChange={() => onVarToggle(i)}
            />
            <span>x{i}</span>
          </label>
        ))}
      </div>
    </div>
  );
};

export default VariableSelector;
