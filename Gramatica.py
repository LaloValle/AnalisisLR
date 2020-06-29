# -*- coding: utf-8 -*-
#@author: Lalo Valle

from tabulate import *

class Gramatica():

    def __init__(self):
        # Las llave del diccionario será el símbolo no terminal del lado izquierdo y el valor de este será una lista con las reglas del lado derecho
        self._reglas = {}

        self._simbolosTerminales = set()
        self._simbolosNoTerminales = set()

        self._simboloInicial = ''

    def identificarSimbolosEnCadena(self,cadena,numSimbolos=0):
        """
            Se identifican los símbolos válidos para una cadena dada según los simbolos terminales y no terminales ya reconocidos.
            En el caso de no ser identificado un símbolo como terminal o no terminal se coloca un None en lugar de la tupla.

            Regresa una lista con la subcadena identificada como un símbolo
        """
        if numSimbolos == 0: numSimbolos = len(cadena)

        simbolosIdentificados = []
        simboloAux = ''
        posicion = 0
        # El valor del tipo simbolo será 1:Terminal, 2: no Terminal
        tipoSimbolo = 0
        historialTipoSimbolo = 0

        if len(cadena) > 0:
            # Ciclo que seguira hasta que se alcance en la posición la longitud de la cadena o se hayan encontrado el número de simbolos por identificar especificado
            while posicion < len(cadena)+1 and numSimbolos > 0:
                simbolo = cadena[posicion] if posicion < len(cadena) else cadena[-1]
                simboloAux += simbolo

                if simboloAux in self._simbolosTerminales: tipoSimbolo = 1
                elif simboloAux in self._simbolosNoTerminales: tipoSimbolo = 2
                else: tipoSimbolo = 0

                if historialTipoSimbolo > 0 and tipoSimbolo != historialTipoSimbolo:
                    simbolosIdentificados.append(simboloAux[:-1])
                    simboloAux = ''

                    if posicion < len(cadena): posicion -= 1
                    numSimbolos -= 1
                elif historialTipoSimbolo == 0 and posicion >= len(cadena):
                    simbolosIdentificados.append(None)
                    break

                posicion += 1
                historialTipoSimbolo = tipoSimbolo

        return simbolosIdentificados

    def getReglas(self):
        return self._reglas

    def getSimbolosTerminales(self):
        if len(self._simbolosTerminales) == 0:
            self._identificarSimbolosTerminales()
        return self._simbolosTerminales

    def getSimbolosNoTerminales(self):
        if len(self._simbolosNoTerminales) == 0:
            self._identificarSimbolosNoTerminales()
        return self._simbolosNoTerminales

    def getLadoDerecho(self, simbolosIzquierdos):
        ladosDerechos = []
        if type(simbolosIzquierdos) != list: simbolosIzquierdos = [simbolosIzquierdos]
        
        for simbolo in simbolosIzquierdos:
            if simbolo in self._reglas:
                ladosDerechos.append(self._reglas[simbolo])
        return ladosDerechos[0] if len(ladosDerechos) == 1 else ladosDerechos

    def getLadoIzquierdo(self, ladoDerecho):
        for izquierdo,ladosDerechos in self._reglas.items():
            if ladoDerecho in ladosDerechos:
                return izquierdo

    def getSimboloInicial(self):
        return self._simboloInicial

    def getNumeroRegla(self,ladoIzquierdo,ladoDerecho):
        contador = 0
        for izquierdo,reglas in self._reglas.items():
            for regla in reglas:
                if izquierdo == ladoIzquierdo and regla == ladoDerecho: return contador
                contador += 1

    def getReglaPorNumero(self,numero):
        acumulado = 0
        for izquierdo,reglas in self._reglas.items():
            if numero <= len(reglas)-1+acumulado:
                return [izquierdo,reglas[numero-acumulado]]
            else: acumulado += len(reglas)
        return None

    def isSimboloTerminal(self,simbolo):
        return simbolo in self._simbolosTerminales

    def isSimboloNoTerminal(self,simbolo):
        return simbolo in self._simbolosNoTerminales

    def crearNuevaRegla(self, simbolo):
        if not self._reglas:
            self._simboloInicial = simbolo
        self._reglas[simbolo] = []

    def agregarLadoDerecho(self, simboloIzquierdo, reglas=[]):
        if simboloIzquierdo in self._reglas:
            for regla in reglas:
                if regla not in self._reglas[simboloIzquierdo]:
                    self._reglas[simboloIzquierdo].append(regla)

    def _identificarSimbolosNoTerminales(self):
        for simbolo in self._reglas.keys():
            self._simbolosNoTerminales.add(simbolo)

    def _identificarSimbolosTerminales(self):
        if len(self._simbolosNoTerminales) > 0:
            for _, reglas in self._reglas.items():
                for regla in reglas:
                    simboloAux = ''
                    eraTerminal = True

                    for i in range(len(regla)):
                        simbolo = regla[i]
                        simboloAux += simbolo

                        if simbolo in self._simbolosNoTerminales or simboloAux in self._simbolosNoTerminales or simbolo in self._simbolosTerminales:
                            if not eraTerminal:
                                self._simbolosTerminales.add(
                                    simboloAux[0:len(simboloAux) - 1])
                                simboloAux = simboloAux[len(
                                    simboloAux) - 1:len(simboloAux)]
                            eraTerminal = True

                        if simboloAux not in self._simbolosNoTerminales:
                            if eraTerminal:
                                simboloAux = simboloAux[len(
                                    simboloAux) - 1:len(simboloAux)]
                            eraTerminal = False

                        if i == len(regla) - 1:
                            if simboloAux not in self._simbolosNoTerminales:
                                self._simbolosTerminales.add(simboloAux)

    def imprimirGramaticaConsola(self):
        for izquierdo, reglas in self._reglas.items():
            print('{}→'.format(izquierdo), end='')
            for regla in reglas:
                print('{}|'.format(regla), end='')
            print(';')

    def eliminarRecursionIzquierda(self):
        reglasPrimas = {}

        for simboloIzquierdo, reglas in self._reglas.items():
            alfas = []
            betas = []

            for regla in reglas:
                if regla[0] == simboloIzquierdo:
                    alfas.append(regla[1:len(regla)])
                else:
                    betas.append(regla)

            if alfas and betas:
                simboloPrimo = simboloIzquierdo + 'p'

                self._reglas[simboloIzquierdo].clear()
                for beta in betas:
                    self._reglas[simboloIzquierdo].append(beta + simboloPrimo)

                reglasPrimas[simboloPrimo] = []
                for alfa in alfas:
                    reglasPrimas[simboloPrimo].append(alfa + simboloPrimo)
                reglasPrimas[simboloPrimo].append('ε')

        self._reglas.update(reglasPrimas)


