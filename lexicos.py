import os
from enum import Enum

### ============================ BLOCO DE ESTRUTURAS BÁSICAS DE TOKENS PARA CONTROLE ============================ ###
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


# Tipos de tokens e suas siglas para arquivo de saída
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
    CADEIA_DE_CARACTERES = 1
    COMENTARIO_LINHA = 2
    COMENTARIO_BLOCO = 20
    IDENTIFICADOR = 3
    DELIMITADOR = 4 
    NUMERO = 5 
    PALAVRA_RESERVADA = 6
    OPERADOR_ARITMETICO = 7
    OPERADOR_LOGICO = 8
    OPERADOR_RELACIONAL = 9
    NUMERO_DECIMAL = 10


### ============================ BLOCO DE FUNÇÕES AUXILIARES PARA IDENTIFICAÇÃO E CONTROLE DE TOKENS ============================ ###
def e_cadeia_valida(caracter) -> bool:
    ''' Função que verifica se a cadeia de caracterres é válida. verifica se o caracter está dentro dos permitidos da tabela ASCII
    Return.
        True se for permitido, False se não for 
        '-'
    '''
    valor_inteiro = ord(caracter) # Obtem o valor inteiro de base 10 referente ao caracter ASCII
    return (valor_inteiro >= 32 and valor_inteiro <=126) and (valor_inteiro != 34)


def e_ide_valido(char) -> bool:
    ''' Função que verifica se o identificador é válido. observa se o caracter é permitido para Identificadores
    Return.
        True se for permitido, False se não for 
        '-'
    '''
    return (char in alfabeto) or (char in digitos) or (char == '_')


def e_delimitador(char) -> bool:
    ''' Função que verifica se o caracter é um delimitador ou operador ou espaço
    Return.
        True se for, False se não for 
        '-'
    '''
    return (char in [' ', '"','+', '-', '*', '/', '>', '<', '!', '&&', '||', '>=', '<=', '!=', '=', '==']) or (char in delimitadores)


def salva_lexema(lexema, linha, tipo, lista_TBF, lista_TMF):
    ''' Função que adiciona os lexemas na lista de tokens mal formados ou de tokens normais
    Param.
        lexema      -> valor do lexema a ser salvo
        linha       -> linha do arquivo onde o lexema apareceu
        tipo        -> tipo de token ao qual o lexema pertence
        lista_TBF   -> lista de tokens que não apresentam erros
        lista_TMF   -> lista de tokens que apresentam erros

    Return.
        token       -> Dicionário token salvo, seguindo a estrutura definida no corpo da função
    '''
    token = {'linha': linha, 'tipo': tipo, 'valor': lexema}
    if tipo in [TOKENS_TYPE.TOKEN_MAL_FORMADO,
                TOKENS_TYPE.CADEIA_MAL_FORMADA,
                TOKENS_TYPE.COMENTARIO_MAL_FORMADO,
                TOKENS_TYPE.IDENTIFICADOR_MAL_FORMADO,
                TOKENS_TYPE.NUMERO_MAL_FORMADO]:
        lista_TMF.append(token)
    else:
        lista_TBF.append(token)
    return token


