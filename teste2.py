from enum import Enum

# Alfabeto
alfabeto = [chr(ord('a') + i) for i in range(26)]  # Minusculas
alfabeto += [chr(ord('A') + i) for i in range(26)]  # Maiusculas
# Digitos
digitos = [str(i) for i in range(10)]
# Palavras reservadas
reservadas = ['algoritmo', 'principal', 'variaveis', 'constantes', 'registro', 'funcao',
              'retorno', 'vazio', 'se', 'senao', 'enquanto', 'leia', 'escreva', 'inteiro', 'real', 'booleano',
              'char', 'cadeia', 'verdadeiro', 'falso']
delimitadores = [';', ',', '.', '(', ')', '[', ']', '{', '}']

def salva_lexema(lexema, linha, tipo, lista):
    lista.append({'linha': linha, 'tipo': tipo, 'valor': lexema})

class LEX(Enum):
    INICIO = 0
    STRING = 1
    COMENTARIO = 2
    IDENTIFICADOR = 3
    DELIMITADOR = 4
    NUMERO = 5
    RESERVADO = 6
    OPERADOR_ARITMETICO = 7
    OPERADOR_LOGICO = 8
    OPERADOR_RELACIONAL = 9

with open("files/teste.txt", "r") as a:
    linhas = a.readlines()

tokens = []
for numero_linha, linha in enumerate(linhas, start=1):
    i = 0  # Inicialização do iterador da linha
    estado = LEX.INICIO
    lexema = ''
    while i < len(linha):
        char = linha[i]  # Pega o caractere atual na posição i da linha
        # Verifica o estado atual do autômato
        if estado == LEX.INICIO:
            lexema = ''  # Reinicia o lexema
            if char == '"':
                lexema += char  # Inicia o lexema com a aspa dupla, indicando o início de uma string
                estado = LEX.STRING  # Muda o estado para STRING para capturar o restante da string
            elif char in delimitadores:
                # Se o caractere for um delimitador, salva imediatamente
                salva_lexema(char, numero_linha, 'DELIMITADOR', tokens)
            elif char in '+-':
                lexema += char  # Inicia o lexema com o operador
                # Verifica se o próximo caractere forma um operador composto (++ ou --)
                if i + 1 < len(linha) and linha[i + 1] == char:
                    lexema += linha[i + 1]  # Adiciona o próximo caractere ao lexema
                    i += 1  # Avança o índice, pois o próximo caractere já foi processado
                # Salva o lexema como um operador aritmético
                salva_lexema(lexema, numero_linha, 'OPERADOR_ARITMETICO', tokens)
                lexema = ''  # Reseta o lexema
            elif char in '*/':
                # Se o caractere for * ou /, salva como operador aritmético
                salva_lexema(char, numero_linha, 'OPERADOR_ARITMETICO', tokens)
            elif char in alfabeto:
                lexema = char  # Inicia o lexema com o caractere alfabético
                estado = LEX.IDENTIFICADOR  # Muda o estado para IDENTIFICADOR
            elif char in digitos:
                lexema = char  # Inicia o lexema com o dígito
                estado = LEX.NUMERO  # Muda o estado para NÚMERO
            elif char in "=!<>":
                lexema = char  # Inicia o lexema com o operador relacional
                estado = LEX.OPERADOR_RELACIONAL  # Muda o estado para OPERADOR_RELACIONAL
            elif char == '&' or char == '|':
                lexema += char  # Inicia o lexema com o operador lógico
                estado = LEX.OPERADOR_LOGICO  # Muda o estado para OPERADOR_LÓGICO
            elif char == '!':
                # Salva imediatamente o ! como operador lógico
                salva_lexema(char, numero_linha, 'OPERADOR_LOGICO', tokens)
        elif estado == LEX.OPERADOR_LOGICO:
            if (lexema == '&' and char == '&') or (lexema == '|' and char == '|'):
                lexema += char  # Completa o operador lógico (&& ou ||)
                salva_lexema(lexema, numero_linha, 'OPERADOR_LOGICO', tokens)
                lexema = ''  # Reseta o lexema
                estado = LEX.INICIO  # Retorna ao estado INÍCIO
            else:
                # Se não formar um operador lógico válido, mantém o estado INICIO sem consumir o char
                estado = LEX.INICIO
                continue  # Continua a análise no mesmo caractere com o estado alterado
        elif estado == LEX.OPERADOR_RELACIONAL:
            if lexema in ["=", "!", "<", ">"] and char == "=":
                lexema += char  # Completa o operador relacional (==, !=, <=, >=)
                i += 1  # Avança o índice, pois o próximo caractere já foi processado
            salva_lexema(lexema, numero_linha, 'OPERADOR_RELACIONAL', tokens)
            lexema = ''  # Reseta o lexema
            estado = LEX.INICIO  # Retorna ao estado INÍCIO
            continue  # Continua a análise no próximo caractere
        elif estado == LEX.STRING:
            lexema += char  # Adiciona o caractere à string
            if char == '"':
                # Se o caractere for uma aspa dupla, finaliza a string
                salva_lexema(lexema, numero_linha, 'STRING', tokens)
                estado = LEX.INICIO  # Retorna ao estado INÍCIO
        elif estado == LEX.IDENTIFICADOR:
            if char in alfabeto or char in digitos or char == '_':
                lexema += char  # Continua formando o identificador
            else:
                # Finaliza o identificador e verifica se é uma palavra reservada
                if lexema in reservadas:
                    salva_lexema(lexema, numero_linha, 'RESERVADO', tokens)
                else:
                    salva_lexema(lexema, numero_linha, 'IDENTIFICADOR', tokens)
                lexema = ''  # Reseta o lexema
                estado = LEX.INICIO  # Retorna ao estado INÍCIO
                continue  # Reavalia o mesmo caractere no novo estado
        elif estado == LEX.NUMERO:
            if char in digitos:
                lexema += char  # Continua formando o número
            else:
                salva_lexema(lexema, numero_linha, 'NUMERO', tokens)
                lexema = ''  # Reseta o lexema
                estado = LEX.INICIO  # Retorna ao estado INÍCIO
                continue  # Reavalia o mesmo caractere no novo estado
        i += 1  # Avança para o próximo caractere
    # Verifica se um lexema foi capturado mas não salvo devido ao final da linha
    if lexema:
        # Salva o lexema de acordo com o estado atual
        if estado == LEX.IDENTIFICADOR:
            if lexema in reservadas:
                salva_lexema(lexema, numero_linha, 'RESERVADO', tokens)
            else:
                salva_lexema(lexema, numero_linha, 'IDENTIFICADOR', tokens)
        elif estado == LEX.NUMERO:
            salva_lexema(lexema, numero_linha, 'NUMERO', tokens)


print(tokens)