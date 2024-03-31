import os


caminho_da_pasta = 'files/'

# =====================================================================
def obtem_arquivos_entrada():
    # Listar arquivos na pasta (Nomes)
    arquivos_na_pasta = os.listdir(caminho_da_pasta)
    arquivos_entrada = []
    # Imprimir os nomes dos arquivos
    for arquivo in arquivos_na_pasta:
        #print(arquivo)
        if arquivo.endswith(".txt"):
            arquivos_entrada.append(arquivo)
    return arquivos_entrada


def criar_arquivo_saida(nome_arquivo_entrada, lista_tokens):
    with open(caminho_da_pasta + nome_arquivo_entrada.replace('.txt', '') + '-saida.txt', 'w') as f:
        f.write('Conteúdo do arquivo') # escreve a lista de tokens


def analisador (linha) -> str: # RETORNA O TOKEN
    linha = linha.replace('\n', '') # Retirando o \n
    # Acessando os caracters
    for i in range(len(linha)):
        print(linha[i])
        # Tento descobrir oq o caracter atual é
        # Se não descobrir, tento analisar o primeiro com o segundo caracter
        # Após descobrir oq é, continuo percorrendo até achar um delimitador para encontrar qual tipo de palavra ele é
        # Repito o processo até concluir a linha


# =============== Obtenho os arquivos na pasta files/ =============== #
entradas = obtem_arquivos_entrada()





# =============== Acesso os arquivos de entrada obtidos =============== #
for arquivo in entradas:
    with open(caminho_da_pasta + arquivo, 'r') as f:
        # Acessando as linhas
        for linha in f:
            linha = linha.replace('\n', '') # Retirando o \n
            # Acessando os caracters
            for i in range(len(linha)):
                print(linha[i])

