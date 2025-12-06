// src/pages/admin/PendingList.jsx
import { useEffect, useState } from "react";
import { useAuth } from "@clerk/clerk-react";
import { adminGet } from "@/lib/adminApi";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";

export default function PendingList() {
  const { getToken } = useAuth();
  const [list, setList] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    (async () => {
      const token = await getToken({ template: "backend" });
      console.log("ADMIN BACKEND JWT:", token);
      try {
        const res = await adminGet("/admin/registrations", token);
        setList(res.pending || []);
      } catch (err) {
        console.error("Pending fetch error:", err);
      }
    })();
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Pending Registrations</h1>

      <div className="space-y-3">
        {list.length === 0 && (
          <div className="text-sm text-gray-500">No pending items</div>
        )}

        {list.map((r) => (
          <Card key={r.registration_id}>
            <CardContent className="flex items-center justify-between">
              <div>
                <div className="font-medium">{r.person_data.name}</div>
                <div className="text-sm text-gray-500">{r.submitted_at}</div>
              </div>

              <Button
  onClick={() =>
    navigate(`/admin/pending/${r.registration_id}`, { state: r })
  }
>
  Review
</Button>

            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
