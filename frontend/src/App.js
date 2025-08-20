// Import React (JS Modules concept: import/export)
import React, { useEffect, useState } from "react";

// ✅ Functional Component (React uses functions + JSX)
function App() {
  // ✅ useState Hook (React State concept)
  const [articles, setArticles] = useState([]);

  // ✅ useEffect Hook (React lifecycle: runs after component mounts)
  useEffect(() => {
    // ✅ async/await (JS concept for API calls)
    async function fetchArticles() {
      const res = await fetch("http://127.0.0.1:8000/api/articles/");
      const data = await res.json();
      setArticles(data); // updates state
    }
    fetchArticles();
  }, []); // [] = run only once

  // ✅ JSX (HTML-like syntax inside JS)
  return (
    <div style={{ padding: "20px" }}>
      <h1>📰 News Summarizer</h1>

      {/* ✅ Array.map (JS Array concept) */}
      {articles.map((article) => (
        // ✅ Destructuring used below: pulling fields directly
        <div key={article.id} style={{ marginBottom: "20px" }}>
          <h2>{article.date}</h2>
          <h2>{article.title}</h2>
          <p><b>Summary:</b> {article.summary}</p>
          <a href={article.link} target="_blank" rel="noreferrer">
            Read more
          </a>
          <p>📌 Source: {article.source}</p>
        </div>
      ))}
    </div>
  );
}

// ✅ Exporting Component (JS export/import concept)
export default App;
