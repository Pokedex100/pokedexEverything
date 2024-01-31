const express = require("express");
const cors = require("cors");
const fs = require("fs");
const path = require("path");

const app = express();
const port = 3000;

// Enable CORS for all origins
app.use(cors({ origin: "*" }));

app.get("/api/pokedex", (req, res) => {
  // Construct the correct file path
  const jsonFilePath = path.join(__dirname, "../data/", "pokédex.json");

  // Read the JSON file
  const pokedexData = JSON.parse(fs.readFileSync(jsonFilePath, "utf-8"));
  res.json(pokedexData);
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
