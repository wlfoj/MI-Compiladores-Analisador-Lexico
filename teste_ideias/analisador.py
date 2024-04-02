from enum import Enum

class LEX(Enum):
    INICIO = 0
    STRING = 1
    COMENTARIO = 2
    IDENTIFICADOR = 3
    DELIMITADOR = 4
    NUMERO = 5
    RESERVADO = 6
    OPERADOR1CHAR = 7
    OPERADOR2CHAR = 8


estado = LEX.INICIO

char = ""
delimitadores = []
operadores = []
reservado = []


linha = ""
pos_ini = 0 # posição inicial do token na linha
pos_fim = 0 # posição final do token na linha
i = 0 # iterador da linha para fazer o fatiamento da string

match estado:

    case LEX.INICIO:
        if char == b'"':
            pos_ini = i
            estado = LEX.STRING


    case LEX.STRING:
        if char != b'"': # Se o caracter lido não for o fim da string, não faça nada
            pass
        else: # Se for o fim
            pos_fim = i
            print() # Printa a string
            estado = LEX.INICIO # Volta para posição inicial
        
    case LEX.IDENTIFICADOR:
        if (char not in delimitadores) or (char not in operadores): # Se ainda estiver lendo algo permitido para um identificador, não faça nada
            pass
        else:
            # faço um teste antes se não é uma palavra reservada
            if linha[pos_ini:pos_fim] in reservado: # Se a palavra formada for uma palavra reservada, vai pro estado determinado
                estado = LEX.RESERVADO # Talvez eu não precise ir para esse estado, posso resolver aqui mesmo
            # Se não for
            else:
                print() # Printa o identificador
                estado = LEX.INICIO # Volta para posição inicial




'''
A iideia é fazer append em uma lista de tokens sempre que encontrar um.
Cada elemento da lista terá o nome, o tipo de token, e a linha onde ocorreu
EX:[{aux, IDENTIFICADOR, 4}, {algoritmo, RESERVADO, 1}, ...]

'''