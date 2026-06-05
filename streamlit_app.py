"""Aplicacion Streamlit para Presupuesto Digno."""

from __future__ import annotations

import streamlit as st

from src.budget import BudgetInput, calculate_budget
from src.recommendations import build_recommendations


def format_money(value: float) -> str:
    """Format a number as an Argentine-style currency string."""
    return f"$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def render_calculator() -> None:
    """Render the budgeting calculator page."""
    st.header("Calculadora de presupuesto")
    st.write(
        "Completá tus ingresos y gastos mensuales para ver si tu presupuesto está equilibrado."
    )

    with st.form("budget-form"):
        income = st.number_input("Ingreso mensual", min_value=0.0, step=1000.0, value=0.0)
        housing = st.number_input("Alquiler / vivienda", min_value=0.0, step=1000.0, value=0.0)
        food = st.number_input("Comida", min_value=0.0, step=1000.0, value=0.0)
        transportation = st.number_input("Transporte", min_value=0.0, step=500.0, value=0.0)
        utilities = st.number_input("Servicios", min_value=0.0, step=500.0, value=0.0)
        debt = st.number_input("Pago de deudas", min_value=0.0, step=500.0, value=0.0)
        other = st.number_input("Otros gastos", min_value=0.0, step=500.0, value=0.0)
        submitted = st.form_submit_button("Calcular")

    if not submitted:
        st.info("Ingresá tus datos y presioná Calcular para ver el resultado.")
        return

    budget_input = BudgetInput(
        income=income,
        housing=housing,
        food=food,
        transportation=transportation,
        utilities=utilities,
        debt=debt,
        other=other,
    )
    result = calculate_budget(budget_input)
    recommendations = build_recommendations(result)

    color_by_risk = {
        "green": "🟢 Estable",
        "yellow": "🟡 Necesita atención",
        "red": "🔴 Crítico",
    }

    st.subheader("Resultado")
    st.metric("Gastos totales", format_money(result.total_expenses))
    st.metric("Dinero restante", format_money(result.remaining_money))

    col1, col2, col3 = st.columns(3)
    col1.metric("Tasa de ahorro", f"{result.savings_rate:.1f}%")
    col2.metric("Vivienda / ingresos", f"{result.housing_percentage:.1f}%")
    col3.metric("Deuda / ingresos", f"{result.debt_percentage:.1f}%")

    st.markdown(f"**Nivel de riesgo:** {color_by_risk[result.risk_level]}")

    st.subheader("Recomendaciones")
    for recommendation in recommendations:
        st.write(f"- {recommendation}")


def render_tips() -> None:
    """Render beginner-friendly financial education tips."""
    st.header("Consejos financieros básicos")
    st.write("- Anotá todos tus ingresos y gastos durante el mes, aunque sean pequeños.")
    st.write("- Separá los gastos necesarios de los gastos que se pueden ajustar.")
    st.write("- Si tenés deudas, priorizá pagar las que tengan mayor interés o atraso.")
    st.write("- Intentá construir un fondo de emergencia equivalente a 1 mes de gastos.")
    st.write("- Revisá tu presupuesto cada vez que cambien tus ingresos o gastos fijos.")


def render_about() -> None:
    """Render information about the project."""
    st.header("Acerca del proyecto")
    st.write(
        "Presupuesto Digno es un MVP open-source de educación financiera básica. "
        "Su objetivo es ayudar a personas y familias a entender su presupuesto mensual "
        "con una herramienta simple, gratuita y en español."
    )
    st.write(
        "El proyecto no reemplaza asesoramiento financiero profesional. Busca ofrecer "
        "una primera orientación clara para tomar mejores decisiones cotidianas."
    )


def main() -> None:
    """Run the Streamlit app."""
    st.set_page_config(page_title="Presupuesto Digno", page_icon="💰", layout="centered")
    st.title("Presupuesto Digno")
    st.caption("Educación financiera básica, simple y abierta.")

    page = st.sidebar.radio(
        "Secciones",
        ["Calculadora", "Consejos básicos", "Acerca del proyecto"],
    )

    if page == "Calculadora":
        render_calculator()
    elif page == "Consejos básicos":
        render_tips()
    else:
        render_about()


if __name__ == "__main__":
    main()
