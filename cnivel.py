from tkinter.constants import ROUND
import db

def calcular(id):

    global multiplicadorRatios

    db.consultaVisor(id)
    viaCalc= str(db.itemsVisor).split(", ")

    inicioCalcX=[]
    inicioCalcY=[]
    rutaCalcX=[]
    rutaCalcY=[]
    topCalcX=[]
    topCalcY=[]

    numIniciPresas= int(len(str(viaCalc[4].replace("'","").replace("-","")))/4)
    numRutaPresas= int(len(str(viaCalc[5].replace("'","").replace("-","")))/4)
    numTopPresas= int(len(str(viaCalc[6].replace("'","").replace("-","")))/4)
    numTotalPresas= numIniciPresas + numRutaPresas + numTopPresas

    columnas= int(viaCalc[7])
    filas= int(viaCalc[8])
        
    n=2
    inicioCalc= [str(viaCalc[4].replace("'","").replace("-",""))[index : index + n] for index in range(0, len(str(viaCalc[4].replace("'","").replace("-",""))), n)]
    for i in inicioCalc[::2]:
        inicioCalcY.append(i)
    for i in inicioCalc[1::2]:
        inicioCalcX.append(i)
            
    rutaCalc= [str(viaCalc[5].replace("'","").replace("-",""))[index : index + n] for index in range(0, len(str(viaCalc[5].replace("'","").replace("-",""))), n)] 
    for i in rutaCalc[::2]:
        rutaCalcY.append(i)
    for i in rutaCalc[1::2]:
        rutaCalcX.append(i)

    topCalc= [str(viaCalc[6].replace("'","").replace("-",""))[index : index + n] for index in range(0, len(str(viaCalc[6].replace("'","").replace("-",""))), n)] 
    for i in topCalc[::2]:
        topCalcY.append(i)
    for i in topCalc[1::2]:
        topCalcX.append(i)

    viaCalcY= inicioCalcY + rutaCalcY + topCalcY
    viaCalcX= inicioCalcX + rutaCalcX + topCalcX

    #RATIOS -------------------------------------------------------------------------------------------------------------------------------------
    
    #COMO MÁS SE ACERQUE A 1, MÁS DIFÍCIL

    # 1 - Porcentaje de ocupación de las presas en el tablero
    ratioDimensiones= round(1-(numTotalPresas/(columnas*filas)), 3)
    
    # 2 - Distancia de la primera presa de todas en relación con la última o penúltima en el eje Y
    ratioInicioTopY = round((abs(int(inicioCalcY[0]) - int(topCalcY[0])+1))/filas, 3)

    # 3 - Distancia de la primera presa de todas en relación con la última o penúltima en el eje X
    ratioInicioTopX = round((abs(int(inicioCalcX[0]) - int(topCalcX[0])+1))/columnas, 3)

    # 4 - Distancia entre cada una de las presas con la siguiente
    ratioDistanciaY= []
    ratioDistanciaX= []
    ratioDistancia= 0
    for i in range(int(((len(inicioCalc) + len(rutaCalc) + len(topCalc))/2)-1)):
        ratioDistanciaY.append(abs(int(viaCalcY[i])-int(viaCalcY[i+1])))  
    for i in range(int(((len(inicioCalc) + len(rutaCalc) + len(topCalc))/2)-1)):
        ratioDistanciaX.append(abs(int(viaCalcX[i])-int(viaCalcX[i+1])))
    for i in range(len(ratioDistanciaY)):
        ratioDistancia = ratioDistancia + ratioDistanciaY[i] + ratioDistanciaX[i]

    ratioDistancia= ratioDistancia + 1
    ratioDistancia= round(1 - abs(numTotalPresas/ratioDistancia) ,3)

    # 5 - Inclinación (0º = 0% , 80º = 100%)
    ratioInclinacion= (1/80*int(viaCalc[9][:-2]))

    #------------------------------------------------------

    ratioInicioTop= (ratioInicioTopY + ratioInicioTopX) / 2

    multiplicadorRatios = round( (ratioDimensiones + ratioInicioTop + ratioDistancia + (ratioInclinacion*2))/     5    *10, 3)



    # IMPRESIONES POR CONSOLA ---------------------------------------------------------------------------------------------------------------------
    
    # print("\tPresas por tipo: " + str(numIniciPresas) + " " + str(numRutaPresas) + " " + str(numTopPresas))
    # print("\tColumnas x filas: " + str(columnas) + " " + str(filas))

    # print("\tInicio: " + str(viaCalc[4]))
    # print("\t\t" + str(inicioCalcX))
    # print("\t\t" + str(inicioCalcY))
    # print("\tRuta: " + str(viaCalc[5]))
    # print("\t\t" + str(rutaCalcX))
    # print("\t\t" + str(rutaCalcY))
    # print("\tTop: " + str(viaCalc[6]))
    # print("\t\t" + str(topCalcX))
    # print("\t\t" + str(topCalcY))
    # print("\tPresas via eje X concatenadas: " + str(viaCalcX))
    # print("\tPresas via eje Y concatenadas: " + str(viaCalcY))

    print("\n\t---------Ratios-----------------------")
    print("\tDimensiones: " + str(ratioDimensiones))
    print("\tDistancia inicio top Y: " + str(ratioInicioTopY))
    print("\tDistancia inicio top X: " + str(ratioInicioTopX))
    print("\tRatio distancia entre cada presa: " + str(ratioDistancia))
    print("\tRatio inclinación: " + str(ratioInclinacion))
    #print()
    print("\t----------------------------------------")
    itemsPrint= str(db.itemsVisor).split(",")
    print("\t" + str(itemsPrint[0].replace("[(","")) + " - " + str(itemsPrint[1].replace("'","")))
    print("\t = " + str(multiplicadorRatios))

    calcNivelAprox()

    print("\t = " + str(nivelAprox))
    print("\tWORK IN PROGRESS")
    print("Se aceptan sugerencias y aportaciones: gerard.ggf@gmail.com")


