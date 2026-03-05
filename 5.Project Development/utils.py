import re

# ─────────────────────────────────────────────
# Split advice sections
# ─────────────────────────────────────────────

def split_advice_sections(advice_text):
    """
    Splits lengthy AI financial advice into separate (title, html_content) tuples
    for display as individual cards in Streamlit.

    Sections detected:
        Current Financial Health | Existing Savings Utilization |
        Monthly Savings Strategy | Debt Plan | Investment Advice |
        Investment Allocation | Goal Guidance | Budgeting & Expense Tips
    """
    advice_text = advice_text.replace("*", "").replace("{", " ").replace("}", " ")

    pattern = r"(Current Financial Health:|Existing Savings Utilization:|Monthly Savings Strategy:|Debt Plan:|Investment Advice:|Investment Allocation:|Goal Guidance:|Budgeting & Expense Tips:)"

    splits   = re.split(pattern, advice_text)
    sections = []

    for i in range(1, len(splits), 2):
        title   = splits[i].strip()
        content = splits[i + 1].strip()

        if "Current Financial Health" in title:
            content_html = (
                "<p style='margin:0; line-height:1.4em'>"
                + content.replace("\n", "<br>")
                + "</p>"
            )
        else:
            content_html = "<ul style='margin:0; padding-left:18px; line-height:1.4em'>"
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("-"):
                    content_html += f"<li>{line[1:].strip()}</li>"
                elif line:
                    content_html += f"<li>{line}</li>"
            content_html += "</ul>"

        sections.append((title, content_html))

    return sections


# ─────────────────────────────────────────────
# Split goal sections
# ─────────────────────────────────────────────

def split_goal_sections(goal_text):
    """
    Splits goal-oriented AI advice into separate (title, html_content) tuples
    for organised card display in Streamlit.

    Sections detected:
        Instruction Implementation Strategy | Financial Impact Analysis |
        Revised Goal Timeline | Monthly Action Plan |
        Resource Allocation Strategy | Risk Assessment & Mitigation |
        Progress Tracking Framework | Contingency Planning |
        Key Success Metrics | Next Immediate Actions
    """
    goal_text = goal_text.replace("*", "")

    pattern = r"(Instruction Implementation Strategy:|Financial Impact Analysis:|Revised Goal Timeline:|Monthly Action Plan:|Resource Allocation Strategy:|Risk Assessment & Mitigation:|Progress Tracking Framework:|Contingency Planning:|Key Success Metrics:|Next Immediate Actions:)"

    splits   = re.split(pattern, goal_text)
    sections = []

    for i in range(1, len(splits), 2):
        title   = splits[i].strip()
        content = splits[i + 1].strip()

        content_html = "<ul style='margin:0; padding-left:18px; line-height:1.5em'>"
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("-"):
                content_html += f"<li>{line[1:].strip()}</li>"
            elif line:
                content_html += f"<li>{line}</li>"
        content_html += "</ul>"

        sections.append((title, content_html))

    return sections


# ─────────────────────────────────────────────
# Quick test
# ─────────────────────────────────────────────
if __name__ == "__main__":
    sample_advice = """
Current Financial Health:
Your finances are stable with a savings ratio of 37.5% and a moderate debt load.

Existing Savings Utilization:
- Use ₹10,000 of existing savings to top up your emergency fund
- Keep remaining ₹20,000 in a liquid FD for short-term goals

Monthly Savings Strategy:
- Allocate ₹5,000 per month to SIP in an index fund
- Set aside ₹3,000 for emergency fund top-up

Debt Plan:
- Pay an extra ₹2,000 per month towards your loan principal
- Avoid new debt for the next 12 months
"""

    sample_goal = """
Instruction Implementation Strategy:
- Open a dedicated RD account for your house down payment goal
- Automate ₹8,000 monthly transfer on salary day

Financial Impact Analysis:
- Before: ₹0 dedicated to house fund
- After: ₹96,000 saved in 12 months towards down payment

Revised Goal Timeline:
- At ₹8,000/month you will reach ₹5,00,000 in 52 months
- Milestone: ₹1,00,000 by Month 13

Monthly Action Plan:
- Month 1-6: ₹8,000 to RD + ₹2,000 emergency fund
- Month 7-12: Review and increase SIP by ₹1,000
"""

    print("=== Advice Sections ===")
    for title, html in split_advice_sections(sample_advice):
        print(f"\n[{title}]\n{html}")

    print("\n=== Goal Sections ===")
    for title, html in split_goal_sections(sample_goal):
        print(f"\n[{title}]\n{html}")