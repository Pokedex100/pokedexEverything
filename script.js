const dataUrl = "./data.json";

const pokemonInput = document.getElementById("pokemonInput");
const jsonOutput = document.getElementById("jsonOutput");

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
    return;
  }

  try {
    const pokemon = await getPokemonData(input);
    if (pokemon) {
      displayJSON(pokemon);
    } else {
      jsonOutput.textContent = `Error: Pokémon ${input} not found`;
    }
  } catch (error) {
    jsonOutput.textContent = `Error: Failed to load data - ${error.message}`;
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
  jsonOutput.textContent = formatted;
}
