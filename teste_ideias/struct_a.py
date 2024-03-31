import string

lexico = {
    "reservado": ['algoritmo', 'principal', 'variaveis',
    'constantes', 'registro', 'funcao',
    'retorno', 'vazio', 'se', 'senao', 'enquanto',
    'leia', 'escreva', 'inteiro', 'real', 'booleano',
    'char', 'cadeia', 'verdadeiro', 'falso'],
    "operadores_relacionais" : ['=', '<', '>', '!=', '==', '<=', '>='],
    "operadores_aritmeticos": ['+', '-', '*', '/', '++', '--'],
    "operadores_logicos": ['!', '&&', '||', '&', '|'],
    "delimitadores": [';', ',', '.', '(', ')', '[', ']', '{', '}'],
    "letras" : list(string.ascii_lowercase) + list(string.ascii_uppercase),
    "digitos": list(string.digits),
}