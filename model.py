import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import datetime as dt
#cargar el dataset en un dataframe
url  = 'supabase_Vivienda_Table.csv'
data = pd.read_csv(url)

#Eliminamos columnas que no sirven para el modelo
data.drop(['id_vivienda', 'nombre_propiedad', 'descripcion', 'ubicacion', 'fecha_creacion', 'links_contacto', 'id_vecindario',
           'id_comuna', 'id_ciudad', 'id_region', 'tipo_subsidio', 'latitud', 'longitud'], axis=1, inplace=True)

#eliminamos columnas que mantienen datos nulos
data.dropna(axis=1, how='all', inplace=True)

#Eliminamos columnas que contiene arriendo en True
data.drop(data[data['tipo_operacion'] == True].index, inplace=True)

#Eliminamos la columna de tipo de operacion
data.drop('tipo_operacion', axis=1, inplace=True)

#Cambiamos la columnas object a category
for col in data.columns:
    if data[col].dtype == 'object':
        data[col] = data[col].astype('category')

#imputacion de valores nulos
for col in data.columns:
    if pd.api.types.is_numeric_dtype(data[col]):
        data[col] = data[col].fillna(data[col].mean())

for col in data.columns:
    if pd.api.types.is_categorical_dtype(data[col]):
        data[col] = data[col].fillna(data[col].mode()[0])

data.reset_index(drop=True, inplace=True)

#tipo_vivienda categorica es necesario transformarla
# Create a mapping dictionary
tipo_vivienda_mapping = {0: 'Departamento', 1: 'Casa', 2: 'Otro'}

# Apply the mapping to the 'tipo_vivienda' column
data['tipo_vivienda'] = data['tipo_vivienda'].map(tipo_vivienda_mapping)
data['tipo_vivienda'] = data['tipo_vivienda'].astype('category')

#Confirmación de variables categoricas
from sklearn.preprocessing import LabelEncoder
encoders = {}
categoricas = data.select_dtypes(include=['category', 'object']).columns

for column in categoricas:
    encoders[column] = LabelEncoder()  # Create a new LabelEncoder for each column.
    data[column] = encoders[column].fit_transform(data[column])


#tratamiento de los outliers
outliers=['area_total',	'habitaciones',	'banos', 'area_construida', 'precio_uf']
for col in outliers:
  try:
    max = data[col].describe()[6]+1.5*(data[col].describe()[6]-data[col].describe()[4]) #Q3+1.5*IQR
  except:
    continue
  query = col+'>@max'
  data.drop(data.query(query).index, inplace=True)

data=data.reset_index(drop=True)


#entrenamiento del modelo
X = data.drop('precio_uf', axis=1)
y = data['precio_uf']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=102)

#regresión lineal
model = LinearRegression()
model.fit(X_train, y_train)
# Imprimimos los coeficientes y el intercepto
print(model.intercept_)
print(model.coef_)

#evaluar el modelo
y_pred = model.predict(X_test)

#calcular las métricas de evaluación
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Error cuadrático medio (MSE): {mse}")
print(f"R-cuadrado (R2): {r2}")

#Guardar el modelo
import joblib
joblib.dump(model, 'modelo_vivienda.pkl')
print('Modelo guardado')
#guardar las columnas relevantes
model_columns = list(X.columns)
joblib.dump(model_columns, 'model_columns.pkl')
print('Columnas guardadas')



