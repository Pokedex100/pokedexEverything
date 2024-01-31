const apiUrl = "http://localhost:3000/api/pokedex";

// Function to fetch Pokémon data
async function getPokemonData(pokemonName) {
  try {
    // Fetch data from the API
    const response = await fetch(apiUrl);

    // Check if the response is successful (status code 200)
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    // Parse the JSON response
    const data = await response.json();

    // Find the Pokémon data by name
    const pokemon = data.find(
      (p) => p.name.english.toLowerCase() === pokemonName.toLowerCase()
    );

    if (pokemon) {
      console.log(`ID: ${pokemon.id}`);
      console.log(`Name (English): ${pokemon.name.english}`);
      console.log(`Name (Japanese): ${pokemon.name.japanese}`);
      console.log(`Description: ${pokemon.description}`);
    } else {
      console.log(`Pokemon with name "${pokemonName}" not found.`);
    }
  } catch (error) {
    console.error("Error fetching data:", error.message);
  }
}

// Example: Get data for Pikachu
getPokemonData("pikachu");
