try:
    import tkinter as tk
except ImportError:
    print(ImportError,"Se requiere el modulo Tkinter")
import re

def error(linea, textbox,color):
    pos = str(linea)
    textbox.tag_add(pos, pos+".0", pos+".90")
    textbox.tag_config(pos, foreground=color)

def correcto(linea, textbox):
    pos = str(linea)
    textbox.tag_add(pos, pos+".0", pos+".90")
    textbox.tag_config(pos, foreground="white")

def separar(contenido):
    respuesta = []
    code = re.search("CODE:", contenido)
    data = re.search("DATA:", contenido)
    if data != None:
        data = data.start()
    if code != None:
        code = code.start()
        respuesta.append(contenido[code+6:])
    if code != None and data != None:
        respuesta.append(contenido[data+6:code])
    if data == None and code == None:
        respuesta.append(contenido)
        respuesta.append('')
    return respuesta

def fuera_rango(pos_textbox, textbox, linea, lineas_malas):
    rango_valido = True
    valores = re.findall("[0-9]+|['#'][0-9A-F]+",linea)
    for val in valores:
        if val[0] == '#':
            val = int((val[1:]),16)
        else: 
            val = int(val)
        if (val > 256 or val < 0):
            error(pos_textbox, textbox, "yellow")
            rango_valido = False
            lineas_malas += 1
    return rango_valido, lineas_malas 

def variable_data(pos_textbox, textbox, linea, lineas_malas): # variable no declarada en data
    declarada = True
    valores = re.findall("['('][a-z]+[0-9a-z]*[')']",linea)
    if valores != []:
        error(pos_textbox, textbox, "magenta")
        declarada = False
        lineas_malas += 1
    return declarada, lineas_malas 

def label_declarado(pos_textbox, textbox, linea, lineas_malas): # label no declarada
    declarada = True
    valores = re.findall("['\s']+[a-z]+[0-9a-z]*",linea)
    if valores != [] and len(valores) == 1:
        error(pos_textbox, textbox, "cyan")
        declarada = False
        lineas_malas += 1
    return declarada, lineas_malas 

def buscar_data(texto, textbox, textbox_mem=None):
    dicc = {}
    posicion = 0
    lineas_correctas = 0
    lineas_malas = 0
    rango_valido = True
    if texto == "":
        pos_textbox = 1 
    else:
        pos_textbox = 2
    texto = texto.split('\n')
    if texto != [""]:
        for linea in texto:
            x = re.search("['\s']*[a-z]+[a-z0-9]*['\s']+([0-9]+|['#'][A-F0-9]+)", linea)
    
            if x != None:
                if len(x.group()) == len(linea):
                    rango_valido, lineas_malas = fuera_rango(pos_textbox, textbox, linea, lineas_malas)
    
                    if rango_valido:
                        name = re.search("[a-z]+[a-z0-9]*", linea).group()
                        valor = re.search("['\s']([0-9]+|['#'][A-F0-9]+)", linea).group()
                        dicc[name] = posicion
                        if textbox_mem != None:
                            valor = binario(valor[1:])
                            textbox_mem.insert(tk.INSERT, str(valor)+"\n")
                        posicion += 1
                        correcto(pos_textbox, textbox)
                        lineas_correctas+=1
                    else:
                        error(pos_textbox, textbox, "red")
                        lineas_malas+=1

            if x == None and rango_valido:
                error(pos_textbox, textbox, "red")
            
            pos_textbox += 1
        pos_textbox += 1

    return dicc, pos_textbox, [lineas_correctas,lineas_malas]

