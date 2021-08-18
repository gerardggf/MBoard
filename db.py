import sqlite3
from datetime import datetime

nombreBD="bbddRutas"


def creardb():
    con=sqlite3.connect(nombreBD + ".db")
    try:
        con.execute("""
            CREATE TABLE RUTAS (
                ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                NOMBRE TEXT,
                NIVEL TEXT,
                FECHA TEXT, 
                INICIO TEXT,
                RUTA TEXT,
                TOP TEXT,
                COLUMNAS INTEGER,
                FILAS INTEGER,
                INCLINACION INTEGER
            )
        """)
        print("Tabla creada correctamente")
    except sqlite3.OperationalError:
        print("")
    con.close()



fecha= datetime.now().strftime('%d/%m/%y %H:%M')

def insertardb(nombre, nivel, inicio, ruta, top, columnas, filas, inclinacion):
    con=sqlite3.connect(nombreBD + ".db")
    c=con.cursor()
    c.execute("""
        INSERT INTO RUTAS(
            NOMBRE,
            NIVEL,
            FECHA,
            INICIO,
            RUTA,
            TOP,
            COLUMNAS,
            FILAS,
            INCLINACION
        ) 
        VALUES (
            ?,?,?,?,?,?,?,?,?
            )
    """,
    (nombre, nivel, fecha, inicio, ruta, top, columnas, filas, inclinacion))
    
    con.commit()
    con.close()



def consulta():
    con = sqlite3.connect(nombreBD + ".db")
    c=con.cursor()
    c.execute("SELECT * FROM RUTAS")
    global items
    items= c.fetchall()

    con.commit()
    con.close()



def imprimir():
    print("\n\tID" + "\t\tNOMBRE" + "\t\tNIVEL" + "\t\tFECHA" + "\t\tCOLUMNAS" + "\tFILAS" + "\t\tINCLINACIÓN")
    print("\t----" + "\t\t----" + "\t\t----" + "\t\t----" + "\t\t----" + "\t\t----" + "\t\t----")
    for item in items:
        print("\n\t" + str(item[0]) + "\t\t" + str(item[1]).upper() + "\t\t" + str(item[2]) + "\t\t" + str(item[3]) + "\t\t" + str(item[7]) + "\t\t" + str(item[8]) + "\t\t" + str(item[9]) + "\n\t" + str(item[4]) + "\n\t" + str(item[5]) + "\n\t" + str(item[6]) + "\n")




def borrardb(idBorrar):
    con=sqlite3.connect(nombreBD + ".db")
    c=con.cursor()
    c.execute("DELETE FROM RUTAS WHERE ID = ?", (idBorrar,))
    
    con.commit()
    consulta()
    con.close()



def consultaVisor(id):
    con = sqlite3.connect(nombreBD + ".db")
    c=con.cursor()
    c.execute("SELECT * FROM RUTAS WHERE ID= ?", (id,))

    global itemsVisor
    itemsVisor= c.fetchall()

    con.commit()
    con.close()






#####################################################
def main():   
    creardb()
    consulta()
    imprimir()

main()
