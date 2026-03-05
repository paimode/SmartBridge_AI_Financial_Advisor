# import streamlit as st
# import matplotlib
# matplotlib.use("Agg")

# from finance_analysis import analyze_finances
# from ai_advisor import generate_financial_advice, generate_goal_plan, finance_chatbot_response
# from visualization import (
#     plot_advised_financial_overview,
#     plot_income_allocation,
#     plot_debt_health,
#     plot_savings_performance,
# )
# from utils import split_advice_sections, split_goal_sections

# # ─────────────────────────────────────────────
# # Page Configuration
# # ─────────────────────────────────────────────
# st.set_page_config(
#     page_title="AI Financial Advisor",
#     page_icon="💰",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# # ─────────────────────────────────────────────
# # Load CSS from file
# # ─────────────────────────────────────────────
# def load_css():
#     try:
#         with open("styles.css", "r") as f:
#             css = f.read()
#         st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
#     except FileNotFoundError:
#         # Inline fallback styles if styles.css is not present
#         st.markdown("""
#         <style>
#         .main-header {
#             font-size: 2rem; font-weight: 800;
#             color: #1a1a2e; text-align: center;
#             padding: 1rem 0 0.2rem 0;
#         }
#         .subheader {
#             font-size: 1rem; color: #555;
#             text-align: center; margin-bottom: 1.5rem;
#         }
#         .hero-section {
#             background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
#             border-radius: 16px; padding: 2.5rem 2rem;
#             margin-bottom: 2rem;
#         }
#         .section-card {
#             background: #ffffff; border-radius: 12px;
#             padding: 1.2rem 1.5rem; margin-bottom: 1rem;
#             border-left: 4px solid #0f3460;
#             box-shadow: 0 2px 8px rgba(0,0,0,0.07);
#         }
#         .metric-box {
#             background: #f0f4ff; border-radius: 10px;
#             padding: 1rem; text-align: center;
#         }
#         .alert-danger { color: #c0392b; font-weight: 600; }
#         .alert-success { color: #27ae60; font-weight: 600; }
#         </style>
#         """, unsafe_allow_html=True)

# load_css()

# # ─────────────────────────────────────────────
# # Initialize Session State
# # ─────────────────────────────────────────────
# if "user_data"         not in st.session_state: st.session_state.user_data         = None
# if "analysis_data"     not in st.session_state: st.session_state.analysis_data     = None
# if "generated_advice"  not in st.session_state: st.session_state.generated_advice  = None
# if "goal_plan"         not in st.session_state: st.session_state.goal_plan         = None
# if "chat_history"      not in st.session_state: st.session_state.chat_history      = []
# if "user_query"        not in st.session_state: st.session_state.user_query        = ""

# # ─────────────────────────────────────────────
# # Header Section
# # ─────────────────────────────────────────────
# st.markdown('<div class="main-header">💰 AI Financial Advisor</div>', unsafe_allow_html=True)
# st.markdown('<div class="subheader">Your Personal AI-Powered Financial Planning Assistant</div>', unsafe_allow_html=True)

# st.markdown("""
# <div class="hero-section" style="text-align: center;">
#     <h2 style="color: white; font-size: 2.5rem; margin-bottom: 1rem;">
#         Take Control of Your Financial Future
#     </h2>
#     <p style="font-size: 1.2rem; color: #f0f0f0; margin-bottom: 0.5rem;">
#         Get personalized financial advice, investment strategies, and goal planning powered by AI
#     </p>
# </div>
# """, unsafe_allow_html=True)

# # ─────────────────────────────────────────────
# # Sidebar — User Input
# # ─────────────────────────────────────────────
# with st.sidebar:
#     st.markdown(" ")

#     # ── Profile ──────────────────────────────────────────────────────────────
#     profile = st.selectbox(
#         "👤 Select Profile Type",
#         ["Professional", "Student", "Business Owner / Freelancer"],
#         help="Your profile shapes the advice you receive.",
#     )

#     # ── Profile-Conditional Income Input ─────────────────────────────────────
#     if profile == "Student":
#         income = st.number_input(
#             "💵 Monthly Income / Stipend (₹)",
#             min_value=0,
#             value=15000,
#             step=500,
#             help="Include scholarship, allowance, or stipend amount.",
#         )
#         part_time = st.selectbox(
#             "Do you have part-time income?",
#             ["No", "Yes"],
#             help="Select if you have additional income from part-time work",
#         )
#         if part_time == "Yes":
#             extra_income = st.number_input(
#                 "💼 Part-Time / Freelance Income (₹)",
#                 min_value=0,
#                 value=5000,
#                 step=500,
#                 help="Additional monthly income from part-time or freelance work.",
#             )
#             income += extra_income

#     elif profile == "Professional":
#         income = st.number_input(
#             "💵 Monthly Take-Home Income (₹)",
#             min_value=0,
#             value=80000,
#             step=1000,
#             help="Your net monthly salary after tax and deductions.",
#         )

#     else:  # Business Owner / Freelancer
#         income = st.number_input(
#             "💵 Average Monthly Income (₹)",
#             min_value=0,
#             value=60000,
#             step=1000,
#             help="Use your average monthly earnings over the last 3–6 months.",
#         )

#     # ── Expenses ─────────────────────────────────────────────────────────────
#     expenses = st.number_input(
#         "🛒 Monthly Expenses (₹)",
#         min_value=0,
#         value=50000,
#         step=1000,
#         help="Total of rent, food, transport, subscriptions, and other fixed/variable costs.",
#     )

#     # ── Existing Savings ──────────────────────────────────────────────────────
#     existing_savings = st.number_input(
#         "🏦 Existing Savings & Investments (₹)",
#         min_value=0,
#         value=30000,
#         step=1000,
#         help="Current balance across FDs, savings accounts, mutual funds, etc.",
#     )

#     # ── Debts ─────────────────────────────────────────────────────────────────
#     debts = st.number_input(
#         "💳 Total Outstanding Debts (₹)",
#         min_value=0,
#         value=20000,
#         step=1000,
#         help="Sum of all loans, credit card balances, EMIs, etc.",
#     )

#     # ── Financial Goals (free-text) ───────────────────────────────────────────
#     goals_input = st.text_area(
#         "🎯 Financial Goals",
#         value="Buy a House, Retirement Planning",
#         height=80,
#         help="Enter your goals separated by commas. e.g. Buy a House, Save for Education, Retire Early",
#     )
#     goals = [goal.strip() for goal in goals_input.split(",") if goal.strip()]

