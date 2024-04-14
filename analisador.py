from enum import Enum

# Alfabeto 
alfabeto = [chr(ord('a') + i) for i in range(26)] # Minusculas
alfabeto = alfabeto + [chr(ord('A') + i) for i in range(26)] # Maiusculas
# Digitos
digitos = [str(i) for i in range(10)]
# Palavras reservadas
reservadas = ['algoritmo', 'principal', 'variaveis', 'constantes', 'registro', 'funcao',
                'retorno', 'vazio', 'se', 'senao', 'enquanto', 'leia', 'escreva', 'inteiro', 'real', 'booleano',
                'char', 'cadeia', 'verdadeiro', 'falso']

delimitadores = [ ';', ',', '.', '(', ')', '[', ']', '{', '}' ]

# Função para validar a cadeia ou identificador. Ver se o caracter é um simbolo valido
def e_cadeia_valida(caracter):
    valor_inteiro = ord(caracter) # Obtem o valor inteiro de base 10 referente ao caracter ASCII
    return (valor_inteiro >= 32 and valor_inteiro <=126) and (valor_inteiro != 34)

# Função que retorna 1 se o caracter for valido para um identificado
def e_ide_valido(char):
    return (char in alfabeto) or (char in digitos) or (char == '_')

# Retorna 1 se char for delimitador
def e_delimitador(char):
    return char in " +-*/><=!&|" or char in delimitadores

def salva_lexema(lexema, linha, tipo, lista):
    lista.append({'linha': linha, 'tipo': tipo, 'valor': lexema})

# Tipos de tokens
class TOKENS_TYPE (Enum):
    TOKEN_MAL_FORMADO = "TMF"
    CADEIA_MAL_FORMADA = "CMF"
    COMENTARIO_MAL_FORMADO = "CoMF"
    IDENTIFICADOR_MAL_FORMADO = "IMF"
    NUMERO_MAL_FORMADO = "NMF"

    CADEIA_DE_CARACTERES = "CAC"
    IDENTIFICADOR = "IDE"
    PALAVRA_RESERVADA = "PRE"
    NUMERO = "NRO"
    DELIMITADOR = "DEL"
    OPERADOR_RELACIONAL = "REL"
    OPERADOR_ARITMETICO = "ART"
    OPERADOR_LOGICO = "LOG"


# Estados
class STATE(Enum):
    INICIO = 0
    STRING = 1 # OK
    COMENTARIO_LINHA = 2
    COMENTARIO_BLOCO = 20
    IDENTIFICADOR = 3 # OK +-
    DELIMITADOR = 4 
    NUMERO = 5 
    RESERVADO = 6 # OK
    OPERADOR_ARITMETICO = 7
    OPERADOR_LOGICO = 8
    OPERADOR_RELACIONAL = 9



with open("files/teste.txt", "r") as a:
    linhas = a.readlines()
#print("Tamanho da linha", len(linha))


estado = STATE.INICIO
lexema = ''
tokens = []
erro = False

linha_num = 0 # Número da linha analisada

