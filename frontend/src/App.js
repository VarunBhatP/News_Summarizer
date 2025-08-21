// Import React (JS Modules concept: import/export)
import React, { useEffect, useState } from "react";

// ✅ Functional Component
function App() {
  // State for articles
  const [articles, setArticles] = useState([]);
  // State for selected category
  const [category, setCategory] = useState("general");

  // ✅ Function to fetch articles
  async function fetchArticles(selectedCategory = "general") {
    try {
      const res = await fetch(
        `http://127.0.0.1:8000/api/articles/?category=${selectedCategory}`
      );
      const data = await res.json();
      setArticles(data);
    } catch (error) {
      console.error("Error fetching articles:", error);
    }
  }

  // ✅ Run fetch on mount (default category = general)
  useEffect(() => {
    fetchArticles(category);
  }, [category]); // runs whenever category changes

  // ✅ JSX (HTML-like syntax inside JS)
  return (
    <div style={{ padding: "20px" }}>
      <h1>📰 News Summarizer</h1>

      {/* Category Dropdown */}
      <label style={{ marginRight: "10px" }}>Choose a category:</label>
      <select
        value={category}
        onChange={(e) => setCategory(e.target.value)}
        style={{ marginBottom: "20px" }}
      >
        <option value="general">General</option>
        <option value="sports">Sports</option>
        <option value="politics">Politics</option>
        <option value="business">Business</option>
      </select>

      {/* Article List */}
      {articles.length === 0 ? (
        <p>No articles found.</p>
      ) : (
        articles.map((article) => (
          <div key={article.id} style={{ marginBottom: "20px" }}>
            <h2>{article.title}</h2>
            <p>
              <b>Summary:</b> {article.summary}
            </p>
            <a href={article.url} target="_blank" rel="noreferrer">
              Read more
            </a>
            <p>📌 Source: {article.source || "Unknown"}</p>
            <p>🗂️ Category: {article.category || "General"}</p>
          </div>
        ))
      )}
    </div>
  );
}

// ✅ Exporting Component
export default App;
