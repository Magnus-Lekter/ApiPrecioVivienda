import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import datetime as dt
#cargar el dataset en un dataframe
url  = 'supabase_vivienda_table.csv'
data = pd.read_csv(url)

data.fillna('', inplace=True)
data['precio_uf'] = data['precio_uf'].astype(int)
data['tipo_operacion'] = data['tipo_operacion'].astype(str)
dic = {'True': 'Arriendo', 'False': 'Venta'}
data['tipo_operacion']= data['tipo_operacion'].replace(dic)
#data['id_vecindario'] = data['id_vecindario'].astype(int)
data['tipo_vivienda'] = data['tipo_vivienda'].astype(int)
data['habitaciones'] = data['habitaciones'].astype(int)
data['fecha_creacion'] = pd.to_datetime(data['fecha_creacion'])
#calcular el indice de pobreza
data['pobreza'] = (data['precio_uf'] / data['area_total']) / data['habitaciones']
data['año'] = data['fecha_creacion'].dt.year  # Asegúrate de tener una columna de fecha y extraer el año
X = data[['habitaciones', 'pobreza', 'area_total', 'año']]  # variables independientes
y = data['precio_uf']  # variable objetivo

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)
#evaluar el modelo
y_pred = model.predict(X_test)

#calcular las métricas de evaluación
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

#Guardar el modelo
import joblib
joblib.dump(model, 'modelo_vivienda.pkl')
print('Modelo guardado')

#cargar el modelo
#model = joblib.load('modelo_vivienda.pkl')

#guardar las columnas relevantes
model_columns = list(X.columns)
joblib.dump(model_columns, 'model_columns.pkl')
print('Columnas guardadas')



