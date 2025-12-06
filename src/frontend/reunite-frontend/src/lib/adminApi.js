// src/lib/adminApi.js
import api from "./axios";

// ❌ REMOVED THIS LINE - It was causing the crash:
// import { getToken } from "@clerk/clerk-react";

// Helper functions that accept token as parameter
export async function adminGet(path, token) {
  const res = await api.get(path, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data;
}

export async function adminPost(path, body, token) {
  const res = await api.post(path, body, {
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": body instanceof FormData ? "multipart/form-data" : "application/json",
    },
  });
  return res.data;
}

export async function adminPut(path, body, token) {
  const res = await api.put(path, body, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data;
}

export async function adminDelete(path, token) {
  const res = await api.delete(path, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data;
}