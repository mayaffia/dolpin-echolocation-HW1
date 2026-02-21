import axios from "axios";

const API_URL = "http://localhost:5000/api";

export const getFunctions = async () => {
  const response = await axios.get(`${API_URL}/functions`);
  return response.data.functions;
};

export const initializeOptimization = async (params) => {
  const response = await axios.post(`${API_URL}/initialize`, {
    function: params.functionName,
    dimension: params.dimension,
    population_size: params.populationSize,
    max_iterations: params.maxIterations,
  });
  return response.data;
};

export const stepOptimization = async () => {
  const response = await axios.post(`${API_URL}/step`);
  return response.data;
};

export const resetOptimization = async () => {
  const response = await axios.post(`${API_URL}/reset`);
  return response.data;
};

export const evaluateGrid = async (params) => {
  const response = await axios.post(`${API_URL}/evaluate_grid`, {
    function: params.functionName,
    fixed_vars: params.fixedVars,
    var_indices: params.varIndices,
    resolution: params.resolution || 50,
  });
  return response.data;
};
