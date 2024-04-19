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
    CADEIA_DE_CARACTERES = 1 # OK
    COMENTARIO_LINHA = 2
    COMENTARIO_BLOCO = 20
    IDENTIFICADOR = 3 # OK +-
    DELIMITADOR = 4 
    NUMERO = 5 
    PALAVRA_RESERVADA = 6 # OK
    OPERADOR_ARITMETICO = 7
    OPERADOR_LOGICO = 8
    OPERADOR_RELACIONAL = 9


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
    ''' Função que verifica se o caracter é um delimitador ou operador
    Return.
        True se for, False se não for 
        '-'
    '''
    return char in " +-*/><=!&|" or char in delimitadores


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
        if (erro_no_processo):
            f.write("A analise lexica não pôde ser concluído, pois houver erro durante o processo")
        else:
            f.write("Analise lexica concluida com sucesso!!")


def obtem_todas_linhas(nome_arquivo_entrada) -> list:
    ''' Função para obter todas as linhas do arquivo de entrada.
    Param.
        nome_arquivo_entrada -> Caminho completo relativo até o arquivo, incluindo seu nome.
                                EX. nome_arquivo_entrada = "files/entrada.txt"
    Return.
        linhas               -> Todas as linhas presentes no arquivo de entrada
    '''
    with open(nome_arquivo_entrada, "r") as a:
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
        if arquivo.endswith('.txt') and '-saida.txt' not in arquivo:
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

    ### ===== Inicio do processo de analise lexica ===== ###
    for linha in linhas:
        linha = linha.replace('\n', '')

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
                    lexema = '' # Reseta o lexema
                    token_atual = None
                    ## == Ignora espaços == ## OOOOKKKK
                    if char == " " or char == "":
                        pass
                    ## == Transição para cadeia == ## OOOOKKKKK
                    elif char == '"':
                        lexema = lexema + char # Adiciono o caracter de inicio 
                        print("achei", linha_num)
                        print(lexema+"\n\n")
                        token_atual = TOKENS_TYPE.CADEIA_DE_CARACTERES
                        estado = STATE.CADEIA_DE_CARACTERES # e vou pro prox estado
                    ## == Transição para delimitadores == ## OOOOKKKKK
                    elif char in delimitadores:
                        lexema = lexema + char
                        # if char == '}':
                        #     print("achei", linha_num)
                        #     print(lexema+"\n\n")
                        token_atual = TOKENS_TYPE.DELIMITADOR
                        estado = STATE.DELIMITADOR
                        continue
                    ## == Transição para operadores aritméticos == ## OOOOKKKKK
                    elif char in '+-*/':
                        lexema = lexema + char
                        token_atual = TOKENS_TYPE.OPERADOR_ARITMETICO
                        estado = STATE.OPERADOR_ARITMETICO
                    ## == Transição para operadores lógicos == ## OOOOKKKKK
                    elif char in '!&|':
                        lexema = lexema + char
                        token_atual = TOKENS_TYPE.OPERADOR_LOGICO
                        estado = STATE.OPERADOR_LOGICO
                    ## == Transição para operadores RELACIONAIS == ## OOOOKKKKK
                    elif char in '><=':
                        lexema = lexema + char
                        token_atual = TOKENS_TYPE.OPERADOR_RELACIONAL
                        estado = STATE.OPERADOR_RELACIONAL
                    ## == Transição para identificadores == ## OOOOKKKKK
                    elif char in alfabeto:
                        lexema = lexema + char
                        token_atual = TOKENS_TYPE.IDENTIFICADOR
                        estado = STATE.IDENTIFICADOR
                    ## == Transição para números == ## VER OS NEGATIVOS      
                    elif char.isdigit():
                        lexema = lexema + char
                        token_atual = TOKENS_TYPE.NUMERO
                        estado = STATE.NUMERO      
                    ## == PARA TOKENS MAL FORMADOS == ## OOOOKKKKK
                    else:
                        lexema = lexema + char
                        token_atual = TOKENS_TYPE.TOKEN_MAL_FORMADO
                        ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
                    i=i+1# Passo a linha



                # ---------- Estado para analise de CADEIA_DE_CARACTERESS ---------- # OOOOKKKKK
                case STATE.CADEIA_DE_CARACTERES:
                    print("Entrei", linha_num, "lexema: ", lexema)
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

                # ---------- Estado para analise de operador ARITMETICO ---------- #  
                case STATE.OPERADOR_ARITMETICO:
                    # Se for um operador Relacional, transfere a responsabilidade
                    if lexema == "/" and char == "/":
                        estado = STATE.COMENTARIO_LINHA
                        continue
                    elif lexema == "/" and char == "*":
                        lexema = lexema + char # Eestou salvando pq posso precisar usar para comentario mal formado
                        estado = STATE.COMENTARIO_BLOCO
                        i=i+1
                        continue
                    # Se for um aritmético duplo
                    elif (lexema=="+" and char=="+") or (lexema=="-" and char=="-"):
                        lexema = lexema + char
                        ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
                        estado = STATE.INICIO # Volta para posição inicial
                        i=i+1
                    ## Se for o caso de um número negativo
                    elif (lexema=='-' and char.isdigit()) and (ultimo_token['tipo'] in [TOKENS_TYPE.OPERADOR_ARITMETICO, 
                                                                                TOKENS_TYPE.OPERADOR_LOGICO, 
                                                                                TOKENS_TYPE.OPERADOR_RELACIONAL, 
                                                                                TOKENS_TYPE.DELIMITADOR,
                                                                                TOKENS_TYPE.NUMERO_MAL_FORMADO,
                                                                                TOKENS_TYPE.IDENTIFICADOR_MAL_FORMADO,
                                                                                TOKENS_TYPE.CADEIA_DE_CARACTERES,
                                                                                TOKENS_TYPE.CADEIA_MAL_FORMADA,
                                                                                None]):
                        estado = STATE.NUMERO
                    # Se for o um único dos +-/* e depois não vier um número
                    else:
                        ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
                        estado = STATE.INICIO # Volta para posição inicial
            

            
                case STATE.COMENTARIO_LINHA:
                    i=i+1
                case STATE.COMENTARIO_BLOCO:
                    lexema = lexema + char 
                    if (lexema[-2:] == "*/"):
                        estado = STATE.INICIO # Ignora tudo oq fez até aqui
                    # LEMBRAR DE INCLUIR O \n QUANDO CHEGAR NO FINAL DA LINHA E N TIVER FECHADO O COMENTARIO
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

                # -----------iniciando numero------------------# EDITANDO... 
                case STATE.NUMERO:
                    if char.isdigit():  # Continua lendo dígitos
                        lexema += char
                    elif char == '.':  # Ponto pode indicar início de um float ou ser um delimitador
                        if '.' in lexema and not any(c.isalpha() for c in lexema):  # Já contém um ponto e não letras
                            partes = lexema.split('.')
                            if len(partes) > 2 or lexema.endswith('.'):  # Mais de um ponto ou termina com ponto
                                #tokens.append(lexema)  # Salva como número mal formado
                                lexema = ''  # Reinicia lexema para o próximo token
                                #tokens.append('.')  # Adiciona o ponto como delimitador
                            else:
                                lexema += char  # Assume continuação de um float
                                if i + 1 < final_pos_linha and linha[i + 1] == '-':
                                    lexema += '-'  # Adiciona '-' para fazer parte do token atual
                                    i += 1  # Incrementa para pular o caractere '-' no processamento subsequente
                        else:
                            # Verifica se estamos encerrando um token com caracteres não-digitais
                            if any(c.isalpha() for c in lexema):
                                #tokens.append(lexema)  # Salva o token atual como mal formado ou completo
                                lexema = ''  # Reinicia lexema
                                #tokens.append('.')  # Adiciona o ponto como delimitador separado
                            else:
                                lexema += char  # Primeiro ponto, possível início de float
                                if i + 1 < final_pos_linha and linha[i + 1] == '-':
                                    lexema += '-'  # Adiciona '-' para fazer parte do token atual
                                    i += 1  # Incrementa para pular o caractere '-' no processamento subsequente
                    elif char.isalpha():  # Trata caracteres alfabéticos após o número
                        lexema += char  # Adiciona o caractere ao lexema atual
                    else:  # Qualquer outro caractere que não seja dígito ou ponto
                        if lexema.endswith('.'):
                            if any(c.isalpha() for c in lexema):  # Verifica se tem letras antes do ponto
                                #tokens.append(lexema[:-1])  # Salva a parte numérica e letras como mal formado
                                #tokens.append('.')  # Salva o ponto como delimitador
                                pass
                            else:
                                #tokens.append(lexema[:-1])  # Salva a parte numérica
                                #tokens.append('.')  # Salva o ponto final como delimitador
                                pass
                        elif lexema.count('.') > 1:  # Múltiplos pontos
                            #tokens.append(lexema)  # Salva como número mal formado
                            pass
                        else:
                            #tokens.append(lexema)  # Salva como número válido ou float com um único ponto
                            pass
                        lexema = ''  # Reinicia lexema
                        estado = STATE.INICIO  # Retorna ao estado inicial
                        continue  # Importante para não perder o caractere de transição atual
                    i += 1  # Avança para o próximo caractere


                # ---------- Estado para analise de operador relacional ---------- #  OOOKKKKK
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

                # ---------- Estado para analise de IDENTIFICADORES ---------- #  OOOOKKKKK
                case STATE.IDENTIFICADOR:
                    # Se for letra, num ou underline e não for o final da linha
                    if (not e_delimitador(char)):
                        # Se tiver algum caracter fora dos permitidos, sinalizo o erro
                        if not e_ide_valido(char):
                            token_atual = TOKENS_TYPE.IDENTIFICADOR_MAL_FORMADO
                        lexema = lexema + char
                    else: # Se for um delimitador
                        # Se for palavra reservada
                        if lexema in reservadas:
                            estado = STATE.PALAVRA_RESERVADA
                            token_atual = TOKENS_TYPE.PALAVRA_RESERVADA
                        else:
                            ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
                            estado = STATE.INICIO # Vai para o inicio
                        continue
                    i=i+1# Passo a linha


                case STATE.PALAVRA_RESERVADA:
                    ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
                    estado = STATE.INICIO # Vai para o inicio      


                # ---------- Estado para analise de DELIMITADORES ---------- # OOOOKKKKK
                case STATE.DELIMITADOR:
                    # só serve para salvar na estrutura de palavra reservada
                    ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
                    estado = STATE.INICIO
                    i=i+1# Passo a linha
        

        # Se o lexema que estiver aqui for de algum estado incompleto
        ## PENSAR QUANDO TIVER O COMENTÁRIO
        if lexema and estado != STATE.INICIO:
            if estado == STATE.COMENTARIO_LINHA:
                estado = STATE.INICIO
            elif estado == STATE.COMENTARIO_BLOCO:
                lexema = lexema + "\n"
            # Se tenho algum lexema para pôr e é do tipo cac, significa que n fechei ela
            elif estado == STATE.CADEIA_DE_CARACTERES:
                token_atual = TOKENS_TYPE.CADEIA_MAL_FORMADA
            else:
                ### LEMBRE-SE DE OLHAR ISSO AQUI ### LEMBRE-SE DE OLHAR ISSO AQUI ### LEMBRE-SE DE OLHAR ISSO AQUI ### LEMBRE-SE DE OLHAR ISSO AQUI ### LEMBRE-SE DE OLHAR ISSO AQUI 
                ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#??????????????????????????!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!?????????????????????????
                ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#??????????????????????????!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!?????????????????????????
                ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#??????????????????????????!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!?????????????????????????
                ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
                # Lembrar de ver a lógica para o caso de 
                estado = STATE.INICIO

    # para tratar o comentário de bloco mal formado
    if lexema and estado==STATE.COMENTARIO_BLOCO:
        token_atual = TOKENS_TYPE.COMENTARIO_MAL_FORMADO
        ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
    
    return tokens_bem_formados, tokens_mal_formados






### ====================== EXECUÇÃO DO CÓDIGO ====================== ###
if __name__ == '__main__':
    # Obtem a lista de arquivos que podem ser lidos
    arquivos_entrada = obter_nomes_arquivos_entrada()
    # Começa um for em cada um deles
    for arquivo in arquivos_entrada:
        # Obtem as linhas
        linhas = obtem_todas_linhas(arquivo)
        # Passa pela analise lexica
        try:
            TBF, TMF = analisador_lexico(linhas)
            erro = False
        except:
            erro = True
        # Escreve a saída após passar pelo analisador (Lembrar de escrever quando der erro também, então bota um try except no analisador)
        escreve_saida(arquivo, TBF, TMF, erro)
