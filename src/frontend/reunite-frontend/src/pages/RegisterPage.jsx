import { useState } from "react";
import api from "../lib/axios";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";

export default function RegisterPage() {
  const [facePreview, setFacePreview] = useState("");
  const [aadharPreview, setAadharPreview] = useState("");

  const [form, setForm] = useState({
    name: "",
    age: "",
    gender: "",
    height: "",
    contact_info: "",
    last_seen_date: "",
    last_seen_time: "",
    last_seen_location: "",
    additional_details: "",
    reporter: "",
    reporter_contact: "",
    aadhar_number: "",
  });

  const [faceImage, setFaceImage] = useState(null);
  const [aadharImage, setAadharImage] = useState(null);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleImage = (e, type) => {
    const file = e.target.files[0];

    if (type === "face") {
      setFaceImage(file);
      setFacePreview(URL.createObjectURL(file));
    } else {
      setAadharImage(file);
      setAadharPreview(URL.createObjectURL(file));
    }
  };

  const handleSubmit = async () => {
    if (!faceImage) {
      alert("Face image is required.");
      return;
    }

    const data = new FormData();
    Object.keys(form).forEach((key) => data.append(key, form[key]));
    data.append("image", faceImage);
    if (aadharImage) data.append("aadhar_image", aadharImage);

    try {
      const res = await api.post("/register", data, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      alert("Registration submitted successfully!");
    } catch (err) {
      console.error(err);
      alert("Failed to submit registration.");
    }
  };

  return (
    <div className="min-h-screen bg-gradient p-10 flex flex-col items-center">
      <h1 className="text-4xl font-semibold mb-8 bg-clip-text text-transparent 
        bg-gradient-to-r from-blue-600 to-indigo-600">
        Register Missing Person
      </h1>

      <div className="w-full max-w-3xl space-y-8">
        
        {/* CARD 1 — BASIC INFO */}
        <Card className="shadow-md border border-gray-200">
          <CardContent className="p-6 space-y-4">
            <h2 className="text-xl font-semibold mb-2">Basic Information</h2>

            <Input placeholder="Full Name" name="name" value={form.name} onChange={handleChange} />
            <Input placeholder="Age" type="number" name="age" value={form.age} onChange={handleChange} />
            <Input placeholder="Gender (Male/Female)" name="gender" value={form.gender} onChange={handleChange} />
            <Input placeholder="Height (optional)" name="height" value={form.height} onChange={handleChange} />
            <Input placeholder="Contact Info" name="contact_info" value={form.contact_info} onChange={handleChange} />

            <Input placeholder="Reporter Name" name="reporter" value={form.reporter} onChange={handleChange} />
            <Input placeholder="Reporter Contact" name="reporter_contact" value={form.reporter_contact} onChange={handleChange} />
            <Input placeholder="Aadhar Number (optional)" name="aadhar_number" value={form.aadhar_number} onChange={handleChange} />
          </CardContent>
        </Card>

        {/* CARD 2 — LAST SEEN DETAILS */}
        <Card className="shadow-md border border-gray-200">
          <CardContent className="p-6 space-y-4">
            <h2 className="text-xl font-semibold mb-2">Last Seen Details</h2>

            <Input type="date" name="last_seen_date" value={form.last_seen_date} onChange={handleChange} />
            <Input type="time" name="last_seen_time" value={form.last_seen_time} onChange={handleChange} />
            <Input placeholder="Last Seen Location" name="last_seen_location" value={form.last_seen_location} onChange={handleChange} />

            <Textarea 
              placeholder="Additional details (clothing, hairstyle, unique features)" 
              name="additional_details"
              value={form.additional_details}
              onChange={handleChange}
            />
          </CardContent>
        </Card>

        {/* CARD 3 — UPLOADS */}
        <Card className="shadow-md border border-gray-200">
          <CardContent className="p-6 space-y-4">
            <h2 className="text-xl font-semibold mb-2">Upload Images</h2>

            <p className="text-gray-600 text-sm">Face Image (required)</p>
            <Input type="file" accept="image/*" onChange={(e) => handleImage(e, "face")} />
            {facePreview && <img src={facePreview} className="w-32 rounded-lg shadow-md" />}

            <p className="text-gray-600 text-sm mt-4">Aadhar Image (optional)</p>
            <Input type="file" accept="image/*" onChange={(e) => handleImage(e, "aadhar")} />
            {aadharPreview && <img src={aadharPreview} className="w-32 rounded-lg shadow-md" />}
          </CardContent>
        </Card>

        {/* SUBMIT BUTTON */}
        <Button 
          className="w-full bg-indigo-600 hover:bg-indigo-700 py-3 text-lg"
          onClick={handleSubmit}
        >
          Submit Registration
        </Button>

      </div>
    </div>
  );
}