def buscar_code(texto, variables, pos_textbox, textbox, lineas):
    texto, posicion_direccionamiento = direccionamientos(texto)
    
    for val in variables:
        texto = texto.replace(val,str(variables[val]))
    instrucciones_texto = texto
 
    literales = re.findall("[0-9]+|['#'][A-F0-9]+",instrucciones_texto) # guardamos literales
    literales = binario_lista(literales)
    instrucciones_texto = re.sub("['(']([0-9]+|['#'][A-F0-9]+)[')']","(Dir)",instrucciones_texto)
    instrucciones_texto = re.sub("([0-9]+|['#'][A-F0-9]+)","Lit",instrucciones_texto)
    instrucciones_texto = re.sub("['\s']Lit['\n']"," Dir\n",instrucciones_texto)
    
    instrucciones = open("instrucciones.txt","r")
    inst={}
    
    for i in instrucciones.readlines():
        i = i.split("|")
        inst[i[0]]=i[1][:-1]
    
    #inst = {"MOV A,B": "0000000", "MOV B,A": "0000001"}
    instrucciones_validas = exp_regulares(inst.keys())
    
    lineas_correctas = lineas[0]
    lineas_malas = lineas[1]
    texto = texto.split('\n')
    n=0
    while n < len(posicion_direccionamiento):
        posicion_direccionamiento[n] += pos_textbox
        n+=1
    for linea in texto:
        if pos_textbox-1 in posicion_direccionamiento:
            pos_textbox += 1
        x = re.findall("['\s''\n']+", linea)
        
        if x == []:
            x = [""]

        if len(x[0]) != len(linea):
            valido = buscar(instrucciones_validas, linea)
        
            if valido:
                rango_valido, lineas_malas = fuera_rango(pos_textbox, textbox, linea, lineas_malas)
                if rango_valido:
                    correcto(pos_textbox, textbox)
                    lineas_correctas += 1
            else:
                declarado, lineas_malas = label_declarado(pos_textbox, textbox, linea, lineas_malas)

                if declarado:
                    declarado, lineas_malas = variable_data(pos_textbox, textbox, linea, lineas_malas)
                if declarado:
                    error(pos_textbox, textbox,"red") 
                    lineas_malas+=1
        pos_textbox += 1
    return [instrucciones_texto, inst, literales, [lineas_correctas,lineas_malas]]

def exp_regulares(lista):
    expreciones = {} 
    for txt in lista:
        exp = str(txt)
        exp = re.sub("Lit", "([0-9]+|['#'][A-F0-9]+)", exp)
        exp = re.sub("['(']Dir[')']", "['(']([0-9]+|['#'][A-F0-9]+)[')']", exp)
        exp = re.sub("Dir", "([0-9]+|['#'][A-F0-9]+)", exp)
        exp = re.sub("['(']A[')']", "['(']A[')']", exp)
        exp = re.sub("['(']B[')']", "['(']B[')']", exp)
        exp = re.sub("\s", "['\\\s']+", exp)
        exp = re.sub(",", "['\\\s']+", exp)
        expreciones[txt]=exp
    return expreciones

def buscar(exp_reg,texto): # exp_reg = {instruccion:expresion_regular}
    texto = re.sub(",", " ", texto)
    for ins in exp_reg.values():
        x = re.search("['\s']*"+ins+"['\s']*", texto)
        if x!=None:
            x = x.group(0)
            if len(x) == len(texto):
                return True
    return False

def binario_lista(lista):
    resultado = []
    for h in lista: 
        if h[0] == "#":
            h = h[1:]
            h_size = len(h) * 4
            resultado.append((bin(int(h, 16))[2:]).zfill(h_size))
        else:
            h = bin(int(h))[2:]
            resultado.append(h.zfill(8))
    return resultado

def binario(h):
    if h[0] == "#":
        h = h[1:]
        h_size = len(h) * 4
        return (bin(int(h, 16))[2:]).zfill(h_size)
    else:
        h = bin(int(h))[2:]
        return h.zfill(8)
 
def direccionamientos(texto):
    texto = re.sub("[':']['\s']", ":\n", texto)
    texto = re.sub("[':']['\t']", ":\n", texto)
 
    lineas = texto.split('\n')
    nombre_direcciones = (re.findall("[a-z]+[':']",texto))
    direcciones = {}

    posicion = 0
    for linea in lineas:
        for nombre in nombre_direcciones:
            x = re.findall(nombre,linea)
            if x != []:
                direcciones[nombre] = posicion
                lineas.pop(posicion)
                break
        posicion += 1

    texto = ""
    for i in lineas:
        texto += i+"\n"
    texto=texto[:-1]

    for nombre in direcciones:
        texto = texto.replace(nombre[:-1], str(direcciones[nombre]))
        
    return texto, list(direcciones.values())