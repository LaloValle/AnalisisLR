# -*- coding: utf-8 -*-
# @author: Lalo Valle 

from AnalizadorLexico import *
from AnalizadorSintactico import *
from GeneradorAutomatas import *

import sys

rutaReglas = sys.argv[1]

with open(rutaReglas, 'r') as archivo:
	lineas = archivo.readlines()


"""
	Obtención de la cadena sin espacios, saltos de línea, ni comentarios en la ruta indicada

"""
comentarioActivo = False
cadena = ''

for linea in lineas:
	linea = linea.replace('\n','')
	if linea.find(' ') > -1:
		linea = linea.replace(' ','')

	if not comentarioActivo:
		# Obtiene la posicion de los caracteres /* que indican un comentario de multiples líneas
		comentario = linea.find('/*')
		if comentario > -1:
			linea = linea[:comentario]
			comentarioActivo = True

		# Obtiene la posición del caracter # que indica un comentario de una sola línea
		comentario = linea.find('#')
		if comentario > -1:
			linea = linea[:comentario]
	else:
		comentario = linea.find('*/')
		if comentario > -1:
			linea = linea[comentario+2:]
			comentarioActivo = False
		else: linea = ''

	cadena += linea

automata = ManejadorTabulares.generarAFDDeTabular(ManejadorTabulares.recuperarTabular('TabularReglas.dat'))

lexico = AnalizadorLexico(automata, cadena)

sintactico = AnalizadorSintacticoReglas(lexico)

resultado = -1

valido = sintactico.analizar()

if valido:
	cadenaVerificar = '(aora)*&a+'

	print('\n Gramatica reconocida\n')
	gramatica = sintactico.getGramaticaGenerada()
	gramatica.imprimirGramaticaConsola()

	print('\n Simbolos terminales y no terminales\n')

	print(gramatica.getSimbolosNoTerminales())
	print(gramatica.getSimbolosTerminales())
	
	LR = AnalizadorSintacticoLR(gramatica)
	LR.setCadena(cadenaVerificar)

	print(gramatica.identificarSimbolosEnCadena(cadenaVerificar))

	print('\n Cerradura del primer elemento \n')
	estado = LR.cerradura([Item(gramatica.getSimboloInicial(), gramatica.getLadoDerecho(gramatica.getSimboloInicial())[0],terminalesValidos = set('$'))],LR1=True)
	print(estado.getEstadoEnCadena())

	print('\n Tablas SLR')
	LR.generarTablaSLR()

	for estado in LR.getConjuntoEstados():
		print(estado.getEstadoEnCadena())

	print(LR.getTablaLREnCadena())

	print('\n Analisis SLR:')
	print('\n cadena que se analiza:',cadenaVerificar)
	valido,tabla = LR.analizarCadena()
	print(tabulate(tabla,tablefmt='fancy_grid'))
	if valido: print('\n LRS >> La cadena es válida')

	print('\n Tablas LR(1)')
	LR.generarTablaSLR(True)
	for estado in LR.getConjuntoEstados():
		print(estado.getEstadoEnCadena())

	print(LR.getTablaLREnCadena())

	print('\n Analisis LR(1):')
	print('\n cadena que se analiza:',cadenaVerificar)
	valido,tabla = LR.analizarCadena()
	print(tabulate(tabla,tablefmt='fancy_grid'))
	if valido: print('\n LR(1) >> La cadena es válida')

else:
	print('Error en al análisis léxico de la regla')