import streamlit as st
from utils import perform_search, fetch_queries_from_file
import time

st.title("Web Search Application")

domain = st.text_input("Digite o domínio alvo (por exemplo, 'example.com'):")
queries_input = st.text_area("Digite as queries (dorks) específicas, separadas por vírgulas (deixe vazio para usar a wordlist padrão):")
search_mode = st.selectbox("Escolha o modo de busca:", ["Surface Web", "Dark Web", "Ambos"])
save_to_file = st.selectbox("Deseja salvar as URLs encontradas em um arquivo de texto?", ["Sim", "Não"])

def create_downloadable_file(results):
    """Cria o conteúdo do arquivo de texto para download"""
    return "\n".join(results)

# Inicializar o estado do botão de parada
if "stop_search" not in st.session_state:
    st.session_state.stop_search = False

def stop_search():
    st.session_state.stop_search = True

# Contêiner para exibir os resultados encontrados
results_placeholder = st.container()
progress_bar = st.progress(0)

if st.button("Buscar"):
    if domain:
        if queries_input:
            queries = queries_input.split(',')
        else:
            queries = fetch_queries_from_file('dorks.txt')
        
        search_mode_value = {'Surface Web': '1', 'Dark Web': '2', 'Ambos': '3'}[search_mode]
        save_to_file_value = 's' if save_to_file == 'Sim' else 'n'
        
        all_results = []
        total_queries = len(queries)
        st.session_state.stop_search = False
        
        # Adicionar o botão "Parar Busca" fora do loop
        st.button("Parar Busca", on_click=stop_search)
        
        for i, query in enumerate(queries):
            if st.session_state.stop_search:
                break

            new_results = perform_search(domain, [query], search_mode_value, save_to_file_value)
            all_results.extend(new_results)
            
            progress_bar.progress((i + 1) / total_queries)

            with results_placeholder:
                st.write(f"**Resultados para a dork:** `{query}`")
                for result in new_results:
                    st.write(f"- {result}")
                st.write("---")
            
            time.sleep(1)

        if st.session_state.stop_search:
            st.warning("Busca interrompida pelo usuário.")
        elif all_results:
            st.success(f"{len(all_results)} resultados encontrados.")
        else:
            st.warning("Nenhum resultado encontrado.")
        
        if all_results:
            file_content = create_downloadable_file(all_results)
            st.download_button(
                label="Baixar resultados como TXT",
                data=file_content,
                file_name="resultados_encontrados.txt",
                mime="text/plain"
            )
    else:
        st.error("Por favor, preencha todos os campos.")
