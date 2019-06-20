from pattern.web import MediaWiki,Wiktionary,URL,extension
import pattern.es
from pattern.es import conjugate, tag,parse                 #DEBIDO A CIRCUNSTANCIAS INESPERADAS HE DEBIDO REALIZAR EL TRABAJO FINAL
import random                                               #SOLA. EL ARCHIVO, SI BIEN TIENE GRAN PARTE DEL CODIGO PROBADA ANTES DE
import sys                                                  #INGRESARLA EN EL IDE, OTRA PARTE NO PUDO SER REALIZADA NI COMPROBADA.
import string                                               #Y NO HE PODIDO TERMINAR DE ENTENDER SG.GRAPH Y COMO ENVIAR LAS COORDENADAS
if sys.version_info[0] >= 3:                                #PARA QUE EL GRAFICO QUEDARA BIEN PROPORCIONADO.
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg
def pedirDefinicion(palabra,clasificacionP):
    '''Pide la definición de la palabra ingresada, en caso de que dicha palabra no se encuentre en Wikcionario,
    pero sí sea reconocida por Pattern.es.'''
    print("Ingrese la definición de la palabra clasificada como ",clasificacionP[0][:len(clasificacionP[0])-1],", ",palabra,": ")
    return input()
def pedirPalabra(clasificacion):
    '''Pide el ingreso de una palabra de un tipo determinado
    sin determinar si es del tipo indicado o correcto.'''
    print("Ingrese un ",clasificacion)
    return input()
def validez(palabra,clasificacion,clasificacionW,clasificacionP):
    '''Chequea que la palabra ingresada corresponda al tipo de clasificación pedido por pantalla (a-s-v)
    y devuelve un booleano. Primero verifica que se encuentre en Wikcionary, luego que se encuentre en Pattern.es,
    y luego que ambos coincidan en la clasificación dada por Wikcionary.
    **>>>En el caso que se encuentre en Wikcionary, pero no en Pattern.es, la toma como válida.
    **>>>En el caso en que se encuentre en Wikcionary y sea reconocida por Pattern.es, pero no coincidan en la
    clasificación dada como principal - o primera- por Wikcionary, se toma como válida, pero se genera un reporte
    con esta situación que es guardado en un archivo denominado "Reporte.txt".
    **>>>En el caso de que sea reconocida sólo por Pattern.es como del tipo de clasificación pedida,
    la toma como válida, y pide que se ingrese una definición por teclado. Si es reconocia por Pattern.es pero no
    coincide con el tipo de clasificación pedida, no la toma como válida.'''
    aceptable=True
    if(clasificacionW=="No clasificado"):
        if (clasificacionP!=("No clasificado",)):
            definicion=pedirDefinicion(palabra,clasificacionP)
        else:
            print("La palabra tampoco es reconocida por Pattern.es. ")
            aceptable=False
    elif(clasificacionW not in clasificacionP)and(clasificacion!=clasificacionW):
        #Si bien no coinciden clasificacionP y clasificacionW, clasificacionW coincide con lo solicitado por teclado.
        #Entonces aún se toma como válida, aunque se genera un reporte.
        cadena = 'Hay conflicto con la palabra: %s. Segun Wikcionary es: %s. Segun Pattern.es es: %s.\n' % (palabra, clasificacionW, clasificacionP[0]) 
        print(cadena)
        arch.write(cadena)
        aceptable=True  #Hay conflicto entre Wikcionary y Pattern.es, pero se acepta igualmente.
    elif(clasificacion!=clasificacionW):
          print("La clasificación pedida no coincide con la dada por Wikcionary, por ende, no es válida. ")
    return aceptable
def clasificarSegunWiktionary(palabra):
    '''Busca la clasificación dada por Wikcionary como principal o primera en orden de aparición.
    En el caso en que no se encuentre en Wikcionary, o no sea ningún tipo de los buscados, se define
    como "No clasificado"'''
    idioma="es"
    buscados=("sustantivo","adjetivo","verbo")
    busqueda=Wiktionary(language=idioma).search(buscar)
    if (busqueda!="None"):
        #Busca entre los títulos de las secciones las palabras dentro de la tupla "buscados".
        #Para ello pasa las palabras que encabezan los títulos de cada sección a minúscula, para no dificultar la búsqueda.
        vw=list((filter((lambda section:section.title.split()[0].lower()=="verbo"),busqueda.sections)))
        aw=list((filter((lambda section:section.title.split()[0].lower()=="adjetivo"),busqueda.sections)))
        sw=list((filter((lambda section:section.title.split()[0].lower()=="sustantivo"),busqueda.sections)))
        #Se asigna un booleano a cada clasificación basándose en que se hayan encontrado las clasificaciones
        #correspondientes dentro de los títulos de secciones.
        esVerboWiki=len(vw)>0
        esAdjetivoWiki=len(aw)>0
        esSustantivoWiki=len(sw)>0
        print("Es verbo: ",esVerboWiki,", es adjetivo: ",esAdjetivoWiki,", es sustantivo: ",esSustantivoWiki)
        clasificacionW="No clasificado"
        clasifiqueW=False
        sumaW=esVerboWiki+esAdjetivoWiki+esSustantivoWiki   #Cada True suma 1, cada False suma 0.
        if (sumaW>=1):
            #La palabra esta en el diccionario Wiki y es a/s/v
            #posee una o mas de una clasificacion
            cabeceras=[]    #Guardo en esta lista las primeras palabras de cada título de sección, en minúscula.
            for section in busqueda.sections:
                cabeceras.append(section.title.split()[0].lower())
            i=0     #Inicializo un contador para recorrer los títulos guardados en la lista.
            #La búsqueda se detiene cuando logre clasificar la palabra según Wikcionary, o cuando se termine la lista.
            #Esta última condición se podría dar en el caso de que no fuera de ninguna de las 3 clasificaciones
            #usadas en la sopa de letras (por ejemplo, adverbios, preposiciones, etc.).
            while((not clasifiqueW)and(i<len(cabeceras))):
                if (cabeceras[i] in buscados):
                    clasificacionW=cabeceras[i]
                    clasifiqueW=True
                else:
                    i+=1
        print("Clasificacion segun Wikcionary: ",clasificacionW)
    else:
        print("La palabra no se encuentra en Wikcionary.")
    return clasificacionW
