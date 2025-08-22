import React, { useState } from "react";
import ArticleCard from "../components/ArticleCard";

function Search() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  async function handleSearch() {
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/articles/search/?q=${query}`);
      const data = await res.json();
      setResults(data);
    } catch (err) {
      console.error(err);
    }
  }

  return (
    <div>
      <h1>🔍 Search Articles</h1>
      <input 
        type="text" 
        value={query} 
        onChange={(e) => setQuery(e.target.value)} 
        placeholder="Search news..."
      />
      <button onClick={handleSearch}>Search</button>

      {results.map(article => (
        <ArticleCard key={article.id} article={article} />
      ))}
    </div>
  );
}

export default Search;
