# # import streamlit as st
# # import google.generativeai as genai
# # import pandas as pd
# # import matplotlib.pyplot as plt
# # import seaborn as sns
# # import numpy as np

# # from config import get_gemini_api_key, APP_TITLE, GEMINI_MODEL

# # # --- Initialize Gemini ---
# # def init_gemini():
# #     """Configure and return the Gemini model."""
# #     api_key = get_gemini_api_key()
# #     genai.configure(api_key=api_key)
# #     model = genai.GenerativeModel(model_name=GEMINI_MODEL)
# #     return model

# # # --- Streamlit App ---
# # def main():
# #     st.set_page_config(page_title=APP_TITLE, layout="wide")
# #     st.title(APP_TITLE)

# #     # Initialize model (cached to avoid re-init on every rerun)
# #     if "model" not in st.session_state:
# #         try:
# #             st.session_state.model = init_gemini()
# #             st.success(f"✅ Connected to {GEMINI_MODEL}")
# #         except ValueError as e:
# #             st.error(str(e))
# #             st.stop()

# #     model = st.session_state.model

# #     # --- Chat Interface ---
# #     if "chat_history" not in st.session_state:
# #         st.session_state.chat_history = []

# #     user_input = st.chat_input("Ask your AI financial advisor...")

# #     # Display chat history
# #     for message in st.session_state.chat_history:
# #         with st.chat_message(message["role"]):
# #             st.markdown(message["content"])

# #     if user_input:
# #         # Display user message
# #         with st.chat_message("user"):
# #             st.markdown(user_input)
# #         st.session_state.chat_history.append({"role": "user", "content": user_input})

# #         # Get model response
# #         with st.chat_message("assistant"):
# #             with st.spinner("Thinking..."):
# #                 response = model.generate_content(user_input)
# #                 reply = response.text
# #                 st.markdown(reply)
# #         st.session_state.chat_history.append({"role": "assistant", "content": reply})

# # if __name__ == "__main__":
# #     main()
# # # ```

# # # **`.gitignore`** (important — add this too)
# # # ```
# # # .env
# # # __pycache__/
# # # *.pyc

# import google.generativeai as genai
# from config import get_gemini_api_key, GEMINI_MODEL

# # --- Initialize Gemini Model ---
# genai.configure(api_key=get_gemini_api_key())
# model = genai.GenerativeModel(model_name=GEMINI_MODEL)


# # ─────────────────────────────────────────────
# # AI Reasoning Module
# # ─────────────────────────────────────────────

# def generate_financial_advice(user_data, analysis_data):
#     """
#     Provides holistic, AI-generated financial advice based on
#     income, savings, debts, and goals.
#     """
#     if user_data['profile'] == "Student":
#         profile_prompt = """
# The user is a Student. They may have limited income, student loans, or part-time work.
# Focus on building good financial habits, managing student debt, and starting small investments.
# """
#     elif user_data['profile'] == "Professional":
#         profile_prompt = """
# The user is a Working Professional with a stable income.
# Focus on optimizing savings, debt reduction, wealth building, and long-term investment strategies.
# """
#     else:
#         profile_prompt = """
# The user is a Business Owner / Freelancer with variable income.
# Focus on income stabilization, tax planning, emergency fund importance, and diversified investments.
# """

#     prompt = f"""
# You are an expert financial advisor. Generate a sectioned, structured, and actionable personal finance plan.

# {profile_prompt}

# User Data:
# - Profile Type: {user_data['profile']}
# - Monthly Income: ₹{user_data['income']}
# - Monthly Expenses: ₹{user_data['expenses']}
# - Total Debts: ₹{user_data['debts']}
# - Existing Savings & Investments: ₹{user_data['existing_savings']}
# - Estimated Monthly Savings: ₹{analysis_data['savings']}
# - Total Net Worth: ₹{analysis_data['total_net_worth']}
# - Debt-to-Income Ratio: {analysis_data['debt_to_income_ratio']*100:.1f}%
# - Savings Ratio: {analysis_data['savings_ratio']*100:.2f}%
# - Financial Goals: {', '.join(user_data['goals'])}
# - Risk Tolerance: {user_data['risk_tolerance']}
# - Recommended Investment Allocation: {analysis_data['recommended_investment_allocation']}

