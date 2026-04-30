"use client";
import { useState } from "react";

export default function Home() {
  const [script, setScript] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const generateVideoData = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/generate-scenes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ script }),
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Error:", error);
      alert("Backend se connect nahi ho pa raha hai!");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-black text-white p-10 flex flex-col items-center">
      <h1 className="text-4xl font-bold mb-6 text-blue-500">AI Hinglish Video Generator</h1>
      
      <textarea
        className="w-full max-w-2xl p-4 bg-gray-900 border border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="Apni Hinglish script yahan likhein..."
        rows={6}
        value={script}
        onChange={(e) => setScript(e.target.value)}
      />

      <button
        onClick={generateVideoData}
        disabled={loading}
        className="mt-6 px-8 py-3 bg-blue-600 hover:bg-blue-700 rounded-full font-bold transition disabled:opacity-50"
      >
        {loading ? "Processing..." : "Generate Scenes"}
      </button>

      {result && (
        <div className="mt-10 w-full max-w-4xl">
          <h2 className="text-2xl mb-4">Generated Scenes (Module 1 Output):</h2>
          <div className="grid gap-4">
            {result.scenes.map((scene, index) => (
              <div key={index} className="p-4 bg-gray-800 rounded-lg border border-gray-600">
                <p className="text-blue-300 font-bold">Scene {index + 1}</p>
                <p className="text-sm italic text-gray-400 mb-2">Prompt: {scene.visual_prompt}</p>
                <p className="text-lg">Voice: {scene.audio_text}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
