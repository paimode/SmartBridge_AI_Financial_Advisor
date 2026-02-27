import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np


# ─────────────────────────────────────────────
# Visualization: Detailed Advised Financial Health
# ─────────────────────────────────────────────

def plot_advised_financial_overview(user_data, analysis_data):
    """
    Generates a two-panel figure:
      Left  — Pie chart: Savings & Investment Distribution
      Right — Bar chart: Component-wise Financial Impact
    """
    expenses             = user_data["expenses"]
    savings              = analysis_data["savings"]
    emergency_fund_monthly = analysis_data["emergency_fund_monthly"]

    investment_allocation = analysis_data["recommended_investment_allocation"]
    high_interest = investment_allocation.get("High-Interest Savings / RD", 0)
    stocks        = investment_allocation.get("Stocks / Equity Funds", 0)
    etfs          = investment_allocation.get("ETFs / Balanced Funds", 0)
    risk_free     = investment_allocation.get("Debt Mutual Funds / Bonds", 0)

    total_investments  = high_interest + stocks + etfs + risk_free
    remaining_savings  = max(0, savings - (emergency_fund_monthly + total_investments))

    # ── Labels & Values ──────────────────────────────────────────────────────
    labels = [
        "Monthly Expenses",
        "Emergency Fund (Monthly)",
        "High-Interest Savings / RD",
        "Stocks / Equity Funds",
        "ETFs / Balanced Funds",
        "Debt Mutual Funds / Bonds",
        "Remaining Savings",
    ]

    values = [
        expenses,
        emergency_fund_monthly,
        high_interest,
        stocks,
        etfs,
        risk_free,
        remaining_savings,
    ]

    # Remove zero-value slices for the pie
    filtered = [(l, v) for l, v in zip(labels, values) if v > 0]
    pie_labels, pie_values = zip(*filtered) if filtered else ([], [])

    colors = sns.color_palette("pastel", len(pie_values))

    # ── Figure Setup ─────────────────────────────────────────────────────────
    fig, ax = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor("#F9FAFB")

    # ── LEFT: Pie Chart ───────────────────────────────────────────────────────
    wedges, texts, autotexts = ax[0].pie(
        pie_values,
        labels=None,
        autopct=lambda p: f"{p:.1f}%" if p > 2 else "",
        colors=colors,
        startangle=140,
        pctdistance=0.82,
        wedgeprops=dict(width=0.6, edgecolor="white", linewidth=1.5),
    )

    for text in texts:
        text.set_fontsize(9)
    for autotext in autotexts:
        autotext.set_fontsize(8)
        autotext.set_color("#333333")

    # Legend instead of cramped labels
    ax[0].legend(
        wedges,
        [f"{l}  ₹{v:,.0f}" for l, v in zip(pie_labels, pie_values)],
        loc="upper center",
        bbox_to_anchor=(0.5, -0.05),
        fontsize=8,
        frameon=False,
        ncol=2,
    )

    ax[0].set_title(
        "Savings & Investment Distribution",
        pad=35, fontweight="bold", fontsize=11, color="#222222"
    )

    # ── RIGHT: Bar Chart ──────────────────────────────────────────────────────
    sns.set_style("whitegrid")

    bar_colors = sns.color_palette("pastel", len(labels))
    bars = sns.barplot(
        x=labels,
        y=values,
        palette=bar_colors,
        ax=ax[1],
        edgecolor="white",
        linewidth=1.2,
    )

    ax[1].set_facecolor("#FFFFFF")
    ax[1].grid(axis="y", linestyle="--", alpha=0.5)
    ax[1].set_ylabel("Amount (₹)", fontsize=10, fontweight="bold", color="#222222")
    ax[1].tick_params(axis="x", rotation=90, labelsize=9)
    ax[1].set_title(
        "Component-wise Financial Impact",
        pad=35, fontweight="bold", fontsize=11, color="#222222"
    )

    # Value labels above each bar
    for i, value in enumerate(values):
        ax[1].text(
            i,
            value + (max(values) * 0.01),
            f"₹{value:,.0f}",
            ha="center",
            va="bottom",
            fontsize=7.5,
            color="#444444",
            fontweight="bold",
        )

    plt.tight_layout(rect=[0.05, 0.1, 0.95, 0.95])
    plt.subplots_adjust(wspace=0.4)

    return fig


# ─────────────────────────────────────────────
# Visualization: Income Allocation Pie Chart
# ─────────────────────────────────────────────

def plot_income_allocation(user_data, analysis_data):
    """
    Pie chart comparing income split between expenses, savings, and debts.
    """
    income   = user_data["income"]
    expenses = user_data["expenses"]
    savings  = analysis_data["savings"]
    debts    = user_data["debts"]

    debt_payment = min(debts * 0.1, savings * 0.3)  # estimated monthly debt payment
    investable   = max(0, savings - debt_payment)

    labels = ["Expenses", "Debt Repayment", "Investable Savings"]
    values = [expenses, debt_payment, investable]
    colors = sns.color_palette("Set2", len(labels))

    fig, ax = plt.subplots(figsize=(7, 6))
    fig.patch.set_facecolor("#F9FAFB")

    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        colors=colors,
        startangle=90,
        wedgeprops=dict(edgecolor="white", linewidth=2),
    )

    for text in texts:
        text.set_fontsize(10)
    for autotext in autotexts:
        autotext.set_fontsize(9)
        autotext.set_color("#333333")

    ax.set_title(
        f"Monthly Income Allocation  (Total: ₹{income:,})",
        fontweight="bold", fontsize=12, color="#222222", pad=20
    )

    plt.tight_layout()
    return fig


