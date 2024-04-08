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


def salva_lexema(lexema, linha, tipo, lista):
    lista.append({'linha': linha, 'tipo': tipo, 'valor': lexema})


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

    while i <= len(linha)-1:    
        # ---------- Estado inicial da aplicação ---------- #
        if estado == LEX.INICIO: 
            lexema = '' # Reseta o lexema
            ## == Transição para cadeia == ## OOOOKKKKK
            if linha[i] == '"':
                lexema = lexema + linha[i] # Adiciono o caracter de inicio 
                estado = LEX.STRING # e vou pro prox estado
                # Para resolver o problema das linhas que só possuem um char
                if(i==len(linha)-1):
                    tokens.append(lexema)
            ## == Transição para delimitadores == ##
            elif linha[i] in delimitadores:
                lexema = lexema + linha[i]
                estado = LEX.DELIMITADOR
                # Para resolver o problema das linhas que só possuem um char
                if(i==len(linha)-1):
                    tokens.append(lexema)
            ## == Transição para operadores aritméticos == ##
            elif linha[i] in '+-*/':
                lexema = lexema + linha[i]
                estado = LEX.OPERADOR_ARITMETICO
                # Para resolver o problema das linhas que só possuem um char
                if(i==len(linha)-1):
                    tokens.append(lexema)
            ## == Transição para identificadores == ## OOOOKKKKK
            elif linha[i] in alfabeto:
                lexema = lexema + linha[i]
                estado = LEX.IDENTIFICADOR        
                # Para resolver o problema das linhas que só possuem um char
                if(i==len(linha)-1):
                    tokens.append(lexema)  
            i=i+1# Passo a linha

        # ---------- Estado para analise de STRINGS ---------- # OOOOKKKKK
        elif estado == LEX.STRING:
            # Se o caracter lido não for o fim da string, continue concatenando
            if linha[i] != '"' and i != len(linha)-1: 
                lexema = lexema + linha[i]
            else: # Se for o fim
                lexema = lexema + linha[i]
                tokens.append(lexema)
                estado = LEX.INICIO # Volta para posição inicial
            i=i+1# Passo a linha

        # ---------- Estado para analise de operador aritmético ---------- #
        elif estado == LEX.OPERADOR_ARITMETICO:
            if linha[i] in '+-*/' and i != len(linha)-1: # and i != len(linha)-1 corresponde ao finnal da linha
                lexema = lexema + linha[i]
                if lexema == "//":
                    # Devo encerrar a analise do lexema ou ir pro estado do comentário de linha
                    pass
                elif lexema == "/*":
                    # Devo ir pro estado de comentário de bloco
                    pass
            elif i == len(linha)-1: # Se for o fim da linha
                lexema = lexema + linha[i]
                tokens.append(lexema)
                estado = LEX.INICIO # Volta para posição inicial
        
        # ---------- Estado para analise de IDENTIFICADORES ---------- #  OOOOKKKKK
        elif estado == LEX.IDENTIFICADOR:
            # Se for letra, num ou underline e não for o final da linha
            if (((linha[i] in alfabeto) or (linha[i] in digitos) or (linha[i]=='_'))):
                lexema = lexema + linha[i]
                if i == len(linha)-1:
                    if lexema in reservadas:
                        tokens.append(lexema + '_res')
                        estado = LEX.INICIO
                    else:
                        tokens.append(lexema)
                        estado = LEX.INICIO # Vai para o inicio
            else: # Se não for mais letra, num ou underline ou ainda se for o final da linha
                ## !! DEVO VERIFICAR SE É PALAVRA RESERVADA ANTES DE SALVAR NA ESTRUTURA ##
                if lexema in reservadas:
                    tokens.append(lexema + '_res')
                    estado = LEX.INICIO
                else:
                    tokens.append(lexema)
                    estado = LEX.INICIO # Vai para o inicio
                continue
            i=i+1# Passo a linha

        # ---------- Estado para analise de DELIMITADORES ---------- # OOOOKKKKK
        elif estado == LEX.DELIMITADOR:
            # só serve para salvar na estrutura de palavra reservada
            tokens.append(lexema + '_del')
            estado = LEX.INICIO


print(tokens)


'''
A iideia é fazer append em uma lista de tokens sempre que encontrar um.
Cada elemento da lista terá o nome, o tipo de token, e a linha onde ocorreu
EX:[{aux, IDENTIFICADOR, 4}, {algoritmo, RESERVADO, 1}, ...]

'''