#     # ── Risk Tolerance ────────────────────────────────────────────────────────
#     risk_tolerance = st.selectbox(
#         "⚖️ Risk Tolerance",
#         ["Low", "Medium", "High"],
#         index=1,
#         help="Low = safe instruments (FD, bonds). Medium = balanced. High = equity-heavy.",
#     )

#     # Store in session state immediately so other parts can reference it
#     st.session_state.user_data = {
#         "profile":          profile,
#         "income":           income,
#         "expenses":         expenses,
#         "debts":            debts,
#         "existing_savings": existing_savings,
#         "goals":            goals if goals else ["General Savings"],
#         "risk_tolerance":   risk_tolerance,
#     }

#     st.markdown("---")

#     # ── Analyse Button ────────────────────────────────────────────────────────
#     generate_btn = st.button(
#         "Financial Analysis & Advice",
#         use_container_width=True,
#         type="primary",
#     )

# # ─────────────────────────────────────────────
# # On Button Click — Run Analysis
# # ─────────────────────────────────────────────
# if generate_btn:
#     user_data = st.session_state.user_data
#     if user_data["income"] == 0:
#         st.sidebar.error("⚠️ Please enter your monthly income to continue.")
#     elif not user_data["goals"]:
#         st.sidebar.warning("⚠️ Please select at least one financial goal.")
#     else:
#         with st.spinner("🔍 Analysing your finances..."):
#             analysis_data = analyze_finances(user_data)

#         with st.spinner("🤖 Generating AI financial advice..."):
#             generated_advice = generate_financial_advice(user_data, analysis_data)

#         st.session_state.analysis_data    = analysis_data
#         st.session_state.generated_advice = generated_advice
#         st.session_state.goal_plan        = None
#         st.session_state.chat_history     = []  # list of {"user": ..., "bot": ...}

#         st.success("✅ Analysis complete! Scroll down to view your personalised plan.")

# # ─────────────────────────────────────────────
# # MAIN CONTENT AREA
# # ─────────────────────────────────────────────
# if st.session_state.user_data and st.session_state.user_data["income"] > 0:

#     st.markdown("")

#     if st.session_state.analysis_data:
#         ad = st.session_state.analysis_data
#         ud = st.session_state.user_data

#         # ── Key Metrics (4 columns) ───────────────────────────────────────────
#         col1, col2, col3, col4 = st.columns(4)

#         with col1:
#             st.markdown(f"""
#             <div class="section-card" style="text-align:center;">
#                 <div style="font-size:1.8rem;">💰</div>
#                 <div style="font-size:0.85rem; color:#666; margin:4px 0;">Monthly Savings</div>
#                 <div style="font-size:1.5rem; font-weight:800; color:#0f3460;">₹{ad['savings']:,}</div>
#             </div>""", unsafe_allow_html=True)

#         with col2:
#             net_worth_color = "#27ae60" if ad["total_net_worth"] >= 0 else "#c0392b"
#             st.markdown(f"""
#             <div class="section-card" style="text-align:center;">
#                 <div style="font-size:1.8rem;">📈</div>
#                 <div style="font-size:0.85rem; color:#666; margin:4px 0;">Total Net Worth</div>
#                 <div style="font-size:1.5rem; font-weight:800; color:{net_worth_color};">₹{ad['total_net_worth']:,}</div>
#             </div>""", unsafe_allow_html=True)

#         with col3:
#             dti        = ad["debt_to_income_ratio"] * 100
#             dti_color  = "#c0392b" if dti > 40 else "#f39c12" if dti > 20 else "#27ae60"
#             dti_label  = "High Risk ⚠️" if dti > 40 else "Moderate 🔶" if dti > 20 else "Healthy ✅"
#             st.markdown(f"""
#             <div class="section-card" style="text-align:center;">
#                 <div style="font-size:1.8rem;">🏦</div>
#                 <div style="font-size:0.85rem; color:#666; margin:4px 0;">Debt-to-Income Ratio</div>
#                 <div style="font-size:1.5rem; font-weight:800; color:{dti_color};">{dti:.1f}%</div>
#                 <div style="font-size:0.78rem; color:{dti_color};">{dti_label}</div>
#             </div>""", unsafe_allow_html=True)

#         with col4:
#             st.markdown(f"""
#             <div class="section-card" style="text-align:center;">
#                 <div style="font-size:1.8rem;">💼</div>
#                 <div style="font-size:0.85rem; color:#666; margin:4px 0;">Investment Capacity</div>
#                 <div style="font-size:1.5rem; font-weight:800; color:#0f3460;">₹{ad['investment_capacity']:,}</div>
#             </div>""", unsafe_allow_html=True)

#         st.markdown(" ")
#         st.markdown(" ")

#         # ── Secondary Metrics (3 columns) ────────────────────────────────────
#         col1, col2, col3 = st.columns(3)

#         with col1:
#             sr = ad["savings_ratio"] * 100
#             sr_color = "#27ae60" if sr >= 20 else "#f39c12" if sr >= 10 else "#c0392b"
#             st.markdown(f"""
#             <div class="section-card" style="text-align:center;">
#                 <div style="font-size:1.6rem;">📊</div>
#                 <div style="font-size:0.85rem; color:#666; margin:4px 0;">Savings Ratio</div>
#                 <div style="font-size:1.4rem; font-weight:800; color:{sr_color};">{sr:.1f}%</div>
#                 <div style="font-size:0.75rem; color:#888;">{"Great savings rate!" if sr >= 20 else "Try to save more" if sr >= 10 else "Savings need attention"}</div>
#             </div>""", unsafe_allow_html=True)

#         with col2:
#             st.markdown(f"""
#             <div class="section-card" style="text-align:center;">
#                 <div style="font-size:1.6rem;">🆘</div>
#                 <div style="font-size:0.85rem; color:#666; margin:4px 0;">Emergency Fund Gap</div>
#                 <div style="font-size:1.4rem; font-weight:800; color:#e67e22;">₹{ad['emergency_fund_shortfall']:,}</div>
#                 <div style="font-size:0.75rem; color:#888;">Target: ₹{ad['emergency_fund_target']:,}</div>
#             </div>""", unsafe_allow_html=True)

