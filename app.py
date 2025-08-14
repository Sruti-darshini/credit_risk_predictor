import os
import threading
import time
import streamlit as st
import pandas as pd
import numpy as np
from model import CreditRiskModel
from preprocessing import preprocess_input

def _start_idle_shutdown_monitor():
    # Periodically check if there are any active sessions; if none, exit the process.
    # Uses Streamlit's runtime to enumerate sessions.
    def _monitor():
        try:
            from streamlit.runtime.scriptrunner import get_script_run_ctx
            from streamlit.runtime.runtime import Runtime
        except Exception:
            return
        # Give the app time to start
        time.sleep(5)
        while True:
            try:
                runtime = Runtime.instance()
                has_sessions = False
                if runtime is not None:
                    session_infos = list(runtime._session_mgr.list_active_session_infos())
                    has_sessions = len(session_infos) > 0
                # If no sessions or the current script context is gone, exit.
                ctx = None
                try:
                    ctx = get_script_run_ctx()
                except Exception:
                    pass
                if (not has_sessions) or (ctx is None):
                    os._exit(0)
            except Exception:
                pass
            time.sleep(10)
    t = threading.Thread(target=_monitor, name="st-idle-shutdown", daemon=True)
    t.start()

def main():
    _start_idle_shutdown_monitor()
    
    st.set_page_config(
        page_title="Credit Risk Analysis",
        page_icon="📊",
        layout="wide"
    )

    st.title("Credit Risk Analysis")
    st.write("Enter customer details to assess credit risk")

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Make Prediction", "About"])

    if page == "Make Prediction":
        show_prediction_page()
    else:
        show_about_page()

def show_about_page():
    st.header("About")
    st.write("""
    This application predicts credit risk based on customer information.
    It uses machine learning models to assess the likelihood of loan default.
    """)

def show_prediction_page():
    # Create two columns for better layout
    col1, col2 = st.columns(2)

    with col1:
        st.header("Customer Information")
        
        # Personal Information
        st.subheader("Personal Details")
        age = st.number_input("Age", min_value=18, max_value=100, value=25)
        income = st.number_input("Annual Income ($)", min_value=0, value=50000)
        
        # Home Ownership
        home_ownership = st.selectbox(
            "Home Ownership",
            ["RENT", "MORTGAGE", "OWN", "OTHER"]
        )
        
        # Employment
        emp_length = st.number_input("Employment Length (years)", min_value=0, max_value=50, value=5)
        
        # Loan Information
        st.subheader("Loan Details")
        loan_intent = st.selectbox(
            "Loan Purpose",
            ["PERSONAL", "EDUCATION", "MEDICAL", "VENTURE", "HOMEIMPROVEMENT", "DEBTCONSOLIDATION"]
        )
        
        loan_amnt = st.number_input("Loan Amount ($)", min_value=100, value=10000)
        
        # Credit Information
        st.subheader("Credit Information")
        cb_person_cred_hist_length = st.number_input("Credit History Length (years)", min_value=0, max_value=50, value=3)
        cb_person_default_on_file = st.selectbox("Previous Default", ["Y", "N"])
        
        # PAN Upload
        st.subheader("Identity Verification")
        pan_file = st.file_uploader("Upload PAN Card (Optional)", type=["jpg", "jpeg", "png"])
        if pan_file is not None:
            st.success("PAN card uploaded successfully!")
    
    with col2:
        st.header("Prediction Results")
        
        if st.button("Assess Credit Risk"):
            with st.spinner('Analyzing credit risk...'):
                # Create a progress bar
                progress_bar = st.progress(0)
                
                # Simulate processing
                for percent_complete in range(100):
                    time.sleep(0.01)  # Simulate processing time
                    progress_bar.progress(percent_complete + 1)
                
                # Prepare input data
                input_data = {
                    'person_age': age,
                    'person_income': income,
                    'person_home_ownership': home_ownership,
                    'person_emp_length': emp_length,
                    'loan_intent': loan_intent,
                    'loan_amnt': loan_amnt,
                    'cb_person_cred_hist_length': cb_person_cred_hist_length,
                    'cb_person_default_on_file': cb_person_default_on_file
                }
                
                # Preprocess input
                processed_data = preprocess_input(input_data)
                
                # Initialize and load model
                model = CreditRiskModel()
                model.load_models()
                
                # Make predictions
                risk_prob = model.predict_risk(processed_data)
                interest_rate = model.predict_interest_rate(processed_data)
                
                # Display results
                st.subheader("Risk Assessment")
                if risk_prob > 0.5:
                    st.error(f"High Risk of Default: {risk_prob*100:.1f}%")
                else:
                    st.success(f"Low Risk of Default: {(1-risk_prob)*100:.1f}%")
                
                st.subheader("Recommended Interest Rate")
                st.metric("Rate", f"{interest_rate:.2f}%")
                
                # Additional recommendations
                st.subheader("Recommendations")
                if risk_prob > 0.7:
                    st.warning("⚠️ High risk profile detected. Consider additional collateral or higher interest rate.")
                elif risk_prob > 0.4:
                    st.info("ℹ️ Medium risk profile. Standard terms and conditions apply.")
                else:
                    st.success("✓ Low risk profile. Favorable terms can be offered.")

if __name__ == "__main__":
    main()
