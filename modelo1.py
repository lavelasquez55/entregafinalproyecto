from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error

# Eliminar la columna steamId
data = data.drop(columns=['steamId'])

# Convertir releaseDate en una característica numérica (año y mes)
data['releaseYear'] = pd.to_datetime(data['releaseDate'], format='%d-%m-%Y').dt.year
data['releaseMonth'] = pd.to_datetime(data['releaseDate'], format='%d-%m-%Y').dt.month
data = data.drop(columns=['releaseDate'])

# Codificación de variables categóricas
data_encoded = pd.get_dummies(data, columns=['publisherClass', 'publishers', 'developers'], drop_first=True)

# Separar variables predictoras (X) y variable objetivo (y)
X = data_encoded.drop(columns=['revenue'])
y = data_encoded['revenue']

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar el modelo Random Forest
rf_model = RandomForestRegressor(random_state=42, n_estimators=100)
rf_model.fit(X_train, y_train)

# Realizar predicciones
y_pred = rf_model.predict(X_test)

# Evaluación del modelo
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

r2, mae