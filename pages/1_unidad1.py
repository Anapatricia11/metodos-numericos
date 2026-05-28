import streamlit as st
import sympy as sp
import pandas as pd
import matplotlib.pyplot as plt

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

.error-box {
    background-color: #ffe6e6;
    padding: 18px;
    border-radius: 10px;
    border-left: 8px solid red;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# TÍTULO
# ---------------------------------------------------

st.title("📘 Unidad 1")
st.subheader("Método de Punto Fijo y Newton-Raphson")

st.markdown("""
<div class='info-box'>

### 📌 Introducción

En esta unidad se estudian métodos iterativos para resolver ecuaciones no lineales.

### Métodos incluidos:
✅ Método de Punto Fijo  
✅ Método de Newton-Raphson para sistemas

</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# PUNTO FIJO
# ---------------------------------------------------

def punto_fijo(f_str, g_str, x0, iteraciones):

    try:

        x = sp.symbols('x')

        f = sp.sympify(f_str)

        g = sp.sympify(g_str)

    except:

        st.error("❌ Error al interpretar las funciones.")
        st.warning("Verifica la sintaxis matemática.")
        return

    resultados = []

    try:

        for i in range(iteraciones):

            x1 = g.subs(x, x0).evalf()

            if x1.is_real == False:
                st.error("❌ El método generó números complejos.")
                return

            error = abs(x1 - x0)

            resultados.append([
                i + 1,
                round(float(x0), 6),
                round(float(f.subs(x, x0)), 6),
                round(float(g.subs(x, x0)), 6),
                round(float(x1), 6),
                round(float(error), 6)
            ])

            x0 = x1

    except ZeroDivisionError:

        st.error("❌ División entre cero detectada.")
        return

    except:

        st.error("❌ Error durante las iteraciones.")
        return

    df = pd.DataFrame(resultados, columns=[
        "Iteración",
        "xᵢ",
        "f(xᵢ)",
        "g(xᵢ)",
        "xᵢ₊₁",
        "Error"
    ])

    st.markdown("""
    <div class='result-box'>
    <h3>✅ Resultado Final</h3>
    </div>
    """, unsafe_allow_html=True)

    st.success(f"Aproximación final: {round(float(x1),6)}")

    st.info(f"Después de {iteraciones} iteraciones el método converge aproximadamente a {round(float(x1),6)}")

    tab1, tab2 = st.tabs(["📊 Tabla de Iteraciones", "📈 Gráfica"])

    with tab1:

        st.dataframe(
            df.style.format(precision=6),
            use_container_width=True,
            height=420
        )

    with tab2:

        fig, ax = plt.subplots(figsize=(9,5))

        ax.plot(
            df["Iteración"],
            df["xᵢ₊₁"],
            marker='o',
            linewidth=3,
            markersize=8
        )

        ax.grid(True, linestyle='--', alpha=0.7)

        ax.set_title("Convergencia del Método de Punto Fijo")

        ax.set_xlabel("Iteración")

        ax.set_ylabel("Valor Aproximado")

        st.pyplot(fig)

# ---------------------------------------------------
# NEWTON RAPHSON
# ---------------------------------------------------

def newton_sistema(f1_str, f2_str, x0, y0, iteraciones):

    try:

        x, y = sp.symbols('x y')

        f1 = sp.sympify(f1_str)

        f2 = sp.sympify(f2_str)

    except:

        st.error("❌ Error al interpretar las ecuaciones.")
        return

    try:

        F = sp.Matrix([f1, f2])

        J = F.jacobian([x, y])

    except:

        st.error("❌ Error al calcular la Jacobiana.")
        return

    resultados = []

    errores = []

    try:

        for i in range(iteraciones):

            F_val = F.subs({x:x0, y:y0}).evalf()

            J_val = J.subs({x:x0, y:y0}).evalf()

            if J_val.det() == 0:

                st.error("❌ La Jacobiana no tiene inversa.")
                return

            delta = J_val.inv() * F_val

            x1 = x0 - delta[0]

            y1 = y0 - delta[1]

            error = float(sp.sqrt((x1-x0)**2 + (y1-y0)**2))

            resultados.append([
                i + 1,
                round(float(x0),6),
                round(float(y0),6),
                round(float(x1),6),
                round(float(y1),6),
                round(error,6)
            ])

            errores.append(error)

            x0, y0 = x1, y1

    except:

        st.error("❌ Error durante el procedimiento.")
        return

    df = pd.DataFrame(resultados, columns=[
        "Iteración",
        "x",
        "y",
        "x nuevo",
        "y nuevo",
        "Error"
    ])

    st.markdown("""
    <div class='result-box'>
    <h3>✅ Resultado Final</h3>
    </div>
    """, unsafe_allow_html=True)

    st.success(f"x = {round(float(x1),6)}")

    st.success(f"y = {round(float(y1),6)}")

    st.write("### Jacobiana")

    st.latex(sp.latex(J))

    tab1, tab2 = st.tabs(["📊 Tabla de Iteraciones", "📈 Gráfica"])

    with tab1:

        st.dataframe(
            df.style.format(precision=6),
            use_container_width=True,
            height=420
        )

    with tab2:

        fig, ax = plt.subplots(figsize=(9,5))

        ax.plot(
            range(1, iteraciones+1),
            errores,
            marker='o',
            linewidth=3,
            markersize=8
        )

        ax.grid(True, linestyle='--', alpha=0.7)

        ax.set_title("Convergencia del Error")

        ax.set_xlabel("Iteración")

        ax.set_ylabel("Error")

        st.pyplot(fig)

# ---------------------------------------------------
# MENÚ
# ---------------------------------------------------

metodo = st.selectbox(
    "📌 Selecciona método:",
    ["Punto Fijo", "Newton-Raphson"]
)

# ---------------------------------------------------
# PUNTO FIJO
# ---------------------------------------------------

if metodo == "Punto Fijo":

    st.markdown("""
    <div class='info-box'>

    ## 📌 Método de Punto Fijo

    Fórmula utilizada:

    </div>
    """, unsafe_allow_html=True)

    st.latex(r"x_{n+1}=g(x_n)")

    f = st.text_input("Ingrese f(x)", "x**2 - 4")

    g = st.text_input("Ingrese g(x)", "(x+4)/10")

    x0 = st.number_input("Valor inicial", value=1.0)

    it = st.number_input("Iteraciones", min_value=1, value=10)

    if st.button("🚀 Calcular Punto Fijo"):

        punto_fijo(f, g, x0, int(it))

# ---------------------------------------------------
# NEWTON
# ---------------------------------------------------

else:

    st.markdown("""
    <div class='info-box'>

    ## 📌 Método de Newton-Raphson

    Fórmula utilizada:

    </div>
    """, unsafe_allow_html=True)

    st.latex(r"X_{n+1}=X_n-J^{-1}(X_n)F(X_n)")

    f1 = st.text_input("Ingrese f1(x,y)", "x**2 + y**2 - 4")

    f2 = st.text_input("Ingrese f2(x,y)", "x - y")

    x0 = st.number_input("Ingrese x0", value=2.0)

    y0 = st.number_input("Ingrese y0", value=1.0)

    it = st.number_input("Iteraciones ", min_value=1, value=10)

    if st.button("🚀 Calcular Newton-Raphson"):

        newton_sistema(f1, f2, x0, y0, int(it))

