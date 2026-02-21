import React, { useState, useEffect } from "react";
import "./App.css";
import { useOptimization } from "./hooks/useOptimization";
import * as api from "./services/api";
import ParametersPanel from "./components/ParametersPanel";
import VariableSelector from "./components/VariableSelector";
import VariableSliders from "./components/VariableSliders";
import VisualizationPanel from "./components/VisualizationPanel";
import ControlPanel from "./components/ControlPanel";
import InfoPanel from "./components/InfoPanel";
import { buildPlotData, buildPlotLayout } from "./utils/plotBuilder";

function App() {
  const [functions, setFunctions] = useState({});
  const [selectedFunction, setSelectedFunction] = useState("sphere");

  const [dimension, setDimension] = useState(5);
  const [populationSize, setPopulationSize] = useState(20);
  const [maxIterations, setMaxIterations] = useState(50);

  const [selectedVars, setSelectedVars] = useState([0, 1]);
  const [sliderValues, setSliderValues] = useState({});
  const [showTrajectories, setShowTrajectories] = useState(true);

  const [plotData, setPlotData] = useState(null);

  const {
    state,
    isRunning,
    agentHistory,
    initialize,
    step,
    start,
    stop,
    reset,
  } = useOptimization();

  useEffect(() => {
    api
      .getFunctions()
      .then((funcs) => setFunctions(funcs))
      .catch((err) => console.error("Error loading functions:", err));
  }, []);

  useEffect(() => {
    const initial = {};
    for (let i = 0; i < dimension; i++) {
      initial[i] = 0;
    }
    setSliderValues(initial);
  }, [dimension]);

  useEffect(() => {
    if (state) {
      updateVisualization();
    }
  }, [state, selectedVars, sliderValues, showTrajectories]);

  const handleInitialize = async () => {
    const result = await initialize({
      functionName: selectedFunction,
      dimension,
      populationSize,
      maxIterations,
    });

    if (!result.success) {
      alert(result.error);
    }
  };

  const updateVisualization = async () => {
    if (!state || selectedVars.length !== 2) return;

    const fixedVars = {};
    for (let i = 0; i < dimension; i++) {
      if (!selectedVars.includes(i)) {
        fixedVars[i] = sliderValues[i];
      }
    }

    try {
      const gridData = await api.evaluateGrid({
        functionName: selectedFunction,
        fixedVars,
        varIndices: selectedVars,
        resolution: 50,
      });

      const traces = buildPlotData(
        gridData,
        state,
        selectedVars,
        showTrajectories,
        agentHistory,
        functions[selectedFunction]?.name || selectedFunction,
      );

      const layout = buildPlotLayout(
        functions[selectedFunction]?.name || selectedFunction,
        selectedVars,
        gridData.bounds,
      );

      setPlotData({ data: traces, layout });
    } catch (error) {
      console.error("Error updating visualization:", error);
    }
  };

  const handleVarCheckbox = (varIdx) => {
    if (selectedVars.includes(varIdx)) {
      setSelectedVars(selectedVars.filter((v) => v !== varIdx));
    } else {
      if (selectedVars.length < 2) {
        setSelectedVars([...selectedVars, varIdx]);
      } else {
        setSelectedVars([selectedVars[1], varIdx]);
      }
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>🐬 Dolphin Echolocation Optimization</h1>
        <p>Interactive Visualization of Metaheuristic Algorithm</p>
      </header>

      <div className="main-container">
        <div className="left-panel">
          <ParametersPanel
            functions={functions}
            selectedFunction={selectedFunction}
            setSelectedFunction={setSelectedFunction}
            dimension={dimension}
            setDimension={setDimension}
            populationSize={populationSize}
            setPopulationSize={setPopulationSize}
            maxIterations={maxIterations}
            setMaxIterations={setMaxIterations}
            onInitialize={handleInitialize}
          />

          <VariableSelector
            dimension={dimension}
            selectedVars={selectedVars}
            onVarToggle={handleVarCheckbox}
          />

          <VariableSliders
            dimension={dimension}
            sliderValues={sliderValues}
            setSliderValues={setSliderValues}
            selectedVars={selectedVars}
            functionBounds={functions[selectedFunction]?.bounds || [-100, 100]}
          />

          <div className="panel-section">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={showTrajectories}
                onChange={(e) => setShowTrajectories(e.target.checked)}
              />
              <span>Show Trajectories</span>
            </label>
          </div>
        </div>

        <div className="center-panel">
          <VisualizationPanel plotData={plotData} />

          <ControlPanel
            state={state}
            isRunning={isRunning}
            onStart={start}
            onStep={step}
            onStop={stop}
            onReset={reset}
          />
        </div>

        <InfoPanel state={state} maxIterations={maxIterations} />
      </div>
    </div>
  );
}

export default App;
