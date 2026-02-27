# Finance Analysis Module

def analyze_finances(user_data):
    # --- Core Savings & Ratios ---
    savings = max(0, user_data['income'] - user_data['expenses'])

    debt_to_income_ratio = user_data['debts'] / user_data['income'] if user_data['income'] > 0 else 0

    savings_ratio = savings / user_data['income'] if user_data['income'] > 0 else 0

    expense_ratio = user_data['expenses'] / user_data['income'] if user_data['income'] > 0 else 0

    debt_to_savings_ratio = user_data['debts'] / savings if savings > 0 else 0

    investment_capacity = savings * 0.5

    # --- Net Worth ---
    total_net_worth = user_data['existing_savings'] + savings - user_data['debts']

    # --- Emergency Fund ---
    emergency_fund_target = user_data['expenses'] * 6
    emergency_fund_shortfall = max(0, emergency_fund_target - user_data['existing_savings'])
    emergency_fund_monthly = emergency_fund_shortfall / 18

    # --- Risk-Based Investment Allocation ---
    risk = user_data['risk_tolerance'].lower()

    if risk == "low":
        investment_allocation = {
            "High-Interest Savings / RD": investment_capacity * 0.4,
            "Debt Mutual Funds / Bonds": investment_capacity * 0.4,
            "ETFs / Balanced Funds": investment_capacity * 0.2,
        }

    elif risk == "medium":
        investment_allocation = {
            "Stocks / Equity Funds": investment_capacity * 0.3,
            "ETFs / Balanced Funds": investment_capacity * 0.4,
            "Debt Mutual Funds / Bonds": investment_capacity * 0.3,
        }

    elif risk == "high":
        investment_allocation = {
            "Stocks / Equity Funds": investment_capacity * 0.5,
            "ETFs / Balanced Funds": investment_capacity * 0.3,
            "Debt Mutual Funds / Bonds": investment_capacity * 0.2,
        }

    else:
        investment_allocation = {
            "Stocks / Equity Funds": investment_capacity * 0.3,
            "ETFs / Balanced Funds": investment_capacity * 0.4,
            "Debt Mutual Funds / Bonds": investment_capacity * 0.3,
        }

    # --- Alerts ---
    high_debt_alert = debt_to_income_ratio > 0.4

    return {
        "savings": savings,
        "debt_to_income_ratio": debt_to_income_ratio,
        "savings_ratio": savings_ratio,
        "expense_ratio": expense_ratio,
        "debt_to_savings_ratio": debt_to_savings_ratio,
        "investment_capacity": investment_capacity,
        "emergency_fund_target": emergency_fund_target,
        "emergency_fund_shortfall": emergency_fund_shortfall,
        "emergency_fund_monthly": emergency_fund_monthly,
        "total_net_worth": total_net_worth,
        "existing_savings": user_data['existing_savings'],
        "recommended_investment_allocation": investment_allocation,
        "high_debt_alert": high_debt_alert,
    }


# --- Example Usage ---
if __name__ == "__main__":
    sample_user = {
        "income": 80000,
        "expenses": 50000,
        "debts": 20000,
        "existing_savings": 30000,
        "risk_tolerance": "medium",
    }

    result = analyze_finances(sample_user)

    print("=== Financial Analysis Report ===")
    print(f"Monthly Savings:         ₹{result['savings']:,.2f}")
    print(f"Savings Ratio:           {result['savings_ratio']*100:.1f}%")
    print(f"Expense Ratio:           {result['expense_ratio']*100:.1f}%")
    print(f"Debt-to-Income Ratio:    {result['debt_to_income_ratio']*100:.1f}%")
    print(f"Total Net Worth:         ₹{result['total_net_worth']:,.2f}")
    print(f"Investment Capacity:     ₹{result['investment_capacity']:,.2f}")
    print(f"Emergency Fund Target:   ₹{result['emergency_fund_target']:,.2f}")
    print(f"Emergency Fund Shortfall:₹{result['emergency_fund_shortfall']:,.2f}")
    print(f"Monthly Savings Needed:  ₹{result['emergency_fund_monthly']:,.2f}")
    print(f"High Debt Alert:         {'⚠️ Yes' if result['high_debt_alert'] else '✅ No'}")
    print("\n--- Recommended Investment Allocation ---")
    for instrument, amount in result['recommended_investment_allocation'].items():
        print(f"  {instrument}: ₹{amount:,.2f}")