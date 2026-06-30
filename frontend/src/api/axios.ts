import axios from "axios";

const API_VERSION = "/api/v1";

const rawBaseUrl = import.meta.env.VITE_API_BASE_URL;

if (import.meta.env.PROD && !rawBaseUrl) {
  throw new Error("VITE_API_BASE_URL is required in production builds.");
}
const apiBaseUrl = rawBaseUrl
  ? `${rawBaseUrl}${API_VERSION}`
  : `http://127.0.0.1:8000${API_VERSION}`;

if (import.meta.env.PROD && !apiBaseUrl.startsWith("https://")) {
  throw new Error("VITE_API_BASE_URL must use HTTPS in production builds.");
}

const api = axios.create({
  baseURL: apiBaseUrl,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