#         with col3:
#             st.markdown(f"""
#             <div class="section-card" style="text-align:center;">
#                 <div style="font-size:1.6rem;">🏠</div>
#                 <div style="font-size:0.85rem; color:#666; margin:4px 0;">Existing Savings</div>
#                 <div style="font-size:1.4rem; font-weight:800; color:#8e44ad;">₹{ud['existing_savings']:,}</div>
#                 <div style="font-size:0.75rem; color:#888;">Available to deploy</div>
#             </div>""", unsafe_allow_html=True)

#         # ── Progress Indicators ───────────────────────────────────────────────
#         st.markdown(" ")
#         st.markdown(" ")
#         st.markdown("#### Financial Health Indicators")

#         col1, col2 = st.columns(2)

#         with col1:
#             # Savings Rate progress bar
#             sr_capped = min(ad["savings_ratio"] * 100, 100)
#             st.markdown("**💰 Savings Rate**")
#             st.progress(sr_capped / 100)
#             st.caption(f"{ad['savings_ratio']*100:.1f}% of income saved  |  Target: 20%+")

#             st.markdown(" ")

#             # Emergency Fund progress bar
#             ef_progress = min(
#                 ud["existing_savings"] / ad["emergency_fund_target"], 1.0
#             ) if ad["emergency_fund_target"] > 0 else 0
#             st.markdown("**🆘 Emergency Fund Coverage**")
#             st.progress(ef_progress)
#             st.caption(f"₹{ud['existing_savings']:,} of ₹{ad['emergency_fund_target']:,} target  ({ef_progress*100:.0f}%)")

#         with col2:
#             # Debt health progress bar (inverted — lower is better)
#             dti_progress = min(dti / 100, 1.0)
#             st.markdown("**🏦 Debt-to-Income Load**")
#             st.progress(dti_progress)
#             st.caption(f"{dti:.1f}% debt load  |  Safe zone: below 40%")

#             st.markdown(" ")

#             # Expense ratio progress bar
#             er = ad["expense_ratio"] * 100
#             st.markdown("**🛒 Expense Ratio**")
#             st.progress(min(er / 100, 1.0))
#             st.caption(f"{er:.1f}% of income on expenses  |  Ideal: below 70%")

#         st.markdown("---")

#         # ── Tabs ─────────────────────────────────────────────────────────────
#         tab1, tab2, tab3, tab4 = st.tabs([
#             "📋 Financial Advice",
#             "🎯 Goal Plan",
#             "📊 Visualizations",
#             "💬 AI Chatbot",
#         ])

#         advice_text = st.session_state.generated_advice

#         # ── Tab 1: Financial Advice ───────────────────────────────────────────
#         with tab1:
#             st.markdown("### 🤖 Your Personalised Financial Plan")
#             if advice_text:
#                 sections = split_advice_sections(advice_text)
#                 if sections:
#                     for title, html in sections:
#                         st.markdown(f"""
#                         <div class="section-card">
#                             <strong style="font-size:1rem; color:#0f3460;">{title}</strong>
#                             <div style="margin-top:0.5rem;">{html}</div>
#                         </div>
#                         """, unsafe_allow_html=True)
#                 else:
#                     st.markdown(advice_text)
#             else:
#                 st.info("Click **Financial Analysis & Advice** in the sidebar to generate your plan.")

#         # ── Tab 2: Goal Plan ──────────────────────────────────────────────────
#         with tab2:
#             st.markdown("### 🎯 Goal-Oriented Financial Plan")
#             user_instructions = st.text_area(
#                 "Any specific instructions? (optional)",
#                 placeholder="e.g. I want to pay off my debt first, then invest aggressively in stocks...",
#                 height=80,
#             )
#             generate_goal_btn = st.button("📌 Generate Goal Plan", type="primary")

#             if generate_goal_btn:
#                 with st.spinner("🤖 Building your goal plan..."):
#                     goal_plan = generate_goal_plan(ud, ad, user_instructions)
#                 st.session_state.goal_plan = goal_plan

#             if st.session_state.goal_plan:
#                 sections = split_goal_sections(st.session_state.goal_plan)
#                 if sections:
#                     for title, html in sections:
#                         st.markdown(f"""
#                         <div class="section-card">
#                             <strong style="font-size:1rem; color:#0f3460;">{title}</strong>
#                             <div style="margin-top:0.5rem;">{html}</div>
#                         </div>
#                         """, unsafe_allow_html=True)
#                 else:
#                     st.markdown(st.session_state.goal_plan)

#         # ── Tab 3: Visualizations ─────────────────────────────────────────────
#         with tab3:
#             st.markdown("### 📊 Financial Visualizations")

#             col1, col2 = st.columns(2)
#             with col1:
#                 st.pyplot(plot_advised_financial_overview(ud, ad))
#             with col2:
#                 st.pyplot(plot_income_allocation(ud, ad))

#             col3, col4 = st.columns(2)
#             with col3:
#                 st.pyplot(plot_debt_health(ad))
#             with col4:
#                 st.pyplot(plot_savings_performance(ud, ad))

#         # ── Tab 4: AI Chatbot ─────────────────────────────────────────────────
#         with tab4:
#             st.markdown("---")
#             st.markdown("""
#             <div style='background: linear-gradient(135deg, #1a1a2e, #0f3460);
#                         border-radius: 12px; padding: 1.2rem 1.8rem; margin-bottom: 1.2rem;'>
#                 <h3 style='color: white; margin: 0; font-size: 1.3rem;'>
#                     💬 AI Financial Advisor Chat
#                 </h3>
#                 <p style='color: #aac4e0; margin: 4px 0 0 0; font-size: 0.9rem;'>
#                     Ask me anything about budgeting, investments, debt, or your financial goals.
#                 </p>
#             </div>
#             """, unsafe_allow_html=True)

#             # Two-column layout: chat (left) | tips (right)
#             chat_col1, chat_col2 = st.columns([2, 1])

#             with chat_col1:
#                 # Scrollable chat history container
#                 chat_container = st.container()
#                 with chat_container:
#                     if not st.session_state.chat_history:
#                         st.markdown("""
#                         <div style='text-align:center; padding: 2rem; color: #aaa;
#                                     background:#f9fafb; border-radius:10px;'>
#                             <div style='font-size:2rem;'>🤖</div>
#                             <p style='margin-top:0.5rem;'>
#                                 Hi! I'm your AI financial advisor.<br>
#                                 Ask me anything about your finances below.
#                             </p>
#                         </div>
#                         """, unsafe_allow_html=True)
#                     else:
#                         for msg in st.session_state.chat_history:
#                             if msg["user"]:
#                                 st.markdown(
#                                     f'<div class="user-message">{msg["user"]}</div>',
#                                     unsafe_allow_html=True,
#                                 )
#                             if msg["bot"]:
#                                 st.markdown(
#                                     f'<div class="bot-message">{msg["bot"]}</div>',
#                                     unsafe_allow_html=True,
#                                 )

