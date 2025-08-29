import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import numpy as np

# Configuración de la página de Streamlit
st.set_page_config(layout="wide")

st.title('🛒 Optimización de Inventario para Licores Andinos')
st.markdown('---')

@st.cache_data
def load_and_process_data(uploaded_files):
    """
    Carga, combina y procesa los archivos CSV subidos para ventas y compras.
    Devuelve los DataFrames procesados o un mensaje de error.
    """
    if not uploaded_files:
        return None, None, "No se han subido archivos."

    dataframes = {}
    for file in uploaded_files:
        df_name = file.name.rsplit('_part', 1)[0] if '_part' in file.name else file.name.split('.')[0]
        if df_name not in dataframes:
            dataframes[df_name] = []
        try:
            dataframes[df_name].append(pd.read_csv(file))
        except Exception as e:
            return None, None, f"Error al leer el archivo CSV '{file.name}': {e}"
        
    final_dfs = {}
    for name, df_list in dataframes.items():
        final_dfs[name] = pd.concat(df_list, ignore_index=True)

    sales_df = final_dfs.get('SalesFINAL12312016')
    purchases_df = final_dfs.get('PurchasesFINAL12312016')

    if sales_df is None:
        return None, None, "Se requiere el archivo 'SalesFINAL12312016'."
    if purchases_df is None:
        return None, None, "Se requiere el archivo 'PurchasesFINAL12312016'."

    # Procesar el DataFrame de Ventas
    try:
        if 'VendorNo' in sales_df.columns:
            sales_df.rename(columns={'VendorNo': 'VendorNumber'}, inplace=True)
        if 'SalesDate' in sales_df.columns:
            sales_df['SalesDate'] = pd.to_datetime(sales_df['SalesDate'], errors='coerce')
            sales_df.dropna(subset=['SalesDate'], inplace=True)
    except Exception as e:
        return None, None, f"Error al procesar los datos de Ventas: {e}"

    # Procesar el DataFrame de Compras
    try:
        if 'PODate' in purchases_df.columns:
            purchases_df.rename(columns={'PODate': 'PODate'}, inplace=True)
        if 'PODate' in purchases_df.columns:
            purchases_df['PODate'] = pd.to_datetime(purchases_df['PODate'], errors='coerce')
            purchases_df.dropna(subset=['PODate'], inplace=True)
    except Exception as e:
        return None, None, f"Error al procesar los datos de Compras: {e}"

    return sales_df, purchases_df, "Datos cargados y listos."

# Interfaz de usuario para la carga de archivos
st.sidebar.header('Sube tus archivos CSV')
uploaded_files = st.sidebar.file_uploader(
    "Selecciona todas las partes de tus archivos CSV", 
    type="csv", 
    accept_multiple_files=True
)

sales_data, purchases_data, status_message = load_and_process_data(uploaded_files)

if sales_data is None:
    st.warning(status_message)