# ─────────────────────────────────────────────
# Visualization: Debt-to-Income Health Indicator
# ─────────────────────────────────────────────

def plot_debt_health(analysis_data):
    """
    Horizontal stacked bar acting as a ratio gauge for debt-to-income health.
    Green zone ≤ 20%, Yellow 20–40%, Red > 40%.
    """
    ratio   = analysis_data["debt_to_income_ratio"]
    ratio_p = min(ratio * 100, 100)

    fig, ax = plt.subplots(figsize=(8, 2.5))
    fig.patch.set_facecolor("#F9FAFB")
    ax.set_facecolor("#F9FAFB")

    # Background zones
    ax.barh(0, 20,  left=0,  color="#A8D5A2", height=0.5, label="Healthy (≤20%)")
    ax.barh(0, 20,  left=20, color="#FFE082", height=0.5, label="Moderate (20–40%)")
    ax.barh(0, 60,  left=40, color="#EF9A9A", height=0.5, label="High Risk (>40%)")

    # Pointer
    ax.barh(0, 1, left=ratio_p - 0.5, color="#212121", height=0.6, label=f"Your Ratio: {ratio_p:.1f}%")

    ax.set_xlim(0, 100)
    ax.set_ylim(-0.5, 0.8)
    ax.set_xlabel("Debt-to-Income Ratio (%)", fontsize=10, fontweight="bold", color="#222222")
    ax.set_yticks([])
    ax.set_title("Debt-to-Income Health Indicator", fontweight="bold", fontsize=12,
                 color="#222222", pad=15)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.35), ncol=4, fontsize=9, frameon=False)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    plt.tight_layout()
    return fig


# ─────────────────────────────────────────────
# Visualization: Monthly Savings Performance Bar
# ─────────────────────────────────────────────

def plot_savings_performance(user_data, analysis_data):
    """
    Bar graph showing savings breakdown:
    Target Emergency Fund vs. Actual Savings vs. Investment Capacity.
    """
    categories = [
        "Monthly Income",
        "Monthly Expenses",
        "Estimated Savings",
        "Investment Capacity",
        "Emergency Fund\n(Monthly Target)",
    ]
    values = [
        user_data["income"],
        user_data["expenses"],
        analysis_data["savings"],
        analysis_data["investment_capacity"],
        analysis_data["emergency_fund_monthly"],
    ]

    colors = ["#90CAF9", "#EF9A9A", "#A5D6A7", "#FFE082", "#CE93D8"]

    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor("#F9FAFB")
    ax.set_facecolor("#FFFFFF")

    bars = ax.bar(categories, values, color=colors, edgecolor="white", linewidth=1.5, width=0.55)

    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.set_ylabel("Amount (₹)", fontsize=10, fontweight="bold", color="#222222")
    ax.set_title("Monthly Savings Performance Overview",
                 fontweight="bold", fontsize=12, color="#222222", pad=20)
    ax.tick_params(axis="x", labelsize=9)

    for bar, val in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + (max(values) * 0.01),
            f"₹{val:,.0f}",
            ha="center", va="bottom", fontsize=8.5,
            color="#333333", fontweight="bold"
        )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    return fig


# ─────────────────────────────────────────────
# Example / Test
# ─────────────────────────────────────────────
if __name__ == "__main__":
    sample_user = {
        "income": 80000,
        "expenses": 50000,
        "debts": 20000,
        "existing_savings": 30000,
        "risk_tolerance": "medium",
        "profile": "Professional",
        "goals": ["Buy a House", "Retirement"],
    }
    sample_analysis = {
        "savings": 30000,
        "investment_capacity": 15000,
        "emergency_fund_monthly": 2778,
        "emergency_fund_target": 300000,
        "emergency_fund_shortfall": 270000,
        "total_net_worth": 40000,
        "debt_to_income_ratio": 0.25,
        "savings_ratio": 0.375,
        "recommended_investment_allocation": {
            "Stocks / Equity Funds": 9000,
            "ETFs / Balanced Funds": 12000,
            "Debt Mutual Funds / Bonds": 9000,
        },
    }

    fig1 = plot_advised_financial_overview(sample_user, sample_analysis)
    fig2 = plot_income_allocation(sample_user, sample_analysis)
    fig3 = plot_debt_health(sample_analysis)
    fig4 = plot_savings_performance(sample_user, sample_analysis)

    fig1.savefig("overview.png", dpi=150, bbox_inches="tight")
    fig2.savefig("income_allocation.png", dpi=150, bbox_inches="tight")
    fig3.savefig("debt_health.png", dpi=150, bbox_inches="tight")
    fig4.savefig("savings_performance.png", dpi=150, bbox_inches="tight")

    print("Charts saved successfully.")
    plt.show()