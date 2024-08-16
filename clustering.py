# -*- coding: utf-8 -*-
"""Clustering.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VJKzRzdgOp6KekEwskSa6Fr4Vd0Prm9R

## **Clustering Proyect**
"""

import pandas as pd     # Manejo de dataframes
import numpy as np      # Calculos matriciales
import matplotlib.pyplot as plt    # Visualizacion
import seaborn as sns              # Visualizacion
from google.colab import drive     # Drive en Colab


import warnings
warnings.filterwarnings("ignore")  # inhabilita warnings

from pickle import dump    # guardar archivos comprimidos

from google.colab import drive
drive.mount('/content/drive')

df_calendar = pd.read_csv('/content/drive/MyDrive/DSMarket/data_dsmarket/daily_calendar_with_events.csv')
df_prices = pd.read_csv('/content/drive/MyDrive/DSMarket/data_dsmarket/item_prices.csv')
df_sales = pd.read_csv('/content/drive/MyDrive/DSMarket/data_dsmarket/item_sales.csv')

df_calendar.head()

df_prices.head()

df_sales.head()

#AGRUPAMOS LAS TABLAS

#agrupamos las ventas por año

dates = pd.date_range(start='2011-01-29', end='2016-04-24', freq='D').strftime('%Y-%m-%d').tolist()

for i in range(1, 1914):
    col = "d_" + str(i)
    df_sales = df_sales.rename(columns={col: dates[i-1]})

df_sales.head()

# Crear una nueva columna "sales" que sea la suma de todas las columnas desde 2011-01-29 hasta 2016-04-24
df_sales['sales'] = df_sales.iloc[:, 6:].sum(axis=1)

df_sales.head()

# Eliminar las columnas desde 2011-01-29 hasta 2016-04-24
df_sales = df_sales.drop(df_sales.columns[6:-1], axis=1)

df_sales.head(100)

# Eliminar las columnas id, category, department, store, y store_code
df_sales = df_sales.drop(['id', 'category', 'department', 'store', 'store_code'], axis=1)

df_sales.head(100)

# Agrupar los productos con el mismo nombre y sumar sus ventas
df_sales = df_sales.groupby(['item'], as_index=False).sum()

df_sales.head()

df_sales.shape

#analizamos df_prices

df_prices.head()

df_prices.shape

# Eliminar las columnas category y store_code yearweek
df_prices = df_prices.drop(['yearweek'], axis=1)

df_prices.head(100)

# Eliminar los valores nulos
df_prices = df_prices.dropna()

# Agrupar los datos por item y calcular la media de sell_price
df_prices = df_prices.groupby('item').mean()

df_prices.head()

df_prices.shape

#Unimos la tabla df_sales y df_prices

df_final = df_sales.merge(df_prices, on='item', how='left')

df_final.head()

df_final.shape

df_clustering1=df_final.copy()

#CLUSTERING

#Determinamos la cantidad de clusters que necesitamos, utilizamos la técnica del codo para determinar la cantidad óptima de clusters. Esta técnica consiste en calcular la suma de las distancias cuadradas de cada punto a su centroide correspondiente y graficar estas distancias contra el número de clusters. La idea es elegir el número de clusters en el que la suma de las distancias cuadradas comience a disminuir a un ritmo más lento. Este punto se conoce como "el codo" y es un buen indicador de cuántos clusters es óptimo para el conjunto de datos.

#Para hacer esto, primero necesitamos aplicar un algoritmo de clustering (kMeans) a tus datos y luego calcular la suma de las distancias cuadradas para diferentes números de clusters. Finalmente, grafica estas distancias cuadradas contra el número de clusters y busca el punto en el que la tasa de disminución se ralentiza. Ese será tu número óptimo de clusters.

df_clustering1.head(100)

media_sell_price = df_clustering1['sell_price'].mean()
print("La media de la columna 'sell_price' es:", media_sell_price)

df_clustering1.shape



df_clustering1.info()

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans



# Calcular la suma de las distancias cuadradas para diferentes números de clusters
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(df_clustering1.iloc[:, 1:])
    wcss.append(kmeans.inertia_)

# Graficar la suma de las distancias cuadradas contra el número de clusters
plt.plot(range(1, 11), wcss)
plt.title('Gráfico del Codo')
plt.xlabel('Número de Clusters')
plt.ylabel('Suma de las Distancias Cuadradas')
plt.show()

