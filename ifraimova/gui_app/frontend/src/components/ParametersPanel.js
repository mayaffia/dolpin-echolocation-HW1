const ParametersPanel = ({
  functions,
  selectedFunction,
  setSelectedFunction,
  dimension,
  setDimension,
  populationSize,
  setPopulationSize,
  maxIterations,
  setMaxIterations,
  onInitialize,
}) => {
  return (
    <div className="panel-section">
      <h3>⚙️ Algorithm Parameters</h3>

      <label>Function:</label>
      <select
        value={selectedFunction}
        onChange={(e) => setSelectedFunction(e.target.value)}
      >
        {Object.entries(functions).map(([key, func]) => (
          <option key={key} value={key}>
            {func.name}
          </option>
        ))}
      </select>
      <div className="formula">{functions[selectedFunction]?.formula}</div>

      <label>Dimension: {dimension}</label>
      <input
        type="range"
        min="2"
        max="20"
        value={dimension}
        onChange={(e) => setDimension(parseInt(e.target.value))}
      />

      <label>Population Size: {populationSize}</label>
      <input
        type="range"
        min="5"
        max="100"
        value={populationSize}
        onChange={(e) => setPopulationSize(parseInt(e.target.value))}
      />

      <label>Max Iterations: {maxIterations}</label>
      <input
        type="range"
        min="10"
        max="500"
        value={maxIterations}
        onChange={(e) => setMaxIterations(parseInt(e.target.value))}
      />

      <button className="btn-primary" onClick={onInitialize}>
        Initialize
      </button>
    </div>
  );
};

export default ParametersPanel;
