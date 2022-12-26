
from tkinter import *
from tkinter import messagebox, filedialog, scrolledtext, ttk, WORD
import os

from .Analisis_lexico.analisis_lexico import MyLex
#from .Interprete.AnalisadorLexicoYSintactico import LexicoSintactico

# RUTAICONOS SE ENCUENTRA EN EL ARCHIVO __init__.py EN LA CARPETA ICONOS
from .assets.Iconos import RUTAICONOS

# Declaramos la ventana donde se mostrara todo el programa
ventana = Tk()
ventana.title("Proyecto COMPI2 - DIC 2022")
ventana.resizable(0,0)
# ? Color de fondo de la ventana
ventana.config(bg='blue')
# ? Dimensionamos la ventana
ventana.geometry("1500x650")
# variable donde estara guardado el path del archivo
archivo = ""
# Contador para la posicion actual de la columna



# FUNCIONES DE INTERFAZ --------------------------------------------------------------------------------------------------------------------
# FUNCIONALES  -----------------------------------------------------------------------------------------------------------------------------
def Salir():  # SALIR DEL PROGRAMA

    value = messagebox.askokcancel(
        "Salir", "Desea salir de la aplicacion? \n **Se perdera todo lo que no se haya guardado**")
    if value:
        ventana.destroy()

def CrearNuevoArchivo():  # NUEVO ARCHIVO
    global archivo
    TextArea1.delete(1.0, END)
    archivo = ""
    PosicionCursor()

def AbrirArchivo():  # ABRIR ARCHIVO
    global archivo
    archivo = filedialog.askopenfilename(
        title="Abrir Archivo", initialdir="C:/")

    entrada = open(archivo, encoding="utf8")
    content = entrada.read()

    TextArea1.delete(1.0, END)

    TextArea1.insert(1.0, content)

    entrada.close()

    TextArea2.config(state=NORMAL)
    TextArea2.delete(1.0, END)
    TextArea2.config(state=DISABLED)
    Pintar()

def GuardarArchivo():  # GUARDAR
    global archivo
    if archivo == "":
        GuardarComo()
    else:
        guardarc = open(archivo, "w", encoding="utf8")
        guardarc.write(TextArea1.get(1.0, END))
        guardarc.close()

def GuardarComo():  # GUARDAR COMO
    global archivo
    guardar  = filedialog.asksaveasfilename(title="Guardar Archivo", initialdir="C:/")
    fguardar = open(guardar, "w+", encoding="utf8")
    fguardar.write(TextArea1.get(1.0, END))
    fguardar.close()
    archivo = guardar

def Info(): # INFORMACION MIA
    messagebox.showinfo(title="Informacion",
                        message="Frederick Jonathan Faugier Pinto 201602842")


# FUNCIONALES REPORTES  ----------------------------------------------------------------------------------------------------------------------


def openPDF(ruta): # ABRE PDFs
    # ABRIRI UN PDF
    dirname = os.path.dirname(__file__)
    direcc = os.path.join(dirname, ruta)
    os.startfile(direcc)

def AbrirReporteErroes():
    ruta = os.path.abspath(
        os.getcwd())+"\\PROYECTO\\Analizador\\Reportes\\Errores\\Errores.dot.pdf"
    openPDF(ruta)

def AbrirReporteAST():
    ruta = os.path.abspath(
        os.getcwd())+"\\PROYECTO\\Analizador\\Reportes\\AST\\AST.dot.pdf"
    openPDF(ruta)

def AbrirReporteTablaSimbolos():
    ruta = os.path.abspath(
        os.getcwd())+"\\PROYECTO\\Analizador\\Reportes\\Tabla_Simbolos\\Tabla_Simbolos.dot.pdf"
    openPDF(ruta)


# LINEA Y COLUMNA  ----------------------------------------------------------------------------------------------------------------------------

def lineas(*args):  #* ACTUALIZAR LINEAS
    lines.delete("all")
    cont = TextArea1.index("@1,0")
    while True:
        dline = TextArea1.dlineinfo(cont)
        if dline is None:
            break
        y = dline[1]

        strline = str(cont).split(".")[0]
        lines.create_text(2, y, anchor="nw", text=strline,
                          font=("Arial", 14), fill='white')

        cont = TextArea1.index("%s+1line" % cont)