# Aplicar el algoritmo KMeans al dataframe df_clustering1
N = 3 # Número de clusters óptimo según el gráfico del codo
kmeans = KMeans(n_clusters=N, random_state=0)
kmeans.fit(df_clustering1.iloc[:, 1:])

# Agregar la columna 'cluster' al dataframe df_clustering1
df_clustering1['cluster'] = kmeans.labels_

df_clustering1.head()

df_clustering1.info()

df_clustering1.shape

df_clustering1.to_csv("/content/drive/MyDrive/TFM Nuclio/CSV CLUSTERS/Cluster.csv", float_format='%.2f', index=False)

df_clustering1.to_excel("/content/drive/MyDrive/TFM Nuclio/CSV CLUSTERS/Cluster.xlsx", index=False)

#generamos 3 dataframe cada uno con un cluster

cluster0 = df_clustering1[df_clustering1['cluster'] == 0]
cluster1 = df_clustering1[df_clustering1['cluster'] == 1]
cluster2 = df_clustering1[df_clustering1['cluster'] == 2]

#analisis cluster

cluster0

cluster0.shape

cluster1

cluster1.shape

cluster2

cluster2.shape

#generamos CSV de los clusters

#agrupamos los datos por la columna "cluster" y luego calcular la media de las ventas y la media del precio de venta para cada grupo

cluster0 = df_clustering1[df_clustering1['cluster'] == 0]
mean_sales_cluster0 = cluster0['sales'].mean()
mean_price_cluster0 = cluster0['sell_price'].mean()

cluster1 = df_clustering1[df_clustering1['cluster'] == 1]
mean_sales_cluster1 = cluster1['sales'].mean()
mean_price_cluster1 = cluster1['sell_price'].mean()

cluster2 = df_clustering1[df_clustering1['cluster'] == 2]
mean_sales_cluster2 = cluster2['sales'].mean()
mean_price_cluster2 = cluster2['sell_price'].mean()

print("Mean sales for Cluster 0:", mean_sales_cluster0)
print("Mean price for Cluster 0:", mean_price_cluster0)
print("Mean sales for Cluster 1:", mean_sales_cluster1)
print("Mean price for Cluster 1:", mean_price_cluster1)
print("Mean sales for Cluster 2:", mean_sales_cluster2)
print("Mean price for Cluster 2:", mean_price_cluster2)

#Las características que diferencian los clusters son la cantidad promedio de ventas y el precio promedio de venta.

#renombrar cada cluster de la siguiente manera:

#Cluster 0: Venta Baja y precio medio alto (2893 productos)
#Cluster 1: Venta Moderada y precio medio moderado (152 productos)
#Cluster 2: Venta Alta y precio medio bajo (4 productos)
#tot 3049 productos

import matplotlib.pyplot as plt

# Crea una lista de colores para cada cluster
colors = ['red', 'blue', 'green']

# Crea un gráfico de dispersión para cada cluster
for i in range(3):
    plt.scatter(df_clustering1[df_clustering1['cluster'] == i]['sales'],
                df_clustering1[df_clustering1['cluster'] == i]['sell_price'],
                color=colors[i], label='Cluster ' + str(i))

# Agrega etiquetas a los ejes
plt.xlabel('sales')
plt.ylabel('sell_price')

# Agrega una legenda
plt.legend()

# Muestra el gráfico
plt.show()

import matplotlib.pyplot as plt

# Calcula el promedio de sell_price por cluster
df_avg_price = df_clustering1.groupby('cluster')['sell_price'].mean()

# Crea una lista de colores para cada cluster
colors = ['red', 'blue', 'green']

# Crea un gráfico de dispersión para cada cluster
for i in range(3):
    plt.scatter(df_clustering1[df_clustering1['cluster'] == i]['sales'],
                df_clustering1[df_clustering1['cluster'] == i]['sell_price'],
                color=colors[i], label='Cluster ' + str(i))

# Agrega etiquetas a los ejes
plt.xlabel('sales')
plt.ylabel('sell_price')

# Agrega una línea horizontal para mostrar el promedio de sell_price
for i, avg_price in df_avg_price.items():
    plt.axhline(avg_price, color=colors[i], linestyle='dashed', label='Avg Price - Cluster ' + str(i))

# Agrega una legenda
plt.legend()

# Muestra el gráfico
plt.show()

cluster0.head(100)

#generamos la tabla para el grafico de dispersión de Power Bi



contains_garden = cluster0['item'].str.contains('garden', case=False)
has_garden_product = contains_garden.any()

if has_garden_product:
    print("Hay productos que contienen la palabra 'garden' en la columna 'item'.")
