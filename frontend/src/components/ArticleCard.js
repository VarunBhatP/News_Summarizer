import React from "react";

function ArticleCard({ article }) {
  function addToFavorites() {
    let favs = JSON.parse(localStorage.getItem("favorites")) || [];
    favs.push(article);
    localStorage.setItem("favorites", JSON.stringify(favs));
    alert("Added to favorites!");
  }

  function addToHistory() {
    let hist = JSON.parse(localStorage.getItem("history")) || [];
    hist.push(article);
    localStorage.setItem("history", JSON.stringify(hist));
  }

  return (
    <div style={{
      border: "1px solid #ddd",
      padding: "15px",
      margin: "15px 0",
      borderRadius: "8px"
    }}>
      <h2>{article.title}</h2>
      <p><b>Summary:</b> {article.summary}</p>
      <a href={article.url} target="_blank" rel="noreferrer"
         onClick={addToHistory}>Read more</a>
      <p>📌 Source: {article.source || "Unknown"}</p>
      <p>🗂️ Category: {article.category || "General"}</p>
      <button onClick={addToFavorites}>⭐ Add to Favorites</button>
    </div>
  );
}

export default ArticleCard;
