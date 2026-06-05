"""Budget calculation logic for Presupuesto Digno."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


RiskLevel = Literal["green", "yellow", "red"]


@dataclass(frozen=True)
class BudgetInput:
    """Monthly income and expense inputs."""

    income: float
    housing: float
    food: float
    transportation: float
    utilities: float
    debt: float
    other: float


@dataclass(frozen=True)
class BudgetResult:
    """Calculated budget indicators."""

    total_expenses: float
    remaining_money: float
    savings_rate: float
    housing_percentage: float
    debt_percentage: float
    risk_level: RiskLevel


def calculate_percentage(amount: float, income: float) -> float:
    """Return amount as a percentage of income, or 0 when income is zero."""
    if income <= 0:
        return 0.0
    return (amount / income) * 100


def determine_risk_level(
    remaining_money: float,
    housing_percentage: float,
    debt_percentage: float,
    savings_rate: float,
) -> RiskLevel:
    """Determine the basic financial risk level from budget indicators."""
    if remaining_money < 0:
        return "red"

    has_warning = (
        housing_percentage > 40
        or debt_percentage > 30
        or savings_rate < 10
    )
    if has_warning:
        return "yellow"

    return "green"


def calculate_budget(data: BudgetInput) -> BudgetResult:
    """Calculate monthly budget indicators from user input."""
    total_expenses = (
        data.housing
        + data.food
        + data.transportation
        + data.utilities
        + data.debt
        + data.other
    )
    remaining_money = data.income - total_expenses
    savings_rate = calculate_percentage(remaining_money, data.income)
    housing_percentage = calculate_percentage(data.housing, data.income)
    debt_percentage = calculate_percentage(data.debt, data.income)
    risk_level = determine_risk_level(
        remaining_money=remaining_money,
        housing_percentage=housing_percentage,
        debt_percentage=debt_percentage,
        savings_rate=savings_rate,
    )

    return BudgetResult(
        total_expenses=total_expenses,
        remaining_money=remaining_money,
        savings_rate=savings_rate,
        housing_percentage=housing_percentage,
        debt_percentage=debt_percentage,
        risk_level=risk_level,
    )