#                 st.markdown(" ")

#                 # Chat input area
#                 st.session_state.user_query = st.text_area(
#                     "Your Question",
#                     value=st.session_state.user_query,
#                     placeholder="e.g. Should I invest in SIPs? How can I reduce my debt faster?",
#                     height=100,
#                     label_visibility="collapsed",
#                 )

#                 ask_col1, ask_col2, ask_col3 = st.columns([1, 2, 1])
#                 with ask_col2:
#                     ask_btn = st.button("📨 Send Message", use_container_width=True)

#                 if ask_btn:
#                     if not st.session_state.user_query.strip():
#                         st.warning("Please enter a question before sending.")
#                     elif not st.session_state.user_data or st.session_state.user_data.get("income", 0) == 0:
#                         st.error("Please enter your financial details in the sidebar before using the chatbot.")
#                     elif not st.session_state.analysis_data:
#                         st.error("Please generate your financial analysis first.")
#                     else:
#                         with st.spinner("Analyzing your question..."):
#                             try:
#                                 response = finance_chatbot_response(
#                                     st.session_state.user_data,
#                                     st.session_state.analysis_data,
#                                     st.session_state.user_query,
#                                 )
#                                 st.session_state.chat_history.append({
#                                     "user": st.session_state.user_query,
#                                     "bot": response,
#                                 })
#                                 st.session_state.user_query = ""
#                                 st.rerun()
#                             except Exception as e:
#                                 st.error(f"Chatbot Error: {e}")

#             # Right column — Chat Tips card
#             with chat_col2:
#                 st.markdown("""
#                 <div class='section-card'>
#                     <h4>💡 Chat Tips</h4>
#                     <ul style='font-size: 0.9rem;'>
#                         <li>Ask about investments</li>
#                         <li>Get budgeting advice</li>
#                         <li>Discuss debt management</li>
#                         <li>Plan for specific goals</li>
#                         <li>Understand financial terms</li>
#                     </ul>
#                 </div>
#                 """, unsafe_allow_html=True)

#                 st.markdown("""
#                 <div class='section-card' style='margin-top:1rem;'>
#                     <h4>📌 Sample Questions</h4>
#                     <ul style='font-size: 0.85rem; color:#555;'>
#                         <li>How much should I save monthly?</li>
#                         <li>What is a good SIP amount for me?</li>
#                         <li>Should I pay debt or invest first?</li>
#                         <li>How to build an emergency fund?</li>
#                         <li>What does debt-to-income mean?</li>
#                     </ul>
#                 </div>
#                 """, unsafe_allow_html=True)

# else:
#     # ── Welcome / Landing State ───────────────────────────────────────────────
#     st.markdown("""
#     <div style="text-align:center; padding: 2rem 1rem 1rem 1rem;">
#         <div style="font-size:3rem;">👈</div>
#         <h3 style="color:#444; margin-top:0.5rem;">
#             Fill in your financial details in the sidebar<br>and click
#             <span style="color:#667eea; font-weight:800;">Financial Analysis & Advice</span>
#             to get started.
#         </h3>
#         <p style="color:#888; font-size:0.95rem;">
#             Your personalised AI-powered financial plan will appear here.
#         </p>
#     </div>
#     """, unsafe_allow_html=True)

#     st.markdown("---")

#     # ── About Tool Section ────────────────────────────────────────────────────
#     st.markdown("""
#     <div style='background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%);
#                 border-radius: 16px; padding: 2rem 2.5rem; margin: 1rem 0;'>
#         <h2 style='color: white; font-size: 1.8rem; margin-bottom: 0.5rem;'>
#             🤖 About AI Financial Advisor
#         </h2>
#         <p style='color: #aac4e0; font-size: 1rem; margin-bottom: 0;'>
#             Your intelligent, AI-powered personal finance assistant
#         </p>
#     </div>
#     """, unsafe_allow_html=True)

#     about_c1, about_c2, about_c3 = st.columns(3)

#     with about_c1:
#         st.markdown("""
#         <div class="section-card">
#             <h4 style="color:#667eea;">🎯 Purpose</h4>
#             <p style="font-size:0.9rem; color:#444;">
#                 Empowers individuals to make smarter financial decisions through
#                 AI-generated insights, tailored budgeting strategies, and
#                 goal-oriented investment planning — all in one place.
#             </p>
#         </div>
#         """, unsafe_allow_html=True)

#     with about_c2:
#         st.markdown("""
#         <div class="section-card">
#             <h4 style="color:#667eea;">💡 Use Cases</h4>
#             <ul style="font-size:0.9rem; color:#444; padding-left:16px; line-height:1.8;">
#                 <li>Monthly budget planning</li>
#                 <li>Debt reduction strategies</li>
#                 <li>Investment portfolio advice</li>
#                 <li>Emergency fund planning</li>
#                 <li>Retirement & goal tracking</li>
#             </ul>
#         </div>
#         """, unsafe_allow_html=True)

#     with about_c3:
#         st.markdown("""
#         <div class="section-card">
#             <h4 style="color:#667eea;">🛠️ Technologies</h4>
#             <ul style="font-size:0.9rem; color:#444; padding-left:16px; line-height:1.8;">
#                 <li>Google Gemini 2.5 Flash</li>
#                 <li>Streamlit (UI framework)</li>
#                 <li>Python · Pandas · NumPy</li>
#                 <li>Matplotlib · Seaborn</li>
#                 <li>python-dotenv (env config)</li>
#             </ul>
#         </div>
#         """, unsafe_allow_html=True)

#     st.markdown(" ")

#     feat_c1, feat_c2 = st.columns(2)

#     with feat_c1:
#         st.markdown("""
#         <div class="section-card">
#             <h4 style="color:#667eea;">✨ Key Features</h4>
#             <ul style="font-size:0.9rem; color:#444; padding-left:16px; line-height:1.8;">
#                 <li>Profile-aware financial analysis (Student / Professional / Business)</li>
#                 <li>AI-generated personalised financial plans</li>
#                 <li>Goal-oriented planning with custom instructions</li>
#                 <li>Interactive financial health visualizations</li>
#                 <li>Real-time AI chatbot for financial queries</li>
#                 <li>Debt-to-income health indicators</li>
#                 <li>Emergency fund gap analysis</li>
#             </ul>
#         </div>
#         """, unsafe_allow_html=True)

