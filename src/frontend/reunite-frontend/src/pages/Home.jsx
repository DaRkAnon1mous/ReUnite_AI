import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <Card className="w-[400px] shadow-xl">
        <CardContent className="p-6 space-y-4">
          <h1 className="text-2xl font-semibold">ReUnite AI</h1>
          <p className="text-gray-500">Find missing persons using facial recognition.</p>

          <Button className="w-full" onClick={() => navigate("/search")}>
            Search by Image
          </Button>

          <Button variant="outline" className="w-full" onClick={() => navigate("/register")}>
            Register a Missing Person
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
