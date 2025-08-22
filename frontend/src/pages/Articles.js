import React, { useEffect, useState } from "react";
import ArticleCard from "../components/ArticleCard";

function Articles() {
  const [articles, setArticles] = useState([]);
  const [category, setCategory] = useState("general");

  // ✅ Fetch articles from backend
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

  // ✅ Run on mount & whenever category changes
  useEffect(() => {
    fetchArticles(category);
  }, [category]);

  return (
    <div>
      <h1>📰 Articles</h1>

      {/* Category Selector */}
      <label>Choose a category:</label>
      <select 
        value={category} 
        onChange={(e) => setCategory(e.target.value)} 
        style={{ marginLeft: "10px" }}
      >
        <option value="general">General</option>
        <option value="sports">Sports</option>
        <option value="politics">Politics</option>
        <option value="business">Business</option>
      </select>

      {/* List of Articles */}
      {articles.length === 0 ? (
        <p>No articles found.</p>
      ) : (
        articles.map((article) => (
          <ArticleCard key={article.id} article={article} />
        ))
      )}
    </div>
  );
}

export default Articles;