### ============================ BLOCO DE FUNÇÕES PARA LEITURA E ESCRITA DE ARQUIVOS ============================ ###
def escreve_saida(nome_arquivo_entrada, lista_TBF, lista_TMF, erro_no_processo):
    ''' Função para escrever os tokens no arquivo de saída no formato esperado, bem como a mensagem de sucesso ou erro do processo
    Param.
        nome_arquivo_entrada -> Caminho completo relativo até o arquivo, incluindo seu nome.
                                EX. nome_arquivo_entrada = "files/entrada.txt"
        erro_no_processo     -> Para informar se houve erro no processo do analisador lexico (True) ou não (False)
        lista_TBF            -> lista de tokens que não apresentam erros
        lista_TMF            -> lista de tokens que apresentam erros

    '''
    nome_arquivo_saida = nome_arquivo_entrada.replace(".txt", "-saida.txt")
    # Abre o arquivo de saída
    with open(nome_arquivo_saida, 'w', encoding='utf-8') as f:
        # Percorre a lista de tokens bem formados e adiciona no arquivo
        for token in lista_TBF:
            f.write(f"{token['linha']} {token['tipo'].value} {token['valor']}\n")
        f.write("\n") # só para separar melhor os tokens mal formados
        # Percorre a lista de tokens mal formados e escreve no arquivo
        for token in lista_TMF:
            f.write(f"{token['linha']} {token['tipo'].value} {token['valor']}\n")
        f.write("\n") # só para separar melhor os comentários de erro e sucesso
        # Escreve a mensagem de sucesso ou de erro
        if (not erro_no_processo):
            f.write("Analise lexica concluida com sucesso!!")
        #else:
        #    f.write("Analise lexica concluida com sucesso!!")

def obtem_todas_linhas(nome_arquivo_entrada) -> list:
    ''' Função para obter todas as linhas do arquivo de entrada.
    Param.
        nome_arquivo_entrada -> Caminho completo relativo até o arquivo, incluindo seu nome.
                                EX. nome_arquivo_entrada = "files/entrada.txt"
    Return.
        linhas               -> Todas as linhas presentes no arquivo de entrada
    '''
    with open(nome_arquivo_entrada, "r", encoding='utf-8') as a:
        linhas = a.readlines()
    return linhas


def obter_nomes_arquivos_entrada() -> list:
    ''' Função que obtem uma lista com o nome de todos os arquivos que são validos como arquivos de entrada para o analisador lexico
    Return.
        lista_arquivos_entrada -> Caminho completo relativo até o arquivo, incluindo seu nome.
                                EX. nome_arquivo_entrada = "files/entrada.txt"
    '''
    lista_arquivos_entrada = []
    # Define o caminho da pasta onde os arquivos serão lidos
    PASTA = 'files/'
    for arquivo in os.listdir(PASTA):
        # Evita processar arquivos que já contêm "-saida" no nome e os que não o ".txt" no final
        if arquivo.endswith('.txt') and (not arquivo.endswith('-saida.txt')):
            lista_arquivos_entrada.append(PASTA + arquivo)
    return lista_arquivos_entrada
    

