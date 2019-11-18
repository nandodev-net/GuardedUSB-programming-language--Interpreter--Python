#######################################
# CI3715 Traductores e Interpretadores
# Entrega 3. 
# Fernando Gonzalez 08-10464
# Kevin Mena 13-10869
#######################################

from sys import exit
from context_utils import *
from g_AbsSyntaxTree import *



BLUE = '\033[94m'
BLUWHITE = '\033[44m'
END = '\033[0m'

# En este File reposa las clases y metodos relativos a
# aumentar y enriquecer Arbol Sintactico de nuestro programa
# con informacion de contexto y tabla de simbolos.

class ContextSymbol():
    """ Definicion del objeto [ContextSymbol], el cual representa la estructura de un simbolo
    a agregar en cada una de las tablas de hash de nuestra pila.

    inicializa con: 
            s_type : almacena el tipaje de la hoja que generara el simbolo.
            s_value : identificador o valor de la hoja que generara el simbolo.
            s_asignvalue : valor del simbolo si la hoja es de tipo Variable.
            is_index : almacena si el valor de la hoja es usado como contador de un loop.
            is_array : almacena si la hoja es de tipo arreglo.
    """
    def __init__(self, s_value, s_type):
        self.s_type = s_type 
        self.s_value = s_value 
        self.s_asignvalue = None 
        self.is_index = None 
        self.is_array = False