else:
    st.sidebar.success(status_message)
    st.header('🧹 Paso 1: Datos Listos')
    st.write('Vista previa del DataFrame de Ventas:')
    st.write(sales_data.head())
    st.write(f'Dimensiones de los Datos de Ventas: {sales_data.shape}')

    # ---
    st.markdown('---')
    st.header('📈 Paso 2: Pronóstico de Demanda de la Empresa')
    try:
        # Agrupar por fecha para un pronóstico realista de ventas totales
        df_model = sales_data.copy()
        df_model = df_model.groupby('SalesDate')['SalesDollars'].sum().reset_index()

        df_model['month'] = df_model['SalesDate'].dt.month
        df_model['day_of_week'] = df_model['SalesDate'].dt.dayofweek
        
        df_model.dropna(subset=['month', 'day_of_week', 'SalesDollars'], inplace=True)
        
        features = ['month', 'day_of_week']
        target = 'SalesDollars'
        
        X = df_model[features]
        y = df_model[target]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        rf_model.fit(X_train, y_train)
        y_pred = rf_model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        st.success('Modelo de pronóstico de ventas de la empresa entrenado.')
        st.metric('Error Cuadrático Medio (RMSE)', f'{rmse:.2f}')

        # Sección para el pronóstico
        st.markdown('---')
        st.header('🔮 Paso 2.5: Pronóstico de Demanda')

        # Control para seleccionar el período de proyección
        projection_period = st.selectbox(
            'Selecciona el período de proyección:',
            ('1 semana', '1 mes', '6 meses', '1 año')
        )
        
        period_days = {
            '1 semana': 7,
            '1 mes': 30,
            '6 meses': 180,
            '1 año': 365
        }
        
        num_days_to_predict = period_days[projection_period]

        # Crear un DataFrame para pronosticar
        last_date = sales_data['SalesDate'].max()
        future_dates = pd.date_range(start=last_date, periods=num_days_to_predict + 1, freq='D')[1:]
        
        # Crear un DataFrame para la predicción futura
        future_df = pd.DataFrame({'SalesDate': future_dates})
        future_df['month'] = future_df['SalesDate'].dt.month
        future_df['day_of_week'] = future_df['SalesDate'].dt.dayofweek
        
        # Hacer una predicción
        future_sales_prediction = rf_model.predict(future_df[features])
        
        future_df['Predicted_SalesDollars'] = future_sales_prediction
        
        st.write(f'Ventas totales pronosticadas ($) para los próximos {num_days_to_predict} días (para toda la empresa):')
        st.dataframe(future_df[['SalesDate', 'Predicted_SalesDollars']])

        st.line_chart(future_df.set_index('SalesDate')['Predicted_SalesDollars'])

    except Exception as e:
        st.error(f"Error al ejecutar el modelo de pronóstico. Error: {e}")

    # ---
    st.markdown('---')
    st.header('⚙️ Paso 3: Punto de Reorden Predictivo por Marca')
    try:
        # Mapear números de marca a descripciones para una mejor visualización en el filtro
        brand_map = sales_data.set_index('Brand')['Description'].to_dict()
        available_brands = list(brand_map.keys())
        brand_descriptions = [brand_map.get(b, f"Marca {b}") for b in available_brands]

        selected_description = st.selectbox('Selecciona una marca para pronosticar:', brand_descriptions)
        selected_brand = available_brands[brand_descriptions.index(selected_description)]

        if selected_brand:
            st.write(f"Pronosticando ventas para la marca: **{selected_description}**")
            
            # Preparar datos para el modelo de series de tiempo de la marca seleccionada
            brand_df = sales_data[sales_data['Brand'] == selected_brand].copy()
            brand_df = brand_df.groupby('SalesDate')['SalesQuantity'].sum().reset_index()
            brand_df['month'] = brand_df['SalesDate'].dt.month
            brand_df['day_of_week'] = brand_df['SalesDate'].dt.dayofweek
            
            features_brand = ['month', 'day_of_week']
            target_brand = 'SalesQuantity'
            
            # Entrenar el modelo
            rf_brand_model = RandomForestRegressor(n_estimators=100, random_state=42)
            rf_brand_model.fit(brand_df[features_brand], brand_df[target_brand])

            # Usar las mismas fechas de pronóstico que el pronóstico de demanda de la empresa
            # Asegura que ambos pronósticos están alineados en el tiempo.
            future_dates_brand = pd.date_range(start=sales_data['SalesDate'].max(), periods=8, freq='D')[1:]
            
            future_df_brand = pd.DataFrame({'SalesDate': future_dates_brand})
            future_df_brand['month'] = future_df_brand['SalesDate'].dt.month
            future_df_brand['day_of_week'] = future_df_brand['SalesDate'].dt.dayofweek
            
            # Predecir las ventas futuras
            predicted_quantities = rf_brand_model.predict(future_df_brand[features_brand])
            future_df_brand['Predicted_SalesQuantity'] = predicted_quantities

            st.write('Ventas diarias pronosticadas (unidades) para la próxima semana:')
            st.dataframe(future_df_brand[['SalesDate', 'Predicted_SalesQuantity']])
            
            # Calcular el punto de reorden
            predicted_avg_daily_sales = future_df_brand['Predicted_SalesQuantity'].mean()
            lead_time = st.slider('Tiempo de entrega (días)', 1, 30, 7)
            predictive_rop = predicted_avg_daily_sales * lead_time
            
            col1, col2 = st.columns(2)
            with col1: st.metric('Promedio de Venta Diaria Pronosticada', f'{predicted_avg_daily_sales:.2f} unidades')
            with col2: st.metric('Punto de Reorden Predictivo (ROP)', f'{predictive_rop:.2f} unidades')
            
    except Exception as e:
        st.error(f"Error en el cálculo del Punto de Reorden Predictivo. Error: {e}")