def PosicionCursor(*args):  #* ACTUALIZAR POSICION
    posicionactual = TextArea1.index(INSERT)
    Linea          = str(posicionactual.split(".")[0])
    Columna        = str(posicionactual.split(".")[1])
    Cursor         = "Ln:" + Linea+", Col:" + Columna
    pos.config(text=Cursor)
    lineas()
    

def Pintar(*args):
    indiceactual    = TextArea1.index(INSERT)
    analizarypintar = MyLex()
    input           = TextArea1.get(1.0, END)
    if len(input) < 1:
        return

    lista = analizarypintar.Lista_de_Tokens(input)
    TextArea1.delete(1.0, END)
    if len(lista) > 0:
        if lista[len(lista)-1][1] == '\n':
            lista.pop(len(lista)-1)
    for s in lista:

        TextArea1.insert(END, s[1])
        TextArea1.tag_add(str(s[0]), "insert - "+str(len(s[1]))+"c", "insert")

    TextArea1.mark_set("insert", indiceactual)
    TextArea1.see(indiceactual)

    PosicionCursor()


# FUNCIONES ANALIZADOR - INTERPRETAR ------------------------------------------------------------------------------------------------

def Interpretar():
    
    input = TextArea1.get(1.0, END)
    if len(input) < 1:
        return
    #? HABILITAMOS PARA ESCRIBIR EN LA CONSOLA
    TextArea2.config(state=NORMAL)
    #? ELIMINASMOS LO QUE SE TENGA ESCRITO
    TextArea2.delete(1.0, END)
    #? LLAMAMOS A LA CLASE QUE REALIZARA EL ANALISIS 
    
    #Analizador = LexicoSintactico()
    
    Consola = Analizador.Analizar(input)

   
    # INSERTAMOS EL NUEVO MENSAJE EN LA CONSOLA
    TextArea2.insert(END, Consola.getConsola())
    # MOVEMOS EL CURSOR AL FINAL DE LA CONSOLA
    TextArea2.mark_set(INSERT, END)
    TextArea2.see(INSERT)
    # DESHABILITAMOS PARA QUE NO SE PUEDA MODIFICAR
    TextArea2.config(state=DISABLED)
    

#? DECLARAMOS LOS LABELS

pos = ttk.Label(ventana, text="Ln:1,  Col:0", font=(    "Arial", 12), background='gray7', foreground='white')
pos.place(x=50, y=625)

Label1 = Label(text="Consola", font=("Arial", 15), bg="Gray",               background='gray7', foreground='white')
Label1.grid(column=2, row=1)
Label2 = Label(text="Editor de Codigo", font=("Arial", 15),               bg="Gray", background='gray7', foreground='white')
Label2.grid(column=1, row=1)

#? DECLARAMOS LAS AREAS DE TEXTO
TextArea1 = scrolledtext.ScrolledText(ventana, wrap=NONE, undo=True, width=70, height=30, font=(
    "Courier New", 12), bg='gray9', fg='white', insertbackground="white")
TextArea1.grid(column=1, row=3, pady=25, padx=0)
TextArea1.focus()

TextArea2 = scrolledtext.ScrolledText(ventana, wrap=NONE, state=DISABLED, width=70,
                                      height=30, background='black', fg='light green', font=("Courier New", 12, "bold"))
TextArea2.grid(column=2, row=3, pady=25, padx=0)

#?   DECLARAMOS LOS CANVAS
lines = Canvas(ventana, width=35, height=550,
               bg='gray15', highlightthickness=0)
lines.grid(column=0, row=3)

#? DECLARAMSO LOS SCROLLBAR
ScroBar1 = Scrollbar(ventana, orient=HORIZONTAL)
ScroBar1.place(x=40, y=600, width=700)
ScroBar1.config(command=TextArea1.xview)
TextArea1.config(xscrollcommand=ScroBar1.set)

ScroBar2 = Scrollbar(ventana, orient=HORIZONTAL)
ScroBar2.place(x=760, y=600, width=700)
ScroBar2.config(command=TextArea2.xview)
TextArea2.config(xscrollcommand=ScroBar2.set)

#? DECLARAMOS LOS BOTONES
Buttom1 = Button(ventana, width=15, height=1, text="Next Debug",
                 bg='gray10', fg='white', font=("Arial", 12))
Buttom1.place(x=600, y=15)

