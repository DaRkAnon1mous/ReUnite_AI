import { SignIn } from "@clerk/clerk-react";

export default function AdminLogin() {
  return (
    <div className="w-full min-h-screen flex items-center justify-center">
      <SignIn afterSignInUrl="/admin/dashboard" />
    </div>
  );
}
