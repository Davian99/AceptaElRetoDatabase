import sqlite3
from bs4 import BeautifulSoup
from requests import get
conn = sqlite3.connect('F:\Acepta el reto Database\Envios.db')
c = conn.cursor()

def get_datos(l):
    datos = {}
    datos['usuario'] = l[0].replace("\n", "").split(" ")[1]
    datos['envio'] = l[1].replace("\n", "").split(" ")[1]
    if(len(l) > 30): #internal error
        datos['fecha'] = l[8].replace(", ", " ").replace("(CET)", "").replace("/", "-")[:-1]
        datos['problema'] = int(l[10])
        datos['lenguaje'] = l[14]
        datos['veredicto'] = "IE"
        datos['tiempo'] = "NULL"
        datos['memoria'] = "NULL"
        datos['posicion'] = "NULL"
        return datos

    datos['fecha'] = l[3].replace(", ", " ").replace("(CET)", "").replace("/", "-")[:-1]
    datos['problema'] = int(l[5])
    if(len(l) >= 9):
        datos['lenguaje'] = l[9]
    else:
        datos['lenguaje'] = "NULL"
    if(len(l) >= 11):
        datos['veredicto'] = l[11].split(" ")[-1].replace("(", "").replace(")","")
    else:
        datos['veredicto'] = "NULL"
    if(len(l) >= 13):
        datos['tiempo'] = float(l[13].split(" ")[0])
    else:
        datos['tiempo'] = "NULL"
    if(len(l) >= 15):
        datos['memoria'] = int(l[15].split(" ")[0])
    else:
        datos['memoria'] = "NULL"
    if(len(l) >= 17):
        datos['posicion'] = int(l[17].split(" ")[0])
    else:
        datos['posicion'] = "NULL"
    return datos

def insert_datos(datos):
    command = "INSERT INTO ENVIOS VALUES("
    command += datos['envio']
    command += ", \"" + datos['usuario'] + "\""
    command += ", " + str(datos['problema'])
    command += ", \"" + datos['fecha'] + "\""
    command += ", \"" + datos['lenguaje'] + "\""
    command += ", \"" + datos['veredicto'] + "\""
    command += ", " + str(datos['tiempo'])
    command += ", " + str(datos['memoria'])
    command += ", " + str(datos['posicion'])
    command += ")"
    c.execute(command)

ind = 173401
while(True):
    print(ind)
    page = "https://aceptaelreto.com/user/submission.php?id=" + str(ind)
    response = get(page)
    soup = BeautifulSoup(response.content, "html.parser")

    #usuario = soup.findAll('div', attrs={'class':'col-md-10'})
    scrap = soup.findAll('div', attrs={'class':'col-md-10'})[0]
    l = scrap.text.split("\n")
    l = [value for value in l if value != ""]

    if(len(l) < 2):
        conn.commit()
        ind += 1
        continue

    datos = get_datos(l)
    insert_datos(datos)
    if(ind % 100 == 0):
        conn.commit()
    ind += 1


