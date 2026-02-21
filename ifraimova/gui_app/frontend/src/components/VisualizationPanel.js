import Plot from "react-plotly.js";

const VisualizationPanel = ({ plotData }) => {
  console.log(plotData);
  return (
    <div className="plot-container">
      {plotData ? (
        <Plot
          data={plotData.data}
          layout={plotData.layout}
          config={{ responsive: true, displayModeBar: true }}
          style={{ width: "100%", height: "100%" }}
        />
      ) : (
        <div className="placeholder">
          <h2>Initialize Optimization</h2>
          <p>Select parameters and click "Initialize"</p>
        </div>
      )}
    </div>
  );
};

export default VisualizationPanel;
