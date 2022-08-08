path = "D:\\Abaqus_Files\\A350\\15_S19_FR100_prying\\03_SUBMODELO\\RESULTS\\A350_MSN480XMVS08O002F_COLD_NL_PLCNTV16_3D_SUBMODEL.rep"

#-----------------------------METHOHDS DEFINITION-----------

#Lee el fichero y extrae el numero de steps que se han lanzado
def Numero_steps(text):
    for line in text:
        if "Total number of steps" in line:
            return int(line[24])
#Crea una lista con el nombre de todos los steps
def Nombre_steps(text):
    b = []
    for line in text:
        if "Step name \'" in line:
            aa = line.replace("Step name \'","").replace("\'","")
            b.append(aa)
    return b
#Crea una lista con los nombres de cada history output para cada step
def lista_history_outputs(txt):
    lista1 = []
    lista2 = []
    counter = 0
    for line in txt:
        if ("Step name " in line) or ("End of ODB Report" in line):
            if counter > 0:
                lista1.append(lista2)
                lista2 = []
            counter =+ 1
        if "    History Output" in line:
            aa = line.replace("    History Output ","").replace("  "," ").replace(" ","_").replace("\'","").strip()
            lista2.append(aa)

    return lista1

#Crea una lista multidimensional con los valores de cada history output para cada step
def multi_list(text):
    entrar = ""
    Values1 = [] # Lista de history output values
    Values2 = [] # Lista completa de values de un history output
    Values3 = [] # Lista con pares de valores de un history output
    zz = []
    counter = 0
    for line in text:
        if ("Step name " in line) or ("End of ODB Report" in line):
            if counter > 0:
                Values1.append(Values2)
                Values2 = []
            else:
                counter =+ 1
        if line == "" and entrar == "Ahora":
            entrar = ""
            Values2.append(Values3)
            Values3 = []
        if entrar == "Ahora":
            z = line.strip().split(" ")
            for linea2 in z:
                if linea2 != "":
                    zz.append(linea2)
            Values3.append(zz)
            zz = []
        if "      Frame value          Data" in line:
            entrar = "Ahora"

    return Values1

#-----------------------------INICIO SCRIPT-----------
path2 = path.replace(".rep", ".txt")

texto = open(path,"r")
txt = texto.read()

a = txt.split("\n")

c = open(path2,"w")

steps = Numero_steps(a)
print(f"El numero de steps es {str(steps)}")

lista_steps = Nombre_steps(a)
lista_history_outpts = lista_history_outputs(a)
misvalores = multi_list(a)

#-----------------------------CREAR TXT OUTPUT-----------

if len(lista_steps)>0 and len(lista_history_outpts)>0 and len(misvalores)>0:
    escribir = open(path2,"w")
    i = 0
    j = 0
    k = 0
    escribir.write("STEP HISTORY_OUTPUT TIME VALUE" + "\n")
    while j < len(lista_steps):
        k = 0
        while k < len(lista_history_outpts[j]):
            for l in misvalores[j][k]:
                temp_1 = str(l).replace("[","").replace("]","").replace(" ","").replace("\'","").replace(","," ")
                escribir.write(lista_steps[j] + " " + lista_history_outpts[j][k] + " " + temp_1 + "\n")
            k += 1
        j +=1
            
    escribir.close()
else:
    print("El archivo .rep no tiene valores de donde extraer datos. Por favor, carge un archivo .rep adecuado!")
texto.close()

#-----------------------------GENERAR CSV OUTPUT-----------

path_excel = path2.replace(".txt",".xlsx")

import pandas as pd

data = pd.read_csv(path2, sep=" ")
data.to_excel(path_excel, 'Sheet1', index=True)