def esDelTipoPatternEs(tipo,palabra):
    '''Dice si la palabra corresponde con el tipo, ambos recibidos como parámetro.'''
    return (tipo in parse(palabra))
def clasificarSegunPatternEs(palabra):
    '''Busca la clasificación de la palabra a buscar según Pattern.es.
    Si posee más de una clasificación de entre las 3 buscadas, se guardan todas en una tupla
    denominada "clasificacionP".'''
    patternEsVerbo=esDelTipoPatternEs("VB",palabra)
    patternEsAdjetivo=esDelTipoPatternEs("JJ",palabra)
    patternEsSustantivo=esDelTipoPatternEs("NN",palabra)
    print("Pattern es verbo: ",patternEsVerbo,", es adjetivo: ",patternEsAdjetivo,", es sustantivo: ",patternEsSustantivo)
    clasificacionP=()
    sumaP=patternEsVerbo+patternEsAdjetivo+patternEsSustantivo
    if (sumaP>0):
        #Se guardan todas las clasificaciones Pattern.es(a/s/v), ya que la tomada como dominante es la de Wikcionary
        #Entonces luego resta ver si la clasificacion Wiki esta dentro del conjunto de las de Pattern.es
        #de las clasificaciones resultantes de Pattern.es (guardadas en la variable clasificacionP)
        if(patternEsVerbo):
            clasificacionP+=("verbo",)
        if (patternEsAdjetivo):
            clasificacionP+=("adjetivo",)
        if (patternEsSustantivo):
            clasificacionP+=("sustantivo",)
    else:
        clasificacionP=("No clasificado",)
    return clasificacionP
def palabrasPorDefecto():
    '''Crea un diccionario con una cantidad de palabras de cada uno de los tipos.
    Lo hace para los casos en que se quiere comenzar directamente el juego sin configurarlo previamente.'''
    palabras={}
    palabras["adjetivos"]=["grande","chico","mediano","bueno","malo"]
    palabras["sustantivos"]=["mesa","pared","madera","pelota","casa"]
    palabras["verbos"]=["jugar","saltar","comer","pelear","mirar"]
    return palabras
def ingresarPalabras(conformacion):
    '''Pide el ingreso por teclado de las palabras definidas por el usuario, dicha información con las cantidades
    de cada tipo está guardada inicialmente en un diccionario, recibido como parámetro, "conformacion", el cual
    luego es modificado en sus contenidos, o sea, se reemplaza el número por dicho numero de palabras con
    la clasificación guardada como clave del diccionario.  '''
    dic=conformacion[1]
    claves=list(dic.keys())
    for i in range(len(claves)):
        tipoDePalabra=claves[i] #Tipo adjetivos, sustantivos o verbos.
        cantDe_c_u=int(dic[tipoDePalabra])  #Cantidad a pedir de palabras de dicho tipo
        dic[tipoDePalabra]=[]   #Reemplazo, en dic la cantidad guardada como valor, por las palabras que son del tipo necesitado
        for i in range(cantDe_c_u):
            print("Ingrese un ",tipoDePalabra[:len(tipoDePalabra)-1],": ")
            ingreso=pedirPalabra(tipoDePalabra)
            clasificacionW=clasificarSegunWiktionary(ingreso)
            clasificacionP=clasificarSegunPatternEs(ingreso)
            while not validez(ingreso,tipoDePalabra,clasificacionW,clasificacionP):
                ingreso=pedirPalabra(tipoDePalabra)
                clasificacionW=clasificarSegunWiktionary(ingreso)
                clasificacionP=clasificarSegunPatternEs(ingreso)
            dic[tipoDePalabra].append(ingreso)    
    conformacion[1]=dic
    return conformacion