#! FUNCIONALIDADES EN EL TECLADO
TextArea1.bind('<<Change>>', PosicionCursor)
TextArea1.bind('<Motion>', PosicionCursor)
TextArea1.bind('<Button-1>', PosicionCursor)
TextArea1.bind('<KeyRelease>', Pintar)

#! SECCION REGLAS PARA PINTAR
TextArea1.tag_config('CADENA', foreground='dark orange')
TextArea1.tag_config('CARACTER', foreground='dark orange')
TextArea1.tag_config('COMENTARIO_SIMPLE', foreground='gray57')
TextArea1.tag_config('COMENTARIO_MULTILINEA', foreground='gray57')
TextArea1.tag_config('ENTERO', foreground='DarkOrchid2')
TextArea1.tag_config('DECIMAL', foreground='DarkOrchid2')
TextArea1.tag_config('ID', foreground='light goldenrod')
PalabrasReservadas = ['VAR', 'INT', 'DOUBLE', 'CHAR', 'STRING', 'TRUE', 'FALSE', 'NULL', 'IF', 'ELSE', 'WHILE', 'FOR', 'PRINT', 'SWITCH',
                      'CASE', 'BREAK', 'DEFAULT', 'CONTINUE', 'RETURN', 'FUNC', 'READ', 'TOLOWER', 'TOUPPER', 'LENGTH', 'TRUNCATE', 'ROUND', 'TYPEOF', 'MAIN','NEW']
for reservada in PalabrasReservadas:
    TextArea1.tag_config(reservada, foreground='dodger blue')

#! SECCION DEL MENU
#? IMAGENES PARA LOS ICONOS DE LAS OPCIONES
rutaICONOS        = RUTAICONOS+"\\"
Icon_CrearArchivo = PhotoImage(file=rutaICONOS+"CrearArchivo.png")
Icon_AbrirArchivo = PhotoImage(file=rutaICONOS+"AbrirArchivo.png")
Icon_Guardar      = PhotoImage(file=rutaICONOS+"Guardar.png")
Icon_GuardarComo  = PhotoImage(file=rutaICONOS+"GuardarComo.png")
Icon_Salir        = PhotoImage(file=rutaICONOS+"Salir.png")

#* MENUBAR
menubar = Menu(ventana, background='gray7', foreground='white',
               activebackground='gray8', activeforeground='white')
ventana.config(menu=menubar)

#* SUBMENU ARCHIVO
MenuArchivo = Menu(menubar, tearoff=0, background="gray7", foreground="white")
menubar.add_cascade(label="Archivo", menu=MenuArchivo)
MenuArchivo.add_command(label="Crear Archivo", image=Icon_CrearArchivo,
                        compound='left', command=CrearNuevoArchivo)
MenuArchivo.add_command(label="abrir Archivo",
                        image=Icon_AbrirArchivo, compound='left', command=AbrirArchivo)
MenuArchivo.add_separator()
MenuArchivo.add_command(label="Guardar", image=Icon_Guardar,
                        compound='left', command=GuardarArchivo)
MenuArchivo.add_command(
    label="Guardar Como", image=Icon_GuardarComo, compound='left', command=GuardarComo)
MenuArchivo.add_command(label="Salir", image=Icon_Salir,
                        compound='left', command=Salir)

#* SUBMENU HERRAMIENTAS
MenuHerramientas = Menu(
    menubar, tearoff=0, background="gray7", foreground="white")
menubar.add_cascade(label="Herramientas", menu=MenuHerramientas)
MenuHerramientas.add_command(label="Interpretar", command=Interpretar)
MenuHerramientas.add_command(label="Debuguer")

#* SUBMENU REPORTES
MenuReportes = Menu(menubar, tearoff=0, background="gray7", foreground="white")
menubar.add_cascade(label="Reportes", menu=MenuReportes)
MenuReportes.add_command(label="Errores", command=AbrirReporteErroes)
MenuReportes.add_command(label="AST",command=AbrirReporteAST)
MenuReportes.add_command(label="Tabla de simbolos",command=AbrirReporteTablaSimbolos)

#* SUBMENU AYUDA
MenuAyuda = Menu(menubar, tearoff=0, background="gray7", foreground="white")
menubar.add_cascade(label="Ayuda", menu=MenuAyuda)
MenuAyuda.add_command(label="Manual de Usuario")
MenuAyuda.add_command(label="Manual Tecnico")
MenuAyuda.add_command(label="Info", command=Info)
#! TERMINA SECCION DEL MENU


ventana.mainloop()
