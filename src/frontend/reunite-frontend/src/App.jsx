import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import SearchPage from "./pages/SearchPage";
import RegisterPage from "./pages/RegisterPage";

import AdminLogin from "./pages/admin/AdminLogin";
import AdminDashboard from "./pages/admin/AdminDashboard";

import AdminRoute from "./components/AdminRoute";
import AdminLayout from "./pages/admin/AdminLayout";

import PendingList from "./pages/admin/PendingList";
import PendingReview from "./pages/admin/PendingReview";

import ApprovedList from "./pages/admin/ApprovedList";
import RejectedList from "./pages/admin/RejectedList";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* PUBLIC ROUTES */}
        <Route path="/" element={<Home />} />
        <Route path="/search" element={<SearchPage />} />
        <Route path="/register" element={<RegisterPage />} />

        {/* ADMIN LOGIN (UNPROTECTED) */}
        <Route path="/admin/login" element={<AdminLogin />} />

        {/* ADMIN PROTECTED ROUTES */}
        <Route
  path="/admin"
  element={
    <AdminRoute>
      <AdminLayout />
    </AdminRoute>
  }
>
  <Route path="dashboard" element={<AdminDashboard />} />
  <Route path="pending" element={<PendingList />} />
  <Route path="pending/:id" element={<PendingReview />} />

  {/* NEW ROUTES */}
  <Route path="approved" element={<ApprovedList />} />
  <Route path="rejected" element={<RejectedList />} />
</Route>

        {/* 404 */}
        <Route path="*" element={<div>Page Not Found</div>} />

      </Routes>
    </BrowserRouter>
  );
}