class Item():

    def __init__(self, ladoIzquierdo, ladoDerecho, posicionPunto=0, terminalesValidos=set()):
        self._ladoIzquierdo = ladoIzquierdo
        self._ladoDerecho = ladoDerecho
        self._posicionPunto = posicionPunto

        # Conjunto de terminales válidos utilizados en el análisis sintáctico LR(1)
        self._terminalesValidos = terminalesValidos

    def item(self):
        return Item(str(self._ladoIzquierdo),str(self._ladoDerecho),int(self._posicionPunto),set(self._terminalesValidos))

    def getLadoIzquierdo(self):
        return self._ladoIzquierdo

    def getLadoDerecho(self):
        return self._ladoDerecho

    def getPosicionPunto(self):
        return self._posicionPunto

    def getTerminalesValidos(self):
        return self._terminalesValidos

    def getCaracterPrecedenteAlPunto(self,gramatica,caracterPrecedente=1):
        caracteres = gramatica.identificarSimbolosEnCadena(self._ladoDerecho[self._posicionPunto:],caracterPrecedente)
        if len(caracteres) >= caracterPrecedente:
            return caracteres[caracterPrecedente-1]
        return None

    def getItemEnCadena(self):
        cadena = '{}→{}.{}'.format(self._ladoIzquierdo,self._ladoDerecho[:self._posicionPunto],self._ladoDerecho[self._posicionPunto:])
        if self._terminalesValidos:
            cadena += ',{'
            for terminal in frozenset(self._terminalesValidos):
                cadena += '{},'.format(terminal)
            cadena = cadena[:-1]
            cadena += '}'
        return cadena

    def incrementarPosicionPunto(self, incremento=1):
        self._posicionPunto += incremento

    def agregarTerminalesValidos(self,terminales):
        if type(terminales) != set: terminales = set(terminales)
        while  terminales:
            self._terminalesValidos.add(terminales.pop())

