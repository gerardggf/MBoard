from tkinter import *
from tkinter import ttk, messagebox
import tkinter, math, sys, os
import db, cnivel 

############################
proyecto= "MBoard"
color= "orange"
filas=18 #18
columnas=11 #11
############################

#globales
fuente= round(15 * 15/((filas+columnas+3)/2))

heightBoard = str(600) #600
widthBoard = str(400) #400
heightRaiz = str(600) #600
widthRaiz = str(700) #700

height = filas+1
width = columnas+1
total= filas*columnas

presasInicio=0
presasRuta=0
presasTop=0
estado="inicio"

inicioArray= []
rutaArray= []
topArray= []

maxColumnas=40
maxFilas=70

maxPresasRuta=15

visor=False


def main():

    db.creardb()

    raiz=Tk()
    raiz.title(proyecto + " - Configurador de ruta")
    raiz.resizable(0,0)
    raiz.geometry(widthRaiz + "x" + heightRaiz + "+610+200")
    raiz.config(bg = color)

    def inicios():
        global estado
        estado="inicio"
    def rutas():
        global estado
        estado="ruta"
    def tops():
        global estado
        estado="top"



    # BORRAR / REHACER RUTA EXISTENTE ---------------------------------------------------------------------------------------------------------

    def rehacer():
        global presasInicio, presasRuta, presasTop, presas, estado
        presasInicio=0
        presasRuta=0
        presasTop=0
        presas= 0

        t=IntVar()
        t.set(00)
        labelPInicio = tkinter.Label(viaFrame, textvariable= t, font=("Arial", 16))
        labelPInicio.grid(row = 2, column = 0, sticky="nsew")

        labelPRuta = tkinter.Label(viaFrame, textvariable= t, font=("Arial", 16))
        labelPRuta.grid(row = 2, column = 1, sticky="nsew")
    
        labelPTop = tkinter.Label(viaFrame, textvariable= t, font=("Arial", 16))
        labelPTop.grid(row = 2, column = 2, sticky="nsew")

        canvas.delete("all")
        crearBoard()
        estado="inicio"
        inicioArray.clear()
        rutaArray.clear()
        topArray.clear()

        nombreEntry.delete(0, END)
        nombreEntry.insert(0, "")
        nivelEntry.delete(0, END)
        nivelEntry.insert(0, "")


    # CREAR NUEVA RUTA --------------------------------------------------------------------------------------------------------------------------------------------  

    def crear():

        msgnombre= ""
        msgnivel = ""
        msginicio = ""
        msgruta = ""
        msgtop = ""

        if(len(nombre.get())==0):
            msgnombre = "El nombre no puede estar vacío. "

        if(len(nivel.get())==0):
            msgnivel = "El nivel no puede estar vacío. "

        if(len(inicioArray)<1):
            msginicio = "Tiene que haber almenos una presa de incio. "
        
        if(len(rutaArray)<2):
            msgruta = "Tienen que haber almenos dos presas de ruta. "

        if(len(topArray)<1):
            msgtop = "Tiene que haber almenos una presa de Top. "

        if(msgnombre!="") and (msgnivel!="") and(msginicio!="") and(msgruta!="") and(msgtop!=""):
            messagebox.showinfo( message = "Tienes que poner las presas e indicar los datos que se piden", title="Error de creación")
        elif(len(nombre.get())==0) or (len(nivel.get())==0) or (len(inicioArray)<1) or (len(rutaArray)<2) or (len(topArray)<1):
            messagebox.showinfo( message = msgnombre + msgnivel + msginicio + msgruta + msgtop, title="Falta información")

        else:
            db.creardb()  
            db.insertardb( str(nombre.get()), str(nivel.get()), '-'.join(inicioArray), '-'.join(rutaArray), '-'.join(topArray), width-1, height-1, desplome.get())
            print("\t-----------------------------------------------------------------------------------------------")
            print("\n\t - Registro creado")
            db.consulta()
            db.imprimir()
            actualizarListBox()
            rehacer()


    # ACTUALIZAR LISTBOX ----------------------------------------------------------------------------------------------------------------------------------------------------

    def actualizarListBox():
        lista.delete('0','end')
        items=db.items
        for item in items:
            if(item[7]==11) and (item[8]==18):
                lista.insert(END, "  " + str(item[0]) + " - " + item[1] + " - " + item[2])
            else:
                lista.insert(END, "  " + str(item[0]) + " - " + item[1] + " - " + item[2] + "   (" + str(item[7]) + "x" + str(item[8]) + ")")



    # TÍTULO ----------------------------------------------------------------------------------------------------------------------------------------------------------------

    creacerFrame=Frame(raiz)
    creacerFrame.config(bg=color)
    creacerFrame.grid(row=0,column=0, rowspan=2, padx=15, pady=15, sticky="nsew")

    proyectoLabel = Label(creacerFrame, bg=color, text = proyecto, font=("Arial", 20))
    proyectoLabel.grid(row=0,column=0, sticky="nsew")


    # REHACER Y CREAR -----------------------------------------------------------------------------------------------------


    botonCrear=ttk.Button(creacerFrame, text="Crear", command= crear)
    botonCrear.grid(column=0, row=1, padx=10, pady=20, ipadx=10, ipady=5, sticky="nsew")

    botonRehacer=ttk.Button(creacerFrame, text="Rehacer", command= rehacer)
    botonRehacer.grid(column=0, row=2, padx=15, pady=5, ipadx=5, ipady=4, sticky="nsew")


    # NOMBRE Y NIVEL -------------------------------------------------------------------------------------------------------------------

    datosYviaFrame= Frame(raiz)
    datosYviaFrame.config(bg=color)
    datosYviaFrame.grid(row=0,column=1, columnspan=3, rowspan=2, sticky="n")

    nombre=StringVar()
    nivel=StringVar()

    datosFrame=ttk.LabelFrame(datosYviaFrame, text = "Datos")
    datosFrame.grid(row=0,column=1, columnspan=3, ipady=10, padx=5,pady=10)
    ##
    nombreLabel = Label(datosFrame, text = 'Nombre', font=("Arial", 10))
    nombreLabel.grid(row=0,column=0, padx=5, pady=10)
    
    nombreEntry = Entry(datosFrame, textvariable=nombre, font=("Arial", 10), width=15)
    nombreEntry.grid(row=0,column=1, padx=5, pady=10)

    nivelLabel = Label(datosFrame, text = 'Nivel', font=("Arial", 10))
    nivelLabel.grid(row=0,column=2, padx=5, pady=10)

    nivelEntry = ttk.Combobox(datosFrame, textvariable=nivel, font=("Arial", 10), width=5)
    nivelEntry.grid(row=0,column=3, padx=5, pady=10)
    
    opciones=[
        "III", "IV", "V", "V+", 
        "6A", "6A+", "6B", "6B+", "6C", "6C+", 
        "7A", "7A+", "7B", "7B+", "7C", "7C+", 
        "8A", "8A+", "8B", "8B+", "8C", "8C+", 
        "9A", "9A+", "9B", "9B+", "9C", "9C+"
    ]
    nivelEntry['values']=opciones



    # VIA --------------------------------------------------------------------------------------------------------------------------

    viaFrame= ttk.LabelFrame(datosYviaFrame, text="Via")
    viaFrame.grid(row=1, column=1, columnspan=3)  
    ##
    botonInicio=ttk.Button(viaFrame, text="Inicio", command=inicios)
    botonInicio.grid(column=0, row=0, padx=10, pady=5)

    botonRuta=ttk.Button(viaFrame, text="Ruta", command= rutas)
    botonRuta.grid(column=1, row=0, padx=10, pady=5)

    botonTop=ttk.Button(viaFrame, text="Top", command= tops)
    botonTop.grid(column=2, row=0, padx=10, pady=5)
    ##

    t=IntVar()
    t.set(presasInicio)
    labelPInicio = tkinter.Label(viaFrame, textvariable= t, font=("Arial", 16))
    labelPInicio.grid(row = 2, column = 0, sticky="nsew")
    
    t.set(presasRuta)
    labelPRuta = tkinter.Label(viaFrame, textvariable= t, font=("Arial", 16))
    labelPRuta.grid(row = 2, column = 1, sticky="nsew")
    
    t.set(presasTop)
    labelPTop = tkinter.Label(viaFrame, textvariable= t, font=("Arial", 16))
    labelPTop.grid(row = 2, column = 2, sticky="nsew")



    # LISTBOX ----------------------------------------------------------------------------------------------------------

    listaFrame=ttk.LabelFrame(raiz, text = "Rutas")
    listaFrame.grid(row=2,column=0, padx=10, pady=10, columnspan=4, rowspan=3, sticky="n")

    def curSelec(event):
        
        global idBoC, index, visor,valor2
        try:
            visor=True

            selec=lista.curselection()
            index=selec[0]
            valor=lista.get(index)
            valor2=valor.split(" - ")
            idBoC=int(valor2[0])
            db.consultaVisor(idBoC)
            infoVia()
            precalc()
        except:
            print("\t x Ahora no tienes ningún registro seleccionado en la Listbox")

    lista= Listbox(listaFrame,  font=("Arial", 12))
    lista.bind('<<ListboxSelect>>',curSelec)
    lista.grid(row=0,column=0, padx=10, ipadx=120, ipady=75, columnspan=4)

    print("\t - Base de datos " + proyecto)
    db.consulta()
    db.imprimir()
    actualizarListBox()


    # BORRAR UN REGISTRO DE LA BBDD ---------------------------------------------------------------------------------------------------------------

    def borrar():
        try:
            respuesta= messagebox.askyesno(message="¿Seguro que quieres borrar la ruta '" + str(idBoC) + "'?", title="Borrar registro")
            
            if(respuesta):
                try:
                    db.borrardb(idBoC)
                
                    print("\t - Registro " + str(idBoC) + " borrado correctamente")

                    db.consulta
                    actualizarListBox()
                except:
                    print("\t x Ya está borrada la ruta seleccionada")
        except:
            print("x - No hay ninguna ruta seleccionada")

    botonBorrar=ttk.Button(listaFrame, text="Borrar registro", command= borrar)
    botonBorrar.grid(row=1, column=0, padx=10, pady=5)



    # CARGAR UN REGISTRO DESDE LA BBDD -------------------------------------------------------------------------------------------

    def cargar():
        if(visor==False):
            print("\t x No hay ninguna ruta seleccionada")
        else:
            crearBoardVisor()

    botonCargar=ttk.Button(listaFrame, text="Cargar registro", command= cargar)
    botonCargar.grid(row=1, column=1, padx=10, pady=5)



    # CALCULAR NIVEL -----------------------------------------------------------------------------------------------------------------------

    def precalc():
        try:
            cnivel.calcular(idBoC)
            nivelAprox= str(cnivel.nivelAprox)

            calcularLabel = Label(listaFrame, text = "Nivel aproximado: " + nivelAprox, font=("Arial", 10))
            calcularLabel.grid(row=1,column=3, padx=5, pady=5, columnspan=2, sticky="nsew")

        except:
            print("\t x No funciona")



    #-----------------------------------------------------------------------------------------------------------------------------------------------

    dimEincFrame=Frame(raiz)
    dimEincFrame.config(bg=color)
    dimEincFrame.grid(row=0,column=4, padx=10, pady=10, sticky="ne", rowspan=4)

    # DIMENSIONES --------------------------------------------------------------------------------------------------------

    def cMedidaNormal():
        global width, height,fuente, maxPresasRuta
        width=12
        height=19
        fuente= round(15 * 15/((width+height+2)/2))
        print("\t - Dimensiones cambiadas a: " + str(width-1) + " " + str(height-1))
        rehacer()
        maxPresasRuta=9
        boardInclinacion()

    def cMedidas():
        global width, height,fuente, maxFilas, maxColumnas, maxPresasRuta
        try:
            width= eColumnas.get()+1
            height= eFilas.get()+1
            if(width-1>maxColumnas) or (height-1>maxFilas):
                messagebox.showinfo(message= "El número de columnas y/o filas tiene que ser más pequeño", title="Cambio medidas tablero")
            else:
                fuente= round(15 * 15/((width+height+2)/2))
                print("\t - Dimensiones cambiadas a: " + str(width-1) + " " + str(height-1))
                rehacer()
                if(height-1 > 25):
                    maxPresasRuta=40
                boardInclinacion()
        except:
            messagebox.showinfo(message = "Introduce números", title="Cambio medidas tablero")
   

    eColumnas = IntVar()
    eFilas = IntVar()
    eColumnas.set(11)
    eFilas.set(18)

    tablaFrame=ttk.LabelFrame(dimEincFrame, text = "Tabla")
    tablaFrame.grid(row=0,column=0, padx=5, pady=10)
    ##
    columnLabel = Label(tablaFrame, text = 'Columnas', font=("Arial", 10))
    columnLabel.grid(row=0,column=0, padx=5, pady=5)
    
    columnEntry = ttk.Combobox(tablaFrame, textvariable= eColumnas, font=("Arial", 10), width=5)
    columnEntry.grid(row=0,column=1, padx=5, pady=5)

    filasLabel = Label(tablaFrame, text = 'Filas', font=("Arial", 10))
    filasLabel.grid(row=1,column=0, padx=5, pady=5)

    filasEntry = ttk.Combobox(tablaFrame, textvariable= eFilas, font=("Arial", 10), width=5)
    filasEntry.grid(row=1,column=1, padx=5, pady=5)

    botonCambiarNormal=ttk.Button(tablaFrame, text="11 x 18", command= cMedidaNormal)
    botonCambiarNormal.grid(row=2, column=0, padx=10, pady=10)

    botonCambiar=ttk.Button(tablaFrame, text="Cambiar", command= cMedidas)
    botonCambiar.grid(row=2, column=1, padx=10, pady=10)

    col=[]
    for i in range(maxColumnas):
        col.append(i+1)
    columnEntry['values']=col
    fil=[]
    for i in range(maxFilas):
        fil.append(i+1)
    filasEntry['values']=fil



    # INCLINACIÓN -------------------------------------------------------------------------------------------------------------------------

    desplome = IntVar()
    desplome.set(0)

    def boardInclinacionVisor():
        canvasVisor.create_rectangle(0, 0, int(widthBoard)/widthV, int(heightBoard)/heightV, fill="white")
        canvasVisor.create_text(0 + int(widthBoard)/widthV/2, 0 + int(heightBoard)/heightV/2, text=str(viaVisor[9][:-2]) + "º", font="Arial " + str(fuente))

    def boardInclinacion():
        canvas.create_rectangle(0, 0, int(widthBoard)/width, int(heightBoard)/height, fill="darkorange2")
        canvas.create_text(0 + int(widthBoard)/width/2, 0 + int(heightBoard)/height/2, text=str(desplome.get()) + "º", font="Arial " + str(fuente))

    def aplicarDesplomeNormal():
        desplome.set(0)
        print(desplome.get())
        boardInclinacion()

    def aplicarDesplome():
        print(desplome.get())
        boardInclinacion()


    desplomeFrame=ttk.LabelFrame(dimEincFrame, text = "Grado de inclinación")
    desplomeFrame.grid(row=1,column=0, padx=5, pady=10)
    ##
    desplomeLabel = Label(desplomeFrame, text = 'Desplome (en º)', font=("Arial", 10))
    desplomeLabel.grid(row=0,column=0, padx=5, pady=5)
    
    desplomeEntry = ttk.Combobox(desplomeFrame, textvariable= desplome, font=("Arial", 10), width=5)
    desplomeEntry.grid(row=0,column=1, padx=5, pady=5)

    botonCambiar=ttk.Button(desplomeFrame, text="0º", command= aplicarDesplomeNormal)
    botonCambiar.grid(row=1, column=0, padx=10, pady=10)

    botonCambiar=ttk.Button(desplomeFrame, text="Cambiar", command= aplicarDesplome)
    botonCambiar.grid(row=1, column=1, padx=10, pady=10)

    inclinacion=[
        "0", "5", "10", "15", "20", "25", "30", "35", "40", "45", 
        "50", "55", "60", "65", "70", "75", "80"
    ]
    desplomeEntry['values']=inclinacion


    # INFORMACIÓN VIA ------------------------------------------------------------------------------------------------------------------------

    def infoVia():
        viaVisor= str(db.itemsVisor).split(", ")
        infoNombre= viaVisor[1].replace("'", "")
        infoFecha= viaVisor[3].replace("'", "")
        infoId= viaVisor[0][-2:].replace("(", "")

        infoFrame = ttk.LabelFrame(dimEincFrame, text = "Información ruta")
        infoFrame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        ##
        if(len(infoNombre)<=17):
            infoLabel1 = Label(infoFrame, text = 
                "- ID: " +
                infoId + 
                "\n- Nombre: " +
                infoNombre + 
                "\n- Dimensiones: " +
                viaVisor[7] + "x" + viaVisor[8] +
                "\n- Fecha: " + 
                infoFecha +
                "\n- Inclinación: " + 
                str(viaVisor[9][:-2]) + "º"
            , font=("Arial", 10), justify=LEFT)
        else:
            infoLabel1 = Label(infoFrame, text = 
                "- ID: " +
                infoId + 
                "\n- Nombre: " +
                infoNombre[:17] + "..." + 
                "\n- Dimensiones: " +
                viaVisor[7] + "x" + viaVisor[8]+
                "\n- Fecha: " + 
                infoFecha +
                "\n- Inclinación: " + 
                str(viaVisor[9][:-2]) + "º"
            , font=("Arial", 10), justify=LEFT)

        infoLabel1.grid(row=0,column=0, padx=5, pady=10)

    # INSTRUCCIONES -----------------------------------------------------------------------------------------------------------------------
    
    def instrucciones():
        os.startfile("Instrucciones.pdf")

    botonInstrucciones= ttk.Button(raiz, text="Instrucciones", command= instrucciones)
    botonInstrucciones.grid(row=4, column=4, padx=5, pady=5, ipadx=30, ipady=10)

    # CREAR VENTANA BOARD ----------------------------------------------------------------------------------------------------------------
    
    global canvas

    board=Tk()
    board.title("Creador de rutas")
    board.iconbitmap('./icono.ico')
    board.resizable(0,0)
    board.geometry(widthBoard + "x" + heightBoard + "+200+200")

    canvas = Canvas(board, width=widthBoard, height=heightBoard, bg='white')
    canvas.pack(expand=YES, fill=BOTH)
    canvas.pack()

    def crearBoard():

        for i in range(height): #filas
            for j in range(width): #columnas
                canvas.create_line(int(widthBoard)/width*j,0,int(widthBoard)/width*j,int(heightBoard))
                canvas.create_line(0, int(heightBoard)/height*i, int(widthBoard), int(heightBoard)/height*i)     

        canvas.create_rectangle(0, int(heightBoard)/height, int(widthBoard)/width, int(heightBoard), fill=color)
        canvas.create_rectangle(int(widthBoard)/width, 0, int(widthBoard), int(heightBoard)/height, fill=color)
        canvas.create_rectangle(0, 0, int(widthBoard)/width, int(heightBoard)/height, fill=color)

        for i in range(height): #filas
            canvas.create_text(int(widthBoard)/width - int(widthBoard)/width/2 ,int(heightBoard)/height*i + int(heightBoard)/height/2, text=i, font="Arial " + str(fuente)) 

        for i in range(width): #columnas
            canvas.create_text(int(widthBoard)/width*i + int(widthBoard)/width/2,int(heightBoard)/height - int(heightBoard)/height/2, text=i, font="Arial " + str(fuente))

        boardInclinacion()

    crearBoard()
    


    # ENVIAR A ARRAY --------------------------------------------------------------------------------------------------------------------------------------------

    def enviar(event):
       
        global inicioArray, rutaArray, topArray

        col= math.trunc(width* event.x/ int(widthBoard))
        if(len(str(col))==1):
            col="0" + str(col)
        fila= math.trunc(height* event.y/ int(heightBoard)) 
        if(len(str(fila))==1):
            fila="0" + str(fila)
    
        if(estado=="inicio"):
            inicioArray.append(str(fila) + str(col))
        if(estado=="ruta"):
            rutaArray.append(str(fila) + str(col))
        if(estado=="top"):
            topArray.append(str(fila) + str(col))



    # GUARDAR PRESAS E INFO --------------------------------------------------------------------------------------------------------------------------------------------

    def guardar(event):
        x= math.trunc(width* event.x/ int(widthBoard))
        y= math.trunc(height* event.y/ int(heightBoard))
        
        global presasInicio, presasRuta, presasTop, canvas, estado, celdaInici, celdaRuta, celdaTop

        if(estado):

            if(event.x > int(widthBoard)/width) and (event.y > int(heightBoard)/height) and (estado=="inicio") and (presasInicio<2):
                celdaInici= canvas.create_rectangle(int(widthBoard)/width*(x) , int(heightBoard)/height*(y) , int(widthBoard)/width*(x+1) , int(heightBoard)/height*(y+1) , fill='green')
                presasInicio=presasInicio+1

                t=IntVar()
                t.set(presasInicio)
                label1 = tkinter.Label(viaFrame, textvariable= t, font=("Arial", 16))
                label1.grid(row = 2, column = 0)

                enviar(event)       
 

            if(event.x > int(widthBoard)/width) and (event.y > int(heightBoard)/height) and (estado=="ruta") and (presasRuta<maxPresasRuta):
                celdaRuta= canvas.create_rectangle(int(widthBoard)/width*(x) , int(heightBoard)/height*(y) , int(widthBoard)/width*(x+1) , int(heightBoard)/height*(y+1) , fill='deep sky blue')
                presasRuta=presasRuta+1

                t=IntVar()
                t.set(presasRuta)
                label2 = tkinter.Label(viaFrame, textvariable= t, font=("Arial", 16))
                label2.grid(row = 2, column = 1)

                enviar(event)                
                

            if(event.x > int(widthBoard)/width) and (event.y > int(heightBoard)/height) and (estado=="top") and (presasTop<2):
                celdaTop= canvas.create_rectangle(int(widthBoard)/width*(x) , int(heightBoard)/height*(y) , int(widthBoard)/width*(x+1) , int(heightBoard)/height*(y+1) , fill='red')
                presasTop=presasTop+1

                t=IntVar()
                t.set(presasTop)
                label3 = tkinter.Label(viaFrame, textvariable= t, font=("Arial", 16))
                label3.grid(row = 2, column = 2)

                enviar(event)
                
            
            if(estado=="inicio"):
                if(presasInicio==2):
                        estado="ruta"

            if(estado=="ruta"):
                if(presasRuta==maxPresasRuta):
                        estado="top"
            

        else:
            print("\t X Error")


    canvas.bind('<Button-1>', guardar)



    # DESHACER CREACIÓN DE UNA PRESA

    # def deshacer(event):
    #     x= math.trunc(width* event.x/ int(widthBoard))
    #     y= math.trunc(height* event.y/ int(heightBoard))
    #     print(str(x) + " " + str(y))

    # canvas.bind('<Button-3>', deshacer)



    # CREAR BOARD PARA VISUALIZAR RUTAS YA GUARDADAS EN LA BBDD ----------------------------------------------------------------------------------------------------------------

    def crearBoardVisor():

        global boardVisor, canvasVisor, widthV, heightV
        try:
            boardVisor.destroy() #Ignorar este error (o buscar una forma más eficaz de no acumular ventanas e visores)
        except:
            pass

        boardVisor=Tk()
        boardVisor.title(valor2[1] + " - Visualizador de rutas (Solo lectura)")
        boardVisor.iconbitmap('./icono.ico')
        boardVisor.resizable(1,1)
        boardVisor.geometry(widthBoard + "x" + heightBoard + "+1320+200")

        canvasVisor = Canvas(boardVisor, width=widthBoard, height=heightBoard, bg='white')
        canvasVisor.pack(expand=YES, fill=BOTH)
        canvasVisor.pack()
        
        db.consultaVisor(idBoC)

        viaVisor= str(db.itemsVisor).split(", ")
        widthV= int(viaVisor[7])+1
        heightV= int(viaVisor[8])+1
        fuenteV= round(15 * 15/((widthV+heightV+2)/2))

        for i in range(heightV): #filas
            for j in range(widthV): #columnas
                canvasVisor.create_line(int(widthBoard)/widthV*j,0,int(widthBoard)/widthV*j,int(heightBoard))
                canvasVisor.create_line(0, int(heightBoard)/heightV*i, int(widthBoard), int(heightBoard)/heightV*i)     

        canvasVisor.create_rectangle(0, int(heightBoard)/heightV, int(widthBoard)/widthV, int(heightBoard), fill='white')
        canvasVisor.create_rectangle(int(widthBoard)/widthV, 0, int(widthBoard), int(heightBoard)/heightV, fill='white')

        for i in range(heightV): #filas
            canvasVisor.create_text(int(widthBoard)/widthV - int(widthBoard)/widthV/2 ,int(heightBoard)/heightV*i + int(heightBoard)/heightV/2, text=i, font="Arial " + str(fuenteV)) 

        for i in range(widthV): #columnas
            canvasVisor.create_text(int(widthBoard)/widthV*i + int(widthBoard)/widthV/2,int(heightBoard)/heightV - int(heightBoard)/heightV/2, text=i, font="Arial " + str(fuenteV))


        cargarRegistro()



    # CARGAR LA CONSULTA SQL AL VISOR DE RUTAS --------------------------------------------------------------------------------------------------------------------------------------

    def cargarRegistro():

        # CÁLCULOS VARIOS PARA SEPARAR XS E YS EN DISTINTOS ARRAYS
        global viaVisor

        viaVisor= str(db.itemsVisor).split(", ")
        iniciVisorX=[]
        iniciVisorY=[]
        rutaVisorX=[]
        rutaVisorY=[]
        topVisorX=[]
        topVisorY=[]
        boardInclinacionVisor()

        n=2
        iniciVisor= [str(viaVisor[4].replace("'","").replace("-",""))[index : index + n] for index in range(0, len(str(viaVisor[4].replace("'","").replace("-",""))), n)]
        for i in iniciVisor[::2]:
            iniciVisorY.append(i)
        for i in iniciVisor[1::2]:
            iniciVisorX.append(i)
            
        rutaVisor= [str(viaVisor[5].replace("'","").replace("-",""))[index : index + n] for index in range(0, len(str(viaVisor[5].replace("'","").replace("-",""))), n)] 
        for i in rutaVisor[::2]:
            rutaVisorY.append(i)
        for i in rutaVisor[1::2]:
            rutaVisorX.append(i)

        topVisor= [str(viaVisor[6].replace("'","").replace("-",""))[index : index + n] for index in range(0, len(str(viaVisor[6].replace("'","").replace("-",""))), n)] 
        for i in topVisor[::2]:
            topVisorY.append(i)
        for i in topVisor[1::2]:
            topVisorX.append(i)

        
        # DIBUJAR PRESAS A PARTIR DE LOS ARRAYS X E Y E CADA TRAMO 

        for i in range(len(iniciVisorX)):
            celdaVisorInici= canvasVisor.create_rectangle(int(widthBoard)/widthV*(int(iniciVisorX[i])) , int(heightBoard)/heightV*(int(iniciVisorY[i])) , int(widthBoard)/widthV*(int(iniciVisorX[i])+1) , int(heightBoard)/heightV*(int(iniciVisorY[i])+1) , fill='green')
         
        for i in range(len(rutaVisorX)):   
            celdaVisorInici= canvasVisor.create_rectangle(int(widthBoard)/widthV*(int(rutaVisorX[i])) , int(heightBoard)/heightV*(int(rutaVisorY[i])) , int(widthBoard)/widthV*(int(rutaVisorX[i])+1) , int(heightBoard)/heightV*(int(rutaVisorY[i])+1) , fill='deep sky blue')           
            
        for i in range(len(topVisorX)):
            celdaVisorInici= canvasVisor.create_rectangle(int(widthBoard)/widthV*(int(topVisorX[i])) , int(heightBoard)/heightV*(int(topVisorY[i])) , int(widthBoard)/widthV*(int(topVisorX[i])+1) , int(heightBoard)/heightV*(int(topVisorY[i])+1) , fill='red')

        print("\t - Ruta " + viaVisor[1] + " cargada correctamente. Dimensiones: " + viaVisor[7] + "x" + viaVisor[8])



    # CERRAR LAS DOS VENTANAS A LA VEZ ------------------------------------------------------------------------------------------------------------

    def cerrarVentana():
        raiz.destroy()
        board.destroy()
        try:
            boardVisor.destroy()
        except:
            print()

    raiz.protocol("WM_DELETE_WINDOW", cerrarVentana)
    board.protocol("WM_DELETE_WINDOW", cerrarVentana)
    

    board.mainloop()


main()

