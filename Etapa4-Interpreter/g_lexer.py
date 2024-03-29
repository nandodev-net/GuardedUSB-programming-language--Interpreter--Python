#!/usr/bin/env python

#######################################
# CI3715 Traductores e Interpretadores
# Entrega 4. 
# Fernando Gonzalez 08-10464
# Kevin Mena 13-10869
#######################################
import ply.lex as lex
import sys



# Palabras reservadas de GuardedUSB
gusb_keywords = {
    # Lenguaje
    'declare':'TkDeclare',

    # Condicionales
    'if':'TkIf',
    'fi':'TkFi',

    # Loops
    'for':'TkFor',
    'rof':'TkRof',
    'in':'TkIn',
    'to':'TkTo',
    'do':'TkDo',
    'od':'TkOd',

    # E/S
    'print':'TkPrint',
    'println':'TkPrintln',
    'read': 'TkRead',

    # Tipaje
    'int':'TkInt',
    'bool':'TkBool',
    'array':'TkArray',

    # Valores booleanos
    'true':'TkTrue',
    'false':'TkFalse',

    # Funciones embebidas
    'atoi':'TkAtoi',
    'size':'TkSize',
    'max':'TkMax',
    'min':'TkMin'
}

tokens = [
    # Identificadores
    'TkId',
    'TkNum',
    'TkString',

    # Separadores
    'TkOBlock',
    'TkCBlock',
    'TkSoForth',
    'TkComma',
    'TkOpenPar',
    'TkClosePar',
    'TkAsig',
    'TkSemicolon',
    'TkArrow',
    'TkGuard',
    'TkQuote',

    #Operadores

    'TkPlus',
    'TkMinus',
    'TkMult',
    'TkDiv',
    'TkMod',
    'TkOr',
    'TkAnd',
    'TkNot',
    'TkLess',
    'TkLeq',
    'TkGeq',
    'TkGreater',
    'TkEqual',
    'TkNEqual',
    'TkOBracket',
    'TkCBracket',
    'TkTwoPoints',
    'TkConcat'
] + list(gusb_keywords.values())


# Definiendo Regex para ignorar comentarios, espacios y Tabs
t_ignore = ' \t'
t_ignore_commentSimple = r'\/\/(.)*'


# Definiendo las Regex de los identificadores
def t_TkNum(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_TkId(t):
    r'[_A-Za-z]([_A-Za-z0-9])*'
    t.type = gusb_keywords.get(t.value,'TkId')
    return t

def t_TkString(t):
    r'"([^"\\\n]|\\"|\\\\|\\n)*"'
    t.value = t.value[0:]
    return t


# Definiendo las Regex para la identificacion de Tokens

# Regex de los separadores
t_TkOBlock = r'\|\['
t_TkCBlock = r'\]\|'
t_TkSoForth = r'\.\.'
t_TkComma = r','
t_TkOpenPar = r'\('
t_TkClosePar = r'\)'
t_TkAsig = r':='
t_TkSemicolon = r';'
t_TkArrow = r'\-\->'
t_TkGuard = r'\[\]'
t_TkQuote = r'\"|\''

# Expresiones de los Operadores

t_TkPlus = r'\+'
t_TkMinus = r'-'
t_TkMult = r'\*'
t_TkDiv = r'/'
t_TkMod = r'%'
t_TkOr = r'\\/'
t_TkAnd = r'\/\\'
t_TkNot = r'!'
t_TkLess = r'<'
t_TkLeq = r'<='
t_TkGeq = r'>='
t_TkGreater = r'>'
t_TkEqual = r'=='
t_TkNEqual = r'!='
t_TkOBracket = r'\['
t_TkCBracket = r'\]'
t_TkTwoPoints = r':'
t_TkConcat = r'\|\|'

# Funcion para realizar un seguimiento de los numeros de linea. El unico caracter
# valido para el salto de linea es '\n'
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Permite encontrar el numero de columna de la linea actual
def find_column(input,token):
    last_cr = input.rfind('\n',0,token.lexpos)
    if last_cr < 0:
        last_cr = -1
    column = token.lexpos - last_cr
    return column
        
# Manejo de errores en caso de encontrar un caracter invalido
def t_error(t):
    error.append(t)
    t.lexer.skip(1)

# Variable global de los errores del lexer si existen.
global error
error = []
token_list = []

# Funcion que imprime la lista de tokens
def TokenPrinter(token_list):
    for aux in token_list:
        if (aux.type == 'TkId') or (aux.type == 'TkString') or (aux.type == 'TkNum'):
            print (str(aux.type) +'("' +str(aux.value)+'") '+\
            str(aux.lineno) +' '+ str(find_column(lexer.lexdata,aux)))
        else:
            print (str(aux.type)+' ' + str(aux.lineno) +' '+ str(find_column(lexer.lexdata,aux)))

# Inicializacion del lexer
lexer = lex.lex()

# Funcion que se encarga de construir el lexer.
def lexer_builder(meta_program):
    lexer.input(meta_program)
    while True:
        tok = lexer.token()
        if not tok: break
        token_list.append(tok)
    
    # Impresion de errores del lexer, en caso de existir.
    if (len(error) != 0):
        for aux in error :
            print('[Lexic Error]: Unexpected character "' + str(aux.value[0]) +'" in row ' + str(aux.lineno) +' ,column '+ str(find_column(lexer.lexdata,aux)))
        sys.exit()
    else:
        #TokenPrinter(token_list)
        pass

lex.lex()
