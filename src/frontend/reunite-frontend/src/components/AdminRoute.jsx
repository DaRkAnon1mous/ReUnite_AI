// src/components/AdminRoute.jsx
import { useUser } from "@clerk/clerk-react";
import { Navigate } from "react-router-dom";

const ADMIN_EMAIL = import.meta.env.VITE_ADMIN_EMAIL;

export default function AdminRoute({ children }) {
  const { user, isLoaded } = useUser();

  if (!isLoaded) return null; // or a loader

  // Not signed in → send to admin login
  if (!user) {
    return <Navigate to="/admin/login" replace />;
  }

  // Signed in but not admin → send to home
  if (user.primaryEmailAddress?.emailAddress !== ADMIN_EMAIL) {
    return <Navigate to="/" replace />;
  }

  // Admin → allow access
  return children;
}