# Important: The user already has ₹{user_data['existing_savings']} in existing savings and investments.
# Consider how best to utilize these existing funds alongside new monthly savings.

# Instructions:
# - Sections with clear headers (e.g., Existing Savings Utilization:, Monthly Savings Strategy:, Debt Plan:, Investment Advice:, Goal Guidance:, Budgeting & Expense Tips:)
# - Include specific advice on how to utilize existing savings
# - Consider if existing savings should be used for debt repayment, emergency fund completion, or goal acceleration
# - Include short, actionable bullet points in each section
# - Tailor advice to the user's profile and risk tolerance
# - Keep tone professional and easy to follow
# - Avoid long paragraphs and executive summaries
# - Do not use markdown, tables, or bold formatting

# Output:
# - Ready-to-read actionable plan that incorporates existing savings
# """
#     try:
#         response = model.generate_content(prompt)
#         return response.text.strip()
#     except Exception as e:
#         return f"Gemini API Error: {e}"


# # ─────────────────────────────────────────────
# # Advanced Goal Oriented Advisor with User Instructions
# # ─────────────────────────────────────────────

# def generate_goal_plan(user_data, analysis_data, user_instructions=""):
#     """
#     Creates specific, step-by-step goal plans (e.g., retirement or education funds).
#     Strictly follows any user-provided custom instructions.
#     """
#     prompt = f"""
# You are a highly experienced and practical financial advisor. Generate a structured, actionable, and goal-specific financial plan that PRIORITIZES and STRICTLY FOLLOWS the user's specific instructions above all other considerations.

# USER'S SPECIFIC INSTRUCTIONS (MUST FOLLOW STRICTLY):
# {user_instructions}

# CRITICAL: The user's instructions above are NON-NEGOTIABLE and must be the PRIMARY FOCUS of this plan. All other financial advice must work AROUND these instructions.

# User Goals: {', '.join(user_data['goals'])}
# Profile Type: {user_data['profile']}
# Monthly Income: ₹{user_data['income']}
# Monthly Expenses: ₹{user_data['expenses']}
# Total Debts: ₹{user_data['debts']}
# Existing Savings & Investments: ₹{user_data['existing_savings']}
# Estimated Monthly Savings: ₹{analysis_data['savings']}
# Total Net Worth: ₹{analysis_data['total_net_worth']}
# Debt-to-Income Ratio: {analysis_data['debt_to_income_ratio']*100:.1f}%
# Savings Ratio: {analysis_data['savings_ratio']*100:.2f}%
# Risk Tolerance: {user_data['risk_tolerance']}
# Recommended Investment Allocation: {analysis_data['recommended_investment_allocation']}

# Existing Savings Available: ₹{user_data['existing_savings']}

# MANDATORY INSTRUCTION FOLLOWING FRAMEWORK:
# 1. FIRST AND FOREMOST: Implement the user's specific instruction exactly as requested
# 2. SECOND: Build the entire financial plan around supporting this instruction
# 3. THIRD: Adjust all other financial aspects to accommodate the instruction
# 4. FOURTH: Ensure the instruction doesn't compromise basic financial security

# Instructions for Advanced Planning:
# - The USER'S INSTRUCTION is YOUR TOP PRIORITY — everything else is secondary
# - Create a mathematically sound plan that implements the user's instruction while maintaining financial stability
# - Calculate exact timelines, amounts, and milestones based on the instruction
# - Show how this instruction accelerates or modifies the original goal achievement
# - Provide contingency plans for potential risks introduced by the instruction
# - Be brutally honest about trade-offs and compromises required

# ORGANIZE OUTPUT INTO THESE EXACT SECTIONS WITH COLONS:

# Instruction Implementation Strategy:
# Detail exactly how the user's specific instruction will be executed step by step

# Financial Impact Analysis:
# Show how this instruction affects all aspects of finances with before/after comparisons

# Revised Goal Timeline:
# Provide exact timeline calculations showing new completion dates and milestones

# Monthly Action Plan:
# Break down monthly financial actions with specific ₹ amounts and allocations

# Resource Allocation Strategy:
# Show how existing savings and monthly income will be distributed to support the instruction

# Risk Assessment & Mitigation:
# Justify potential risks from following this instruction and provide mitigation strategies

# Progress Tracking Framework:
# Define clear metrics and checkpoints to monitor progress

# Contingency Planning:
# Provide alternative scenarios if circumstances change or challenges arise