else:
    print("No hay productos que contengan la palabra 'garden' en la columna 'item'.")

# Cálculo del precio medio
precio_medio = cluster0['sell_price'].mean()

# Cálculo del total de ventas
total_ventas = cluster0['sales'].sum()

print("Precio medio: ", precio_medio)
print("Total de ventas: ", total_ventas)

cluster0.shape

unique_items = cluster0['item'].unique()
print(unique_items)

accessories_count = len(cluster0[cluster0['item'].str.startswith('ACCESORIES')])
supermarket_count = len(cluster0[cluster0['item'].str.startswith('SUPERMARKET')])
home_and_garden_count = len(cluster0[cluster0['item'].str.startswith('HOME_&_GARDEN')])

print("Accessories count:", accessories_count)
print("Supermarket count:", supermarket_count)
print("Home & Garden count:", home_and_garden_count)

total_count = len(cluster0)

accessories_percentage = (accessories_count / total_count) * 100
supermarket_percentage = (supermarket_count / total_count) * 100
home_and_garden_percentage = (home_and_garden_count / total_count) * 100

print("Porcentaje de valores que comienzan con 'ACCESORIES':", accessories_percentage)
print("Porcentaje de valores que comienzan con 'SUPERMARKET':", supermarket_percentage)
print("Porcentaje de valores que comienzan con 'GARDEN':", home_and_garden_percentage)

data=cluster0

# Estadísticas descriptivas
print(data.describe())

# Histogramas
data['sales'].hist()
plt.xlabel('Total ventas')
plt.ylabel('Frecuencia')
plt.show()

data['sell_price'].hist()
plt.xlabel('Precio de venta')
plt.ylabel('Frecuencia')
plt.show()

# Crear la cuadrícula de subgráficos
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

# Histograma de ventas
ax1.hist(data['sales'])
ax1.set_xlabel('Total ventas')
ax1.set_ylabel('Numero venta por producto')

# Histograma de precio de venta
ax2.hist(data['sell_price'])
ax2.set_xlabel('Precio de venta')
ax2.set_ylabel('Frecuencia')

# Ajustar los márgenes entre los subgráficos
plt.subplots_adjust(hspace=0.5)

# Mostrar el gráfico
plt.show()

plt.scatter(cluster0['sell_price'], cluster0['sales'], c='blue', alpha=0.5)

plt.xlabel('Precio de venta')
plt.ylabel('Ventas')
plt.title('Relación entre precio y ventas')

plt.show()

#estos patrones de frecuencia en ambos gráficos sugieren que hay una mayor demanda y acceso a productos o servicios con precios más bajos, mientras que a medida que los precios aumentan, la demanda disminuye y se dirige a un grupo más específico de clientes dispuestos a pagar precios más alto

# Diagrama de dispersión
plt.scatter(data['sell_price'], data['sales'])
plt.xlabel('Precio de venta')
plt.ylabel('Ventas')
plt.show()

# Matriz de correlación
corr_matrix = data[['sales', 'sell_price']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.show()

#se encuentra una correlación negativa  (valor de -0.27) entre los precios de venta y las ventas. Esto indica que a medida que los precios de venta aumentan, las ventas tienden a disminuir



cluster1.head()

data1=cluster1

# Estadísticas descriptivas
print(data1.describe())

# Histogramas
data1['sales'].hist()
plt.xlabel('Ventas')
plt.ylabel('Frecuencia')
plt.show()

data1['sell_price'].hist()
plt.xlabel('Precio de venta')
plt.ylabel('Frecuencia')
plt.show()

# Diagrama de dispersión
plt.scatter(data1['sell_price'], data1['sales'])
plt.xlabel('Precio de venta')
plt.ylabel('Ventas')
plt.show()

# Matriz de correlación
corr_matrix = data1[['sales', 'sell_price']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.show()

cluster2.head()

cluster2.shape

cluster2.info()

data2=cluster2

# Estadísticas descriptivas
print(data2.describe())

# Histogramas
data2['sales'].hist()
plt.xlabel('Ventas')
plt.ylabel('Frecuencia')
plt.show()

data2['sell_price'].hist()
plt.xlabel('Precio de venta')
plt.ylabel('Frecuencia')
plt.show()

# Diagrama de dispersión
plt.scatter(data2['sell_price'], data2['sales'])
plt.xlabel('Precio de venta')
plt.ylabel('Ventas')
plt.show()

# Matriz de correlación
corr_matrix = data2[['sales', 'sell_price']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.show()