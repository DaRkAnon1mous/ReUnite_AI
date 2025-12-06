import { useLocation, useParams, useNavigate } from "react-router-dom";
import { useAuth } from "@clerk/clerk-react";
import { Button } from "@/components/ui/button";

export default function PendingReview() {
  const { state } = useLocation();
  const { id } = useParams();
  const navigate = useNavigate();
  const { getToken } = useAuth();

  if (!state) return <div>Invalid state</div>;

  const pdata = state.person_data;

  async function handleApprove() {
    const token = await getToken({ template: "backend" });
    await fetch(`${import.meta.env.VITE_API_URL}/admin/verify/${id}?approve=true`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
    });
    navigate("/admin/pending");
  }

  async function handleReject() {
    const token = await getToken({ template: "backend" });
    await fetch(`${import.meta.env.VITE_API_URL}/admin/verify/${id}?approve=false`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
    });
    navigate("/admin/pending");
  }

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Review Registration</h1>

      <img src={state.person_image_url} className="w-48 rounded mb-4" />

      <div className="space-y-2 text-sm">
        <div><b>Name:</b> {pdata.name}</div>
        <div><b>Age:</b> {pdata.age}</div>
        <div><b>Gender:</b> {pdata.gender}</div>
        <div><b>Location:</b> {pdata.last_seen_location}</div>
        <div><b>Details:</b> {pdata.additional_details}</div>
      </div>

      <div className="mt-4 flex gap-3">
        <Button onClick={handleApprove}>Approve</Button>
        <Button variant="outline" onClick={handleReject}>Reject</Button>
        <Button onClick={() => navigate("/admin/pending")}>Back</Button>
      </div>
    </div>
  );
}