# Key Success Metrics:
# List the specific numbers and targets that define success

# Next Immediate Actions:
# Provide the first 3-5 actions the user should take immediately

# Output Requirements:
# - Use exactly the section headers provided above with colons
# - Each section must have 3-5 clear, actionable points
# - Include specific calculations and ₹ amounts in every relevant section
# - Show mathematical formulas used for timeline calculations
# - Provide monthly breakdowns with exact dates and amounts
# - Be realistic about challenges while maintaining focus on the user's instruction
# - Use simple, direct language without financial jargon
# - Start each section immediately after the header without blank lines
# - Do not use numbering the points just bullet points
# """
#     try:
#         response = model.generate_content(prompt)
#         return response.text.strip()
#     except Exception as e:
#         return f"Gemini API Error: {e}"


# # ─────────────────────────────────────────────
# # Chatbot Module for Any Query
# # ─────────────────────────────────────────────

# def finance_chatbot_response(user_data, analysis_data, user_query):
#     """
#     Enables interactive, AI-powered conversations for ongoing financial queries.
#     """
#     prompt = f"""
# You are a professional, highly knowledgeable, and practical financial advisor. Respond to the user's question with clear, actionable, and personalized advice based on their financial profile.

# User Profile Details:
# - Profile Type: {user_data['profile']}
# - Monthly Income: ₹{user_data['income']}
# - Monthly Expenses: ₹{user_data['expenses']}
# - Total Debts: ₹{user_data['debts']}
# - Existing Savings & Investments: ₹{user_data['existing_savings']}
# - Estimated Monthly Savings: ₹{analysis_data['savings']}
# - Total Net Worth: ₹{analysis_data['total_net_worth']}
# - Debt-to-Income Ratio: {analysis_data['debt_to_income_ratio']:.2f}
# - Savings Ratio: {analysis_data['savings_ratio']:.2f}
# - Risk Tolerance: {user_data['risk_tolerance']}
# - Recommended Investment Allocation: {analysis_data['recommended_investment_allocation']}
# - Financial Goals: {', '.join(user_data['goals'])}

# User Question: {user_query}

# Instructions for response:
# - First, determine if the question is related to finance, budgeting, savings, debts, investments, or financial goals.
# - If unrelated, respond politely: "I'm a financial advisor, so I can best answer questions about budgeting, savings, debts, investments, and financial planning."
# - Just answer the question, do not add any extra info.
# - Tailor the response specifically to the user's financial profile, risk tolerance, and goals.
# - If the question includes a financial term or abbreviation (e.g., SIP, ROI), briefly define it and explain how it may relate to the user's financial situation.
# - Provide 3-5 actionable points tailored to the user's profile and goals.
# - Include numeric suggestions whenever relevant (e.g., amounts to save, invest, or allocate).
# - Consider how existing savings can be utilized in the response.
# - Keep the tone professional, friendly, and concise.
# - Reference the user's profile, savings, risk tolerance, and goals only if it adds value.
# - Make the answer clear, easy to follow, and directly helpful for financial decision-making.
# - Do not use BOLD words, any markdown formatting along with tables, long paragraphs, and special characters (e.g. _, ~, +, *).

# Output:
# - Clear, actionable, and personalized financial advice.
# """
#     try:
#         if model is None:
#             return "Gemini model not configured. Set GEMINI_API_KEY to use AI responses."
#         response = model.generate_content(prompt)
#         return response.text.strip()
#     except Exception as e:
#         return f"Gemini API Error: {e}"
from google import genai
from google.genai import types
from config import get_gemini_api_key, GEMINI_MODEL

# --- Initialize Gemini Client ---
client = genai.Client(api_key=get_gemini_api_key())


# ─────────────────────────────────────────────
# AI Reasoning Module
# ─────────────────────────────────────────────

