import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
###PASO 2
url = 'https://companies-market-cap-copy.vercel.app/index.html'
response = requests.get(url)
html_content = response.text

html_content
###PASO 3
soup = BeautifulSoup(html_content, 'html.parser')

table = soup.find('table')

table

filas = table.find_all("tr")

datos = []  

for fila in filas[1:]:
    columnas = fila.find_all("td") 
    año = columnas[0].text.strip()
    ingresos = columnas[1].text.strip()

    datos.append([año, ingresos]) 


datos

###PASO 4

import pandas as pd

df = pd.DataFrame(datos, columns=["Años", "Ingresos"])

df["Ingresos"] = df["Ingresos"].str.replace("$", "")
df["Ingresos"] = df["Ingresos"].str.replace("B", "")
df["Ingresos"] = pd.to_numeric(df["Ingresos"])

df = df.dropna()

print(df)

#PASO 5

import sqlite3

conexion = sqlite3.connect("tesla_datos.db")
cursor = conexion.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS ingresos_tesla (
        Años INTEGER,
        Ingresos REAL
    )
""")

df.to_sql('ingresos_tesla', conexion, if_exists='replace', index=False)

conexion.commit()

conexion.close()

#PASO 6

plt.figure(figsize=(10,6))
sns.lineplot(data=df, x='Años', y='Ingresos', marker='o')

plt.title("Evolución anual de ingresos de Tesla")
plt.xlabel("Año")
plt.ylabel("Ingresos (Billones de USD)")
plt.grid(True)

plt.show()




plt.figure(figsize=(10,6))
sns.barplot(data=df, x='Años', y='Ingresos', palette="Blues_d")

plt.title("Comparación anual de ingresos de Tesla")
plt.xlabel("Año")
plt.ylabel("Ingresos (Billones de USD)")
plt.grid(axis='y')

plt.show()



plt.figure(figsize=(10,6))
sns.histplot(df['Ingresos'], bins=10, kde=True, color='skyblue')

plt.title("Distribución de ingresos anuales de Tesla")
plt.xlabel("Ingresos (Billones de USD)")
plt.ylabel("Frecuencia")
plt.grid(True)

plt.show()