for linha in linhas:
    linha = linha.replace('\n', '')

    linha_num = linha_num + 1
    i = 0 # iterador da linha para fazer o fatiamento da string
    final_pos_linha = len(linha)-1

    # Não atualizo as infos, pois posso estar vindo de um comentário de bloco mal formado
    if estado != STATE.COMENTARIO_BLOCO:
        lexema = '' # não resetar se for um comentário
        erro = False

    while i <= final_pos_linha:  
        char = linha[i]


        match estado:
            # ---------- Estado inicial da aplicação ---------- #
            case STATE.INICIO:
                lexema = '' # Reseta o lexema
                erro = False
                ## == Ignora espaços == ## OOOOKKKK
                if char == " ":
                    pass
                ## == Transição para cadeia == ## OOOOKKKKK
                elif char == '"':
                    lexema = lexema + char # Adiciono o caracter de inicio 
                    estado = STATE.STRING # e vou pro prox estado
                ## == Transição para delimitadores == ## OOOOKKKKK
                elif char in delimitadores:
                    lexema = lexema + char
                    estado = STATE.DELIMITADOR
                    continue
                ## == Transição para operadores aritméticos == ## OOOOKKKKK
                elif char in '+-*/':
                    lexema = lexema + char
                    estado = STATE.OPERADOR_ARITMETICO
                ## == Transição para operadores lógicos == ## OOOOKKKKK
                elif char in '!&|':
                    lexema = lexema + char
                    estado = STATE.OPERADOR_LOGICO
                ## == Transição para operadores RELACIONAIS == ## OOOOKKKKK
                elif char in '><=':
                    lexema = lexema + char
                    estado = STATE.OPERADOR_RELACIONAL
                ## == Transição para identificadores == ## OOOOKKKKK
                elif char in alfabeto:
                    lexema = lexema + char
                    estado = STATE.IDENTIFICADOR        
                ## == PARA TOKENS MAL FORMADOS == ## OOOOKKKKK
                else:
                    erro = True 
                    lexema = lexema + char
                    tokens.append(lexema) 
                i=i+1# Passo a linha



            # ---------- Estado para analise de STRINGS ---------- # OOOOKKKKK
            case STATE.STRING:
                # Se o caracter lido não for o fim da string, continue concatenando
                if char != '"': 
                    lexema = lexema + char
                    # Se tiver algum caracter fora dos permitidos, sinalizo o erro
                    if not e_cadeia_valida(char):
                        erro = True
                else: # Se for o fim
                    lexema = lexema + char
                    tokens.append(lexema)
                    estado = STATE.INICIO # Volta para posição inicial
                i=i+1# Passo a linha

            # ---------- Estado para analise de operador ARITMETICO ---------- #  
            case STATE.OPERADOR_ARITMETICO:
                # Se for um operador Relacional, transfere a responsabilidade
                if lexema == "/" and char == "/":
                    estado = STATE.COMENTARIO_LINHA
                    continue
                elif lexema == "/" and char == "*":
                    estado = STATE.COMENTARIO_BLOCO
                    continue
                # Se for um lógico duplo
                elif (lexema=="|" and char=="|") or (lexema=="&" and char=="&"):
                    lexema = lexema + char
                    tokens.append(lexema)
                    estado = STATE.INICIO # Volta para posição inicial
                    i=i+1
                # Se for o ! ou um lógico mal formado
                else:
                    # Se for mal formado
                    if lexema == "&" or lexema == "|":
                        erro = True
                    tokens.append(lexema)
                    estado = STATE.INICIO # Volta para posição inicial
        
            case STATE.COMENTARIO_LINHA:
                i=i+1

            # ---------- Estado para analise de operador logico ---------- #  OOOKKKKK
            case STATE.OPERADOR_LOGICO:
                # Se for um operador Relacional, transfere a responsabilidade
                if lexema == "!" and char == "=":
                    estado = STATE.OPERADOR_RELACIONAL
                    continue
                # Se for um lógico duplo
                elif (lexema=="|" and char=="|") or (lexema=="&" and char=="&"):
                    lexema = lexema + char
                    tokens.append(lexema)
                    estado = STATE.INICIO # Volta para posição inicial
                    i=i+1
                # Se for o ! ou um lógico mal formado
                else:
                    # Se for mal formado
                    if lexema == "&" or lexema == "|":
                        erro = True
                    tokens.append(lexema)
                    estado = STATE.INICIO # Volta para posição inicial


            # ---------- Estado para analise de operador relacional ---------- #  OOOKKKKK
            case STATE.OPERADOR_RELACIONAL:
                # Se for um operador Relacional, transfere a responsabilidade
                if lexema == "!" and char == "=":
                    lexema = lexema + char
                    tokens.append(lexema)
                    estado = STATE.INICIO
                # Se for um lógico duplo
                elif (lexema=="=" and char=="=") or (lexema=="<" and char=="=") or (lexema==">" and char=="="):
                    lexema = lexema + char
                    tokens.append(lexema)
                    estado = STATE.INICIO # Volta para posição inicial
                # Se for o ! ou um lógico mal formado
                else:
                    tokens.append(lexema)
                    estado = STATE.INICIO # Volta para posição inicial
                    continue
                i=i+1

            # ---------- Estado para analise de IDENTIFICADORES ---------- #  OOOOKKKKK
            case STATE.IDENTIFICADOR:
                # Se for letra, num ou underline e não for o final da linha
                if (not e_delimitador(char)):
                    # Se tiver algum caracter fora dos permitidos, sinalizo o erro
                    if not e_ide_valido(char):
                        erro = True
                    lexema = lexema + char
                else: # Se não for mais letra, num ou underline ou ainda se for o final da linha
                    tokens.append(lexema)
                    estado = STATE.INICIO # Vai para o inicio
                    continue
                i=i+1# Passo a linha

            # ---------- Estado para analise de DELIMITADORES ---------- # OOOOKKKKK
            case STATE.DELIMITADOR:
                # só serve para salvar na estrutura de palavra reservada
                tokens.append(lexema)
                estado = STATE.INICIO
                i=i+1# Passo a linha

    # Se o lexema que estiver aqui for de algum estado incompleto
    ## PENSAR QUANDO TIVER O COMENTÁRIO
    if lexema and estado != STATE.INICIO:
        if estado == STATE.COMENTARIO_LINHA:
            estado = STATE.INICIO
        else:
            tokens.append(lexema)
            # Lembrar de ver a lógica para o caso de 
            estado = STATE.INICIO

print(tokens)


'''
A iideia é fazer append em uma lista de tokens sempre que encontrar um.
Cada elemento da lista terá o nome, o tipo de token, e a linha onde ocorreu
EX:[{aux, IDENTIFICADOR, 4}, {algoritmo, RESERVADO, 1}, ...]

'''