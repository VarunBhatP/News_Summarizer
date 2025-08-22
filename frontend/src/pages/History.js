import React, { useEffect, useState } from "react";
import ArticleCard from "../components/ArticleCard";

function History() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const data = JSON.parse(localStorage.getItem("history")) || [];
    setHistory(data);
  }, []);

  return (
    <div>
      <h1>📜 History</h1>
      {history.length === 0 ? (
        <p>No articles viewed yet.</p>
      ) : (
        history.map((article, idx) => (
          <ArticleCard key={idx} article={article} />
        ))
      )}
    </div>
  );
}

export default History;
