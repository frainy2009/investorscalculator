
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Get2Million Analyzer", layout="wide")
st.title("🏠 Get2Million Real Estate Deal Analyzer")

st.markdown("Use this interactive tool to analyze real estate investments with side-by-side Actual vs Pro Forma projections.")

# Toggle between views
mode = st.radio("View Mode", ["Actual", "Pro Forma"])
is_pro_forma = mode == "Pro Forma"

# Sidebar Inputs
st.sidebar.header("🔢 Property & Financing Info")
sale_price = st.sidebar.number_input("Purchase Price ($)", value=250000)
down_payment_percent = st.sidebar.number_input("Down Payment (%)", value=25.0) / 100
loan_rate = st.sidebar.number_input("Interest Rate (%)", value=6.5) / 100
loan_years = st.sidebar.number_input("Loan Term (Years)", value=30)

st.sidebar.header("🏘️ Rental Income")
unit_count = st.sidebar.number_input("Number of Units", value=3, min_value=1)
rents = []
for i in range(unit_count):
    rent = st.sidebar.number_input(f"Unit {i+1} Rent ($)", value=1200 if not is_pro_forma else 1400)
    rents.append(rent)
gross_rent = sum(rents) * 12

# Operating Expenses
st.sidebar.header("💸 Operating Expenses")
vacancy_rate = st.sidebar.number_input("Vacancy Rate (%)", value=5.0) / 100
taxes = st.sidebar.number_input("Property Taxes ($/year)", value=7200)
insurance = st.sidebar.number_input("Insurance ($/year)", value=1200)
repairs = st.sidebar.number_input("Repairs & Maintenance ($/year)", value=1500)
mgmt_fee_rate = st.sidebar.number_input("Management Fee (%)", value=8.0) / 100
utilities = st.sidebar.number_input("Utilities ($/year)", value=1800)
reserves = st.sidebar.number_input("Reserves ($/year)", value=600)

# Calculations
down_payment = sale_price * down_payment_percent
loan_amount = sale_price - down_payment
monthly_rate = loan_rate / 12
months = loan_years * 12
monthly_pmt = loan_amount * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
annual_debt_service = monthly_pmt * 12

vacancy_loss = gross_rent * vacancy_rate
mgmt_fee = gross_rent * mgmt_fee_rate

expenses = taxes + insurance + repairs + mgmt_fee + utilities + reserves + vacancy_loss
noi = gross_rent - expenses
cash_flow = noi - annual_debt_service
cap_rate = (noi / sale_price) * 100
dcr = noi / annual_debt_service

# Depreciation & Tax Savings
structure_value = sale_price * 0.85
annual_depreciation = structure_value / 27.5
tax_savings = annual_depreciation * 0.24

# Year 1 principal paydown
balance = loan_amount
principal_paid = 0
for _ in range(12):
    interest = balance * monthly_rate
    principal = monthly_pmt - interest
    balance -= principal
    principal_paid += principal

# Appreciation
appreciation_rate = 0.03
value_after_1_year = sale_price * (1 + appreciation_rate)
equity_gain = value_after_1_year - sale_price

# ROI
total_return = cash_flow + tax_savings + principal_paid + equity_gain
total_investment = down_payment
roi = (total_return / total_investment) * 100

# Output
st.subheader("📊 Investment Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Net Operating Income (NOI)", f"${noi:,.0f}")
col2.metric("Cash Flow (Year 1)", f"${cash_flow:,.0f}")
col3.metric("Cap Rate", f"{cap_rate:.2f}%")

col4, col5, col6 = st.columns(3)
col4.metric("DCR", f"{dcr:.2f}")
col5.metric("Tax Savings", f"${tax_savings:,.0f}")
col6.metric("Principal Paid", f"${principal_paid:,.0f}")

col7, col8, col9 = st.columns(3)
col7.metric("Equity from Appreciation", f"${equity_gain:,.0f}")
col8.metric("Total ROI", f"${total_return:,.0f}")
col9.metric("ROI %", f"{roi:.2f}%")

# Rent Growth Table
st.subheader("📈 Rent Growth Projection")
rent_growth_rate = st.number_input("Annual Rent Growth Rate (%)", value=3.0) / 100
years = np.arange(1, 11)
rent_growth = np.array(sum(rents)) * ((1 + rent_growth_rate) ** (years - 1))
rent_df = pd.DataFrame({
    "Year": years,
    "Total Monthly Rent": rent_growth.round(2),
    "Total Annual Rent": (rent_growth * 12).round(2)
})
st.dataframe(rent_df)