class SyntaxTreeContext:
    """ Definicion del objeto [SyntaxTreeContext], el cual representa una estructura
    de pila conformada por tablas de Hash (en python, la estructura diccionario es,
    en realidad, el build in de una tabla de hash), de modo que crearemos una pila
    de diccionarios.

    inicializa con: 
            c_scopes : lista que se comportara a modo de pila para almacenar los diccionarios.
            c_secScopes : pila auxiliar para operaciones sobre la c_scopes.
            c_currentLine : entero que representa el numero de linea en proceso.
    """
    def __init__(self):
        self.c_scopes = []
        self.c_secScopes = []
        self.c_currentLine = 1


    def ExpressionAnalizer(self, expression):
        for child in expression.childs:
            if (child.p_type == 'BooleanOperator'):
                oprator1 = child.childs[0]
                oprator2 = child.childs[1]
                type1 = self.ExpressionAnalizer(oprator1)
                type2 = self.ExpressionAnalizer(oprator2)
                if (type1 != type2 != 'bool'):
                    print("[Context Error] line " + str(self.c_currentLine) + '. Boolean operator wrong type.')
                    sys.exit(0)
                else:
                    return 'bool'       

    def AppendContextSymbol(self, leaf, s_type, is_array):
        """ Definicion del metodo [AppendContextSymbol], el cual se encarga de la creacion del
        objeto simbolo el cual sera insertado en la tabla de hash (diccionario) que se encuentra
        en el tope de la pila.
        
        recibe: leaf : hoja a analizar.
                s_type : tipaje de la hoja.
                is_array : booleano si es un arreglo.
        """
        stack_top = self.c_scopes[0]
        if leaf.p_value in stack_top:
            print("[Context Error] Line " + str(self.c_currentLine) +'. Variable has been declared before.')
            sys.exit(0)
        
        if(isinstance(s_type.p_value, SyntaxLeaf)):
            s_type.p_value = "array[" + str(s_type.p_value.childs[0].p_value) + ".." + str(s_type.p_value.childs[1].p_value) + "]"
        
        new_symbol = ContextSymbol(leaf.p_value, s_type.p_value)
        new_symbol.is_array = is_array
        stack_top[leaf.p_value] = new_symbol

        if ((len(leaf.childs))>0):
            for leaf in leaf.childs:
                if (leaf.p_type == 'Variable'):
                    self.AppendContextSymbol(leaf, s_type.childs[0], is_array)
                elif (leaf.p_type == 'Expression'):
                    #t = self.ExpressionAnalizer(leaf)
                    if (t != p_type):
                        print("[Context Error] line " + str(self.c_currentLine) + 'Variable types does not match.')
                        sys.exit(0)
                    else:
                        stack_top[leaf.p_value].s_asignvalue = leaf

    def CreateContextScope(self, leaf):
        """ Definicion del metodo [CreateContextScope], el cual se encarga de hacer el manejo del
        metodo de creacion de simbolos en la tabla.
        
        recibe: leaf : hoja a analizar.
        """
        leaf_type = leaf.p_value
        
        if leaf_type == 'Array':
            is_array = True
        else:
            is_array = False

        for child in leaf.childs:
            if (child.p_type == 'Declare'):
                self.c_currentLine += 1
                self.CreateContextScope(child)
            elif (child.p_type == 'Variable'):
                print(leaf)
                self.AppendContextSymbol(child, leaf_type, is_array)
            # elif child.p_type == 'Array':
            #     p_type = self.getType(child)
            #     self.getArrayType(child)


    def ContextAnalyzer(self, SyntaxTreeStructure):
        """ Definicion del metodo [ContextAnalyzer], el cual se encarga de revisar 
        linea a linea de forma recursiva todos los componentes del Arbol Sintactico
        generado por el parser.
        
        recibe: SyntaxTreeStructure : Estructura completa del arbol sintactico a analizar.
        """
        if SyntaxTreeStructure:
            if (len(SyntaxTreeStructure.childs) > 0):
                for leaf in SyntaxTreeStructure.childs:

                    if (leaf.p_type == 'Block'):
                        self.c_currentLine+=1
                        self.ContextAnalyzer(leaf)
                        self.c_scopes.pop(0)

                    elif (leaf.p_type == 'Declare'):
                        self.c_currentLine+=1
                        new_scope ={}
                        self.c_scopes.insert(0,new_scope)
                        self.CreateContextScope(leaf)
                        self.c_secScopes.append(self.c_scopes[0])

                    # elif (leaf.p_type  == 'Asign'):
                    #     self.c_currentLine += 1
                    #     if (isinstance(leaf.p_value, str)):
                    #         var = self.variableAnalizer(leaf.p_value)
                    #         if (var.contador):
                    #             print("[Context Error] line " + str(self.c_currentLine) + ". tries to modify varible" + leaf.p_value + "of iteration.")
                    #             sys.exit(0)
                    #         var = var.tipo
                    #     else:
                    #         var = self.getTipoId(leaf.p_value)

                    #     _type = self.ExpressionAnalizer(leaf.childs[0])

                    #     if (var != _type):
                    #         print("[Context Error] line " + str(self.c_currentLine) + ". Different variable types.")
                    #         sys.exit(0)


        else:
            print('[Error]: No SyntaxTreeStructure')


    def PrintSymbolTable(self):
        values =[]
        types =[]
        for scope in self.c_secScopes:
            for var in scope:
                print('hey',var)        
                print('hey',scope[var].s_value,scope[var].s_type)        
                values.append(scope[var].s_value)
                types.append(scope[var].s_type)
            
        sortpre =sorted(values, key=len)
        sorttyp = sorted(types, key=len)
        longest_val = len(sortpre[-1])
        longest_type = len(sorttyp[-1])
        margin_table = ' '*(((longest_val+longest_type)//2)+4)

        print(BLUWHITE +margin_table+ "SYMBOL TABLE"+margin_table+ END)
        for scope in self.c_secScopes:
            for i in scope:
                if len(scope[i].s_value) < longest_val:
                    if len(scope[i].s_value) % 2 == 0:
                        print(BLUE+'Variable '+END+' '*((longest_val-len(scope[i].s_value)))+scope[i].s_value+' '+BLUE+'|'+END+ ' '+ BLUE+'Type '+END+scope[i].s_type)
                    else:
                        print(BLUE+'Variable '+END+' '*((longest_val-len(scope[i].s_value)))+scope[i].s_value+' '+BLUE+'|'+END+ ' '+ BLUE+'Type '+END+scope[i].s_type)

                else:
                    print(BLUE+'Variable '+END+scope[i].s_value+' ' +BLUE+'|'+END+ ' '+ BLUE+'Type '+END+scope[i].s_type)