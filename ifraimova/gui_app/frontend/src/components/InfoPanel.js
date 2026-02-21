const InfoPanel = ({ state, maxIterations }) => {
  return (
    <div className="right-panel">
      <div className="panel-section">
        <h3>📈 Progress</h3>
        {state ? (
          <>
            <div className="info-item">
              <span>Iteration:</span>
              <strong>
                {state.iteration} / {maxIterations}
              </strong>
            </div>
            <div className="info-item">
              <span>Best Fitness:</span>
              <strong>{state.best_fitness.toExponential(4)}</strong>
            </div>
            <div className="info-item">
              <span>PP Value:</span>
              <strong>{state.pp.toFixed(4)}</strong>
            </div>
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{ width: `${(state.iteration / maxIterations) * 100}%` }}
              />
            </div>
          </>
        ) : (
          <p className="no-data">No data</p>
        )}
      </div>

      <div className="panel-section">
        <h3>⭐ Best Solution</h3>
        {state?.best_position ? (
          <div className="solution-display">
            {state.best_position.map((val, idx) => (
              <div key={idx}>
                x{idx} = {val.toFixed(6)}
              </div>
            ))}
          </div>
        ) : (
          <p className="no-data">Not found yet</p>
        )}
      </div>
    </div>
  );
};

export default InfoPanel;
