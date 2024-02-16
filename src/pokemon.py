import requests
from bs4 import BeautifulSoup
import json
import re
import string


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
        # Added a numbered iteration
        for table_number, table in enumerate(tables):
            # for row_number, row in enumerate(table.find_all('tr')): # Added a numbered iteration

            if table_number == 0:
                # Look for the <span> inside an anchor tag with title "List of Pokémon by National Pokédex number"
                id_element = table.find(
                    'a', {'title': 'List of Pokémon by National Pokédex number'})
                if id_element:
                    pokemon_info['id'] = id_element.text.strip()

                # Extract other information based on the structure
                name_element = table.find(
                    'td', {'class': 'roundy'}).find('big').find('b')
                if name_element:
                    pokemon_info['name'] = {
                        'english': name_element.text.strip(),
                        'japanese': table.find('span', {'lang': 'ja'}).text.strip()
                    }

                forms_elements = table.find(
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

                # Initiate 'formData' with 'names'
                pokemon_info['formData'] = []
                for form in pokemon_info['forms']:
                    pokemon_info['formData'].append({'form': form})

                # Store forms in a temporary variable as well excluding text manipulation in order to use it as keys for data extraction against 'form'
                temp_forms = []
                temp_form_elements = table.find_all(
                    'tr')[3].find_all('a', {'class': 'image'})

                # print(table.find_all( 'tr')[3].prettify())
                if temp_form_elements:
                    count = 0
                    for temp_form_element_index, temp_form_element in enumerate(temp_form_elements):
                        if not temp_form_element.find_parent('tr').has_attr('style'):
                            if (temp_forms.count(temp_form_element.get('title', '')) < 1):
                                temp_forms.append(
                                    temp_form_element.get('title', ''))
                                pokemon_info['formData'][count]['formName'] = temp_form_element.get(
                                    'title', '')
                                count += 1
                    print(temp_forms)

                # Extracting 'types' of pokemon against 'form'
                type_element = table.find(
                    'a', {'title': re.compile('Type')}).find_parent('tr')
                types = []
                for td in type_element.find_all('td', style=re.compile('display: none;+')):
                    td.extract()
                if (len(temp_forms) > 1):
                    for form_index, form in enumerate(temp_forms):
                        form_type_element = type_element.find(
                            "small", string=form)
                        single_forms = []
                        if form_type_element:
                            form_types = form_type_element.parent.find_all('b')
                            for single_form in form_types:
                                single_forms.append(single_form.text.strip())
                            for index, iter in enumerate(single_forms):
                                if iter == 'Unknown' and index > 0:
                                    single_forms.pop(index)
                            types.append(single_forms)
                        else:
                            form_types = type_element.find_all(
                                'td')[1].find_all('b')
                            for single_form in form_types:
                                single_forms.append(single_form.text.strip())
                            types.append(single_forms)
                        pokemon_info['formData'][form_index]['type'] = single_forms
                else:
                    form_section = type_element.find_all('b')
                    for iter in form_section:
                        parent_a = iter.find_parent('a')
                        if parent_a and parent_a.has_attr('class'):
                            continue
                        types.append(iter.text)
                    if types:
                        types.pop(0)
                    pokemon_info['formData'][0]['type'] = types
                print(types)

                # Extracting the height of Pokemon against 'form'
                height_element = table.find(
                    'a', {'title': 'List of Pokémon by height'}).find_parent('td')
                default_pokemon_height = ''
                for form_index, form in enumerate(temp_forms):
                    form_height_element_identifier = height_element.find(
                        "small", string=form)
                    if form_height_element_identifier:
                        form_height_element = form_height_element_identifier.find_parent(
                            'tr').find_previous_sibling('tr')
                        form_height = form_height_element.find_all('td')[
                            1].text.strip()
                        if (form_height != '0 m'):
                            default_pokemon_height = form_height
                        if (form_height == '0 m'):
                            form_height = default_pokemon_height
                        pokemon_info['formData'][form_index]['height'] = form_height
                    else:
                        pokemon_info['formData'][form_index]['height'] = default_pokemon_height

                # Extracting the weight of Pokemon against 'form'
                weight_element = table.find(
                    'a', {'title': 'Weight'}).find_parent('td')
                default_pokemon_weight = ''
                for form_index, form in enumerate(temp_forms):
                    form_weight_element_identifier = weight_element.find(
                        "small", string=form)
                    if form_weight_element_identifier:
                        form_weight_element = form_weight_element_identifier.find_parent(
                            'tr').find_previous_sibling('tr')
                        form_weight = form_weight_element.find_all('td')[
                            1].text.strip()
                        if (form_weight != '0 kg'):
                            default_pokemon_weight = form_weight
                        else:
                            form_weight = default_pokemon_weight
                        pokemon_info['formData'][form_index]['weight'] = form_weight
                    else:
                        pokemon_info['formData'][form_index]['weight'] = default_pokemon_weight

            # Look for Pokémon category
            category_element = table.find(
                'a', {'title': 'Pokémon category'})
            if category_element:
                pokemon_info['species'] = category_element.text.strip()
            else:
                continue

            description = table.find_next('p')
            if description:
                pokemon_info['description'] = description.text.strip()

            # Generation
            gen_element = description.find(
                'a', {'title': re.compile('Generation*')})
            if gen_element:
                pokemon_info['generation'] = gen_element.text.strip()
            else:
                continue

            ability_elements = table.find_all(
                'a', {'title': re.compile('.+\\(Ability\\)')})
            if ability_elements:
                ability = []
                for ability_element in ability_elements:
                    if (ability.count(ability_element.text.strip()) < 1):
                        if (ability_element.text.strip() != "Cacophony"):
                            ability.append(
                                ability_element.text.strip())
                pokemon_info['profile'] = {'ability': ability}

            # Egg Group
            egg_element = table.find(
                'a', {'title': re.compile('.+\\(Egg Group\\)')})
            if egg_element:
                pokemon_info['profile'].update(
                    {'egg': egg_element.text.strip()})

            # Category:Pokémon with a gender ratio
            genderElement = table.find('a', {'title': re.compile(
                'Category:Pokémon with a gender ratio.+')})
            if genderElement:
                pokemon_info['profile'].update(
                    {'gender': genderElement.text.strip()})

            # Catch Rate: When an ordinary Poké Ball
            catchElement = table.find('span', {'title': re.compile(
                'When an ordinary Poké Ball.+')})
            if catchElement:
                pokemon_info['profile'].update(
                    {'catchRate': catchElement.text.strip()})

        return pokemon_info

    else:
        print(
            f"Failed to retrieve the page. Status code: {response.status_code}")
        with open("../data/pokemonFailedToFetch.log", "a", encoding="utf-8") as f:
            f.write(pokemon_url + '\n')
        return None


def get_pokemon_names_from_json(json_file):
    # Read the JSON file
    with open(json_file, 'r', encoding='utf-8') as file:
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

# Capitalize the letter after hyphen


def capitalize_after_hyphen(s):
    if (s.count('-') > 0):
        parts = s.split('-')
        capitalized_parts = [string.capwords(part) for part in parts[:-1]]
        last_part = ''
        if not parts[-1].endswith('o'):
            last_part = string.capwords(parts[-1])
        elif len(parts[-1]) > 1:
            last_part = string.capwords(parts[-1])
        else:
            last_part = parts[-1].lower()
        capitalized_parts.append(last_part)
        return '-'.join(capitalized_parts)
    return s


# Loop through the Pokémon names
for pokemon_name in pokemon_names[:1025]:
    pokemon_name = string.capwords(pokemon_name)
    pokemon_name = capitalize_after_hyphen(pokemon_name)
    print(pokemon_name)
    pokemon_name = pokemon_name.replace(' ', '_')
    pokemon_url = pokemon_base_url.format(pokemon_name)
    print(pokemon_url)

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
