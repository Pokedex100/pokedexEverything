import requests
from bs4 import BeautifulSoup
import json
import re


def scrape_pokemon_info(pokemon_url):
    # Send a GET request to the Bulbapedia page for the specified Pokemon
    response = requests.get(pokemon_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Example: Extracting more information about Pikachu
        pokemon_info = {}

        # Find the content area
        content_area = soup.find('div', {'id': 'mw-content-text'})

        # Find all tables containing Pokemon details
        tables = content_area.find_all('table', {'class': 'roundy'})

        # Extract relevant information
        for table in tables:
            for row in table.find_all('tr'):
                ability_elements = row.find_all(
                    'a', {'title': re.compile('.+\(Ability\)')})
                if ability_elements:
                    ability = []
                    for ability_element in ability_elements:
                        if (ability_element.text.strip() != "Cacophony"):
                            ability.append(
                                ability_element.text.strip())
                    pokemon_info['profile'] = {'ability': ability}

                # Egg Group
                egg_element = row.find(
                    'a', {'title': re.compile('.+\(Egg Group\)')})
                if egg_element:
                    pokemon_info['profile'].update(
                        {'egg': egg_element.text.strip()})

                # Category:Pokémon with a gender ratio
                genderElement = row.find('a', {'title': re.compile(
                    'Category:Pokémon with a gender ratio.+')})
                if genderElement:
                    pokemon_info['profile'].update(
                        {'gender': genderElement.text.strip()})

                # Catch Rate: When an ordinary Poké Ball
                catchElement = row.find('span', {'title': re.compile(
                    'When an ordinary Poké Ball.+')})
                if catchElement:
                    pokemon_info['profile'].update(
                        {'catchRate': catchElement.text.strip()})

                # Look for the <span> inside an anchor tag with title "List of Pokémon by National Pokédex number"
                id_element = row.find(
                    'a', {'title': 'List of Pokémon by National Pokédex number'})
                if id_element:
                    pokemon_info['id'] = id_element.text.strip()
                else:
                    continue

                # Extract other information based on the structure
                name_element = row.find(
                    'td', {'class': 'roundy'}).find('big').find('b')
                if name_element:
                    pokemon_info['name'] = {
                        'english': name_element.text.strip(),
                        'japanese': row.find('span', {'lang': 'ja'}).text.strip()
                    }
                else:
                    continue

                forms_elements = row.find(
                    'td').find_all('small')
                if forms_elements:
                    pokemon_info['forms'] = ["Unset"]
                    for form_element in forms_elements:
                        if form_element.text.strip() and form_element.text.strip() != name_element.text.strip():
                            form = form_element.text.strip().replace(
                                name_element.text.strip(), "").replace("  ", " ").strip()
                            form = re.sub(' +', ' ', form)
                            if form not in pokemon_info['forms']:
                                pokemon_info['forms'].append((form))

                # Look for Pokémon category
                category_element = row.find(
                    'a', {'title': 'Pokémon category'})
                if category_element:
                    pokemon_info['species'] = category_element.text.strip()
                else:
                    continue

                description = row.find_next('p')
                if description:
                    pokemon_info['description'] = description.text.strip()

                 # Generation
                gen_element = description.find(
                    'a', {'title': re.compile('Generation*')})
                if gen_element:
                    pokemon_info['generation'] = gen_element.text.strip()
                else:
                    continue

        return pokemon_info

    else:
        print(
            f"Failed to retrieve the page. Status code: {response.status_code}")
        return None


def get_pokemon_names_from_json(json_file):
    # Read the JSON file
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Extract Pokémon names from the JSON data
    pokemon_names = [data[key] for key in sorted(data.keys())]

    return pokemon_names


# Get Pokémon names from the "pokédexdata.json" file
pokemon_names = get_pokemon_names_from_json('../data/pokédexdata.json')

# URL template for Pokémon pages
pokemon_base_url = 'https://bulbapedia.bulbagarden.net/wiki/{}_(Pokémon)'

# Create a list to store information for the Pokémons
pokemon_list = []

# Loop through the Pokémon names
for pokemon_name in pokemon_names[:6]:
    pokemon_url = pokemon_base_url.format(pokemon_name)

    # Scrape information for the current Pokémon
    pokemon_info = scrape_pokemon_info(pokemon_url)

    if pokemon_info:
        # Append the information to the list
        pokemon_list.append(pokemon_info)

# Write the JSON output to the "pokédex.json" file
with open('../data/pokédex.json', 'w', encoding='utf-8') as output_file:
    json.dump(pokemon_list, output_file, indent=2,
              ensure_ascii=False)

# Write the JSON output to the "pokédex.json" dist file
with open('../dist/json/pokédex.json', 'w', encoding='utf-8') as output_file:
    json.dump(pokemon_list, output_file, indent=2,
              ensure_ascii=False)

print("Scraped data has been written to 'pokédex.json'")
