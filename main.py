import streamlit as st

st.set_page_config(
    page_title="Proyecto Métodos Numéricos",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# ESTILOS CSS
# -----------------------------

st.markdown("""
<style>

/* Fondo general */
.main {
    background-color: #f4f6f9;
}

/* Títulos */
h1 {
    color: #003366;
    text-align: center;
    font-size: 48px;
    font-weight: bold;
}

h2, h3 {
    color: #004080;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #003366;
}

[data-testid="stSidebar"] * {
    color: white;
}

/* Botones */
.stButton > button {
    background-color: #003366;
    color: white;
    border-radius: 12px;
    height: 50px;
    font-size: 17px;
    width: 100%;
    border: none;
    transition: 0.3s;
}

.stButton > button:hover {
    background-color: #0059b3;
    color: white;
}

/* Tablas */
.stDataFrame {
    border: 2px solid #003366;
    border-radius: 12px;
    overflow: hidden;
}

/* Cajas informativas */
.info-box {
    background-color: #dbeeff;
    padding: 20px;
    border-radius: 12px;
    border-left: 8px solid #003366;
    margin-bottom: 20px;
}

/* Tarjetas */
.card {
    background-color: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    margin-top: 20px;
}

/* Texto */
p {
    font-size: 18px;
}

/* Línea */
hr {
    border: 2px solid #003366;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# PORTADA
# -----------------------------

st.markdown("""
<h1>📘 Proyecto Final</h1>
<h2 style='text-align:center;'>Métodos Numéricos</h2>
""", unsafe_allow_html=True)

st.markdown("---")

# -----------------------------
# INTRODUCCIÓN
# -----------------------------

st.markdown("""
<div class='card'>

## 📌 Descripción del Proyecto

Este sistema fue desarrollado para resolver distintos métodos numéricos vistos durante el curso.

El programa permite:

✅ Resolver ecuaciones no lineales.  
✅ Construir polinomios interpoladores.  
✅ Aproximar integrales numéricamente.  
✅ Visualizar tablas iterativas y gráficas.  

</div>
""", unsafe_allow_html=True)

# -----------------------------
# UNIDADES
# -----------------------------

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown("""
    <div class='card'>

    # 📘 Unidad 1

    ## Métodos:
    
    - Punto Fijo
    - Newton-Raphson

    ### Objetivo:
    
    Resolver ecuaciones y sistemas no lineales mediante procesos iterativos.

    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown("""
    <div class='card'>

    # 📘 Unidad 2

    ## Métodos:
    
    - Interpolación de Lagrange
    - Interpolación de Newton

    ### Objetivo:
    
    Construir polinomios que pasen exactamente por una tabla de datos.

    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown("""
    <div class='card'>

    # 📘 Unidad 3

    ## Métodos:
    
    - Regla Trapezoidal
    - Simpson 1/3
    - Simpson 3/8

    ### Objetivo:
    
    Aproximar el valor de integrales definidas utilizando métodos numéricos.

    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# INSTRUCCIONES
# -----------------------------

st.markdown("---")

st.markdown("""
<div class='info-box'>

# 🧾 Instrucciones de Uso

### Paso 1
Selecciona una unidad desde el menú lateral izquierdo.

### Paso 2
Escoge el método numérico que deseas utilizar.

### Paso 3
Ingresa los datos solicitados.

### Paso 4
Presiona el botón calcular.

### Paso 5
Observa:

✅ Tabla de resultados  
✅ Procedimiento iterativo  
✅ Gráficas  
✅ Resultado final  

</div>
""", unsafe_allow_html=True)

# -----------------------------
# INFORMACIÓN EXTRA
# -----------------------------

st.markdown("""
<div class='card'>

## 📚 Métodos Incluidos

### Unidad 1
- Método de Punto Fijo
- Método de Newton-Raphson

### Unidad 2
- Interpolación de Lagrange
- Interpolación de Newton

### Unidad 3
- Regla Trapezoidal
- Regla de Simpson 1/3
- Regla de Simpson 3/8

</div>
""", unsafe_allow_html=True)

# -----------------------------
# MENSAJE FINAL
# -----------------------------

st.success("✅ Proyecto listo para utilizar.")

st.info("📌 Utiliza el menú lateral para cambiar entre unidades.")