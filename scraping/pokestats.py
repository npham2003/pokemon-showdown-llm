import os
import json
from bs4 import BeautifulSoup
import urllib.parse

def extract_pokemon_data(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')

    # Extract the name
    name = soup.find('h1').text.strip()

    # Extract the type
    type_spans = soup.find('span', class_='inline-block pokedex-header-types')
    pokemon_types = [span.text.strip() for span in type_spans.find_all('span', class_='type')] if type_spans else ['Unknown']  # Default to 'Unknown' if types are not found

    # Extract the usage rate
    usage_rate = soup.find('div', class_='pokemon-ind-summary-text gold-font').text.strip('%')

    # Extract the monthly rank
    monthly_rank_element = soup.find('div', class_='pokemon-ind-summary-title', string='Monthly Rank')
    monthly_rank = monthly_rank_element.find_next('div', class_='pokemon-ind-summary-text purple-font').text.strip('#')

    # Extract base stats
    stats = {stat.text.strip(): value.text.strip() for stat, value in zip(soup.select('.pokemon-stat-container div[style*="text-align: left;"]'), soup.select('.pokemon-stat-container div[style*="margin-left: 20px;"]'))}

    # Extract moves, stop reading after encountering "Other"
    moves = {}
    moves_section = soup.select('.pokedex-move-entry-new')
    for move in moves_section:
        move_name = move.find('div', style=lambda value: value and 'margin-left:10px' in value).text.strip()
        move_percentage = move.find('div', style=lambda value: value and 'float:right' in value).text.strip('%')
        moves[move_name] = move_percentage
        if move_name.lower() == 'other':
            break
   
    # Extract teammates
    teammates_list = []
    teammates_section = soup.find_all('a', class_='teammate_entry pokedex-move-entry-new')
    for teammate in teammates_section:
        teammate_name = urllib.parse.unquote(teammate.get('data-name'))  # Remove "%20" and other URL encoding
        percentage_div = teammate.find('div', style="display:inline-block;float:right;")
        type_spans = teammate.find_all('span', class_='type')
        if teammate_name and percentage_div and type_spans:
            percentages = percentage_div.text.strip('%')
            teammate_types = [span.text.strip() for span in type_spans]
            teammates_list.append({'name': teammate_name, 'percentage': percentages, 'type': teammate_types})

    return {
        'name': name,
        'type': pokemon_types,  # Use the original Pokémon's type here
        'usage_rate': usage_rate,
        'monthly_rank': monthly_rank,
        'stats': stats,
        'moves': moves,
        'teammates': teammates_list,
    }

# Example usage
folder_name = 'gen8_html'  # Use your actual folder name where HTML files are stored
data = []
for html_file in os.listdir(folder_name):
    if html_file.endswith('.html'):
        pokemon_data = extract_pokemon_data(os.path.join(folder_name, html_file))
        data.append(pokemon_data)

# Save data to a file
output_file = 'metagen8.txt'
with open(output_file, 'w', encoding='utf-8') as outfile:
    for pokemon in data:
        json.dump(pokemon, outfile, ensure_ascii=False)
        outfile.write('\n\n')  # Add a double new line after each entry