def generate_financial_advice(user_data, analysis_data):
    """
    Provides holistic, AI-generated financial advice based on
    income, savings, debts, and goals.
    """
    if user_data['profile'] == "Student":
        profile_prompt = """
The user is a Student. They may have limited income, student loans, or part-time work.
Focus on building good financial habits, managing student debt, and starting small investments.
"""
    elif user_data['profile'] == "Professional":
        profile_prompt = """
The user is a Working Professional with a stable income.
Focus on optimizing savings, debt reduction, wealth building, and long-term investment strategies.
"""
    else:
        profile_prompt = """
The user is a Business Owner / Freelancer with variable income.
Focus on income stabilization, tax planning, emergency fund importance, and diversified investments.
"""

    prompt = f"""
You are an expert financial advisor. Generate a sectioned, structured, and actionable personal finance plan.

{profile_prompt}

User Data:
- Profile Type: {user_data['profile']}
- Monthly Income: ₹{user_data['income']}
- Monthly Expenses: ₹{user_data['expenses']}
- Total Debts: ₹{user_data['debts']}
- Existing Savings & Investments: ₹{user_data['existing_savings']}
- Estimated Monthly Savings: ₹{analysis_data['savings']}
- Total Net Worth: ₹{analysis_data['total_net_worth']}
- Debt-to-Income Ratio: {analysis_data['debt_to_income_ratio']*100:.1f}%
- Savings Ratio: {analysis_data['savings_ratio']*100:.2f}%
- Financial Goals: {', '.join(user_data['goals'])}
- Risk Tolerance: {user_data['risk_tolerance']}
- Recommended Investment Allocation: {analysis_data['recommended_investment_allocation']}

Important: The user already has ₹{user_data['existing_savings']} in existing savings and investments.
Consider how best to utilize these existing funds alongside new monthly savings.

Instructions:
- Sections with clear headers (e.g., Existing Savings Utilization:, Monthly Savings Strategy:, Debt Plan:, Investment Advice:, Goal Guidance:, Budgeting & Expense Tips:)
- Include specific advice on how to utilize existing savings
- Consider if existing savings should be used for debt repayment, emergency fund completion, or goal acceleration
- Include short, actionable bullet points in each section
- Tailor advice to the user's profile and risk tolerance
- Keep tone professional and easy to follow
- Avoid long paragraphs and executive summaries
- Do not use markdown, tables, or bold formatting

Output:
- Ready-to-read actionable plan that incorporates existing savings
"""
    try:
        response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
        return response.text.strip()
    except Exception as e:
        return f"Gemini API Error: {e}"


# ─────────────────────────────────────────────
# Advanced Goal Oriented Advisor with User Instructions
# ─────────────────────────────────────────────

def generate_goal_plan(user_data, analysis_data, user_instructions=""):
    """
    Creates specific, step-by-step goal plans (e.g., retirement or education funds).
    Strictly follows any user-provided custom instructions.
    """
    prompt = f"""
You are a highly experienced and practical financial advisor. Generate a structured, actionable, and goal-specific financial plan that PRIORITIZES and STRICTLY FOLLOWS the user's specific instructions above all other considerations.

USER'S SPECIFIC INSTRUCTIONS (MUST FOLLOW STRICTLY):
{user_instructions}

CRITICAL: The user's instructions above are NON-NEGOTIABLE and must be the PRIMARY FOCUS of this plan. All other financial advice must work AROUND these instructions.

User Goals: {', '.join(user_data['goals'])}
Profile Type: {user_data['profile']}
Monthly Income: ₹{user_data['income']}
Monthly Expenses: ₹{user_data['expenses']}
Total Debts: ₹{user_data['debts']}
Existing Savings & Investments: ₹{user_data['existing_savings']}
Estimated Monthly Savings: ₹{analysis_data['savings']}
Total Net Worth: ₹{analysis_data['total_net_worth']}
Debt-to-Income Ratio: {analysis_data['debt_to_income_ratio']*100:.1f}%
Savings Ratio: {analysis_data['savings_ratio']*100:.2f}%
Risk Tolerance: {user_data['risk_tolerance']}
Recommended Investment Allocation: {analysis_data['recommended_investment_allocation']}

Existing Savings Available: ₹{user_data['existing_savings']}

MANDATORY INSTRUCTION FOLLOWING FRAMEWORK:
1. FIRST AND FOREMOST: Implement the user's specific instruction exactly as requested
2. SECOND: Build the entire financial plan around supporting this instruction
3. THIRD: Adjust all other financial aspects to accommodate the instruction
4. FOURTH: Ensure the instruction doesn't compromise basic financial security

Instructions for Advanced Planning:
- The USER'S INSTRUCTION is YOUR TOP PRIORITY — everything else is secondary
- Create a mathematically sound plan that implements the user's instruction while maintaining financial stability
- Calculate exact timelines, amounts, and milestones based on the instruction
- Show how this instruction accelerates or modifies the original goal achievement
- Provide contingency plans for potential risks introduced by the instruction
- Be brutally honest about trade-offs and compromises required

ORGANIZE OUTPUT INTO THESE EXACT SECTIONS WITH COLONS:

Instruction Implementation Strategy:
Detail exactly how the user's specific instruction will be executed step by step

Financial Impact Analysis:
Show how this instruction affects all aspects of finances with before/after comparisons

Revised Goal Timeline:
Provide exact timeline calculations showing new completion dates and milestones

Monthly Action Plan:
Break down monthly financial actions with specific ₹ amounts and allocations

Resource Allocation Strategy:
Show how existing savings and monthly income will be distributed to support the instruction

Risk Assessment & Mitigation:
Justify potential risks from following this instruction and provide mitigation strategies

Progress Tracking Framework:
Define clear metrics and checkpoints to monitor progress

Contingency Planning:
Provide alternative scenarios if circumstances change or challenges arise

Key Success Metrics:
List the specific numbers and targets that define success

Next Immediate Actions:
Provide the first 3-5 actions the user should take immediately

Output Requirements:
- Use exactly the section headers provided above with colons
- Each section must have 3-5 clear, actionable points
- Include specific calculations and ₹ amounts in every relevant section
- Show mathematical formulas used for timeline calculations
- Provide monthly breakdowns with exact dates and amounts
- Be realistic about challenges while maintaining focus on the user's instruction
- Use simple, direct language without financial jargon
- Start each section immediately after the header without blank lines
- Do not use numbering the points just bullet points
"""
    try:
        response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
        return response.text.strip()
    except Exception as e:
        return f"Gemini API Error: {e}"


