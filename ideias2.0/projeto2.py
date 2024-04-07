import os
import re
from lexicos import palavras_reservadas, estrutura_lexica

def classificar_token(token, tipo):
    if tipo == "ERRO":
        return tipo
    elif token in palavras_reservadas:
        return "PALAVRA_RESERVADA"
    elif re.match(estrutura_lexica['identificador'], token):
        return "IDENTIFICADOR"
    elif re.match(estrutura_lexica['numero'], token):
        return "NUMERO"
    elif re.match(estrutura_lexica['cadeia_caracteres'], token):
        return "CADEIA DE CARACTERES"
    elif token in estrutura_lexica['delimitadores']:
        return "DELIMITADOR"
    elif token in estrutura_lexica['operadores_relacionais']:
        return "OPERADOR RELACIONAL" 
    elif token in estrutura_lexica['operadores_logicos']:
        return "LOG" 
    elif token in estrutura_lexica['operadores_relacionais'] or token in estrutura_lexica['operadores_aritmeticos'] or token in estrutura_lexica['operadores_logicos']:
        return "OPERADOR"
    else:
        # Para tokens não reconhecidos explicitamente, podemos retornar um tipo genérico ou erro.
        return "TOKEN NÃO RECONHECIDO"

def analisar_lexicamente_e_criar_saida(caminho_completo):
    diretorio, nome_arquivo = os.path.split(caminho_completo)
    nome_base = nome_arquivo.rsplit('.', 1)[0]
    nome_arquivo_saida = f"{nome_base}-saida.txt"
    caminho_arquivo_saida = os.path.join(diretorio, nome_arquivo_saida)

    tokens = []
    token_atual = ""
    estado_atual = "ESTADO_INICIAL"
    comentario_em_bloco = False
    comentario_atual = ""
    linha_atual = 1  # Adiciona um contador para a linha atual

    with open(caminho_completo, 'r', encoding='utf-8') as arquivo:
        texto = arquivo.read()

    i = 0
    while i < len(texto):
        c = texto[i]

        # Incrementa a contagem de linhas se encontrar uma quebra de linha
        if c == '\n':
            linha_atual += 1

        if comentario_em_bloco:
            comentario_atual += c
            if c == '*' and i + 1 < len(texto) and texto[i + 1] == '/':
                comentario_atual += texto[i + 1]  # Adiciona o '/' do fim do comentário
                tokens.append((comentario_atual, "COMENTARIO EM BLOCO", linha_atual))
                comentario_em_bloco = False
                comentario_atual = ""
                i += 2  # Pula o fim do comentário
            else:
                i += 1
            continue

        if estado_atual == "ESTADO_INICIAL":
            if c == '/' and i + 1 < len(texto) and texto[i + 1] == '*':
                comentario_em_bloco = True
                comentario_atual = "/*"
                i += 2
                continue
            elif c.isalpha():  # Início de um identificador ou palavra reservada
                token_atual = c
                estado_atual = "IDENTIFICADOR"
            elif c.isdigit():  # Início de um número
                token_atual = c
                estado_atual = "NUMERO"
            elif c == '"':  # Início de uma cadeia de caracteres
                token_atual = c
                estado_atual = "CADEIA_CARACTERES"
            elif c in estrutura_lexica['delimitadores']:  # Delimitadores
                tokens.append((c, "DELIMITADOR", linha_atual))
                i += 1
                continue
            elif c in "".join(estrutura_lexica['operadores_relacionais'] + estrutura_lexica['operadores_aritmeticos'] + estrutura_lexica['operadores_logicos']):
                token_atual = c
                estado_atual = "OPERADOR"
            elif c.isspace():  # Ignora espaços em branco
                i += 1
                continue
            else:
                tokens.append((c, "ERRO", linha_atual))
        elif estado_atual == "IDENTIFICADOR":
            if c.isalnum() or c == '_':
                token_atual += c
            else:
                tokens.append((token_atual, "IDENTIFICADOR", linha_atual))
                token_atual = ""
                estado_atual = "ESTADO_INICIAL"
                continue  # Não incrementa i para reavaliar o caractere atual no novo estado
        elif estado_atual == "NUMERO":
            if c.isdigit() or c == '.':
                token_atual += c
            else:
                tokens.append((token_atual, "NUMERO", linha_atual))
                token_atual = ""
                estado_atual = "ESTADO_INICIAL"
                continue
        elif estado_atual == "CADEIA_CARACTERES":
            token_atual += c
            if c == '"':  # Final da cadeia de caracteres
                tokens.append((token_atual, "CADEIA DE CARACTERES", linha_atual))
                token_atual = ""
                estado_atual = "ESTADO_INICIAL"
        elif estado_atual == "OPERADOR":
            token_potencial = token_atual + c

            if token_potencial in estrutura_lexica['operadores_relacionais']:
                token_atual += c
                i += 1  # Isso permite verificar operadores de dois caracteres
                continue
            elif token_atual in estrutura_lexica['operadores_relacionais']:
                tokens.append((token_atual, "OPERADOR RELACIONAL", linha_atual))
                token_atual = ""
                estado_atual = "ESTADO_INICIAL"
            else:
                # Verifica se o token atual ou o token_potencial são outros tipos de operadores
                if token_atual in "".join(estrutura_lexica['operadores_aritmeticos'] + estrutura_lexica['operadores_logicos']):
                    tokens.append((token_atual, "OPERADOR", linha_atual))
                    token_atual = ""
                    estado_atual = "ESTADO_INICIAL"
                continue

        i += 1  # Incrementa o índice para avançar para o próximo caractere

    with open(caminho_arquivo_saida, 'w', encoding='utf-8') as saida:
        for token, tipo, linha in tokens:
            if tipo == "IDENTIFICADOR":
                tipo_abreviado = "IDE"
            elif tipo == "PALAVRA_RESERVADA":
                tipo_abreviado = "PRE"
            elif tipo == "NUMERO":
                tipo_abreviado = "NRO"
            elif tipo == "CADEIA DE CARACTERES":
                tipo_abreviado = "CAC"
            elif tipo == "DELIMITADOR":
                tipo_abreviado = "DEL"
            elif tipo == "OPERADOR RELACIONAL":
                tipo_abreviado = "REL"
            elif tipo == "OPERADOR LOGICO":
                tipo_abreviado = "LOG"
            elif tipo == "OPERADOR ARITMETICO":
                tipo_abreviado = "ART"
            # E assim por diante para os outros tipos de tokens e erros
            else:
                tipo_abreviado = "TMF"  # Para tokens não reconhecidos ou erros

            saida.write(f"{linha:02d} {tipo_abreviado} {token}\n")

    print(f"Análise léxica completa. Arquivo '{caminho_arquivo_saida}' criado/sobrescrito com sucesso.")

def processar_todos_txt_na_pasta_files():
    diretorio = './files'
    
    for arquivo in os.listdir(diretorio):
        if arquivo.endswith('.txt') and '-saida.txt' not in arquivo:
            caminho_completo = os.path.join(diretorio, arquivo)
            analisar_lexicamente_e_criar_saida(caminho_completo)

processar_todos_txt_na_pasta_files()