def conformacionDefault():
    '''Define una conformacion default de cantidad de cada tipo y dirección de escritura de las palabras. '''
    aux=()
    aux+=("Horizontal",)
    aux+=({},)
    aux[1]["sustantivos"]="5"
    aux[1]["adjetivos"]="5"
    aux[1]["verbos"]="5"
    return aux
def definirConformacion():
    '''Pide al usuario que ingrese la cantidad de palabras que desea ingresar de cada tipo en la sopa de letras.
    Retorna la dirección de escritura de las palabras(vertical u horizontal), y un diccionario con claves denominadas
    como cada uno de los tipos buscados, y la cantidad de cada tipo a solicitar por teclado. '''
    layout = [
        [sg.Text('Ingrese las cantidad de palabras de cada categoría: ')],
        [sg.Text('Máximo a sumar entre las 3 categorías: 30.')],
        [sg.Text('Cantidad de adjetivos: ', size=(25, 1)), sg.Input(key='adjetivos')],
        [sg.Text('Cantidad de sustantivos: ', size=(25, 1)), sg.Input(key='sustantivos')],
        [sg.Text('Cantidad de verbos: ', size=(25, 1)), sg.Input(key='verbos')],
        [sg.Text('Ingrese el sentido de escritura de las palabras en la sopa de letras: '),sg.Button('Vertical'),sg.Button('Horizontal')],
        ]
    window = sg.Window('Conformación de la sopa de letras').Layout(layout)
    return window.Read()
'''
def escribirPalabraEnColumna(columna):
    #FALTA IMPLEMENTAR
def escribirPalabraEnFila(fila):
    #FALTA IMPLEMENTAR
'''
def armarCuadricula(conformacion):
    '''Conforma la cuacrícula de la sopa de letras, con la conformación definida por usuario o por defecto'''
    lado=20
    disposicion=conformacion[0]
    palabrasAInsertar=conformacion[1]
    claves=list(palabrasAInsertar.keys())
    maxLongPal=-1
    for i in range(len(claves)):
        claveActual=claves[i]
        for j in range(len(palabrasAInsertar[claveActual])):
            if(len(palabrasAInsertar[claveActual][j])>maxLongPal):
                maxLongPal=len(palabrasAInsertar[claveActual][j])
    ladosGrafico=lado*maxLongPal
                       
    layout = [
        [sg.Text('SOPA DE LETRAS')],
        [sg.Graph(canvas_size=(700,700), graph_bottom_left=(0,700),graph_top_right=(500,0), key='_GRAPH_', change_submits=False, drag_submits=False)],
        [sg.Submit(), sg.Button('Exit')]#NO LOGRO ENTENDER AUN COMO SE CONFIGURAN LOS PARAMETROS DEL GRAFICO
        ]
    window = sg.Window('Para confirmar la palabra, ingrese Submit', ).Layout(layout).Finalize()
    g = window.FindElement('_GRAPH_')
    for fila in range(maxLongPal+2):
        for col in range(maxLongPal+2):
            g.DrawRectangle((col*lado+5, fila*lado+3), (col*lado+lado+5, fila*lado+lado+3), line_color='black',fill_color='green')
            g.DrawText('{}'.format(random.choice(string.ascii_uppercase),font='Courier 25'),(col *lado+10, fila*lado+8))
    cantPal=0
    for i in range(len(claves)):
        cantPal+=len(palabrasAInsertar[claves[i]])
    ocupados=()
'''
    for i in range(cantPal):
        eleccion=random.randrange(maxLongPal)
        while eleccion in ocupados:
            eleccion=random.randrange(maxLongPal)
        ocupados+=(eleccion,)
        if disposicion=="Vertical":
            escribirPalabraEnColumna(eleccion) #FALTA IMPLEMENTAR
        else:
            escribirPalabraEnFila(eleccion) #FALTA IMPLEMENTAR
'''
def main():
    ingresadas=False
    layoutMain = [
        [sg.Button('Configuración'),sg.Button('Jugar')],
        [sg.Button('Salir')],
        ]
    windowMain = sg.Window('SOPA DE LETRAS').Layout(layoutMain)
    button = windowMain.Read()
    while True:
        if button=="Salir":
            break
        elif button=="Configuración":
            #conformacion[0] contiene la orientación de escritura en la sopa de letras.
            #conformacion[1] contiene el diccionario con los tipos como claves y una lista con las palabras
            #aceptadas como tales dentro de los valores de cada tipo correspondiente.
            conformacion=definirConformacion()
            palabras=ingresarPalabras(conformacion)
        #Si se ingresa"Jugar" y no pidió previamente ingresar la conformación y palabras.
        elif not ingresadas:
            conformacion=conformacionDefault()
            #palabras=palabrasPorDefecto()
            armarCuadricula(conformacion)
        ingresadas=True
        armarCuadricula(palabrasYOrientacion)

nomArch="Reporte.txt"
arch=open(nomArch,"w+") 
if __name__=="__main__":
    main()
arch.close()    