#     with feat_c2:
#         st.markdown("""
#         <div class="section-card">
#             <h4 style="color:#667eea;">🔒 Privacy & Security</h4>
#             <p style="font-size:0.9rem; color:#444; line-height:1.7;">
#                 All financial data entered is processed locally within your
#                 session and is never stored, shared, or retained after you
#                 close the app. API keys are secured via environment variables
#                 and are never exposed in the interface.
#             </p>
#             <h4 style="color:#667eea; margin-top:1rem;">📊 How It Works</h4>
#             <ol style="font-size:0.9rem; color:#444; padding-left:16px; line-height:1.8;">
#                 <li>Enter your financial profile in the sidebar</li>
#                 <li>Click <strong>Financial Analysis & Advice</strong></li>
#                 <li>Review your AI-generated financial plan</li>
#                 <li>Explore charts, goals & chatbot for deeper insights</li>
#             </ol>
#         </div>
#         """, unsafe_allow_html=True)

#     st.markdown("---")
#     st.markdown("""
#     <div style="text-align:center; padding: 1rem; color: #aaa; font-size: 0.85rem;">
#         Built with ❤️ using Google Gemini AI · Streamlit · Python
#         <br>⚠️ This tool provides AI-generated financial guidance for informational purposes only.
#         Please consult a certified financial advisor for professional advice.
#     </div>
#     """, unsafe_allow_html=True)
import streamlit as st
import matplotlib
matplotlib.use("Agg")

from finance_analysis import analyze_finances
from ai_advisor import generate_financial_advice, generate_goal_plan, finance_chatbot_response
from visualization import (
    plot_advised_financial_overview,
    plot_income_allocation,
    plot_debt_health,
    plot_savings_performance,
)
from utils import split_advice_sections, split_goal_sections

# ─────────────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Financial Advisor",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Load CSS from file
# ─────────────────────────────────────────────
def load_css():
    try:
        with open("styles.css", "r") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        # Inline fallback styles if styles.css is not present
        st.markdown("""
        <style>
        .main-header {
            font-size: 2rem; font-weight: 800;
            color: #1a1a2e; text-align: center;
            padding: 1rem 0 0.2rem 0;
        }
        .subheader {
            font-size: 1rem; color: #555;
            text-align: center; margin-bottom: 1.5rem;
        }
        .hero-section {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            border-radius: 16px; padding: 2.5rem 2rem;
            margin-bottom: 2rem;
        }
        .section-card {
            background: #ffffff; border-radius: 12px;
            padding: 1.2rem 1.5rem; margin-bottom: 1rem;
            border-left: 4px solid #0f3460;
            box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        }
        .metric-box {
            background: #f0f4ff; border-radius: 10px;
            padding: 1rem; text-align: center;
        }
        .alert-danger { color: #c0392b; font-weight: 600; }
        .alert-success { color: #27ae60; font-weight: 600; }
        </style>
        """, unsafe_allow_html=True)

load_css()

# ─────────────────────────────────────────────
# Initialize Session State
# ─────────────────────────────────────────────
if "user_data"         not in st.session_state: st.session_state.user_data         = None
if "analysis_data"     not in st.session_state: st.session_state.analysis_data     = None
if "generated_advice"  not in st.session_state: st.session_state.generated_advice  = None
if "goal_plan"         not in st.session_state: st.session_state.goal_plan         = None
if "chat_history"      not in st.session_state: st.session_state.chat_history      = []
if "user_query"        not in st.session_state: st.session_state.user_query        = ""

# ─────────────────────────────────────────────
# Header Section
# ─────────────────────────────────────────────
st.markdown('<div class="main-header">💰 AI Financial Advisor</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Your Personal AI-Powered Financial Planning Assistant</div>', unsafe_allow_html=True)

