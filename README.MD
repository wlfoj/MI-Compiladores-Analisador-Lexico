ver os casos com && e || em identificadores, numeros inteiros e números decimais


if char in '&|' and i < final_pos_linha:
    # Finalizo
    if char == '&' and linha[i+1] == '&':
        ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
        estado = STATE.INICIO # Volta para posição inicial
        continue
    # Finalizo
    elif char == '|' and linha[i+1] == '|':
        ultimo_token = salva_lexema(lexema, linha_num, token_atual, tokens_bem_formados, tokens_mal_formados)
        estado = STATE.INICIO # Volta para posição inicial
        continue
    else:
        token_atual = TOKENS_TYPE.IDENTIFICADOR_MAL_FORMADO
        lexema = lexema + char

