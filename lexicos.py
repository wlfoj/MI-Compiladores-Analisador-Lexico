palavras_reservadas = {
"algoritmo", 
"principal", 
"variaveis",
"constantes", 
"registro", 
"função",
"retorno", 
"vazio", 
"se", 
"senao", 
"enquanto",
"leia", 
"escreva", 
"inteiro", 
"real", 
"booleano",
"char", 
"cadeia", 
"verdadeiro", 
"falso"
}

# expressões regulares da estrutura léxica da linguagem.
estrutura_lexica = {
    "identificador": r"^[a-zA-Z][a-zA-Z0-9_]*$",
    "numero": r"^[0-9]+(\.[0-9]+)?$",
    "cadeia_caracteres": r'^"[\x20-\x21\x23-\x7E]*"$',
    "comentario": r"^/\*.*?\*/$",
    "delimitadores": [";", ",", ".", "(", ")", "[", "]", "{", "}", "->"],
    "operadores_relacionais": ["!=", "==", "<", "<=", ">", ">=", "="],
    "operadores_aritmeticos": ["+", "-", "*", "/", "++", "--"],
    "operadores_logicos": ["!", "&&", "||"],
}


#  Códigos dos erros/tokens.
codigos = {
    "num": ("NMF", "NRO"),
    "coment": ("CoMF", ""),
    "str": ("CMF", "CAC"),
    "ident": ("IMF", "IDE"),
    "delimitadores": ("", "DEL"),
    "tokenmf": ("TMF", ""),
    "operadores_relacionais": ("", "REL"),
    "operadores_aritmeticos": ("", "ART"),
    "operadores_logicos": ("", "LOG"),
}