import { useEffect, useState } from "react";
import { useAuth } from "@clerk/clerk-react";
import { adminGet } from "@/lib/adminApi";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";

export default function AdminDashboard() {
  const { getToken } = useAuth();
  const [stats, setStats] = useState(null);
  const [pending, setPending] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    (async () => {
      try {
        const token = await getToken({ template: "backend" });
        console.log("ADMIN BACKEND JWT:", token);
        const data = await adminGet("/admin/dashboard", token);
        setStats(data);
      } catch (err) {
        console.error("Failed to load dashboard:", err);
      }
    })();
  }, [getToken]); // ✅ FIXED: Added getToken dependency

  useEffect(() => {
    (async () => {
      try {
        const token = await getToken({ template: "backend" });
        console.log("ADMIN BACKEND JWT:", token);
        const list = await adminGet("/admin/pending", token);
        setPending(list.pending || list || []); // ✅ FIXED: Added fallback to []
      } catch (err) {
        console.error(err);
      }
    })();
  }, [getToken]); // ✅ FIXED: Added getToken dependency

  return (
    <div>
      <h1 className="text-3xl font-bold mb-4">Admin Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <Card>
          <CardContent className="p-6">
            <div>Total: {stats?.total_persons ?? "—"}</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div>Verified: {stats?.verified_persons ?? "—"}</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div>Pending: {stats?.pending_registrations ?? "—"}</div>
          </CardContent>
        </Card>
      </div>

      <div>
        <h2 className="text-xl font-semibold mb-2">Recent Pending</h2>
        <div className="space-y-3">
          {pending.length === 0 && (
            <div className="text-sm text-gray-500">No pending registrations</div>
          )}
          {pending.map((r) => {
            // ✅ FIXED: Safely parse person_data
            let personData = {};
            try {
              personData = typeof r.person_data === "string" 
                ? JSON.parse(r.person_data) 
                : r.person_data || {};
            } catch (e) {
              console.error("Failed to parse person_data:", e);
            }

            return (
              <Card key={r.registration_id || r.id}>
                <CardContent className="p-4 flex items-center justify-between">
                  <div>
                    <div className="font-medium">{personData?.name || "Unknown"}</div>
                    <div className="text-sm text-gray-500">
                      {r.submitted_at || r.submittedAt}
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <Button 
                      onClick={() => navigate(`/admin/pending/${r.registration_id || r.id}`)}
                    >
                      View
                    </Button>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>
    </div>
  );
}