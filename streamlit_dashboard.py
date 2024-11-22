# Cargar las librerías
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar los datos
data_path = 'Steam_2024_with_predictions.csv'
data = pd.read_csv(data_path)

# Definir el lienzo
st.set_page_config(page_title="Panel de Steam 2024", layout="wide")

# Panel de navegación
st.sidebar.title("Navegación del Panel")
options = st.sidebar.radio("Ir a", ["Resumen de los Datos", "Predicciones", "Análisis de Errores"])

# ---- Resumen de los Datos ----
if options == "Resumen de los Datos":
    st.title("Resumen de los Datos: Estadísticas de Steam 2024")

    # Métricas Claves
    st.header("Métricas Claves")
    total_revenue = data['revenue'].sum()
    total_games_sold = data['copiesSold'].sum()
    total_games = data['name'].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric("Ingresos Totales", f"${total_revenue/1e9:.2f}B")
    col2.metric("Juegos Vendidos", f"{total_games_sold/1e6:.1f}M")
    col3.metric("Total de Juegos", total_games)

    # Distribución de los Ingresos con escala logarítmica
    st.subheader("Distribución de los Ingresos (Escala Logarítmica)")
    fig1, ax1 = plt.subplots()
    sns.histplot(data['revenue'], bins=30, kde=True, ax=ax1, log_scale=(True, False))
    ax1.set_title("Distribución de los Ingresos")
    ax1.set_xlabel("Ingresos (escala logarítmica)")
    st.pyplot(fig1)

    # Juegos Vendidos vs Ingresos
    st.subheader("Principales Juegos por Ingresos")
    top_games = data.nlargest(10, 'revenue')
    fig2, ax2 = plt.subplots()
    ax2.barh(top_games['name'], top_games['revenue'], color='skyblue')
    ax2.set_xlabel("Ingresos")
    ax2.set_ylabel("Nombre del Juego")
    ax2.set_title("Top 10 Juegos por Ingresos")
    st.pyplot(fig2)

    # Juegos Vendidos vs Ingresos
    st.subheader("Juegos Vendidos vs Ingresos")
    top_games = data.nlargest(10, 'revenue')
    fig3, ax3 = plt.subplots()
    ax3.barh(top_games['name'], top_games['copiesSold'], label='Juegos Vendidos', color='skyblue')
    ax3.set_xlabel("Juegos Vendidos")
    ax3.set_ylabel("Juego")
    ax32 = ax3.twinx()
    ax32.barh(top_games['name'], top_games['revenue'], label='Ingresos', color='pink', alpha=0.7)
    ax32.set_xlabel("Ingresos")
    fig3.legend(["Juegos Vendidos", "Ingresos"], loc="lower right")
    st.pyplot(fig3)

# ---- Predicciones ----
elif options == "Predicciones":
    st.title("Predicciones de Ingresos: Reales vs Predichos")

    # Gráfico de dispersión de ingresos reales vs predichos
    st.subheader("Ingresos Reales vs Predichos")
    fig4, ax4 = plt.subplots()
    sns.scatterplot(data=data, x='revenue', y='predicted_revenue', hue='publisherClass', alpha=0.7, ax=ax4)
    ax4.plot([0, data['revenue'].max()], [0, data['revenue'].max()], 'r--', label="Predicción Perfecta")
    ax4.set_xlabel("Ingresos Reales")
    ax4.set_ylabel("Ingresos Predichos")
    ax4.legend()
    st.pyplot(fig4)

    # Filtrar juegos por rango de ingresos
    st.subheader("Filtrar Juegos por Rango de Ingresos")
    min_revenue, max_revenue = st.slider(
        "Selecciona el rango de ingresos:",
        min_value=float(data['revenue'].min()),
        max_value=float(data['revenue'].max()),
        value=(float(data['revenue'].min()), float(data['revenue'].max()))
    )
    filtered_data = data[(data['revenue'] >= min_revenue) & (data['revenue'] <= max_revenue)]
    st.write(filtered_data[['name', 'revenue', 'predicted_revenue', 'publisherClass']])

# ---- Análisis de Errores ----
elif options == "Análisis de Errores":
    st.title("Análisis de Errores: Desempeño de las Predicciones")

    # Calcular errores
    data['error'] = abs(data['revenue'] - data['predicted_revenue'])

    # Principales 10 errores
    st.subheader("Top 10 Juegos con Mayores Errores de Predicción")
    top_errors = data.nlargest(10, 'error')
    st.write(top_errors[['name', 'revenue', 'predicted_revenue', 'error']])

    # Visualización de errores
    st.subheader("Visualización de los Errores de Predicción")
    fig5, ax5 = plt.subplots()
    ax5.barh(top_errors['name'], top_errors['revenue'], label="Ingresos Reales", color='blue')
    ax5.barh(top_errors['name'], top_errors['predicted_revenue'], label="Ingresos Predichos", color='orange', alpha=0.7)
    ax5.set_xlabel("Ingresos")
    ax5.legend()
    st.pyplot(fig5)
