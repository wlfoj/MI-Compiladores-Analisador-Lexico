


PATH = 'files/' 
# Criar um arquivo
with open(PATH + 't1' + '.txt', 'r') as f:
    count = 0
    for linha in f:
        count = count + 1
        print(linha.replace('\n', '') + ' -- ', count)