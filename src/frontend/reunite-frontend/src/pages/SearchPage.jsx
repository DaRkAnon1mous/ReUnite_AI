import { useState } from "react";
import api from "../lib/axios";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

export default function SearchPage() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFile = (e) => {
    const f = e.target.files[0];
    setFile(f);
    setPreview(URL.createObjectURL(f));
  };

  const handleSearch = async () => {
    if (!file) return;

    setLoading(true);
    const form = new FormData();
    form.append("file", file);

    try {
      const res = await api.post("/search", form, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      console.log("SEARCH RESPONSE RAW:", res.data);

      setResults(res.data.matches || []);
    } catch (err) {
      console.error(err);
      alert("Something went wrong while searching.");
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient flex flex-col items-center p-10">
      
      <h1 className="text-4xl font-semibold mb-8 bg-clip-text text-transparent 
        bg-gradient-to-r from-indigo-600 to-purple-600">
        Search Missing Person
      </h1>

      {/* Upload Card */}
      <Card className="w-full max-w-lg shadow-lg border border-purple-100">
        <CardContent className="p-6 space-y-6">

          <Input 
            type="file" 
            accept="image/*" 
            onChange={handleFile} 
            className="cursor-pointer"
          />

          {preview && (
            <img 
              src={preview} 
              className="w-full rounded-lg shadow-md transition-all duration-200"
            />
          )}

          <Button 
            className="w-full bg-purple-600 hover:bg-purple-700" 
            onClick={handleSearch}
            disabled={loading || !file}
          >
            {loading ? "Searching..." : "Search"}
          </Button>
        </CardContent>
      </Card>

      {/* Results */}
      <div className="mt-12 w-full max-w-3xl">
        <h2 className="text-2xl font-semibold mb-4">Matches</h2>

        {results.length === 0 ? (
          <p className="text-gray-500">No matches found.</p>
        ) : (
          <div className="space-y-4">
            {results.map((r, idx) => (
              <Card key={idx} className="shadow-md border border-gray-100">
                <CardContent className="p-4 flex gap-5">

                  <img 
                    src={r.image_url} 
                    className="w-24 h-24 rounded-md object-cover shadow-sm"
                  />

                  <div className="flex-grow">
                    <p className="text-lg font-medium">{r.name || "Unknown"}</p>
                    <p className="text-sm text-gray-600">Case ID: {r.case_id}</p>
                    <p className="text-sm text-gray-600">Location: {r.last_seen_location}</p>

                    {/* Similarity Bar */}
                    <div className="mt-2">
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-purple-600 h-2 rounded-full" 
                          style={{ width: `${r.similarity * 100}%` }}
                        />
                      </div>
                      <p className="text-xs mt-1 text-gray-500">
                        {(r.similarity * 100).toFixed(1)}% similarity
                      </p>
                    </div>

                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
