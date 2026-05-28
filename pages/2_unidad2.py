import streamlit as st
import sympy as sp
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------
# ESTILOS
# ---------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #f4f6f9;
}

h1 {
    color: #003366;
    text-align: center;
    font-size: 42px;
}

h2, h3 {
    color: #004080;
}

.stButton > button {
    background-color: #003366;
    color: white;
    border-radius: 12px;
    height: 50px;
    width: 100%;
    font-size: 17px;
    border: none;
}

.stButton > button:hover {
    background-color: #0059b3;
}

.info-box {
    background-color: #dbeeff;
    padding: 18px;
    border-radius: 10px;
    border-left: 8px solid #003366;
    margin-bottom: 20px;
}

.result-box {
    background-color: #e8ffe8;
    padding: 18px;
    border-radius: 10px;
    border-left: 8px solid green;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# TÍTULO
# ---------------------------------------------------

st.title("📘 Unidad 2")
st.subheader("Interpolación de Lagrange y Newton")

st.markdown("""
<div class='info-box'>

### 📌 Introducción

La interpolación permite construir polinomios que pasan exactamente por una tabla de datos.

### Métodos incluidos:
✅ Interpolación de Lagrange  
✅ Interpolación de Newton

</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# MÉTODO LAGRANGE
# ---------------------------------------------------

def lagrange(puntos):

    x = sp.symbols('x')

    n = len(puntos)

    polinomio = 0

    for i in range(n):

        xi, yi = puntos[i]

        termino = yi

        for j in range(n):

            if i != j:

                xj, _ = puntos[j]

                if xi == xj:

                    raise ValueError("Existen valores x repetidos.")

                termino *= (x - xj)/(xi - xj)

        polinomio += termino

    return polinomio

# ---------------------------------------------------
# MÉTODO NEWTON
# ---------------------------------------------------

def newton(puntos):

    n = len(puntos)

    x_vals = [p[0] for p in puntos]

    y_vals = [p[1] for p in puntos]

    tabla = [[0]*n for _ in range(n)]

    for i in range(n):

        tabla[i][0] = y_vals[i]

    for j in range(1,n):

        for i in range(n-j):

            denominador = x_vals[i+j]-x_vals[i]

            if denominador == 0:

                raise ValueError("Existen valores x repetidos.")

            tabla[i][j] = (
                tabla[i+1][j-1] - tabla[i][j-1]
            ) / denominador

    x = sp.symbols('x')

    polinomio = tabla[0][0]

    prod = 1

    for j in range(1,n):

        prod *= (x - x_vals[j-1])

        polinomio += tabla[0][j]*prod

    return polinomio, tabla

# ---------------------------------------------------
# MENÚ
# ---------------------------------------------------

metodo = st.selectbox(
    "📌 Selecciona método:",
    ["Lagrange", "Newton"]
)

# ---------------------------------------------------
# INFORMACIÓN
# ---------------------------------------------------

if metodo == "Lagrange":

    st.markdown("""
    <div class='info-box'>

    ## 📌 Método de Lagrange

    Construye un polinomio que pasa exactamente por todos los puntos.

    </div>
    """, unsafe_allow_html=True)

    st.latex(r"P(x)=\sum_{i=0}^{n} y_iL_i(x)")

else:

    st.markdown("""
    <div class='info-box'>

    ## 📌 Método de Newton

    Utiliza diferencias divididas para construir el polinomio interpolador.

    </div>
    """, unsafe_allow_html=True)

    st.latex(r"P(x)=f[x_0]+f[x_0,x_1](x-x_0)+...")

# ---------------------------------------------------
# ENTRADA DE DATOS
# ---------------------------------------------------

st.markdown("""
### 🧾 Instrucciones

Ingrese los puntos separados por comas.

### ✏️ Ejemplo:

(0,1),(1,2),(2,5)

""")

puntos_str = st.text_input(
    "Ingrese tabla de puntos",
    "(0,1),(1,2),(2,5)"
)

# ---------------------------------------------------
# BOTÓN
# ---------------------------------------------------

if st.button("🚀 Calcular"):

    try:

        puntos = []

        for par in puntos_str.split("),("):

            par = par.replace("(", "").replace(")", "")

            valores = par.split(",")

            if len(valores) != 2:

                st.error("❌ Formato incorrecto en los puntos.")
                st.warning("Usa el formato: (0,1),(1,2),(2,5)")
                st.stop()

            xi, yi = map(float, valores)

            puntos.append((xi, yi))

        if len(puntos) < 2:

            st.error("❌ Debes ingresar al menos 2 puntos.")
            st.stop()

        xs = [p[0] for p in puntos]

        ys = [p[1] for p in puntos]

        # ---------------------------------------------------
        # LAGRANGE
        # ---------------------------------------------------

        if metodo == "Lagrange":

            polinomio = lagrange(puntos)

            polinomio_simple = sp.expand(polinomio)

            st.markdown("""
            <div class='result-box'>
            <h3>✅ Resultado</h3>
            </div>
            """, unsafe_allow_html=True)

            st.write("### Polinomio sin simplificar")

            st.latex(sp.latex(polinomio))

            st.write("### Polinomio simplificado")

            st.latex(sp.latex(polinomio_simple))

            df = pd.DataFrame(puntos, columns=["x", "y"])

            tab1, tab2 = st.tabs([
                "📊 Tabla de Datos",
                "📈 Gráfica"
            ])

            with tab1:

                st.dataframe(
                    df.style.format(precision=6),
                    use_container_width=True,
                    height=300
                )

            with tab2:

                f_lagrange = sp.lambdify(
                    sp.symbols('x'),
                    polinomio_simple,
                    'numpy'
                )

                X = np.linspace(min(xs), max(xs), 300)

                Y = f_lagrange(X)

                fig, ax = plt.subplots(figsize=(9,5))

                ax.plot(
                    X,
                    Y,
                    linewidth=3,
                    label="Interpolación"
                )

                ax.scatter(
                    xs,
                    ys,
                    s=80,
                    label="Puntos"
                )

                ax.grid(True, linestyle='--', alpha=0.7)

                ax.set_title("Interpolación de Lagrange")

                ax.legend()

                st.pyplot(fig)

        # ---------------------------------------------------
        # NEWTON
        # ---------------------------------------------------

        else:

            polinomio, tabla = newton(puntos)

            polinomio_simple = sp.expand(polinomio)

            st.markdown("""
            <div class='result-box'>
            <h3>✅ Resultado</h3>
            </div>
            """, unsafe_allow_html=True)

            st.write("### Polinomio sin simplificar")

            st.latex(sp.latex(polinomio))

            st.write("### Polinomio simplificado")

            st.latex(sp.latex(polinomio_simple))

            columnas = []

            for i in range(len(tabla)):

                columnas.append(f"Δ{i}")

            df = pd.DataFrame(tabla, columns=columnas)

            tab1, tab2 = st.tabs([
                "📊 Tabla de Diferencias",
                "📈 Gráfica"
            ])

            with tab1:

                st.dataframe(
                    df.style.format(precision=6),
                    use_container_width=True,
                    height=350
                )

            with tab2:

                f_newton = sp.lambdify(
                    sp.symbols('x'),
                    polinomio_simple,
                    'numpy'
                )

                X = np.linspace(min(xs), max(xs), 300)

                Y = f_newton(X)

                fig, ax = plt.subplots(figsize=(9,5))

                ax.plot(
                    X,
                    Y,
                    linewidth=3,
                    label="Interpolación"
                )

                ax.scatter(
                    xs,
                    ys,
                    s=80,
                    label="Puntos"
                )

                ax.grid(True, linestyle='--', alpha=0.7)

                ax.set_title("Interpolación de Newton")

                ax.legend()

                st.pyplot(fig)

    except ValueError as e:

        st.error(f"❌ {e}")

    except:

        st.error("❌ Error en los datos ingresados.")
        st.warning("Verifica el formato correctamente.")

