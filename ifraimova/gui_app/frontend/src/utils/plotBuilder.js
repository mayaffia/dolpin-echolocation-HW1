export const buildPlotData = (
  gridData,
  state,
  selectedVars,
  showTrajectories,
  agentHistory,
  functionName,
) => {
  const traces = [];

  traces.push({
    type: "contour",
    x: gridData.x,
    y: gridData.y,
    z: gridData.z,
    colorscale: "Jet",
    contours: {
      coloring: "heatmap",
    },
    colorbar: {
      title: "f(x)",
      titleside: "right",
    },
  });

  const agentX = state.agent_positions.map((pos) => pos[selectedVars[0]]);
  const agentY = state.agent_positions.map((pos) => pos[selectedVars[1]]);

  traces.push({
    type: "scatter",
    mode: "markers+text",
    x: agentX,
    y: agentY,
    text: agentX.map((_, i) => i.toString()),
    textposition: "top center",
    marker: {
      size: 12,
      color: "white",
      line: {
        color: "black",
        width: 2,
      },
    },
    name: "Agents",
  });

  if (state.best_position) {
    traces.push({
      type: "scatter",
      mode: "markers",
      x: [state.best_position[selectedVars[0]]],
      y: [state.best_position[selectedVars[1]]],
      marker: {
        size: 18,
        color: "yellow",
        symbol: "star",
        line: {
          color: "black",
          width: 2,
        },
      },
      name: "Best Solution",
    });
  }

  if (showTrajectories && agentHistory.length > 1) {
    const recentHistory = agentHistory.slice(-10);
    for (
      let agentIdx = 0;
      agentIdx < state.agent_positions.length;
      agentIdx++
    ) {
      const trajectoryX = recentHistory.map(
        (h) => h[agentIdx][selectedVars[0]],
      );
      const trajectoryY = recentHistory.map(
        (h) => h[agentIdx][selectedVars[1]],
      );

      traces.push({
        type: "scatter",
        mode: "lines",
        x: trajectoryX,
        y: trajectoryY,
        line: {
          color: "rgba(255, 255, 255, 0.3)",
          width: 1,
          dash: "dash",
        },
        showlegend: false,
        hoverinfo: "skip",
      });
    }
  }

  return traces;
};

export const buildPlotLayout = (functionName, selectedVars, bounds) => {
  return {
    title: `${functionName} (x${selectedVars[0]} vs x${selectedVars[1]})`,
    xaxis: {
      title: `x${selectedVars[0]}`,
      range: [bounds[0], bounds[1]],
    },
    yaxis: {
      title: `x${selectedVars[1]}`,
      range: [bounds[0], bounds[1]],
    },
    autosize: true,
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(255,255,255,0.9)",
    font: { color: "#333" },
  };
};
