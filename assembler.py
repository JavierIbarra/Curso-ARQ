try:
    import tkinter as tk
    from tkinter import filedialog
    import tkinter.font as tkFont
    import tkinter.messagebox as MessageBox
except ImportError:
    print(ImportError,"Se requiere el modulo Tkinter")

from funciones import *
import operator

def beep_error(f):
    def applicator(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except:
            if args and isinstance(args[0], tk.Widget):
                args[0].bell()
    
    return applicator
        
class MyText(tk.Text):
    def __init__(self, parent=None, *args, **kwargs):
        tk.Text.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.bind('<Control-a>', self.seleccionar_todo)
        self.bind('<Control-x>', self.cortar)
        self.bind('<Control-c>', self.copiar)
        self.bind('<Control-v>', self.pegar)
        self.bind('<Control-z>', self.deshacer)
        self.bind('<Control-y>', self.rehacer)
        self.bind("<Button-3><ButtonRelease-3>", self.mostrar_menu)
        
    def mostrar_menu(self, event):
        menu = tk.Menu(self, tearoff=0, bg='white', fg='black')
        menu.add_command(label="Cortar", command=self.cortar)
        menu.add_command(label="Copiar", command=self.copiar)
        menu.add_command(label="Pegar", command=self.pegar)
        menu.tk.call("tk_popup", menu, event.x_root, event.y_root)
    
    def copiar(self, event=None):
        self.event_generate("<<Copy>>")
        self.see("insert")
        return 'break'
    
    def cortar(self, event=None):
        self.event_generate("<<Cut>>")
        return 'break'
    
    def pegar(self, event=None):
        self.event_generate("<<Paste>>")
        self.see("insert")
        return 'break'
    
    def seleccionar_todo(self, event=None):
        self.event_generate("<<SelectAll>>")
        return 'break'
    
    @beep_error
    def deshacer(self, event=None):
        self.tk.call(self, 'edit', 'undo')
        return 'break'
    
    @beep_error
    def rehacer(self, event=None):
        self.tk.call(self, 'edit', 'redo')
        return 'break'
    
class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Assembler')
        self.geometry("1200x720")
        self.grid_rowconfigure((0,1), weight=1)
        self.grid_columnconfigure((1,2), weight=1)
        self.config(bg='#242424')
        self.bind("<Control-Up>", self.increase_text_font)
        self.bind("<Control-Down>", self.decrease_text_font)
        self.bind("<Control-s>", self.guardar_archivo)
        self.bind("<Control-o>", self.abrir_archivo)
        self.bind("<Control-r>", self.marcar_error)
        self.bind("<F5>", self.assembler)
        self.text_font = tkFont.Font(family='Consolas', size=12)
        
        self.text_01 = MyText(self, wrap=tk.WORD, bd=0, undo=True)
        self.text_01.config(bd=0, padx=6, pady=4, font=self.text_font,
            selectbackground='lightblue',
            bg='black', fg='white',
            insertbackground='white',
            highlightbackground='black',
            highlightcolor='white'
            )
        self.text_01.grid(row=0, column=1, rowspan=2, padx=(8,4), pady=8, sticky="nsew")

        self.text_02 = MyText(self, wrap=tk.WORD, bd=0, undo=True)
        self.text_02.config(bd=0, padx=6, pady=4, font=self.text_font,
            selectbackground='lightblue',
            bg='black', fg='white',
            insertbackground='white',
            highlightbackground='black',
            highlightcolor='white'
            )
        self.text_02.grid(row=0, column=2, padx=(4,8), pady=(8,4),sticky="nsew")
        #self.text_02.config(state=tk.DISABLED)

        self.text_03 = MyText(self, wrap=tk.WORD, bd=0, undo=True)
        self.text_03.config(bd=0, padx=6, pady=4, font=self.text_font,
            selectbackground='lightblue',
            bg='black', fg='white',
            insertbackground='white',
            highlightbackground='black',
            highlightcolor='white'
            )
        self.text_03.grid(row=1, column=2, padx=(4,8), pady=(4,8),sticky="nsew")
        #self.text_03.config(state=tk.DISABLED)
        self.menu()

    def menu(self):
        menubar = tk.Menu(self, bg='white', fg='black')
        self.config(menu=menubar)
        filemenu = tk.Menu(menubar, tearoff=0, bg='white', fg='black')
        menubar.add_cascade(label='Archivos', menu=filemenu, underline=0)
        runmenu = tk.Menu(menubar, tearoff=0, bg='white', fg='black')
        menubar.add_cascade(label='Ejecutar', menu=runmenu, underline=0)
        editmenu = tk.Menu(menubar, tearoff=0, bg='white', fg='black')
        menubar.add_cascade(label='Editar', menu=editmenu, underline=0)
        helpmenu = tk.Menu(menubar, tearoff=0, bg='white', fg='black')
        menubar.add_cascade(label='Ayuda', menu=helpmenu, underline=0)
        editmenu.add_command(label='Deshacer', command=self.text_01.deshacer, accelerator='Ctrl+Z')

        editmenu.add_command(label='Rehacer',command=self.text_01.rehacer,accelerator='Ctrl+Y')
        editmenu.add_separator()
        editmenu.add_command(label='Cortar', command=self.text_01.cortar, accelerator='Ctrl+X')
        editmenu.add_command(label='Copiar', command=self.text_01.copiar, accelerator='Ctrl+C')
        editmenu.add_command(label='Pegar', command=self.text_01.pegar, accelerator='Ctrl+V')
        editmenu.add_command(label='Seleccionar todo',command=self.text_01.seleccionar_todo,accelerator='Ctrl+A')
        helpmenu.add_command(label="Ayuda", command=self.ayuda)
        helpmenu.add_command(label="Acerca de...", command=self.acerca_de)
        filemenu.add_command(label="Abrir", command=self.abrir_archivo, accelerator="Ctrl+O")
        filemenu.add_command(label="Guardar como", command=self.guardar_archivo, accelerator="Ctrl+S")
        filemenu.add_separator()
        filemenu.add_command(label="Salir", command=self.quit)
        
        runmenu.add_command(label="Errores", command=self.marcar_error, accelerator="Ctrl+R")
        runmenu.add_command(label="Assembler", command=self.assembler, accelerator="F5")

    def ayuda(self):
        t1 = tk.Toplevel(self, bg="#F7F7F7")
        t1.geometry("600x200")
        t1.title("Ayuda")
        t1.grid_rowconfigure((0,1), weight=1)
        t1.grid_columnconfigure((0,1), weight=1)
        t1.focus_set()
        t1.grab_set()
        t1.transient(master=self)
        texto_lectura = tk.Text(t1, bg="#F7F7F7", fg="black", width=80, height=6, 
        highlightbackground="white", font=('Consolas', 14))
        texto_lectura.insert(tk.INSERT, "\n Instrucción no existe\n")
        texto_lectura.insert(tk.INSERT, " Literal fuera de rango permitido\n")
        texto_lectura.insert(tk.INSERT, " Variable no declarada en bloque DATA\n")
        texto_lectura.insert(tk.INSERT, " Etiqueta no existe en programa\n")
        texto_lectura.tag_add(1, "2.3", "2.6")
        texto_lectura.tag_config(1, background="red")
        texto_lectura.tag_add(2, "3.3", "3.6")
        texto_lectura.tag_config(2, background="yellow")
        texto_lectura.tag_add(3, "4.3", "4.6")
        texto_lectura.tag_config(3, background="magenta")
        texto_lectura.tag_add(4, "5.3", "5.6")
        texto_lectura.tag_config(4, background="cyan")
        texto_lectura.grid(row=0, column=1)
        texto_lectura.config(state=tk.DISABLED)
        boton = tk.Button(t1,text="Cerrar", command=t1.destroy)
        boton.grid(row=1, column=1)
        t1.wait_window(t1)
        
    def acerca_de(self):
        MessageBox.showinfo("Acerca de", "ASSEMBLER\n\nversion: 1.0\nfecha: 06.10.2020\npython: 3.8\ntkinter: 8.6" )
    
    def increase_text_font(self, event):
        fontsize = self.text_font['size'] 
        self.text_font.configure(size=fontsize+2)
    
    def decrease_text_font(self, event):
        fontsize = self.text_font['size'] 
        self.text_font.configure(size=fontsize-2)
    
    def abrir_archivo(self, event=True):
        files = [("ass","*.ass"), ("Archivos de texto","*.txt"), ('All Files', '*.*')]
        archivo = filedialog.askopenfilename(title="Abrir", filetypes=files)
        if archivo != '' and archivo != ():
            self.text_01.delete('1.0', tk.END)
            self.text_02.delete('1.0', tk.END)
            self.text_03.delete('1.0', tk.END)
            texto = open(archivo, "r")
            for linea in texto.readlines():
                self.text_01.insert(tk.INSERT, linea)
        self.marcar_error()

    def guardar_archivo(self, event=True):
        files = [("out","*.out")]
        archivo = filedialog.asksaveasfilename(title="Guardar", filetypes=files)
        if archivo != '' and archivo != ():
            save = open(archivo, "w")
            contenido = self.text_02.get("1.0",'end-1c')
            save.write(contenido)
            save.close()
            save = open(archivo[:-4]+".mem", "w")
            contenido = self.text_03.get("1.0",'end-1c')
            save.write(contenido)
            save.close()
            save = open(archivo[:-4]+".ass", "w")
            contenido = self.text_01.get("1.0",'end-1c')
            save.write(contenido)
            save.close()
            
    def marcar_error(self, event=True):
        self.text_02.delete('1.0', tk.END)
        self.text_03.delete('1.0', tk.END)
        texto = self.text_01.get("1.0",'end-1c')
        
        contenido = separar(texto)
        data = contenido[1][:-1]
        code = contenido[0]
        variables, pos_textbox, lineas = buscar_data(data,self.text_01)
        respuesta = buscar_code(code, variables, pos_textbox, self.text_01, lineas)
        MessageBox.showinfo("Revision", "Se han detectado:\n- {correcto} lineas validas\n- {incorrecto} errores".format(correcto=respuesta[3][0], incorrecto=respuesta[3][1]))
    
    def assembler(self, event=True):
        self.text_02.delete('1.0', tk.END)
        self.text_03.delete('1.0', tk.END)
        texto = self.text_01.get("1.0",'end-1c')
        
        contenido = separar(texto)

        data = contenido[1][:-1]
        code = contenido[0]
        
        variables, pos_textbox, lineas = buscar_data(data, self.text_01, self.text_03)
        respuesta = buscar_code(code, variables, pos_textbox, self.text_01, lineas)
        instrucciones_texto , inst, literales = respuesta[0], respuesta[1], respuesta[2]
        
        ordenado = sorted(inst.items(), key=operator.itemgetter(0), reverse=True)
        if respuesta[3][1] == 0: # No hay errores
            for codigo in ordenado: #inst = {"MOV A,B": "0000000", "MOV B,A": "0000001"}
                instrucciones_texto = instrucciones_texto.replace(codigo[0], inst[codigo[0]])
            for lit in literales:
                instrucciones_texto = instrucciones_texto.replace("Lit", lit, 1)
            
            instrucciones_texto = instrucciones_texto.replace(" ", "")
            instrucciones_texto = instrucciones_texto.replace("\t", "")
            instrucciones_texto = instrucciones_texto.split()
            largo = len(instrucciones_texto)
            instrucciones_texto = "\n".join(instrucciones_texto)
            MessageBox.showinfo("El archivo .out", "El archivo de salida contiene {lineas} lineas".format(lineas=largo))
            self.text_02.insert(tk.INSERT, instrucciones_texto)
        else:
            self.text_03.delete('1.0', tk.END)
            MessageBox.showerror("Error Archivo", "El archivo no se puede ejecutar\n- contiene {errores} erroes".format(errores=respuesta[3][1]))

if __name__ == "__main__":
    MainApp().mainloop()