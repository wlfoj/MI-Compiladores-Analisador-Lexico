"""
Trecho de código que obtem a lista de entradas
"""
import os

caminho_da_pasta = 'files'

# Listar arquivos na pasta (Nomes)
arquivos_na_pasta = os.listdir(caminho_da_pasta)

arquivos_entrada = []

# Imprimir os nomes dos arquivos
for arquivo in arquivos_na_pasta:
    #print(arquivo)
    if arquivo.endswith(".txt"):
        arquivos_entrada.append(arquivo)

print(arquivos_entrada)