### ============================ BLOCO DA FUNÇÃO QUE FAZ A ANALISE LEXICA () ============================ ###
def analisador_lexico(linhas):
    ''' Função que realiza a analise lexica para cada arquivo de entrada. O mesmo deve receber todas, e apenas, as linhas de um único arquivo por vez.
    Param.
        linhas              -> Todas as linhas de um determinando arquivo de entrada.
    
    Return.
        tokens_bem_formados -> Lista dos tokens normais (seguindo a estrutura de token apresentada em salva_lexema)
        tokens_mal_formados -> Lista dos tokens mal formados (seguindo a estrutura de token apresentada em salva_lexema)
    '''
    ### ===== Minibloco de inicialização de variaveis importantes para a analise lexica de cada arquivo ===== ###
    estado = STATE.INICIO
    ultimo_token = {'linha':  None, 'tipo': None, 'valor': None}
    token_atual = None
    lexema = ''
    tokens_bem_formados = []
    tokens_mal_formados = []
    linha_num = 0 # Número da linha analisada
    flag_erro_num = False

    ### ===== Inicio do processo de analise lexica ===== ###
    for linha in linhas:
        linha = linha.replace('\n', '').replace('\t', '')

        linha_num = linha_num + 1
        i = 0 # iterador da linha para fazer o fatiamento da CADEIA_DE_CARACTERES
        final_pos_linha = len(linha)-1

        # Não atualizo as infos, pois posso estar vindo de um comentário de bloco mal formado
        if estado != STATE.COMENTARIO_BLOCO:
            lexema = '' # não resetar se for um comentário
            ultimo_token = {'linha':  None, 'tipo': None, 'valor': None}

        while i <= final_pos_linha:  
            char = linha[i]

            match estado:
                # ---------- Estado inicial da aplicação ---------- #
                case STATE.INICIO:
                    flag_erro_num = False
                    lexema = '' # Reseta o lexema
                    #token_atual = None
                    ## == Ignora espaços == ##
                    if char == " " or char == "":
                        pass
                    ## == Transição para cadeia == ##
                    elif char == '"':
                        lexema = lexema + char # Adiciono o caracter de inicio 
                        token_atual = TOKENS_TYPE.CADEIA_DE_CARACTERES
                        estado = STATE.CADEIA_DE_CARACTERES # e vou pro prox estado
                    ## == Transição para delimitadores == ## 
                    elif char in delimitadores:
                        lexema = lexema + char
                        token_atual = TOKENS_TYPE.DELIMITADOR
                        estado = STATE.DELIMITADOR
                        continue
                    ## == Transição para operadores aritméticos == ## 
                    elif char in '+-*/':
                        lexema = lexema + char
                        token_atual = TOKENS_TYPE.OPERADOR_ARITMETICO
                        estado = STATE.OPERADOR_ARITMETICO
                    ## == Transição para operadores lógicos == ## 
                    elif char in '!&|':
                        lexema = lexema + char
                        token_atual = TOKENS_TYPE.OPERADOR_LOGICO
                        estado = STATE.OPERADOR_LOGICO
                    ## == Transição para operadores RELACIONAIS == ## 
                    elif char in '><=':
                        lexema = lexema + char
                        token_atual = TOKENS_TYPE.OPERADOR_RELACIONAL
                        estado = STATE.OPERADOR_RELACIONAL
                    ## == Transição para identificadores == ## 
                    elif char in alfabeto:
                        lexema = lexema + char
                        token_atual = TOKENS_TYPE.IDENTIFICADOR
                        estado = STATE.IDENTIFICADOR
                    ## == Transição para números == ## VER OS NEGATIVOS      
                    elif char.isdigit():
                        lexema = lexema + char
                        token_atual = TOKENS_TYPE.NUMERO
                        estado = STATE.NUMERO      
                    ## == PARA TOKENS MAL FORMADOS == ## 
                    else:
                        lexema = lexema + char
                        token_atual = TOKENS_TYPE.TOKEN_MAL_FORMADO
                        ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
                    i=i+1# Passo a linha



                # ---------- Estado para analise de CADEIA_DE_CARACTERESS ---------- # 
                case STATE.CADEIA_DE_CARACTERES:
                    # Se o caracter lido não for o fim da string, continue concatenando
                    if char != '"': 
                        lexema = lexema + char
                        # Se tiver algum caracter fora dos permitidos, sinalizo o erro
                        if not e_cadeia_valida(char):
                            token_atual = TOKENS_TYPE.CADEIA_MAL_FORMADA
                    else: # Se for o fim
                        lexema = lexema + char
                        ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
                        estado = STATE.INICIO # Volta para posição inicial
                    i=i+1# Passo a linha
            
                # Este é o estado para comentários em bloco.
                case STATE.COMENTARIO_LINHA:
                    i=i+1
                case STATE.COMENTARIO_BLOCO:
                    lexema = lexema + char 
                    # Se os dois últimos caracteres do lexema formarem '*/', indica o fim do comentário em bloco.
                    if (lexema[-2:] == "*/"):
                        estado = STATE.INICIO # Ignora tudo oq fez até aqui
                    i=i+1


                # ---------- Estado para analise de operador logico ---------- # 
                case STATE.OPERADOR_LOGICO:
                    # Se for um operador Relacional, transfere a responsabilidade
                    if lexema == "!" and char == "=":
                        estado = STATE.OPERADOR_RELACIONAL
                        continue
                    # Se for um lógico duplo
                    elif (lexema=="|" and char=="|") or (lexema=="&" and char=="&"):
                        lexema = lexema + char
                        ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
                        estado = STATE.INICIO # Volta para posição inicial
                        i=i+1
                    # Se for o ! ou um lógico mal formado
                    else:
                        # Se for mal formado
                        if lexema == "&" or lexema == "|":
                            token_atual = TOKENS_TYPE.TOKEN_MAL_FORMADO

                        ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
                        estado = STATE.INICIO # Volta para posição inicial

                # ---------- Estado para analise de operador ARITMETICO ---------- #  
                case STATE.OPERADOR_ARITMETICO:
                    # Se for um operador Relacional, transfere a responsabilidade
                    if lexema == "/" and char == "/":
                        estado = STATE.COMENTARIO_LINHA
                        continue
                    elif lexema == "/" and char == "*":
                        lexema = lexema + char # Estou salvando pq posso precisar usar para comentario mal formado
                        estado = STATE.COMENTARIO_BLOCO
                        # token_atual = TOKENS_TYPE.
                        continue
                    # Se for um aritmético duplo
                    elif (lexema=="+" and char=="+") or (lexema=="-" and char=="-"):
                        lexema = lexema + char
                        ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
                        estado = STATE.INICIO # Volta para posição inicial
                    ## Se for o caso de um número negativo
                    elif (lexema=='-' and char.isdigit()) and (ultimo_token['tipo'] in [TOKENS_TYPE.OPERADOR_ARITMETICO, 
                                                                                TOKENS_TYPE.OPERADOR_LOGICO, 
                                                                                TOKENS_TYPE.OPERADOR_RELACIONAL, 
                                                                                TOKENS_TYPE.DELIMITADOR,
                                                                                TOKENS_TYPE.CADEIA_DE_CARACTERES,
                                                                                TOKENS_TYPE.NUMERO_MAL_FORMADO,
                                                                                TOKENS_TYPE.IDENTIFICADOR_MAL_FORMADO,
                                                                                TOKENS_TYPE.CADEIA_MAL_FORMADA,
                                                                                TOKENS_TYPE.TOKEN_MAL_FORMADO,
                                                                                None]):
                        estado = STATE.NUMERO
                        token_atual = TOKENS_TYPE.NUMERO
                        lexema = lexema + char
                    # Se for o um único dos +-/* e depois não vier um número
                    else:
                        ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
                        estado = STATE.INICIO # Volta para posição inicial
                        continue
                    i = i+1


                # ---------- Estado para análise de números inteiros ----------
                case STATE.NUMERO:
                    ## Caso especial em que preciso olhar o proximo caracter
                    # Aqui tratamos de casos especiais onde precisamos olhar o próximo caractere.
                    if char in '&|' and i < final_pos_linha:
                        # Se o caractere atual é '&' ou '|', e ainda não chegamos ao final da linha:
                        # Finalizo se for '&&'
                        if char == '&' and linha[i+1] == '&':
                            # Se for '&&', finalizamos o lexema atual e voltamos para o estado inicial.
                            ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
                            estado = STATE.INICIO # Volta para posição inicial
                            continue
                        # Finalizo se for '||'
                        elif char == '|' and linha[i+1] == '|':
                            # Se for '||', finalizamos o lexema atual e voltamos para o estado inicial.
                            ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
                            estado = STATE.INICIO # Volta para posição inicial
                            continue
                    elif char.isdigit():  # Continua lendo dígitos
                        # Se o caractere atual é um dígito, continuamos lendo e adicionando ao lexema.
                        lexema += char
                    elif char == '.' and (not flag_erro_num):
                        # Se encontrarmos um ponto e ainda não estamos em erro numérico, consideramos um número decimal.
                        lexema += char
                        estado = STATE.NUMERO_DECIMAL
                    elif e_delimitador(char):  # Finaliza o token de número e volta ao estado inicial
                        # Se encontrarmos um delimitador, finalizamos o token de número e voltamos ao estado inicial.
                        ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
                        estado = STATE.INICIO
                        continue  # Não avança o índice, pois o caractere atual pode ser o início de um novo token
                    else:
                        # Se nenhuma das condições acima for satisfeita, há um erro numérico.
                        flag_erro_num = True
                        lexema += char
                        token_atual = TOKENS_TYPE.NUMERO_MAL_FORMADO
                    i += 1  # Avança para o próximo caractere

                # ---------- Estado para análise de números decimais ----------
                case STATE.NUMERO_DECIMAL:
                    # Verifica se o caractere atual é '&' ou '|' e se há um próximo caractere na linha
                    if char in '&|' and i < final_pos_linha:
                        # Se for '&&', finaliza o lexema
                        if char == '&' and linha[i+1] == '&': #Verifica se há &&
                            ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
                            estado = STATE.INICIO # Volta para posição inicial
                            continue
                        # Se for '||', finaliza o lexema
                        elif char == '|' and linha[i+1] == '|': #Verifica se há ||
                            ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
                            estado = STATE.INICIO # Volta para posição inicial
                            continue
                        else:
                            token_atual = TOKENS_TYPE.IDENTIFICADOR_MAL_FORMADO
                            lexema = lexema + char
                    # Se o caractere atual é um dígito, continua concatenando no lexema
                    elif char.isdigit():
                        lexema = lexema + char
                    # Se o caractere atual for um espaço em branco:
                    elif char == ' ':
                        if lexema[-1] == '.':# Se o último caractere do lexema for um ponto decimal:
                            token_atual = TOKENS_TYPE.NUMERO_MAL_FORMADO
                        ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
                        estado = STATE.INICIO
                        continue
                     # Se o último caractere do lexema não é '.' e não estou em erro e encontro um delimitador diferente de '.', finalizo o lexema
                    elif  lexema[-1] != '.' and (not flag_erro_num) and (e_delimitador(char)) and (char !='.'):
                        if lexema[-1] == '.':
                            token_atual = TOKENS_TYPE.NUMERO_MAL_FORMADO
                        ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
                        estado = STATE.INICIO
                        continue
                    # Venho do erro e encontro um delimitador, finaliza o lexema com erro
                    elif flag_erro_num and (e_delimitador(char)):
                        token_atual = TOKENS_TYPE.NUMERO_MAL_FORMADO
                        ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
                        estado = STATE.INICIO
                        continue
                    else:
                        flag_erro_num = True
                        token_atual = TOKENS_TYPE.NUMERO_MAL_FORMADO
                        lexema = lexema + char
                    i=i+1

                # ---------- Estado para analise de operador relacional ---------- # 
                case STATE.OPERADOR_RELACIONAL:
                    # Se for um operador Relacional duplo
                    if (lexema == "!" and char == "=") or (lexema=="=" and char=="=") or (lexema=="<" and char=="=") or (lexema==">" and char=="="):
                        lexema = lexema + char
                        ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
                        estado = STATE.INICIO # Volta para posição inicial
                    # Se for um relacional simples <>=
                    else:
                        ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
                        estado = STATE.INICIO # Volta para posição inicial
                        continue
                    i=i+1

                # ---------- Estado para analise de IDENTIFICADORES ---------- #
                case STATE.IDENTIFICADOR:
                    ## Caso especial em que preciso olhar o próximo caracter
                    # Tratamos de casos especiais onde precisamos olhar o próximo caractere.
                    if char in '&|' and i < final_pos_linha:
                        # Se o caractere atual é '&' ou '|', e ainda não chegamos ao final da linha:
                        # Finalizo se for '&&'
                        if char == '&' and linha[i+1] == '&':
                            # Se for '&&', finalizamos o lexema atual e voltamos para o estado inicial.
                            ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
                            estado = STATE.INICIO # Volta para posição inicial
                            continue
                        # Finalizo se for '||'
                        elif char == '|' and linha[i+1] == '|':
                            ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
                            estado = STATE.INICIO # Volta para posição inicial
                            continue
                        else:
                            # Se não for '&&' ou '||', marcamos o token atual como um identificador mal formado e adicionamos o caractere ao lexema.
                            token_atual = TOKENS_TYPE.IDENTIFICADOR_MAL_FORMADO
                            lexema = lexema + char
                    # Se for letra, número ou underline e não for o final da linha
                    elif (not e_delimitador(char)):
                        # Se o caractere atual não for um delimitador e não for permitido em identificadores, marcamos como identificador mal formado.
                        if not e_ide_valido(char):
                            token_atual = TOKENS_TYPE.IDENTIFICADOR_MAL_FORMADO
                        lexema = lexema + char
                    else: # Se for um delimitador
                       # Se o lexema for uma palavra reservada, mudamos o estado para PALAVRA_RESERVADA.
                        if lexema in reservadas:
                            estado = STATE.PALAVRA_RESERVADA
                            token_atual = TOKENS_TYPE.PALAVRA_RESERVADA
                        else:
                             # Caso contrário, finalizamos o lexema atual e voltamos para o estado inicial.
                            ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
                            estado = STATE.INICIO # Vai para o inicio
                        continue
                    i=i+1# Passo a linha


                case STATE.PALAVRA_RESERVADA:
                    ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
                    estado = STATE.INICIO # Vai para o inicio      


                # ---------- Estado para analise de DELIMITADORES ---------- #
                case STATE.DELIMITADOR:
                    # só serve para salvar na estrutura de palavra reservada
                    ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
                    estado = STATE.INICIO
                    i=i+1# Passo a linha
        

        # Se o lexema não tiver sido salvo ainda
        if lexema and estado != STATE.INICIO:
            ##
            if estado == STATE.COMENTARIO_LINHA:
                estado = STATE.INICIO
            ## Adiciono uma quebra de linha, se não for a última linha do arquivo, para que fique igual ao arquivo de entrada
            elif estado == STATE.COMENTARIO_BLOCO :
                if(linha_num != len(linhas)):
                    lexema = lexema + "\n"
            ## Se tenho algum lexema para pôr e é do tipo cac, significa que n fechei ela
            elif estado == STATE.CADEIA_DE_CARACTERES:
                token_atual = TOKENS_TYPE.CADEIA_MAL_FORMADA
                ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
                estado = STATE.INICIO
            ## condição para o numero decimal
            elif estado == STATE.NUMERO_DECIMAL:
                if lexema[-1] == '.':
                    token_atual = TOKENS_TYPE.NUMERO_MAL_FORMADO
                ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
                estado = STATE.INICIO
            ##condição para os identificadores
            elif estado == STATE.IDENTIFICADOR:
                if lexema in reservadas:
                    token_atual = TOKENS_TYPE.PALAVRA_RESERVADA
                ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
                estado = STATE.INICIO
            else:
                ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
                # Lembrar de ver a lógica para o caso de 
                estado = STATE.INICIO

    # para tratar o comentário de bloco mal formado
    if lexema and estado==STATE.COMENTARIO_BLOCO:
        token_atual = TOKENS_TYPE.COMENTARIO_MAL_FORMADO
        linha_num = linha_num - lexema.count('\n')
        ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
    
    return tokens_bem_formados, tokens_mal_formados






### ====================== EXECUÇÃO DO CÓDIGO ====================== ###
if __name__ == '__main__':
    erro = False
    # Obtem a lista de arquivos que podem ser lidos
    arquivos_entrada = obter_nomes_arquivos_entrada()
    # Começa um for em cada um deles
    for arquivo in arquivos_entrada:
        # Obtem as linhas
        linhas = obtem_todas_linhas(arquivo)
        # Passa pela analise lexica
        TBF, TMF = analisador_lexico(linhas)
        # Se a lista de tokens mal formados tiver algum elemento, aviso para a função não escrever a mensagem de sucesso no arquivo de saida
        if len(TMF)>0:
            erro = True
        # Escreve a saída após passar pelo analisador
        escreve_saida(arquivo, TBF, TMF, erro)