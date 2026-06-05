"""Recommendation messages for budget results."""

from __future__ import annotations

from src.budget import BudgetResult


def build_recommendations(result: BudgetResult) -> list[str]:
    """Build simple Spanish recommendations from budget indicators."""
    recommendations: list[str] = []

    if result.remaining_money < 0:
        recommendations.append(
            "Tu presupuesto está en déficit. El primer objetivo es reducir gastos "
            "variables o renegociar deudas."
        )

    if result.housing_percentage > 40:
        recommendations.append(
            "Tu alquiler representa una parte alta de tus ingresos."
        )

    if result.debt_percentage > 30:
        recommendations.append(
            "Tus deudas ocupan una parte alta del presupuesto. Revisá vencimientos, "
            "intereses y opciones de renegociación."
        )

    if result.savings_rate < 10 and result.remaining_money >= 0:
        recommendations.append(
            "Tu margen de ahorro es bajo. Intentá separar una parte pequeña apenas "
            "cobrás, aunque sea gradual."
        )

    if not recommendations:
        recommendations.append(
            "Tu presupuesto está balanceado. Intentá construir un fondo de emergencia "
            "equivalente a 1 mes de gastos."
        )

    return recommendations