# ─────────────────────────────────────────────
# Chatbot Module for Any Query
# ─────────────────────────────────────────────

def finance_chatbot_response(user_data, analysis_data, user_query):
    """
    Enables interactive, AI-powered conversations for ongoing financial queries.
    """
    prompt = f"""
You are a professional, highly knowledgeable, and practical financial advisor. Respond to the user's question with clear, actionable, and personalized advice based on their financial profile.

User Profile Details:
- Profile Type: {user_data['profile']}
- Monthly Income: ₹{user_data['income']}
- Monthly Expenses: ₹{user_data['expenses']}
- Total Debts: ₹{user_data['debts']}
- Existing Savings & Investments: ₹{user_data['existing_savings']}
- Estimated Monthly Savings: ₹{analysis_data['savings']}
- Total Net Worth: ₹{analysis_data['total_net_worth']}
- Debt-to-Income Ratio: {analysis_data['debt_to_income_ratio']:.2f}
- Savings Ratio: {analysis_data['savings_ratio']:.2f}
- Risk Tolerance: {user_data['risk_tolerance']}
- Recommended Investment Allocation: {analysis_data['recommended_investment_allocation']}
- Financial Goals: {', '.join(user_data['goals'])}

User Question: {user_query}

Instructions for response:
- First, determine if the question is related to finance, budgeting, savings, debts, investments, or financial goals.
- If unrelated, respond politely: "I'm a financial advisor, so I can best answer questions about budgeting, savings, debts, investments, and financial planning."
- Just answer the question, do not add any extra info.
- Tailor the response specifically to the user's financial profile, risk tolerance, and goals.
- If the question includes a financial term or abbreviation (e.g., SIP, ROI), briefly define it and explain how it may relate to the user's financial situation.
- Provide 3-5 actionable points tailored to the user's profile and goals.
- Include numeric suggestions whenever relevant (e.g., amounts to save, invest, or allocate).
- Consider how existing savings can be utilized in the response.
- Keep the tone professional, friendly, and concise.
- Reference the user's profile, savings, risk tolerance, and goals only if it adds value.
- Make the answer clear, easy to follow, and directly helpful for financial decision-making.
- Do not use BOLD words, any markdown formatting along with tables, long paragraphs, and special characters (e.g. _, ~, +, *).

Output:
- Clear, actionable, and personalized financial advice.
"""
    try:
        if client is None:
            return "Gemini client not configured. Set GEMINI_API_KEY to use AI responses."
        response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
        return response.text.strip()
    except Exception as e:
        return f"Gemini API Error: {e}"