class EstadoItems():

    """
        Clase modelo de un estado generado resultado de la aplicación de la operación IrA en un conjunto de estados.

        @param nombre : String
        @param itemsCabezera: list (Lista que especifica los estados resultados de la operación mover e identifican al estado)
        @param itemsDerivados: list (Lista que especifica los estados resultados de la operación cerradura)
    """

    def __init__(self,nombre='',itemsCabezera=[],itemsDerivados=[]):
        self._nombre = nombre
        self._itemsCabezera = itemsCabezera
        self._itemsDerivados = itemsDerivados
        # Se indica como llave el símbolo terminal y como valor un elemento EstadoItems al que transiciona
        self._transiciones = {}

    def getNombre(self):
        return self._nombre

    def getItemsCabezera(self,numeroItem=-1):
        return self._itemsCabezera if numeroItem == -1 else self._itemsCabezera[numeroItem]

    def getItemsDerivados(self):
        return self._itemsDerivados

    def getTransiciones(self):
        return self._transiciones

    def getEstadoTransicion(self,simbolo):
        if simbolo in self._transiciones:
            return self._transiciones[simbolo]
        return None

    def getItems(self):
        # Regresa una lista de todos los items con el formato de cabezera, donde el primer elemento es un entero que indica el número de items pertenecientes a la cabezera
        return [len(self._itemsCabezera)]+self._itemsCabezera+self._itemsDerivados

    def getCaracteresPrecedentesALosPuntos(self,gramatica):
        itemsAux = self.getItems()
        itemsAux.pop(0)

        caracteres = set()

        for item in itemsAux:
            caracter = item.getCaracterPrecedenteAlPunto(gramatica)
            if caracter != None:
                caracteres.add(caracter)

        return caracteres

    def getEstadoEnCadena(self):
        tabla = [[self._nombre]]

        tabla.append(['<Cabezera>'])
        for item in self._itemsCabezera:
            tabla.append([item.getItemEnCadena()])

        tabla.append(['<Derivados>'])
        for item in self._itemsDerivados:
            tabla.append([item.getItemEnCadena()])

        tabla.append(['<Transiciones>'])
        for simbolo,estado in self._transiciones.items():
            tabla.append(['{}→{}'.format(simbolo,estado.getNombre())])

        return tabulate(tabla, headers="firstrow", tablefmt='grid')

    def setNombre(self,nombre):
        self._nombre = nombre

    def agregarItemCabezera(self,item):
        if type(item) != list: item = [item]
        for it in item:
          self._itemsCabezera.append(it)

    def agregarItemDerivado(self,item):
        if type(item) != list: item = [item]
        for it in item:
          self._itemsDerivados.append(it)

    def agregarTransicion(self,simbolo,estado):
        self._transiciones[simbolo] = estado

    def isCabezeraIgual(self,estado):
        if len(self._itemsCabezera) == len(estado.getItemsCabezera()):
            for i in range(len(self._itemsCabezera)):
                if self.getItemsCabezera(i).getItemEnCadena() != estado.getItemsCabezera(i).getItemEnCadena(): return False
            return True
        return False

    def tienePuntosFinales(self,gramatica):
        """ Verifíca que todos los items pertenecientes a la cabezera del estado tengan punto final.
            El método retorna una tupla con un valor Booleano y en su caso de existir punto final una lista con los lados de la regla
        """
        for item in self._itemsCabezera:
            if item.getCaracterPrecedenteAlPunto(gramatica) == None: return (True,[item.getLadoIzquierdo(),item.getLadoDerecho()])
        return (False,None)