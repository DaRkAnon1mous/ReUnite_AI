import { useState } from "react";
import { Search, Sparkles, X } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import api from "../lib/axios";

// Demo images from your database (replace with actual URLs)
const DEMO_IMAGES = [
  {
    id: "demo-1",
    url: "https://res.cloudinary.com/dn9fmgufm/image/upload/v1764487601/c8wzb30eatjqmobvpg6q.jpg",
    name: "Test Person 1",
    personId: "d7be2380-1c1a-4662-8f33-893e49f43740"
  },
  {
    id: "demo-2", 
    url: "https://res.cloudinary.com/dn9fmgufm/image/upload/v1764487776/xstxubgh8dcivindongp.jpg",
    name: "Test Person 2",
    personId: "979792be-974a-4a98-9d91-7ccc684bd9e5"
  },
  {
    id: "demo-3",
    url: "https://res.cloudinary.com/dn9fmgufm/image/upload/v1764487962/t8cmoyreuo3pkglm4h9v.jpg",
    name: "Test Person 3", 
    personId: "1486bda0-c105-4214-b17f-2099203fcfa1"
  }
];

export default function SearchPage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showDemo, setShowDemo] = useState(true);
  const [demoMode, setDemoMode] = useState(false);

  // Handle file upload from user
  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setPreview(URL.createObjectURL(file));
      setShowDemo(false);
      setDemoMode(false);
    }
  };

  // Handle demo card click
  const handleDemoClick = async (demo) => {
    try {
      // Fetch the demo image as blob
      const response = await fetch(demo.url);
      const blob = await response.blob();
      
      // Create a File object from blob
      const file = new File([blob], `${demo.id}.jpg`, { type: "image/jpeg" });
      
      setSelectedFile(file);
      setPreview(demo.url);
      setShowDemo(false);
      setDemoMode(true);
      
      // Auto-scroll to preview
      setTimeout(() => {
        document.getElementById("preview-section")?.scrollIntoView({ 
          behavior: "smooth" 
        });
      }, 100);
      
    } catch (error) {
      console.error("Failed to load demo image:", error);
      alert("Failed to load demo image. Please try again.");
    }
  };

  // Clear selection
  const handleClear = () => {
    setSelectedFile(null);
    setPreview("");
    setResults([]);
    setShowDemo(true);
    setDemoMode(false);
  };

  // Submit search
  const handleSearch = async () => {
    if (!selectedFile) {
      alert("Please select an image first");
      return;
    }

    setLoading(true);
    setResults([]);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const res = await api.post("/search", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      console.log("=== BACKEND RESPONSE ===");
      console.log("Full response:", res.data);
      console.log("Response type:", typeof res.data);
      console.log("Response keys:", Object.keys(res.data));
      
      // Try different possible response structures
      let matches = [];
      
      if (Array.isArray(res.data)) {
        // Response is directly an array
        matches = res.data;
        console.log("Response is direct array");
      } else if (res.data.results) {
        // Response has results key
        matches = res.data.results;
        console.log("Response has results key");
      } else if (res.data.matches) {
        // Response has matches key
        matches = res.data.matches;
        console.log("Response has matches key");
      } else if (res.data.data) {
        // Response has data key
        matches = res.data.data;
        console.log("Response has data key");
      }
      
      console.log("Parsed matches:", matches);
      console.log("Number of matches:", matches.length);
      
      setResults(matches);
      
      if (matches.length === 0) {
        alert("No matches found in database");
      }
    } catch (error) {
      console.error("=== SEARCH ERROR ===");
      console.error("Error object:", error);
      console.error("Error response:", error.response?.data);
      console.error("Error status:", error.response?.status);
      alert(`Search failed: ${error.response?.data?.detail || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50 p-6">
      <div className="max-w-6xl mx-auto">
        
        {/* Header */}
        <div className="text-center mb-10">
          <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600 mb-2">
            Search for Missing Persons
          </h1>
          <p className="text-gray-600">Upload a photo to find matches in our database</p>
        </div>

        {/* Demo Cards - Show when no image selected */}
        {showDemo && (
          <div className="mb-8 bg-white rounded-2xl shadow-lg p-6 border border-indigo-100">
            <div className="flex items-center gap-2 mb-4">
              <Sparkles className="w-5 h-5 text-indigo-600" />
              <h2 className="text-xl font-semibold text-gray-800">Try Demo Search</h2>
            </div>
            <p className="text-sm text-gray-600 mb-4">
              Click on any demo image below to test the search feature with sample data
            </p>
            
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {DEMO_IMAGES.map((demo) => (
                <Card 
                  key={demo.id}
                  className="cursor-pointer hover:shadow-xl transition-all duration-300 hover:-translate-y-1 border-2 border-transparent hover:border-indigo-400"
                  onClick={() => handleDemoClick(demo)}
                >
                  <CardContent className="p-4">
                    <div className="relative aspect-square mb-3 rounded-lg overflow-hidden bg-gray-100">
                      <img 
                        src={demo.url} 
                        alt={demo.name}
                        className="w-full h-full object-cover"
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent flex items-end p-3">
                        <span className="text-white font-medium text-sm">{demo.name}</span>
                      </div>
                    </div>
                    <Button 
                      variant="outline" 
                      size="sm" 
                      className="w-full"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleDemoClick(demo);
                      }}
                    >
                      <Sparkles className="w-4 h-4 mr-2" />
                      Try This Demo
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        )}

        {/* Upload Section */}
        <Card className="shadow-lg border border-gray-200 mb-8">
          <CardContent className="p-6">
            <div className="space-y-4">
              
              {/* File Input */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {demoMode ? "Demo Image Selected" : "Upload Your Own Image"}
                </label>
                <Input
                  type="file"
                  accept="image/*"
                  onChange={handleFileChange}
                  className="cursor-pointer"
                  disabled={loading}
                />
                {demoMode && (
                  <p className="text-xs text-indigo-600 mt-1 flex items-center gap-1">
                    <Sparkles className="w-3 h-3" />
                    Using demo image for testing
                  </p>
                )}
              </div>

              {/* Preview Section */}
              {preview && (
                <div id="preview-section" className="bg-gray-50 rounded-lg p-4">
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-medium text-gray-700">Preview</h3>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={handleClear}
                      className="h-8 w-8 p-0"
                    >
                      <X className="w-4 h-4" />
                    </Button>
                  </div>
                  <img
                    src={preview}
                    alt="Preview"
                    className="max-w-xs mx-auto rounded-lg shadow-md"
                  />
                </div>
              )}

              {/* Search Button */}
              <Button
                className="w-full bg-indigo-600 hover:bg-indigo-700 py-6 text-lg font-semibold"
                onClick={handleSearch}
                disabled={!selectedFile || loading}
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2" />
                    Searching...
                  </>
                ) : (
                  <>
                    <Search className="w-5 h-5 mr-2" />
                    Search Database
                  </>
                )}
              </Button>

            </div>
          </CardContent>
        </Card>

        {/* Results Section */}
        {results.length > 0 && (
          <div>
            <h2 className="text-2xl font-bold mb-6 text-gray-800">
              Search Results ({results.length})
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {results.map((result, idx) => (
                <Card key={idx} className="shadow-lg hover:shadow-xl transition-shadow">
                  <CardContent className="p-6">
                    <div className="aspect-square mb-4 rounded-lg overflow-hidden bg-gray-100">
                      <img
                        src={result.image_url}
                        alt={result.name || "Match"}
                        className="w-full h-full object-cover"
                      />
                    </div>
                    
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="font-semibold text-lg">{result.name || "Unknown"}</span>
                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                          result.similarity > 0.8 
                            ? "bg-green-100 text-green-800"
                            : result.similarity > 0.6
                            ? "bg-yellow-100 text-yellow-800"
                            : "bg-gray-100 text-gray-800"
                        }`}>
                          {(result.similarity * 100).toFixed(0)}% Match
                        </span>
                      </div>
                      
                      {result.age && (
                        <p className="text-sm text-gray-600">Age: {result.age}</p>
                      )}
                      
                      {result.last_seen_location && (
                        <p className="text-sm text-gray-600">
                          Last Seen: {result.last_seen_location}
                        </p>
                      )}
                      
                      <Button 
                        variant="outline" 
                        className="w-full mt-3"
                        onClick={() => {
                          // Navigate to detail page or show modal
                          alert(`View details for: ${result.name}`);
                        }}
                      >
                        View Full Details
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        )}

        {/* No Results */}
        {!loading && results.length === 0 && preview && (
          <div className="text-center py-12 bg-white rounded-lg shadow-md">
            <div className="text-gray-400 mb-4">
              <Search className="w-16 h-16 mx-auto" />
            </div>
            <p className="text-gray-600 text-lg">
              {demoMode 
                ? "Click 'Search Database' to find matches"
                : "Upload an image and click search to find matches"}
            </p>
          </div>
        )}

      </div>
    </div>
  );
}