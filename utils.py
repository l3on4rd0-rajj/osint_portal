import random
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Lista de user agents comuns
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/92.0.902.67",
    # Adicione mais user agents conforme necessário
]

def generate_random_user_agent():
    """Gera um user-agent aleatório a partir de uma lista predefinida."""
    return random.choice(USER_AGENTS)

def fetch_queries_from_file(file_path):
    """Obtém consultas (dorks) de um arquivo de texto."""
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Arquivo {file_path} não encontrado.")
        return []
    except Exception as e:
        print(f"Erro ao ler o arquivo {file_path}: {e}")
        return []

def get_search_results(query, user_agent):
    """Obtém resultados de busca da Google para uma consulta específica."""
    headers = {
        "User-Agent": user_agent,
    }
    url = f"https://www.google.com/search?q={query}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Levanta um erro se a resposta for ruim
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a")
        results = [link["href"] for link in links if link.get("href") and "http" in link["href"]]
        return results
    except requests.RequestException as e:
        print(f"Erro ao buscar resultados para a consulta '{query}': {e}")
        return []
    except Exception as e:
        print(f"Erro ao processar a resposta da consulta '{query}': {e}")
        return []

def perform_search(domain, queries, search_mode, save_to_file):
    """Realiza buscas para as dorks fornecidas e retorna resultados filtrados por domínio."""
    results = []
    for query in queries:
        full_query = f"{domain} {query}"
        print(f"Executando busca com query: {full_query}")
        try:
            user_agent = generate_random_user_agent()
            search_results = get_search_results(full_query, user_agent)
            print(f"Resultados da busca: {search_results}")
            if search_results:
                for url in search_results:
                    parsed_url = urlparse(url)
                    if domain in parsed_url.hostname:
                        results.append(url)

            time.sleep(random.randint(5, 10))  # Pausa entre as buscas

        except Exception as e:
            print(f"Erro ao realizar a busca: {e}")

    if save_to_file == 's':
        try:
            with open("filtered_urls.txt", 'a') as file:
                for url in results:
                    file.write(url + '\n')
        except IOError as e:
            print(f"Erro ao salvar os resultados em arquivo: {e}")

    return results

def save_results_to_file(results):
    """Salva os resultados da busca em um arquivo de texto."""
    try:
        with open("filtered_urls.txt", 'a') as file:
            for url in results:
                file.write(url + '\n')
    except IOError as e:
        print(f"Erro ao salvar os resultados em arquivo: {e}")
