import PySimpleGUI as sg
from AnalizadorLexico import *
from AnalizadorSintactico import *
from GeneradorAutomatas import *

sg.theme('GreenTan')
btnSintactico = 'Analizar sintácticamente'
txtInput= 'texto entrada'
txtSin = 'Caja de texto Sintac'
txtSinD = 'Caja de texto estados'
archivo = 'FILE'
LR = None


# STEP 1 define the layout
layout = [
		[
			sg.Text('Gramática para analizar'),
			sg.In(key=archivo),
			sg.FileBrowse(file_types=(("Archivos de texto plano", "*.txt"),))
		],

		[
        sg.Multiline(key=txtSin, default_text='', size=(90, 50)), #análisis sin
        sg.Multiline(key=txtSinD, default_text='', size=(40, 50)) #análisis sin
        ],

        [
			sg.Text('Analizar cadena'),
			sg.In(key=txtInput),
		],
        
        [
        	sg.Button(btnSintactico)
        ]
	]

#STEP 2 - create the window
window = sg.Window('My new window', layout, grab_anywhere=True)

# STEP3 - the event loop
while True:
	event, values = window.read()   # Read the event that happened and the values dictionary
	if event == sg.WIN_CLOSED:     # If user closed window with X or if user clicked "Exit" button then exit
		break
	elif event == btnSintactico:
		#Se limpia la caja con los resultados del sintáctico
		window[txtSin]('')
		if window[archivo].get() is not None and window[archivo].get() is not '' and window[txtInput].get() is not None:
			cadenaVerificar = window[txtInput].get()			
			lineas = open(window[archivo].get(),'r').readlines()
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
				#cadenaVerificar = '(aora)*&a+'
				window[txtSin].Update(value='\n GRAMÁTICA RECONOCIDA\n', append=True)
				gramatica = sintactico.getGramaticaGenerada()

				window[txtSin].Update(value=gramatica.imprimirGramatica(), append=True)

				window[txtSin].Update(value='\n Simbolos terminales y no terminales\n', append=True)

				window[txtSin].Update(value=gramatica.getSimbolosNoTerminales(), append=True)
				window[txtSin].Update(value='\n', append=True)
				window[txtSin].Update(value=gramatica.getSimbolosTerminales(), append=True)
				window[txtSin].Update(value='\n', append=True)
				
				LR = AnalizadorSintacticoLR(gramatica)
				LR.setCadena(cadenaVerificar)

				window[txtSin].Update(value=gramatica.identificarSimbolosEnCadena(cadenaVerificar), append=True)
				window[txtSin].Update(value='\n', append=True)

				window[txtSinD].Update(value='\n Cerradura del primer elemento \n', append=True)


				estado = LR.cerradura([Item(gramatica.getSimboloInicial(), gramatica.getLadoDerecho(gramatica.getSimboloInicial())[0],terminalesValidos = set('$'))],LR1=True)
				window[txtSinD].Update(value=estado.getEstadoEnCadena(), append=True)

				window[txtSinD].Update(value='\n Tablas SLR\n', append=True)
				LR.generarTablaSLR()

				for estado in LR.getConjuntoEstados():
					window[txtSinD].Update(value=estado.getEstadoEnCadena() , append=True)
					window[txtSinD].Update(value='\n', append=True)
					#print(estado.getEstadoEnCadena())
				window[txtSin].Update(value='\n', append=True)
				window[txtSin].Update(value='\n', append=True)
				window[txtSin].Update(value=LR.getTablaLREnCadena() , append=True)
				#print(LR.getTablaLREnCadena())

				window[txtSin].Update(value='\n', append=True)
				window[txtSin].Update(value='\nAnalisis SLR:\n' , append=True)
				#print('\n Analisis SLR:')
				window[txtSin].Update(value='\n cadena que se analiza: ' + cadenaVerificar , append=True)
				window[txtSin].Update(value='\n', append=True)
				#print('\n cadena que se analiza:',cadenaVerificar)
				
				valido,tabla = LR.analizarCadena()
				window[txtSin].Update(value=tabulate(tabla), append=True)
				#print(tabulate(tabla,tablefmt='fancy_grid'))
				if valido:
					window[txtSin].Update(value='\n\n\tLRS >> La cadena es válida\n\n' , append=True)
					#print('\n LRS >> La cadena es válida')
				window[txtSinD].Update(value='\n Tablas LR(1)\n' , append=True)
				#print('\n Tablas LR(1)')
				LR.generarTablaSLR(True)
				for estado in LR.getConjuntoEstados():
					window[txtSinD].Update(value=estado.getEstadoEnCadena(), append=True)
					window[txtSinD].Update(value='\n', append=True)
					#print(estado.getEstadoEnCadena())

				window[txtSin].Update(value=LR.getTablaLREnCadena(), append=True)
				#print(LR.getTablaLREnCadena())

				window[txtSin].Update(value='\n\nAnalisis LR(1):\n\n', append=True)
				#print('\n Analisis LR(1):')
				window[txtSin].Update(value='cadena que se analiza:' + cadenaVerificar + '\n', append=True)
				#print('\n cadena que se analiza:',cadenaVerificar)
				valido,tabla = LR.analizarCadena()
				window[txtSin].Update(value=tabulate(tabla), append=True)
				#print(tabulate(tabla,tablefmt='fancy_grid'))
				if valido:
					window[txtSin].Update(value='\n\nLR(1) >> La cadena es válida', append=True)
					#print('\n LR(1) >> La cadena es válida')

			else:
				window[txtSin].Update(value='\nError en al análisis léxico de la regla\n', append=True)


window.close()