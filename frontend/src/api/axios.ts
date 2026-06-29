import axios from "axios";

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

if (import.meta.env.PROD && !apiBaseUrl) {
  throw new Error("VITE_API_BASE_URL is required in production builds.");
}

if (import.meta.env.PROD && !apiBaseUrl.startsWith("https://")) {
  throw new Error("VITE_API_BASE_URL must use HTTPS in production builds.");
}

const api = axios.create({
  baseURL: apiBaseUrl ?? "http://127.0.0.1:8000/api/v1",
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
