import React, { useEffect, useState } from "react";
import ArticleCard from "../components/ArticleCard";

function Favorites() {
  const [favorites, setFavorites] = useState([]);

  useEffect(() => {
    const data = JSON.parse(localStorage.getItem("favorites")) || [];
    setFavorites(data);
  }, []);

  return (
    <div>
      <h1>⭐ Favorites</h1>
      {favorites.length === 0 ? (
        <p>No favorites saved yet.</p>
      ) : (
        favorites.map((article, idx) => (
          <ArticleCard key={idx} article={article} />
        ))
      )}
    </div>
  );
}

export default Favorites;
