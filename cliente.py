import requests
import matplotlib.pyplot as plt
url = 'http://127.0.0.1:5000/predict'
#data = [{
#    "habitaciones": 3,
#    "pobreza": 10,
#    "area_total": 100,
#    "año": 2024
#}]
headers = {'Content-Type': 'application/json'}
vivienda = {
            "area_total": 139,
            "habitaciones": 6,
            "tipo_vivienda": 0,
            "banos": 3,
            "area_construida": 130,
            "nom_comuna": 30,
            "nom_ciudad": 5,
            "nom_region": 0,
            "nom_vecindario":111
            }

# Enviar la solicitud POST a la API
response = requests.post(url, json=[vivienda], headers=headers)

# Verificar la respuesta
if response.status_code == 200:
    prediction = response.json()['prediction'][0]
    print(f"Predicción del costo de la vivienda: {prediction} UF")
else:
    print(f"Error: {response.status_code}")
    print(response.json())

#otra predicción basada en años futuros
#future_years = list(range(2022, 2027))
#for year in future_years:
#    data.append({
#        "habitaciones": 3,
#        "pobreza": 10,
#        "area_total": 100,
#        "año": year
#    })


# Imprimir el valor calculado por año con el incremento del 0.03
#incremented_predictions = []
#for i, (year, prediction) in enumerate(zip(future_years, predictions)):
#    incremented_value = prediction * (1 + 0.03) ** i
#    incremented_value = round(incremented_value, 1)
#    incremented_predictions.append(incremented_value)
#    print(f"Predicción para el año {year}: {incremented_value}")

# Graficar la proyección resultante
#plt.plot(future_years, incremented_predictions, marker='o')
#plt.xlabel('Año')
#plt.ylabel('Predicción de Precio (UF)')
#plt.title('Proyección de Precios de Vivienda con Incremento del 3% Anual')
#plt.grid(True)
#plt.show()