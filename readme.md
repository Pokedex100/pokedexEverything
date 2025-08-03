<div align="center">
  <img src="logo.png" alt="Pokédex Everything Logo" width="200"/>
  
# 🔍 Pokédex Everything - Complete Pokemon JSON Database

  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Pokemon Count](https://img.shields.io/badge/Pokémon-1,025-blue)](#)
  [![JSON Size](https://img.shields.io/badge/JSON-1.7MB-green)](#)
</div>

A comprehensive, developer-friendly Pokemon database with complete JSON data for all 1,025 Pokemon. Features a clean, minimal JSON viewer for developers who need quick access to Pokemon data.

## ✨ Features

- 🎯 **Complete Dataset**: All 1,025 Pokemon through Generation IX
- 📋 **Rich Data**: Names, types, abilities, descriptions, forms, images
- 🔍 **Developer JSON Viewer**: Clean interface with ID-based lookup (#25, #150, etc.)
- 🎨 **Multiple Forms**: Supports Mega, Gigantamax, Regional variants  
- 📸 **Image Assets**: Normal and shiny sprite paths included
- 🚀 **Zero Dependencies**: Just JSON data + simple HTML viewer

---

## JSON Schema

### Current Implementation (v1.0)

```typescript
interface PokemonData {
  id: string;                    // Format: "#0001"
  assets: {
    normal: string[];            // Array of normal sprite image paths
    shiny: string[];             // Array of shiny sprite image paths
  };
  name: {
    english: string;             // English name
    japanese: string;            // Japanese name (original)
  };
  forms: string[];               // Array of form names ["Default", "Mega", "Gigantamax"]
  formData: FormData[];          // Array of form-specific data
  species: string;               // Pokémon category (e.g., "Seed Pokémon")
  description: string;           // Pokédex description
  generation: string;            // Generation introduced (e.g., "Generation I")
  profile: {
    ability: string[];           // Array of abilities
    egg: string;                 // Egg group
    gender: string;              // Gender ratio (e.g., "87.5% male, 12.5% female")
    catchRate: string;           // Catch rate percentage
  };
}

interface FormData {
  form: string;                  // Form name (e.g., "Default", "Mega")
  formName: string;              // Full form name (e.g., "Mega Charizard X")
  type: string[];                // Types for this form
  weaknessTypes: string[];       // Calculated type weaknesses
  height: string;                // Height with units (e.g., "1.7 m")
  weight: string;                // Weight with units (e.g., "90.5 kg")
}
```

### Planned Extensions (v2.0)

```typescript
interface PokemonDataV2 extends PokemonData {
    // Future Extensions (Optional - Not Priority)
  evolution?: {
    evolutionChain: EvolutionNode[];
    evolutionStage: number;      // 1 = basic, 2 = stage 1, 3 = stage 2
  };

  moves?: {
    levelUp: LevelUpMove[];
    tm: string[];                // TM move names
    tr: string[];                // TR move names (if applicable)
    egg: string[];               // Egg moves
    tutor: string[];             // Move tutor moves
  };

  // Additional Data (Optional)
  habitat?: string;              // Natural habitat
  baseExperience?: number;       // Base experience points
  growthRate?: string;           // Experience growth rate
  baseHappiness?: number;        // Base happiness/friendship
}

interface EvolutionNode {
  pokemonId: string;             // Pokémon ID in chain
  evolutionMethod?: {
    trigger: "level" | "stone" | "trade" | "happiness" | "other";
    condition?: string;          // Level number, stone name, etc.
    details?: string;            // Additional requirements
  };
}

interface LevelUpMove {
  name: string;
  level: number;
  method: "level-up" | "evolution" | "reminder";
}
```

## Current API Endpoints

```
GET /api/pokedex          // Returns all Pokémon data
```

## Planned API Endpoints (v2.0)

```
GET /api/pokedex                    // All Pokémon
GET /api/pokedex?pokemon=all        // All Pokémon (explicit)
GET /api/pokedex?pokemon=pikachu    // Specific Pokémon by name
GET /api/pokedex?pokemon=025        // Specific Pokémon by ID
GET /api/pokedex?type=electric      // Filter by type
GET /api/pokedex?generation=1       // Filter by generation
GET /api/search?q=pika             // String search
```

---

## Development Status

### Data Completeness

- **Pokémon Count**: 1,025 (Complete through Pecharunt #1025)
- **Basic Info**: Names, types, forms, height, weight, abilities
- **Type Weaknesses**: Calculated automatically
- **Images**: Normal and shiny sprite paths

### Optional Enhancements 🔮

The core dataset is complete! These are optional additions for future versions:

- **Evolution Data**: Evolution chains and methods
- **Move Data**: Learnable moves and movesets  
- **Habitat Data**: Location/habitat information

### Project Status

**✅ COMPLETE:**

- [x] Complete 1,025 Pokemon JSON dataset
- [x] Clean developer JSON viewer
- [x] Professional documentation
- [x] MIT License and proper attribution
- [x] Image asset paths included
- [x] Multiple Pokemon forms supported
- [x] Data validation completed

**📦 READY FOR USE:**
The project is production-ready! Just download and use the JSON data or run the viewer locally.

## 🚀 Quick Start

### Option 1: Use the JSON Data Directly

```bash
# The complete Pokemon dataset is in:
data.json  # 1.7MB, all 1,025 Pokemon

# Just import and use in your project!
```

### Option 2: Run the JSON Viewer 🔍

```bash
# Start local server
python3 -m http.server 8000

# Open viewer
open http://localhost:8000/dist/examples/

# Enter Pokemon ID: #25, #150, #1, etc.
```

**Alternative Viewer Options:**

- **VS Code**: Install Live Server extension → Right-click `dist/examples/index.html` → "Open with Live Server"  
- **Direct**: Open `dist/examples/index.html` in browser (may have CORS issues)

## 📊 Data Attribution

This project uses Pokemon data sourced from:

- **[Bulbapedia](https://bulbapedia.bulbagarden.net/)** - The community-driven Pokemon encyclopedia
- **[PokemonDB](https://pokemondb.net/)** - Comprehensive Pokemon database

All Pokemon names, images, and related content are copyright of Nintendo, Game Freak, and Creatures Inc.

## 🎯 Use Cases

- **Developers**: Import `data.json` into your Pokemon app
- **Researchers**: Complete dataset for analysis and projects  
- **Quick Lookup**: Use the viewer to find specific Pokemon data
- **Reference**: Comprehensive Pokemon information in structured format

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
