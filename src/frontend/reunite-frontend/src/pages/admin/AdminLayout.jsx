import { Outlet, Link, useNavigate } from "react-router-dom";
import { SignOutButton, useUser } from "@clerk/clerk-react";
import { Button } from "@/components/ui/button";

export default function AdminLayout() {
  const { user, isLoaded } = useUser();
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex bg-gray-50">
      {/* Sidebar - ✅ FIXED: Added flex flex-col */}
      <aside className="w-72 p-6 border-r bg-white flex flex-col">
        <div className="mb-6">
          <h2 className="text-2xl font-semibold">Admin</h2>
          <p className="text-sm text-gray-500">ReUnite AI</p>
        </div>

        <nav className="flex flex-col gap-2">
          <Link 
            to="/admin/dashboard" 
            className="py-2 px-3 rounded hover:bg-gray-100"
          >
            Dashboard
          </Link>
          <Link 
            to="/admin/pending" 
            className="py-2 px-3 rounded hover:bg-gray-100"
          >
            Pending
          </Link>
          <Link 
            to="/admin/approved" 
            className="py-2 px-3 rounded hover:bg-gray-100"
          >
            Approved
          </Link>
          <Link 
            to="/admin/rejected" 
            className="py-2 px-3 rounded hover:bg-gray-100"
          >
            Rejected
          </Link>
        </nav>

        {/* ✅ FIXED: Now mt-auto will work properly */}
        <div className="mt-auto pt-6">
          <div className="mb-3">
            {isLoaded && user ? (
              <div>
                <div className="text-sm">{user.primaryEmailAddress?.emailAddress}</div>
                <div className="text-xs text-gray-500">{user.fullName}</div>
              </div>
            ) : null}
          </div>
          <div className="flex gap-2">
            <SignOutButton>
              <Button variant="outline">Sign out</Button>
            </SignOutButton>
            <Button onClick={() => navigate("/")} variant="outline">
              Site
            </Button>
          </div>
        </div>
      </aside>

      {/* Main */}
      <main className="flex-1 p-8">
        <Outlet />
      </main>
    </div>
  );
}
