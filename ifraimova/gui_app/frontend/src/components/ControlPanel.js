const ControlPanel = ({
  state,
  isRunning,
  onStart,
  onStep,
  onStop,
  onReset,
}) => {
  return (
    <div className="control-panel">
      <button
        className="btn-control btn-start"
        onClick={onStart}
        disabled={!state || isRunning}
      >
        ▶️ Start
      </button>
      <button
        className="btn-control btn-step"
        onClick={onStep}
        disabled={!state || isRunning}
      >
        ⏭️ Step
      </button>
      <button
        className="btn-control btn-stop"
        onClick={onStop}
        disabled={!isRunning}
      >
        ⏹️ Stop
      </button>
      <button className="btn-control btn-reset" onClick={onReset}>
        🔄 Reset
      </button>
    </div>
  );
};

export default ControlPanel;
