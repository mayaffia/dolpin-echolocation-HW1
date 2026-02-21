import { useState, useEffect } from "react";
import * as api from "../services/api";

export const useOptimization = () => {
  const [state, setState] = useState(null);
  const [isRunning, setIsRunning] = useState(false);
  const [agentHistory, setAgentHistory] = useState([]);

  const initialize = async (params) => {
    try {
      const response = await api.initializeOptimization(params);
      setState(response.state);
      setAgentHistory([response.state.agent_positions]);
      return { success: true };
    } catch (error) {
      console.error("Error initializing:", error);
      return {
        success: false,
        error:
          "Ошибка инициализации. Проверьте, что бэкенд запущен на порту 5000",
      };
    }
  };

  const step = async () => {
    try {
      const response = await api.stepOptimization();
      if (response.status === "success") {
        setState(response.state);
        setAgentHistory((prev) => [...prev, response.state.agent_positions]);
        return { success: true, state: response.state };
      }
      return { success: false };
    } catch (error) {
      console.error("Error stepping:", error);
      return { success: false, error: error.message };
    }
  };

  const start = () => {
    setIsRunning(true);
  };

  const stop = () => {
    setIsRunning(false);
  };

  const reset = async () => {
    try {
      await api.resetOptimization();
      setState(null);
      setAgentHistory([]);
      setIsRunning(false);
      return { success: true };
    } catch (error) {
      console.error("Error resetting:", error);
      return { success: false, error: error.message };
    }
  };

  useEffect(() => {
    if (isRunning && state && !state.completed) {
      const timer = setTimeout(() => {
        step();
      }, 100);
      return () => clearTimeout(timer);
    } else if (state?.completed) {
      setIsRunning(false);
    }
  }, [isRunning, state]);

  return {
    state,
    isRunning,
    agentHistory,
    initialize,
    step,
    start,
    stop,
    reset,
  };
};
