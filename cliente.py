import requests
import matplotlib.pyplot as plt
url = 'http://127.0.0.1:12345/predict'
#data = [{
#    "habitaciones": 3,
#    "pobreza": 10,
#    "area_total": 100,
#    "año": 2024
#}]
headers = {'Content-Type': 'application/json'}

#response = requests.post(url, json=data, headers=headers)
#res = round(response.json()['prediction'][0], 1)
#print(res)
#print(response.json())

""" 
Este código hace lo siguiente:

Envía una solicitud POST a la API con los datos para los años futuros.
Recibe las predicciones de la API.
Itera sobre los años futuros y las predicciones, aplicando un incremento del 0.03 a cada predicción.
Imprime el valor calculado por año con el incremento aplicado.

"""

#otra predicción basada en años futuros
future_years = [2024, 2025, 2026, 2027, 2028]
data = []
for year in future_years:
    data.append({
        "habitaciones": 3,
        "pobreza": 10,
        "area_total": 100,
        "año": year
    })

response = requests.post(url, json=data, headers=headers)
predictions = response.json()['prediction']

# Imprimir el valor calculado por año con el incremento del 0.03
incremented_predictions = []
for i, (year, prediction) in enumerate(zip(future_years, predictions)):
    incremented_value = prediction * (1 + 0.03) ** i
    incremented_value = round(incremented_value, 1)
    incremented_predictions.append(incremented_value)
    print(f"Predicción para el año {year}: {incremented_value}")

# Graficar la proyección resultante
plt.plot(future_years, incremented_predictions, marker='o')
plt.xlabel('Año')
plt.ylabel('Predicción de Precio (UF)')
plt.title('Proyección de Precios de Vivienda con Incremento del 3% Anual')
plt.grid(True)
plt.show()