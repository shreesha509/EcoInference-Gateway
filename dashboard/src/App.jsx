import { useState } from "react";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL || "";

function App() {
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzePrompt = async () => {
    if (!prompt.trim()) {
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
        `${API_URL}/v1/inference/generate`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            prompt: prompt.trim(),
          }),
        }
      );

      if (!response.ok) {
        throw new Error(
          `Gateway returned HTTP ${response.status}`
        );
      }

      const data = await response.json();

      setResult(data);
    } catch (err) {
      console.error("EcoInference request failed:", err);

      setError(
        `Request failed: ${err.message || "Unknown error"}`
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="dashboard">
      <header className="header">
        <div>
          <p className="eyebrow">AI SUSTAINABILITY GATEWAY</p>

          <h1>EcoInference</h1>

          <p className="subtitle">
            Don't cool computation you didn't need to perform.
          </p>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          Gateway MVP
        </div>
      </header>

      <section className="hero">
        <div>
          <p className="section-label">INFERENCE REQUEST</p>

          <h2>Intercept before inference.</h2>

          <p className="description">
            Submit an AI prompt. EcoInference checks whether a
            semantically similar result already exists before
            allowing another inference execution.
          </p>
        </div>

        <div className="request-card">
          <textarea
            value={prompt}
            onChange={(event) => setPrompt(event.target.value)}
            placeholder="Example: A futuristic city during sunset"
            rows={5}
          />

          <button
            onClick={analyzePrompt}
            disabled={loading || !prompt.trim()}
          >
            {loading ? "Analyzing..." : "Analyze Request"}
          </button>
        </div>
      </section>

      {error && <div className="error">{error}</div>}

      {result && (
        <section className="results">
          <div className="result-header">
            <div>
              <p className="section-label">GATEWAY DECISION</p>

              <h2>
                {result.cache_hit
                  ? "Inference bypassed"
                  : "Inference required"}
              </h2>
            </div>

            <div
              className={`decision ${
                result.cache_hit ? "hit" : "miss"
              }`}
            >
              {result.cache_hit ? "CACHE HIT" : "CACHE MISS"}
            </div>
          </div>

          <div className="metrics">
            <div className="metric">
              <span>Similarity</span>

              <strong>
                {result.similarity}
              </strong>
            </div>

            <div className="metric">
              <span>GPU compute</span>

              <strong>
                {result.gpu_compute_bypassed
                  ? "Bypassed"
                  : "Executed"}
              </strong>
            </div>

            <div className="metric">
              <span>Energy</span>

              <strong>
                {result.impact.energy_kwh} kWh
              </strong>
            </div>

            <div className="metric">
              <span>Cooling water</span>

              <strong>
                {result.impact.water_ml} mL
              </strong>
            </div>

            <div className="metric">
              <span>CO2 emissions</span>

              <strong>
                {result.impact.co2_grams} g
              </strong>
            </div>
          </div>

          {result.cache_hit && (
            <div className="savings">
              <div>
                <span>Energy avoided</span>

                <strong>
                  {result.savings.energy_saved_kwh} kWh
                </strong>
              </div>

              <div>
                <span>Cooling water avoided</span>

                <strong>
                  {result.savings.water_saved_ml} mL
                </strong>
              </div>

              <div>
                <span>CO2 avoided</span>

                <strong>
                  {result.savings.co2_saved_grams} g
                </strong>
              </div>
            </div>
          )}

          <div className="technical">
            <div>
              <span>Matched prompt</span>

              <p>
                {result.matched_prompt ||
                  "No semantic match found"}
              </p>
            </div>

            <div>
              <span>Cached asset</span>

              <p>
                {result.asset || "None"}
              </p>
            </div>
          </div>

          {result.asset_url && (
            <a
              className="asset-link"
              href={result.asset_url}
              target="_blank"
              rel="noreferrer"
            >
              Open cached S3 asset
            </a>
          )}
        </section>
      )}
    </main>
  );
}

export default App;