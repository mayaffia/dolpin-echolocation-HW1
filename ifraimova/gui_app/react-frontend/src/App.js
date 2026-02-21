import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';
import axios from 'axios';
import './App.css';

const API_URL = 'http://localhost:5000/api';

function App() {
  const [functions, setFunctions] = useState({});
  const [selectedFunction, setSelectedFunction] = useState('sphere');
  const [dimension, setDimension] = useState(5);
  const [populationSize, setPopulationSize] = useState(20);
  const [maxIterations, setMaxIterations] = useState(50);
  const [selectedVars, setSelectedVars] = useState([0, 1]);
  const [sliderValues, setSliderValues] = useState({});
  const [state, setState] = useState(null);
  const [plotData, setPlotData] = useState(null);
  const [isRunning, setIsRunning] = useState(false);
  const [showTrajectories, setShowTrajectories] = useState(true);
  const [agentHistory, setAgentHistory] = useState([]);

  // Load available functions
  useEffect(() => {
    axios.get(`${API_URL}/functions`)
      .then(res => setFunctions(res.data.functions))
      .catch(err => console.error('Error loading functions:', err));
  }, []);

  // Initialize sliders
  useEffect(() => {
    const initial = {};
    for (let i = 0; i < dimension; i++) {
      initial[i] = 0;
    }
    setSliderValues(initial);
  }, [dimension]);

  // Update visualization when state or sliders change
  useEffect(() => {
    if (state) {
      updateVisualization();
    }
  }, [state, selectedVars, sliderValues, showTrajectories]);

  const handleInitialize = async () => {
    try {
      const response = await axios.post(`${API_URL}/initialize`, {
        function: selectedFunction,
        dimension,
        population_size: populationSize,
        max_iterations: maxIterations
      });
      setState(response.data.state);
      setAgentHistory([response.data.state.agent_positions]);
    } catch (error) {
      console.error('Error initializing:', error);
      alert('Ошибка инициализации. Проверьте, что бэкенд запущен на порту 5000');
    }
  };

  const handleStep = async () => {
    try {
      const response = await axios.post(`${API_URL}/step`);
      if (response.data.status === 'success') {
        setState(response.data.state);
        setAgentHistory(prev => [...prev, response.data.state.agent_positions]);
      }
    } catch (error) {
      console.error('Error stepping:', error);
    }
  };

  const handleStart = () => {
    setIsRunning(true);
  };

  const handleStop = () => {
    setIsRunning(false);
  };

  const handleReset = async () => {
    try {
      await axios.post(`${API_URL}/reset`);
      setState(null);
      setAgentHistory([]);
      setIsRunning(false);
    } catch (error) {
      console.error('Error resetting:', error);
    }
  };

  // Auto-step when running
  useEffect(() => {
    if (isRunning && state && !state.completed) {
      const timer = setTimeout(() => {
        handleStep();
      }, 100);
      return () => clearTimeout(timer);
    } else if (state?.completed) {
      setIsRunning(false);
    }
  }, [isRunning, state]);

  const updateVisualization = async () => {
    if (!state || selectedVars.length !== 2) return;

    const fixedVars = {};
    for (let i = 0; i < dimension; i++) {
      if (!selectedVars.includes(i)) {
        fixedVars[i] = sliderValues[i];
      }
    }

    try {
      const response = await axios.post(`${API_URL}/evaluate_grid`, {
        function: selectedFunction,
        fixed_vars: fixedVars,
        var_indices: selectedVars,
        resolution: 50
      });

      const data = response.data;
      const traces = [];

      // Contour plot
      traces.push({
        type: 'contour',
        x: data.x,
        y: data.y,
        z: data.z,
        colorscale: 'Jet',
        contours: {
          coloring: 'heatmap'
        },
        colorbar: {
          title: 'f(x)',
          titleside: 'right'
        }
      });

      // Agent positions
      const agentX = state.agent_positions.map(pos => pos[selectedVars[0]]);
      const agentY = state.agent_positions.map(pos => pos[selectedVars[1]]);
      
      traces.push({
        type: 'scatter',
        mode: 'markers+text',
        x: agentX,
        y: agentY,
        text: agentX.map((_, i) => i.toString()),
        textposition: 'top center',
        marker: {
          size: 12,
          color: 'white',
          line: {
            color: 'black',
            width: 2
          }
        },
        name: 'Агенты'
      });

      // Best solution
      if (state.best_position) {
        traces.push({
          type: 'scatter',
          mode: 'markers',
          x: [state.best_position[selectedVars[0]]],
          y: [state.best_position[selectedVars[1]]],
          marker: {
            size: 18,
            color: 'yellow',
            symbol: 'star',
            line: {
              color: 'black',
              width: 2
            }
          },
          name: 'Лучшее решение'
        });
      }

      // Trajectories
      if (showTrajectories && agentHistory.length > 1) {
        const recentHistory = agentHistory.slice(-10);
        for (let agentIdx = 0; agentIdx < state.agent_positions.length; agentIdx++) {
          const trajectoryX = recentHistory.map(h => h[agentIdx][selectedVars[0]]);
          const trajectoryY = recentHistory.map(h => h[agentIdx][selectedVars[1]]);
          
          traces.push({
            type: 'scatter',
            mode: 'lines',
            x: trajectoryX,
            y: trajectoryY,
            line: {
              color: 'rgba(255, 255, 255, 0.3)',
              width: 1,
              dash: 'dash'
            },
            showlegend: false,
            hoverinfo: 'skip'
          });
        }
      }

      setPlotData({
        data: traces,
        layout: {
          title: `${functions[selectedFunction]?.name || selectedFunction} (x${selectedVars[0]} vs x${selectedVars[1]})`,
          xaxis: { title: `x${selectedVars[0]}`, range: [data.bounds[0], data.bounds[1]] },
          yaxis: { title: `x${selectedVars[1]}`, range: [data.bounds[0], data.bounds[1]] },
          autosize: true,
          paper_bgcolor: 'rgba(0,0,0,0)',
          plot_bgcolor: 'rgba(255,255,255,0.9)',
          font: { color: '#333' }
        }
      });
    } catch (error) {
      console.error('Error updating visualization:', error);
    }
  };

  const handleVarCheckbox = (varIdx) => {
    if (selectedVars.includes(varIdx)) {
      setSelectedVars(selectedVars.filter(v => v !== varIdx));
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
        <p>Интерактивная визуализация метаэвристического алгоритма</p>
      </header>

      <div className="main-container">
        {/* Left Panel - Parameters */}
        <div className="left-panel">
          <div className="panel-section">
            <h3>⚙️ Параметры алгоритма</h3>
            
            <label>Функция:</label>
            <select value={selectedFunction} onChange={(e) => setSelectedFunction(e.target.value)}>
              {Object.entries(functions).map(([key, func]) => (
                <option key={key} value={key}>{func.name}</option>
              ))}
            </select>
            <div className="formula">{functions[selectedFunction]?.formula}</div>

            <label>Размерность: {dimension}</label>
            <input type="range" min="2" max="20" value={dimension} 
                   onChange={(e) => setDimension(parseInt(e.target.value))} />

            <label>Размер популяции: {populationSize}</label>
            <input type="range" min="5" max="100" value={populationSize}
                   onChange={(e) => setPopulationSize(parseInt(e.target.value))} />

            <label>Макс. итераций: {maxIterations}</label>
            <input type="range" min="10" max="500" value={maxIterations}
                   onChange={(e) => setMaxIterations(parseInt(e.target.value))} />

            <button className="btn-primary" onClick={handleInitialize}>
              🚀 Инициализировать
            </button>
          </div>

          <div className="panel-section">
            <h3>📊 Переменные для визуализации</h3>
            <p className="hint">Выберите ровно 2 переменные</p>
            <div className="checkbox-list">
              {Array.from({ length: dimension }, (_, i) => (
                <label key={i} className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={selectedVars.includes(i)}
                    onChange={() => handleVarCheckbox(i)}
                  />
                  <span>x{i}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="panel-section">
            <h3>🎚️ Значения переменных</h3>
            {Array.from({ length: dimension }, (_, i) => (
              <div key={i} className="slider-group">
                <label>
                  x{i}: <span className="slider-value">{sliderValues[i]?.toFixed(2)}</span>
                </label>
                <input
                  type="range"
                  min={functions[selectedFunction]?.bounds[0] || -100}
                  max={functions[selectedFunction]?.bounds[1] || 100}
                  step="0.1"
                  value={sliderValues[i] || 0}
                  onChange={(e) => setSliderValues({...sliderValues, [i]: parseFloat(e.target.value)})}
                  disabled={selectedVars.includes(i)}
                />
              </div>
            ))}
          </div>

          <div className="panel-section">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={showTrajectories}
                onChange={(e) => setShowTrajectories(e.target.checked)}
              />
              <span>Показать траектории</span>
            </label>
          </div>
        </div>

        {/* Center Panel - Visualization */}
        <div className="center-panel">
          <div className="plot-container">
            {plotData ? (
              <Plot
                data={plotData.data}
                layout={plotData.layout}
                config={{ responsive: true, displayModeBar: true }}
                style={{ width: '100%', height: '100%' }}
              />
            ) : (
              <div className="placeholder">
                <h2>👆 Инициализируйте оптимизацию</h2>
                <p>Выберите параметры и нажмите "Инициализировать"</p>
              </div>
            )}
          </div>

          <div className="control-panel">
            <button className="btn-control btn-start" onClick={handleStart} disabled={!state || isRunning}>
              ▶️ Старт
            </button>
            <button className="btn-control btn-step" onClick={handleStep} disabled={!state || isRunning}>
              ⏭️ Шаг
            </button>
            <button className="btn-control btn-stop" onClick={handleStop} disabled={!isRunning}>
              ⏹️ Стоп
            </button>
            <button className="btn-control btn-reset" onClick={handleReset}>
              🔄 Сброс
            </button>
          </div>
        </div>

        {/* Right Panel - Info */}
        <div className="right-panel">
          <div className="panel-section">
            <h3>📈 Прогресс</h3>
            {state ? (
              <>
                <div className="info-item">
                  <span>Итерация:</span>
                  <strong>{state.iteration} / {maxIterations}</strong>
                </div>
                <div className="info-item">
                  <span>Лучший фитнес:</span>
                  <strong>{state.best_fitness.toExponential(4)}</strong>
                </div>
                <div className="info-item">
                  <span>PP значение:</span>
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
              <p className="no-data">Нет данных</p>
            )}
          </div>

          <div className="panel-section">
            <h3>⭐ Лучшее решение</h3>
            {state?.best_position ? (
              <div className="solution-display">
                {state.best_position.map((val, idx) => (
                  <div key={idx}>x{idx} = {val.toFixed(6)}</div>
                ))}
              </div>
            ) : (
              <p className="no-data">Еще не найдено</p>
            )}
          </div>

          <div className="panel-section">
            <h3>📉 Сходимость</h3>
            {state?.convergence_history && state.convergence_history.length > 1 ? (
              <Plot
                data={[{
                  type: 'scatter',
                  mode: 'lines',
                  x: Array.from({ length: state.convergence_history.length }, (_, i) => i),
                  y: state.convergence_history,
                  line: { color: '#667eea', width: 2 }
                }]}
                layout={{
                  autosize: true,
                  margin: { l: 40, r: 20, t: 20, b: 30 },
                  xaxis: { title: 'Итерация' },
                  yaxis: { title: 'Фитнес', type: 'log' },
                  paper_bgcolor: 'rgba(0,0,0,0)',
                  plot_bgcolor: 'rgba(255,255,255,0.9)',
                  font: { size: 10 }
                }}
                config={{ displayModeBar: false }}
                style={{ width: '100%', height: '200px' }}
              />
            ) : (
              <p className="no-data">Нет данных</p>
            )}
          </div>
        </div>
      </div>

      <footer className="app-footer">
        <p>🎓 HW2: Dolphin Echolocation Optimization GUI | Backend: Python Flask | Frontend: React</p>
      </footer>
    </div>
  );
}

export default App;