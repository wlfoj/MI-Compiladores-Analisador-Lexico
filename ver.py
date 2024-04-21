import re

# Definindo as expressões regulares para os tokens
expressoes_regulares = [
    (r'[a-zA-Z][a-zA-Z0-9_]*', 'IDENTIFICADOR'),  # Identificadores (variáveis)
    (r'\d+', 'NUMERO'),  # Números inteiros
    (r'\+', 'MAIS'),     # Operador de adição
    (r'-', 'MENOS'),     # Operador de subtração
    (r'\*', 'VEZES'),    # Operador de multiplicação
    (r'/', 'DIVIDIDO'),  # Operador de divisão
    (r'\(', 'ABRE_PARENTESES'),  # Parêntese esquerdo
    (r'\)', 'FECHA_PARENTESES')   # Parêntese direito
]
EXPRESSAO_CARACTERE_INVALIDO = r'[^a-zA-Z0-9_\s]'
# Função para tokenizar a entrada
def tokenizar(entrada):
    tokens = []
    posicao = 0
    while posicao < len(entrada):
        match = None
        for expressao_regular, tipo_token in expressoes_regulares:
            regex = re.compile(expressao_regular)
            match = regex.match(entrada, posicao)
            if match:
                valor = match.group(0)
                tokens.append((valor, tipo_token))
                posicao = match.end(0)
                break
            if not match:
                print(f"Erro: Caractere inválido encontrado: {entrada[posicao]}")
                return None
    return tokens

# Teste do analisador léxico
entrada = "x 10 + 20"
tokens = tokenizar(entrada.replace(" ", ""))
if tokens:
    for token in tokens:
        print(token)