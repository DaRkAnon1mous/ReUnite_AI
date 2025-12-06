import { useEffect, useState } from "react";
import { useAuth } from "@clerk/clerk-react";
import { adminGet } from "@/lib/adminApi";
import { Card, CardContent } from "@/components/ui/card";

export default function RejectedList() {
  const { getToken } = useAuth();
  const [list, setList] = useState([]);

  useEffect(() => {
    (async () => {
      try {
        const token = await getToken({ template: "backend" });
        console.log("ADMIN BACKEND JWT:", token);
        const res = await adminGet("/admin/rejected", token);
        setList(res.rejected || []);
      } catch (err) {
        console.error("Error loading rejected list:", err);
      }
    })();
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Rejected Registrations</h1>

      <div className="space-y-3">
        {list.length === 0 && (
          <div className="text-sm text-gray-500">No rejected items</div>
        )}

        {list.map((r) => (
          <Card key={r.registration_id}>
            <CardContent className="p-4 space-y-2">
              <div className="font-medium">{r.person_data.name}</div>
              <div className="text-gray-600 text-sm">{r.submitted_at}</div>
              <div className="text-gray-500 text-sm">
                Age: {r.person_data.age} | Gender: {r.person_data.gender}
              </div>
              <div className="text-gray-500 text-xs">
                Last Seen: {r.person_data.last_seen_location}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
