import os

def ler_e_criar_arquivo(nome_arquivo_original):
    # Define o caminho da pasta onde os arquivos serão lidos e escritos
    pasta = 'files'
    nome_arquivo_saida = f"{nome_arquivo_original.split('.')[0]}-saida.txt"
    caminho_arquivo_original = os.path.join(pasta, nome_arquivo_original)
    caminho_arquivo_saida = os.path.join(pasta, nome_arquivo_saida)

    try:
        # Lê o arquivo original com a codificação especificada
        with open(caminho_arquivo_original, 'r', encoding='utf-8') as arquivo_original:
            conteudo_original = arquivo_original.read()
        
        # O conteúdo do arquivo de saída será idêntico ao do arquivo original
        texto_saida = conteudo_original
        
        # Sobrescreve o arquivo de saída se ele já existir, com o conteúdo original
        with open(caminho_arquivo_saida, 'w', encoding='utf-8') as arquivo_saida:
            arquivo_saida.write(texto_saida)
        
        print(f"Arquivo '{nome_arquivo_saida}' criado/sobrescrito com sucesso na pasta '{pasta}'.")
    
    except FileNotFoundError:
        print(f"O arquivo '{caminho_arquivo_original}' não foi encontrado.")

def processar_todos_txt():
    # Define o caminho da pasta onde os arquivos serão lidos
    PASTA = 'files/'
    try:
        for arquivo in os.listdir(PASTA):
            # Evita processar arquivos que já contêm "-saida" no nome
            if arquivo.endswith('.txt') and '-saida.txt' not in arquivo:
                ler_e_criar_arquivo(arquivo)
    except FileNotFoundError:
        print(f"A pasta '{PASTA}' não foi encontrada. Por favor, verifique se o caminho está correto.")

processar_todos_txt()
