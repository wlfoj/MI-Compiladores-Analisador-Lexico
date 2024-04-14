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

# Função apra validar a cadeia
def e_cadeia_valida(caracter):
    valor_inteiro = ord(caracter)
    return (valor_inteiro >= 32 and valor_inteiro <=126) and (valor_inteiro != 34)

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
class LEX(Enum):
    INICIO = 0
    STRING = 1 # OK
    COMENTARIO = 2
    IDENTIFICADOR = 3 # OK +-
    DELIMITADOR = 4 
    NUMERO = 5 
    RESERVADO = 6 # OK
    OPERADOR_ARITMETICO = 7
    OPERADOR_LOGICO = 8
    OPERADOR_RELACIONAL = 9


estado = LEX.INICIO


with open("files/teste.txt", "r") as a:
    linhas = a.readlines()
#print("Tamanho da linha", len(linha))



lexema = ''
tokens = []

linha_num = 0 # Número da linha analisada

for linha in linhas:
    linha = linha.replace('\n', '')

    linha_num = linha_num + 1
    i = 0 # iterador da linha para fazer o fatiamento da string
    final_pos_linha = len(linha)-1

    if estado != LEX.COMENTARIO:
        lexema = '' # não resetar se for um comentário

    while i <= final_pos_linha:  
        char = linha[i]


        match estado:
            # ---------- Estado inicial da aplicação ---------- #
            case LEX.INICIO:
                lexema = '' # Reseta o lexema
                ## == Ignora espaços == ## OOOOKKKK
                if char == " ":
                    pass
                ## == Transição para cadeia == ## OOOOKKKKK
                elif char == '"':
                    lexema = lexema + char # Adiciono o caracter de inicio 
                    estado = LEX.STRING # e vou pro prox estado
                ## == Transição para delimitadores == ## OOOOKKKKK
                elif char in delimitadores:
                    lexema = lexema + char
                    estado = LEX.DELIMITADOR
                    continue
                ## == Transição para operadores aritméticos == ##
                elif char in '+-*/':
                    lexema = lexema + char
                    estado = LEX.OPERADOR_ARITMETICO
                ## == Transição para operadores lógicos == ## OOOOKKKKK
                elif char in '!&|':
                    lexema = lexema + char
                    estado = LEX.OPERADOR_LOGICO
                ## == Transição para operadores RELACIONAIS == ## OOOOKKKKK
                elif char in '><=':
                    lexema = lexema + char
                    estado = LEX.OPERADOR_RELACIONAL
                ## == Transição para identificadores == ## OOOOKKKKK
                elif char in alfabeto:
                    lexema = lexema + char
                    estado = LEX.IDENTIFICADOR        
                ## == PARA TOKENS MAL FORMADOS == ##
                else:
                    lexema = lexema + char
                    tokens.append(lexema) 
                i=i+1# Passo a linha



            # ---------- Estado para analise de STRINGS ---------- # OOOOKKKKK
            case LEX.STRING:
                # Se o caracter lido não for o fim da string, continue concatenando
                if char != '"': 
                    lexema = lexema + char
                else: # Se for o fim
                    lexema = lexema + char
                    tokens.append(lexema)
                    estado = LEX.INICIO # Volta para posição inicial
                i=i+1# Passo a linha

            # ---------- Estado para analise de operador aritmético ---------- #
            case LEX.OPERADOR_ARITMETICO:
                if char in '+-*/' and i != final_pos_linha: # and i != final_pos_linha corresponde ao finnal da linha
                    lexema = lexema + char
                    if lexema == "//":
                        # Devo encerrar a analise do lexema ou ir pro estado do comentário de linha
                        pass
                    elif lexema == "/*":
                        # Devo ir pro estado de comentário de bloco
                        pass
                elif i == final_pos_linha: # Se for o fim da linha
                    lexema = lexema + char
                    tokens.append(lexema)
                    estado = LEX.INICIO # Volta para posição inicial
        
            # ---------- Estado para analise de operador logico ---------- #  OOOKKKKK
            case LEX.OPERADOR_LOGICO:
                # Se for um operador Relacional, transfere a responsabilidade
                if lexema == "!" and char == "=":
                    estado = LEX.OPERADOR_RELACIONAL
                    continue
                # Se for um lógico duplo
                elif (lexema=="|" and char=="|") or (lexema=="&" and char=="&"):
                    lexema = lexema + char
                    tokens.append(lexema)
                    estado = LEX.INICIO # Volta para posição inicial
                    i=i+1
                # Se for o ! ou um lógico mal formado
                else:
                    tokens.append(lexema)
                    estado = LEX.INICIO # Volta para posição inicial


            # ---------- Estado para analise de operador relacional ---------- #  OOOKKKKK
            case LEX.OPERADOR_RELACIONAL:
                # Se for um operador Relacional, transfere a responsabilidade
                if lexema == "!" and char == "=":
                    lexema = lexema + char
                    tokens.append(lexema)
                    estado = LEX.INICIO
                # Se for um lógico duplo
                elif (lexema=="=" and char=="=") or (lexema=="<" and char=="=") or (lexema==">" and char=="="):
                    lexema = lexema + char
                    tokens.append(lexema)
                    estado = LEX.INICIO # Volta para posição inicial
                # Se for o ! ou um lógico mal formado
                else:
                    tokens.append(lexema)
                    estado = LEX.INICIO # Volta para posição inicial
                    continue
                i=i+1

            # ---------- Estado para analise de IDENTIFICADORES ---------- #  OOOOKKKKK
            case LEX.IDENTIFICADOR:
                # Se for letra, num ou underline e não for o final da linha
                if (((char in alfabeto) or (char in digitos) or (char=='_'))):
                    lexema = lexema + char
                else: # Se não for mais letra, num ou underline ou ainda se for o final da linha
                    tokens.append(lexema)
                    estado = LEX.INICIO # Vai para o inicio
                    continue
                i=i+1# Passo a linha

            # ---------- Estado para analise de DELIMITADORES ---------- # OOOOKKKKK
            case LEX.DELIMITADOR:
                # só serve para salvar na estrutura de palavra reservada
                tokens.append(lexema)
                estado = LEX.INICIO
                i=i+1# Passo a linha

    # Se o lexema que estiver aqui for de algum estado incompleto
    if lexema and estado != LEX.INICIO:
        tokens.append(lexema)
        # Lembrar de ver a lógica para o caso de 
        estado = LEX.INICIO

print(tokens)


'''
A iideia é fazer append em uma lista de tokens sempre que encontrar um.
Cada elemento da lista terá o nome, o tipo de token, e a linha onde ocorreu
EX:[{aux, IDENTIFICADOR, 4}, {algoritmo, RESERVADO, 1}, ...]

'''