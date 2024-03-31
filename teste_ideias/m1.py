"""
Trecho de código que cria arquivos de saída e os deleta
"""

import os

PATH = 'files/' 
# Criar um arquivo
with open(PATH + 'arquivo' + '-saida.txt', 'w') as f:
    f.write('Conteúdo do arquivo')

# Deletar um arquivo
os.remove(PATH + 'arquivo' + '-saida.txt')