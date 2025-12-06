import { useEffect, useState } from "react";
import { useAuth } from "@clerk/clerk-react";
import { adminGet } from "@/lib/adminApi";
import { Card, CardContent } from "@/components/ui/card";

export default function ApprovedList() {
  const { getToken } = useAuth();
  const [list, setList] = useState([]);

  useEffect(() => {
    (async () => {
      try {
        const token = await getToken({ template: "backend" });
        console.log("ADMIN BACKEND JWT:", token);
        const res = await adminGet("/admin/approved", token);
        setList(res || []);
      } catch (err) {
        console.error("Error loading approved list:", err);
      }
    })();
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Approved Persons</h1>

      <div className="space-y-3">
        {list.length === 0 && (
          <div className="text-sm text-gray-500">No approved persons</div>
        )}

        {list.map((p) => (
          <Card key={p.person_id}>
            <CardContent className="flex items-center gap-4 p-4">
              <img
                src={p.image_url}
                className="w-20 h-20 rounded object-cover"
              />

              <div className="flex-1">
                <div className="font-medium">{p.name}</div>
                <div className="text-gray-600 text-sm">Case ID: {p.case_id}</div>
                <div className="text-gray-500 text-xs">{p.created_at}</div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
