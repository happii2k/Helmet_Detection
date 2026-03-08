import { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResult(null);
    setError(null);
  };

  const handleSubmit = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/predict", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error(`Request failed: ${res.status}`);
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "0 auto", padding: 20 }}>
      <h1>Helmet Detection</h1>

      <input type="file" accept="image/*" onChange={handleFileChange} />
      <button onClick={handleSubmit} disabled={!file || loading}>
        {loading ? "Detecting..." : "Detect Helmet"}
      </button>

      {error && <p style={{ color: "red" }}>Error: {error}</p>}

      {result && (
        <div style={{ marginTop: 20 }}>
          <p>
            Helmet detected:{" "}
            <strong>{result.has_helmet ? "YES" : "NO"}</strong>
          </p>

          {result.annotated_image_url && (
            <img
              src={`http://localhost:8000${result.annotated_image_url}`}
              alt="Detection result"
              style={{ maxWidth: "100%", marginTop: 10 }}
            />
          )}

          {result.detections && (
            <pre style={{ marginTop: 10 }}>
              {JSON.stringify(result.detections, null, 2)}
            </pre>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
