import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_PROD_API_URL || "http://localhost:8060",
});

export default api;
