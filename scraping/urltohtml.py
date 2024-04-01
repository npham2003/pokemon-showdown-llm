import os
import requests
from bs4 import BeautifulSoup

def save_webpage_html(url, file_path):
    """
    Fetches the HTML content of a website and writes it to a file.
    :param url: The URL of the website to fetch.
    :param file_path: The path of the file where the HTML content will be saved.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for 4xx/5xx errors
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(response.text)
        print(f"HTML content saved to {file_path}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

def get_pokemon_links(base_url):
    """
    Fetches the webpage and parses it to find the links to each Pokémon's page.
    :param base_url: The URL of the website to fetch.
    :return: A list of URLs for each Pokémon's page.
    """
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        link_elements = soup.find_all('a', href=True)
        pokemon_links = [link['href'] for link in link_elements if 'pokedex/rby/' in link['href'] and not link['href'].startswith('http')]
        return pokemon_links
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return []

def save_all_pokemon_html(base_url, folder_name='pokemon_html'):
    """
    Saves the HTML page for each Pokémon by finding their links and calling save_webpage_html.
    :param base_url: The base URL of the main Pokémon list page.
    :param folder_name: The name of the folder where HTML files will be saved.
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    pokemon_links = get_pokemon_links(base_url)
    if not pokemon_links:
        print("No Pokémon links found.")
        return

    for link in pokemon_links:
        pokemon_name = link.split('/')[-1].split('?')[0].strip().lower()  # Trim whitespace and convert to lowercase
        file_path = os.path.join(folder_name, f"{pokemon_name}.html")
        full_url = f"{base_url}/{pokemon_name}"  # Construct the full URL
        save_webpage_html(full_url, file_path)

# Usage example
base_url = "https://www.pikalytics.com/pokedex/rby"
save_all_pokemon_html(base_url)