st.markdown("""
<div class="hero-section" style="text-align: center;">
    <h2 style="color: white; font-size: 2.5rem; margin-bottom: 1rem;">
        Take Control of Your Financial Future
    </h2>
    <p style="font-size: 1.2rem; color: #f0f0f0; margin-bottom: 0.5rem;">
        Get personalized financial advice, investment strategies, and goal planning powered by AI
    </p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Sidebar — User Input
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(" ")

    # ── Profile ──────────────────────────────────────────────────────────────
    profile = st.selectbox(
        "👤 Select Profile Type",
        ["Professional", "Student", "Business Owner / Freelancer"],
        help="Your profile shapes the advice you receive.",
    )

    # ── Profile-Conditional Income Input ─────────────────────────────────────
    if profile == "Student":
        income = st.number_input(
            "💵 Monthly Income / Stipend (₹)",
            min_value=0,
            value=15000,
            step=500,
            help="Include scholarship, allowance, or stipend amount.",
        )
        part_time = st.selectbox(
            "Do you have part-time income?",
            ["No", "Yes"],
            help="Select if you have additional income from part-time work",
        )
        if part_time == "Yes":
            extra_income = st.number_input(
                "💼 Part-Time / Freelance Income (₹)",
                min_value=0,
                value=5000,
                step=500,
                help="Additional monthly income from part-time or freelance work.",
            )
            income += extra_income

    elif profile == "Professional":
        income = st.number_input(
            "💵 Monthly Take-Home Income (₹)",
            min_value=0,
            value=80000,
            step=1000,
            help="Your net monthly salary after tax and deductions.",
        )

    else:  # Business Owner / Freelancer
        income = st.number_input(
            "💵 Average Monthly Income (₹)",
            min_value=0,
            value=60000,
            step=1000,
            help="Use your average monthly earnings over the last 3–6 months.",
        )

    # ── Expenses ─────────────────────────────────────────────────────────────
    expenses = st.number_input(
        "🛒 Monthly Expenses (₹)",
        min_value=0,
        value=50000,
        step=1000,
        help="Total of rent, food, transport, subscriptions, and other fixed/variable costs.",
    )

    # ── Existing Savings ──────────────────────────────────────────────────────
    existing_savings = st.number_input(
        "🏦 Existing Savings & Investments (₹)",
        min_value=0,
        value=30000,
        step=1000,
        help="Current balance across FDs, savings accounts, mutual funds, etc.",
    )

    # ── Debts ─────────────────────────────────────────────────────────────────
    debts = st.number_input(
        "💳 Total Outstanding Debts (₹)",
        min_value=0,
        value=20000,
        step=1000,
        help="Sum of all loans, credit card balances, EMIs, etc.",
    )

    # ── Financial Goals (free-text) ───────────────────────────────────────────
    goals_input = st.text_area(
        "🎯 Financial Goals",
        value="Buy a House, Retirement Planning",
        height=80,
        help="Enter your goals separated by commas. e.g. Buy a House, Save for Education, Retire Early",
    )
    goals = [goal.strip() for goal in goals_input.split(",") if goal.strip()]

    # ── Risk Tolerance ────────────────────────────────────────────────────────
    risk_tolerance = st.selectbox(
        "⚖️ Risk Tolerance",
        ["Low", "Medium", "High"],
        index=1,
        help="Low = safe instruments (FD, bonds). Medium = balanced. High = equity-heavy.",
    )

    # Store in session state immediately so other parts can reference it
    st.session_state.user_data = {
        "profile":          profile,
        "income":           income,
        "expenses":         expenses,
        "debts":            debts,
        "existing_savings": existing_savings,
        "goals":            goals if goals else ["General Savings"],
        "risk_tolerance":   risk_tolerance,
    }

    st.markdown("---")

    # ── Analyse Button ────────────────────────────────────────────────────────
    generate_btn = st.button(
        "Financial Analysis & Advice",
        use_container_width=True,
        type="primary",
    )

# ─────────────────────────────────────────────
# On Button Click — Run Analysis
# ─────────────────────────────────────────────
if generate_btn:
    user_data = st.session_state.user_data
    if user_data["income"] == 0:
        st.sidebar.error("⚠️ Please enter your monthly income to continue.")
    elif not user_data["goals"]:
        st.sidebar.warning("⚠️ Please select at least one financial goal.")
    else:
        with st.spinner("🔍 Analysing your finances..."):
            analysis_data = analyze_finances(user_data)

        with st.spinner("🤖 Generating AI financial advice..."):
            generated_advice = generate_financial_advice(user_data, analysis_data)

        st.session_state.analysis_data    = analysis_data
        st.session_state.generated_advice = generated_advice
        st.session_state.goal_plan        = None
        st.session_state.chat_history     = []  # list of {"user": ..., "bot": ...}

        st.success("✅ Analysis complete! Scroll down to view your personalised plan.")

# ─────────────────────────────────────────────
# MAIN CONTENT AREA
# ─────────────────────────────────────────────
if st.session_state.user_data and st.session_state.user_data["income"] > 0:

    st.markdown("")

    if st.session_state.analysis_data:
        ad = st.session_state.analysis_data
        ud = st.session_state.user_data

        # ── Key Metrics (4 columns) ───────────────────────────────────────────
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="section-card" style="text-align:center;">
                <div style="font-size:1.8rem;">💰</div>
                <div style="font-size:0.85rem; color:#666; margin:4px 0;">Monthly Savings</div>
                <div style="font-size:1.5rem; font-weight:800; color:#0f3460;">₹{ad['savings']:,}</div>
            </div>""", unsafe_allow_html=True)

        with col2:
            net_worth_color = "#27ae60" if ad["total_net_worth"] >= 0 else "#c0392b"
            st.markdown(f"""
            <div class="section-card" style="text-align:center;">
                <div style="font-size:1.8rem;">📈</div>
                <div style="font-size:0.85rem; color:#666; margin:4px 0;">Total Net Worth</div>
                <div style="font-size:1.5rem; font-weight:800; color:{net_worth_color};">₹{ad['total_net_worth']:,}</div>
            </div>""", unsafe_allow_html=True)

        with col3:
            dti        = ad["debt_to_income_ratio"] * 100
            dti_color  = "#c0392b" if dti > 40 else "#f39c12" if dti > 20 else "#27ae60"
            dti_label  = "High Risk ⚠️" if dti > 40 else "Moderate 🔶" if dti > 20 else "Healthy ✅"
            st.markdown(f"""
            <div class="section-card" style="text-align:center;">
                <div style="font-size:1.8rem;">🏦</div>
                <div style="font-size:0.85rem; color:#666; margin:4px 0;">Debt-to-Income Ratio</div>
                <div style="font-size:1.5rem; font-weight:800; color:{dti_color};">{dti:.1f}%</div>
                <div style="font-size:0.78rem; color:{dti_color};">{dti_label}</div>
            </div>""", unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="section-card" style="text-align:center;">
                <div style="font-size:1.8rem;">💼</div>
                <div style="font-size:0.85rem; color:#666; margin:4px 0;">Investment Capacity</div>
                <div style="font-size:1.5rem; font-weight:800; color:#0f3460;">₹{ad['investment_capacity']:,}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown(" ")
        st.markdown(" ")

        # ── Secondary Metrics (3 columns) ────────────────────────────────────
        col1, col2, col3 = st.columns(3)

        with col1:
            sr = ad["savings_ratio"] * 100
            sr_color = "#27ae60" if sr >= 20 else "#f39c12" if sr >= 10 else "#c0392b"
            st.markdown(f"""
            <div class="section-card" style="text-align:center;">
                <div style="font-size:1.6rem;">📊</div>
                <div style="font-size:0.85rem; color:#666; margin:4px 0;">Savings Ratio</div>
                <div style="font-size:1.4rem; font-weight:800; color:{sr_color};">{sr:.1f}%</div>
                <div style="font-size:0.75rem; color:#888;">{"Great savings rate!" if sr >= 20 else "Try to save more" if sr >= 10 else "Savings need attention"}</div>
            </div>""", unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="section-card" style="text-align:center;">
                <div style="font-size:1.6rem;">🆘</div>
                <div style="font-size:0.85rem; color:#666; margin:4px 0;">Emergency Fund Gap</div>
                <div style="font-size:1.4rem; font-weight:800; color:#e67e22;">₹{ad['emergency_fund_shortfall']:,}</div>
                <div style="font-size:0.75rem; color:#888;">Target: ₹{ad['emergency_fund_target']:,}</div>
            </div>""", unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="section-card" style="text-align:center;">
                <div style="font-size:1.6rem;">🏠</div>
                <div style="font-size:0.85rem; color:#666; margin:4px 0;">Existing Savings</div>
                <div style="font-size:1.4rem; font-weight:800; color:#8e44ad;">₹{ud['existing_savings']:,}</div>
                <div style="font-size:0.75rem; color:#888;">Available to deploy</div>
            </div>""", unsafe_allow_html=True)

        # ── Progress Indicators ───────────────────────────────────────────────
        st.markdown(" ")
        st.markdown(" ")
        st.markdown("#### <span style='color:#7c3aed;'>Financial Health Indicators</span>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            # Savings Rate progress bar
            sr_capped = min(ad["savings_ratio"] * 100, 100)
            #st.markdown("**💰 Savings Rate**")
            st.markdown("<span style='color:#7c3aed; font-weight:700;'>💰 Savings Rate</span>", unsafe_allow_html=True)
            st.progress(sr_capped / 100)
            st.markdown(f"<small style='color:#3b82f6;'>{ad['savings_ratio']*100:.1f}% of income saved  |  Target: 20%+</small>", unsafe_allow_html=True)
            st.markdown(" ")

            # Emergency Fund progress bar
            ef_progress = min(
                ud["existing_savings"] / ad["emergency_fund_target"], 1.0
            ) if ad["emergency_fund_target"] > 0 else 0
            st.markdown("<span style='color:#7c3aed; font-weight:700;'>🆘 Emergency Fund Coverage</span>", unsafe_allow_html=True)
            st.progress(ef_progress)
            st.markdown(f"<small style='color:#3b82f6;'>₹{ud['existing_savings']:,} of ₹{ad['emergency_fund_target']:,} target  ({ef_progress*100:.0f}%)</small>", unsafe_allow_html=True)

        with col2:
            # Debt health progress bar (inverted — lower is better)
            dti_progress = min(dti / 100, 1.0)
            st.markdown("<span style='color:#7c3aed; font-weight:700;'>🏦 Debt-to-Income Load</span>", unsafe_allow_html=True)
            st.progress(dti_progress)
            st.markdown(f"<small style='color:#3b82f6;'>{dti:.1f}% debt load  |  Safe zone: below 40%</small>", unsafe_allow_html=True)

            st.markdown(" ")

            # Expense ratio progress bar
            er = ad["expense_ratio"] * 100
            st.markdown("<span style='color:#7c3aed; font-weight:700;'>🛒 Expense Ratio</span>", unsafe_allow_html=True)
            st.progress(min(er / 100, 1.0))
            st.markdown(f"<small style='color:#3b82f6;'>{er:.1f}% of income on expenses  |  Ideal: below 70%</small>", unsafe_allow_html=True)

        st.markdown("---")

        # ── Tabs ─────────────────────────────────────────────────────────────
        tab1, tab2, tab3, tab4 = st.tabs([
            "📋 Financial Advice",
            "🎯 Goal Plan",
            "📊 Visualizations",
            "💬 AI Chatbot",
        ])

        advice_text = st.session_state.generated_advice

        # ── Tab 1: Financial Advice ───────────────────────────────────────────
        with tab1:
            st.markdown("<h3 style='color:#3b82f6;'>🤖 Your Personalised Financial Plan</h3>", unsafe_allow_html=True)
            if advice_text:
                sections = split_advice_sections(advice_text)
                if sections:
                    for title, html in sections:
                        st.markdown(f"""
                        <div class="section-card">
                            <strong style="font-size:1rem; color:#0f3460;">{title}</strong>
                            <div style="margin-top:0.5rem; color:#0f3460">{html}</div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown(advice_text)
            else:
                st.info("Click **Financial Analysis & Advice** in the sidebar to generate your plan.")

        # ── Tab 2: Goal Plan ──────────────────────────────────────────────────
        with tab2:
            st.markdown("<h3 style='color:#3b82f6;'>🎯 Goal-Oriented Financial Plan</h3>", unsafe_allow_html=True)
            user_instructions = st.text_area(
                "Any specific instructions? (optional)",
                placeholder="e.g. I want to pay off my debt first, then invest aggressively in stocks...",
                height=80,
            )
            generate_goal_btn = st.button("📌 Generate Goal Plan", type="primary")

            if generate_goal_btn:
                with st.spinner("🤖 Building your goal plan..."):
                    goal_plan = generate_goal_plan(ud, ad, user_instructions)
                st.session_state.goal_plan = goal_plan

            if st.session_state.goal_plan:
                sections = split_goal_sections(st.session_state.goal_plan)
                if sections:
                    for title, html in sections:
                        st.markdown(f"""
                        <div class="section-card">
                            <strong style="font-size:1rem; color:#0f3460;">{title}</strong>
                            <div style="margin-top:0.5rem; color:#0f3460">{html}</div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown(st.session_state.goal_plan)

        # ── Tab 3: Visualizations ─────────────────────────────────────────────
        with tab3:
            st.markdown("<h3 style='color:#3b82f6;'>📊 Financial Visualizations</h3>", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.pyplot(plot_advised_financial_overview(ud, ad))
            with col2:
                st.pyplot(plot_income_allocation(ud, ad))

            col3, col4 = st.columns(2)
            with col3:
                st.pyplot(plot_debt_health(ad))
            with col4:
                st.pyplot(plot_savings_performance(ud, ad))

        # ── Tab 4: AI Chatbot ─────────────────────────────────────────────────
        with tab4:
            st.markdown("---")
            st.markdown("""
            <div style='background: linear-gradient(135deg, #1a1a2e, #0f3460);
                        border-radius: 12px; padding: 1.2rem 1.8rem; margin-bottom: 1.2rem;'>
                <h3 style='color: white; margin: 0; font-size: 1.3rem;'>
                    💬 AI Financial Advisor Chat
                </h3>
                <p style='color: #aac4e0; margin: 4px 0 0 0; font-size: 0.9rem;'>
                    Ask me anything about budgeting, investments, debt, or your financial goals.
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Two-column layout: chat (left) | tips (right)
            chat_col1, chat_col2 = st.columns([2, 1])

            with chat_col1:
                # Scrollable chat history container
                chat_container = st.container()
                with chat_container:
                    if not st.session_state.chat_history:
                        st.markdown("""
                        <div style='text-align:center; padding: 2rem; color: #aaa;
                                    background:#f9fafb; border-radius:10px;'>
                            <div style='font-size:2rem;'>🤖</div>
                            <p style='margin-top:0.5rem;'>
                                Hi! I'm your AI financial advisor.<br>
                                Ask me anything about your finances below.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        for msg in st.session_state.chat_history:
                            if msg["user"]:
                                st.markdown(
                                    f'<div class="user-message">{msg["user"]}</div>',
                                    unsafe_allow_html=True,
                                )
                            if msg["bot"]:
                                st.markdown(
                                    f'<div class="bot-message">{msg["bot"]}</div>',
                                    unsafe_allow_html=True,
                                )

                st.markdown(" ")

                # Chat input area
                st.session_state.user_query = st.text_area(
                    "Your Question",
                    value=st.session_state.user_query,
                    placeholder="e.g. Should I invest in SIPs? How can I reduce my debt faster?",
                    height=100,
                    label_visibility="collapsed",
                )

                ask_col1, ask_col2, ask_col3 = st.columns([1, 2, 1])
                with ask_col2:
                    ask_btn = st.button("📨 Send Message", use_container_width=True)

                if ask_btn:
                    if not st.session_state.user_query.strip():
                        st.warning("Please enter a question before sending.")
                    elif not st.session_state.user_data or st.session_state.user_data.get("income", 0) == 0:
                        st.error("Please enter your financial details in the sidebar before using the chatbot.")
                    elif not st.session_state.analysis_data:
                        st.error("Please generate your financial analysis first.")
                    else:
                        with st.spinner("Analyzing your question..."):
                            try:
                                response = finance_chatbot_response(
                                    st.session_state.user_data,
                                    st.session_state.analysis_data,
                                    st.session_state.user_query,
                                )
                                st.session_state.chat_history.append({
                                    "user": st.session_state.user_query,
                                    "bot": response,
                                })
                                st.session_state.user_query = ""
                                st.rerun()
                            except Exception as e:
                                st.error(f"Chatbot Error: {e}")

            # Right column — Chat Tips card
            with chat_col2:
                st.markdown("""
                <div class='section-card'>
                    <h4>💡 Chat Tips</h4>
                    <ul style='font-size: 0.9rem;'>
                        <li>Ask about investments</li>
                        <li>Get budgeting advice</li>
                        <li>Discuss debt management</li>
                        <li>Plan for specific goals</li>
                        <li>Understand financial terms</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("""
                <div class='section-card' style='margin-top:1rem;'>
                    <h4>📌 Sample Questions</h4>
                    <ul style='font-size: 0.85rem; color:#555;'>
                        <li>How much should I save monthly?</li>
                        <li>What is a good SIP amount for me?</li>
                        <li>Should I pay debt or invest first?</li>
                        <li>How to build an emergency fund?</li>
                        <li>What does debt-to-income mean?</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

else:
    # ── Welcome / Landing State ───────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center; padding: 2rem 1rem 1rem 1rem;">
        <div style="font-size:3rem;">👈</div>
        <h3 style="color:#444; margin-top:0.5rem;">
            Fill in your financial details in the sidebar<br>and click
            <span style="color:#667eea; font-weight:800;">Financial Analysis & Advice</span>
            to get started.
        </h3>
        <p style="color:#888; font-size:0.95rem;">
            Your personalised AI-powered financial plan will appear here.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── About Tool Section ────────────────────────────────────────────────────
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%);
                border-radius: 16px; padding: 2rem 2.5rem; margin: 1rem 0;'>
        <h2 style='color: white; font-size: 1.8rem; margin-bottom: 0.5rem;'>
            🤖 About AI Financial Advisor
        </h2>
        <p style='color: #aac4e0; font-size: 1rem; margin-bottom: 0;'>
            Your intelligent, AI-powered personal finance assistant
        </p>
    </div>
    """, unsafe_allow_html=True)

    about_c1, about_c2, about_c3 = st.columns(3)

    with about_c1:
        st.markdown("""
        <div class="section-card">
            <h4 style="color:#667eea;">🎯 Purpose</h4>
            <p style="font-size:0.9rem; color:#444;">
                Empowers individuals to make smarter financial decisions through
                AI-generated insights, tailored budgeting strategies, and
                goal-oriented investment planning — all in one place.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with about_c2:
        st.markdown("""
        <div class="section-card">
            <h4 style="color:#667eea;">💡 Use Cases</h4>
            <ul style="font-size:0.9rem; color:#444; padding-left:16px; line-height:1.8;">
                <li>Monthly budget planning</li>
                <li>Debt reduction strategies</li>
                <li>Investment portfolio advice</li>
                <li>Emergency fund planning</li>
                <li>Retirement & goal tracking</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with about_c3:
        st.markdown("""
        <div class="section-card">
            <h4 style="color:#667eea;">🛠️ Technologies</h4>
            <ul style="font-size:0.9rem; color:#444; padding-left:16px; line-height:1.8;">
                <li>Google Gemini 2.5 Flash</li>
                <li>Streamlit (UI framework)</li>
                <li>Python · Pandas · NumPy</li>
                <li>Matplotlib · Seaborn</li>
                <li>python-dotenv (env config)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(" ")

    feat_c1, feat_c2 = st.columns(2)

    with feat_c1:
        st.markdown("""
        <div class="section-card">
            <h4 style="color:#667eea;">✨ Key Features</h4>
            <ul style="font-size:0.9rem; color:#444; padding-left:16px; line-height:1.8;">
                <li>Profile-aware financial analysis (Student / Professional / Business)</li>
                <li>AI-generated personalised financial plans</li>
                <li>Goal-oriented planning with custom instructions</li>
                <li>Interactive financial health visualizations</li>
                <li>Real-time AI chatbot for financial queries</li>
                <li>Debt-to-income health indicators</li>
                <li>Emergency fund gap analysis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with feat_c2:
        st.markdown("""
        <div class="section-card">
            <h4 style="color:#667eea;">🔒 Privacy & Security</h4>
            <p style="font-size:0.9rem; color:#444; line-height:1.7;">
                All financial data entered is processed locally within your
                session and is never stored, shared, or retained after you
                close the app. API keys are secured via environment variables
                and are never exposed in the interface.
            </p>
            <h4 style="color:#667eea; margin-top:1rem;">📊 How It Works</h4>
            <ol style="font-size:0.9rem; color:#444; padding-left:16px; line-height:1.8;">
                <li>Enter your financial profile in the sidebar</li>
                <li>Click <strong>Financial Analysis & Advice</strong></li>
                <li>Review your AI-generated financial plan</li>
                <li>Explore charts, goals & chatbot for deeper insights</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; padding: 1rem; color: #aaa; font-size: 0.85rem;">
        Built with ❤️ using Google Gemini AI · Streamlit · Python
        <br>⚠️ This tool provides AI-generated financial guidance for informational purposes only.
        Please consult a certified financial advisor for professional advice.
    </div>
    """, unsafe_allow_html=True)