import random
import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import stem.process
from urllib.parse import urlparse

def fetch_queries_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"\x1b[31mArquivo {file_path} não encontrado.\x1b[0m")
        return []

def generate_random_user_agent():
    user_agent = UserAgent()
    return user_agent.random

def get_search_results(query, user_agent):
    headers = {
        "User-Agent": user_agent,
    }
    url = f"https://www.google.com/search?q={query}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a")
        results = [link["href"] for link in links if link.get("href") and "http" in link["href"]]
        return results
    return []

def configure_tor():
    tor_process = stem.process.launch_tor_with_config(
        config={
            'SocksPort': str(9050),
            'ControlPort': str(9051),
            'Log': ['NOTICE', 'ERR'],
        },
        init_msg_handler=print,
    )
    return tor_process

def perform_search(domain, queries, search_mode, save_to_file):
    results = []
    tor_process = None

    if search_mode in ['2', '3']:
        tor_process = configure_tor()

    for query in queries:
        full_query = f"{domain} {query}"
        try:
            user_agent = generate_random_user_agent()
            search_results = get_search_results(full_query, user_agent)
            if search_results:
                for url in search_results:
                    parsed_url = urlparse(url)
                    if domain in parsed_url.hostname:
                        results.append(url)

            time.sleep(random.randint(5, 10))

        except Exception as e:
            print(f"Erro ao realizar a busca: {e}")

    if tor_process:
        tor_process.kill()

    if save_to_file == 's':
        with open("filtered_urls.txt", 'a') as file:
            for url in results:
                file.write(url + '\n')

    return results

