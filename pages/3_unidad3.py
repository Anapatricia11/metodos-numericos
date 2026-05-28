import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

# ---------------------------------------------------
# CONFIGURACIÓN
# ---------------------------------------------------

st.set_page_config(
    page_title="Unidad 3",
    page_icon="📘",
    layout="wide"
)

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

st.title("📘 Unidad 3")
st.subheader("Integración Numérica")

st.markdown("""
<div class='info-box'>

### 📌 Introducción

Los métodos de integración numérica permiten aproximar integrales definidas.

### Métodos incluidos

✅ Regla Trapezoidal  
✅ Simpson 1/3  
✅ Simpson 3/8

</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# MÉTODO
# ---------------------------------------------------

metodo = st.selectbox(
    "📌 Selecciona método:",
    ["Trapecio", "Simpson 1/3", "Simpson 3/8"]
)

# ---------------------------------------------------
# FÓRMULAS
# ---------------------------------------------------

if metodo == "Trapecio":

    st.latex(
        r"\int_a^b f(x)dx \approx \frac{h}{2}[f(x_0)+2\sum f(x_i)+f(x_n)]"
    )

elif metodo == "Simpson 1/3":

    st.latex(
        r"\int_a^b f(x)dx \approx \frac{h}{3}[f(x_0)+4\sum f(x_i)+2\sum f(x_i)+f(x_n)]"
    )

else:

    st.latex(
        r"\int_a^b f(x)dx \approx \frac{3h}{8}[f(x_0)+3\sum f(x_i)+2\sum f(x_i)+f(x_n)]"
    )

# ---------------------------------------------------
# TIPO DE ENTRADA
# ---------------------------------------------------

tipo = st.radio(
    "📌 Tipo de entrada",
    ["Tabla de datos", "Función matemática"]
)

# ---------------------------------------------------
# TABLA DE DATOS
# ---------------------------------------------------

if tipo == "Tabla de datos":

    st.markdown("""
    ### ✏️ Ejemplo

    (0,0),(1,1),(2,4),(3,9)
    """)

    puntos_str = st.text_input(
        "Ingrese tabla de puntos",
        "(0,0),(1,1),(2,4),(3,9)"
    )

# ---------------------------------------------------
# FUNCIÓN
# ---------------------------------------------------

else:

    st.markdown("""
    ### ✏️ Ejemplo de función

    1/sqrt(4+x**3)
    """)

    funcion_str = st.text_input(
        "Ingrese f(x)",
        "1/sqrt(4+x**3)"
    )

    a = st.number_input(
        "Límite inferior",
        value=0.0
    )

    b = st.number_input(
        "Límite superior",
        value=4.0
    )

    n = st.number_input(
        "Número de intervalos",
        min_value=1,
        value=4
    )

# ---------------------------------------------------
# BOTÓN
# ---------------------------------------------------

if st.button("🚀 Calcular"):

    try:

        # ---------------------------------------------------
        # GENERAR DATOS
        # ---------------------------------------------------

        if tipo == "Tabla de datos":

            puntos = []

            for par in puntos_str.split("),("):

                par = par.replace("(", "").replace(")", "")

                xi, yi = map(float, par.split(","))

                puntos.append((xi, yi))

            xs = [p[0] for p in puntos]
            ys = [p[1] for p in puntos]

        else:

            x = sp.symbols('x')

            funcion = sp.sympify(funcion_str)

            f = sp.lambdify(x, funcion, 'numpy')

            xs = np.linspace(a, b, n+1)

            ys = [float(f(valor)) for valor in xs]

        # ---------------------------------------------------
        # VALIDAR
        # ---------------------------------------------------

        if len(xs) < 2:

            st.error("❌ Debes ingresar más puntos.")
            st.stop()

        h = xs[1] - xs[0]

        coeficientes = []

        # ---------------------------------------------------
        # TRAPECIO
        # ---------------------------------------------------

        if metodo == "Trapecio":

            for i in range(len(xs)):

                if i == 0 or i == len(xs)-1:
                    coeficientes.append(1)
                else:
                    coeficientes.append(2)

            factor = h / 2

        # ---------------------------------------------------
        # SIMPSON 1/3
        # ---------------------------------------------------

        elif metodo == "Simpson 1/3":

            if (len(xs)-1) % 2 != 0:

                st.error("❌ Simpson 1/3 requiere número par de intervalos.")
                st.stop()

            for i in range(len(xs)):

                if i == 0 or i == len(xs)-1:
                    coeficientes.append(1)

                elif i % 2 == 1:
                    coeficientes.append(4)

                else:
                    coeficientes.append(2)

            factor = h / 3

        # ---------------------------------------------------
        # SIMPSON 3/8
        # ---------------------------------------------------

        else:

            if (len(xs)-1) % 3 != 0:

                st.warning(
                    "⚠ Se aplicará Simpson 3/8 + Trapecio automáticamente."
                )

                xs_simpson = xs[:4]
                ys_simpson = ys[:4]

                xs_trap = xs[3:]
                ys_trap = ys[3:]

                parte1 = (3*h/8) * (
                    ys_simpson[0]
                    + 3*ys_simpson[1]
                    + 3*ys_simpson[2]
                    + ys_simpson[3]
                )

                parte2 = (h/2) * (
                    ys_trap[0]
                    + ys_trap[1]
                )

                resultado = parte1 + parte2

                factor = "Combinado"

                coeficientes = [1,3,3,1]

                while len(coeficientes) < len(xs):
                    coeficientes.append(1)

            else:

                for i in range(len(xs)):

                    if i == 0 or i == len(xs)-1:
                        coeficientes.append(1)

                    elif i % 3 == 0:
                        coeficientes.append(2)

                    else:
                        coeficientes.append(3)

                factor = (3*h) / 8

        # ---------------------------------------------------
        # PRODUCTOS
        # ---------------------------------------------------

        productos = [
            coeficientes[i] * ys[i]
            for i in range(len(xs))
        ]

        suma_total = sum(productos)

        # ---------------------------------------------------
        # RESULTADO
        # ---------------------------------------------------

        if factor != "Combinado":

            resultado = factor * suma_total

        # ---------------------------------------------------
        # TABLA
        # ---------------------------------------------------

        tabla = pd.DataFrame({

            "i": list(range(len(xs))),
            "xi": np.round(xs,6),
            "f(xi)": np.round(ys,6),
            "Coeficiente": coeficientes,
            "Coef*f(xi)": np.round(productos,6)

        })

        tabla.loc["Suma"] = [
            "",
            "",
            "",
            "",
            round(suma_total,6)
        ]

        # ---------------------------------------------------
        # RESULTADOS
        # ---------------------------------------------------

        st.markdown("""
        <div class='result-box'>
        <h3>✅ Resultado Final</h3>
        </div>
        """, unsafe_allow_html=True)

        st.success(f"Resultado numérico = {round(resultado,6)}")

        st.info(f"h = {round(h,6)}")

        st.write("### Sustitución Numérica")

        if factor != "Combinado":

            st.write(
                f"Resultado = {round(factor,6)} × {round(suma_total,6)}"
            )

        else:

            st.write(
                "Resultado usando Simpson 3/8 + Trapecio."
            )

        # ---------------------------------------------------
        # TABS
        # ---------------------------------------------------

        tab1, tab2 = st.tabs([
            "📊 Tabla del Método",
            "📈 Gráfica"
        ])

        # ---------------------------------------------------
        # TABLA
        # ---------------------------------------------------

        with tab1:

            st.dataframe(
                tabla,
                use_container_width=True,
                height=450
            )

        # ---------------------------------------------------
        # GRÁFICA
        # ---------------------------------------------------

        with tab2:

            fig, ax = plt.subplots(figsize=(9,5))

            ax.plot(
                xs,
                ys,
                marker='o',
                linewidth=3
            )

            ax.fill_between(
                xs,
                ys,
                alpha=0.3
            )

            ax.grid(True)

            ax.set_title(f"Método {metodo}")

            ax.set_xlabel("x")

            ax.set_ylabel("f(x)")

            st.pyplot(fig)

    except Exception as e:

        st.error(f"❌ Error: {e}")