# PUNTUACIÓN DEL 1 AL 10 A ASIGNACIÓN DE NIVEL DE ESCALADA --------------------------------------------------------------------------------------------------------

def calcNivelAprox():

    global nivelAprox

    if(multiplicadorRatios>0) and (multiplicadorRatios<1):
        nivelAprox= "III"
    elif(multiplicadorRatios>=1) and (multiplicadorRatios<2.5):
        nivelAprox= "IV"
    elif(multiplicadorRatios>=2.5) and (multiplicadorRatios<3.5):
        nivelAprox= "V"
    elif(multiplicadorRatios>=3.5) and (multiplicadorRatios<4.5):
        nivelAprox= "V+"

    elif(multiplicadorRatios>=4.5) and (multiplicadorRatios<5):
        nivelAprox= "6A"
    elif(multiplicadorRatios>=5) and (multiplicadorRatios<5.5):
        nivelAprox= "6A+"
    elif(multiplicadorRatios>=5.5) and (multiplicadorRatios<6):
        nivelAprox= "6B"
    elif(multiplicadorRatios>=6) and (multiplicadorRatios<6.5):
        nivelAprox= "6B+"
    elif(multiplicadorRatios>=6.5) and (multiplicadorRatios<7):
        nivelAprox= "6C"
    elif(multiplicadorRatios>=7) and (multiplicadorRatios<7.4):
        nivelAprox= "6C+"
    
    elif(multiplicadorRatios>=7.4) and (multiplicadorRatios<7.8):
        nivelAprox= "7A"
    elif(multiplicadorRatios>=7.8) and (multiplicadorRatios<8.2):
        nivelAprox= "7A+"
    elif(multiplicadorRatios>=8.2) and (multiplicadorRatios<8.5):
        nivelAprox= "7B"
    elif(multiplicadorRatios>=8.5) and (multiplicadorRatios<8.7):
        nivelAprox= "7B+"
    elif(multiplicadorRatios>=8.7) and (multiplicadorRatios<8.85):
        nivelAprox= "7C"
    elif(multiplicadorRatios>=8.85) and (multiplicadorRatios<9):
        nivelAprox= "7C+"

    elif(multiplicadorRatios>=9) and (multiplicadorRatios<9.1):
        nivelAprox= "8A"
    elif(multiplicadorRatios>=9.1) and (multiplicadorRatios<9.2):
        nivelAprox= "8A+"
    elif(multiplicadorRatios>=9.2) and (multiplicadorRatios<9.3):
        nivelAprox= "8B"
    elif(multiplicadorRatios>=9.3) and (multiplicadorRatios<9.4):
        nivelAprox= "8B+"
    elif(multiplicadorRatios>=9.4) and (multiplicadorRatios<9.5):
        nivelAprox= "8C"
    elif(multiplicadorRatios>=9.5) and (multiplicadorRatios<9.6):
        nivelAprox= "8C+"

    elif(multiplicadorRatios>=9.6) and (multiplicadorRatios<9.68):
        nivelAprox= "9A"
    elif(multiplicadorRatios>=9.68) and (multiplicadorRatios<9.76):
        nivelAprox= "9A+"
    elif(multiplicadorRatios>=9.76) and (multiplicadorRatios<9.84):
        nivelAprox= "9B"
    elif(multiplicadorRatios>=9.84) and (multiplicadorRatios<9.9):
        nivelAprox= "9B+"
    elif(multiplicadorRatios>=9.9) and (multiplicadorRatios<9.95):
        nivelAprox= "9C"
    elif(multiplicadorRatios>=9.95) and (multiplicadorRatios<=9.97):
        nivelAprox= "9C+"

    elif(multiplicadorRatios>=9.97) and (multiplicadorRatios<9.975):
        nivelAprox= "10A"
    elif(multiplicadorRatios>=9.975) and (multiplicadorRatios<9.98):
        nivelAprox= "10A+"
    elif(multiplicadorRatios>=9.98) and (multiplicadorRatios<9.985):
        nivelAprox= "10B"
    elif(multiplicadorRatios>=9.985) and (multiplicadorRatios<9.99):
        nivelAprox= "10B+"
    elif(multiplicadorRatios>=9.99) and (multiplicadorRatios<9.995):
        nivelAprox= "10C"
    elif(multiplicadorRatios>=9.995) and (multiplicadorRatios<=9.998):
        nivelAprox= "10C+"
    elif(multiplicadorRatios>=9.998) and (multiplicadorRatios<=10):
        nivelAprox= "11A"
    

    else:
        nivelAprox="¿?"