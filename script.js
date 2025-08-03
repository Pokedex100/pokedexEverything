const dataUrl = "./data.json";

const pokemonInput = document.getElementById("pokemonInput");
const jsonOutput = document.getElementById("jsonOutput");
const pokemonImage = document.getElementById("pokemonImage");

// Event listeners
pokemonInput.addEventListener("input", handleInput);
pokemonInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    handleInput();
  }
});

// Load Pikachu by default
window.addEventListener("load", () => {
  pokemonInput.value = "#25";
  handleInput();
});

async function handleInput() {
  const input = pokemonInput.value.trim();

  if (!input) {
    jsonOutput.textContent = "";
    jsonOutput.className = "";
    pokemonImage.style.display = "none";
    return;
  }

  try {
    const pokemon = await getPokemonData(input);
    if (pokemon) {
      displayJSON(pokemon);
    } else {
      jsonOutput.textContent = `Error: Pokémon ${input} not found`;
      jsonOutput.className = "error";
      pokemonImage.style.display = "none";
    }
  } catch (error) {
    jsonOutput.textContent = `Error: Failed to load data - ${error.message}`;
    jsonOutput.className = "error";
    pokemonImage.style.display = "none";
  }
}

async function getPokemonData(input) {
  const response = await fetch(dataUrl);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }

  const data = await response.json();

  // Handle different input formats
  let id;
  if (input.startsWith("#")) {
    // Handle ID input like #25
    id = input.substring(1);
  } else {
    // Handle numeric input like 25
    id = input;
  }

  const paddedId = id.padStart(4, "0");
  return data.find((p) => p.id.substring(1) === paddedId);
}

function displayJSON(pokemon) {
  const formatted = JSON.stringify(pokemon, null, 2);

  // Clear previous highlighting
  jsonOutput.className = "";
  jsonOutput.removeAttribute("data-highlighted");
  jsonOutput.innerHTML = "";

  // Set new content and highlight
  jsonOutput.textContent = formatted;
  jsonOutput.className = "language-json";
  hljs.highlightElement(jsonOutput);

  // Show Pokemon image from PokéDB with fallback
  const pokemonId = parseInt(pokemon.id.substring(1));
  const pokemonName = pokemon.name.english
    .toLowerCase()
    .replace(/[^a-z0-9]/g, "");

  pokemonImage.src = `https://img.pokemondb.net/sprites/home/normal/${pokemonName}.png`;
  pokemonImage.onerror = () => {
    // Fallback to PokeAPI official artwork
    pokemonImage.src = `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/${pokemonId}.png`;
  };
  pokemonImage.style.display = "block";
}
