import streamlit as st
import requests
import pandas as pd
import time

# Page configuration
st.set_page_config(
    page_title="Customer Churn Prediction",
    layout="wide"
)

st.title(" Customer Churn Prediction System")

API_URL = "http://127.0.0.1:8000"

st.write("---")
st.write("Customer Churn Prediction System : with ml model | made by Samsul | power by streamlit | api construction with fastapi ")

# Cache API calls
@st.cache_data(ttl=60)
def fetch_data(url):
    """Fetch data from API with caching"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except:
        return None
    return None

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    " Dashboard", 
    " Customers", 
    " Add Customer", 
    " Predict"
])

# Dashboard Tab
with tab1:
    st.header("System Dashboard")
    
    # API Health Check
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Check API Health"):
            try:
                response = requests.get(f"{API_URL}/health", timeout=5)
                if response.status_code == 200:
                    st.success(" API is healthy")
                else:
                    st.error("API not responding")
            except:
                st.error(" Cannot connect to API")
    
    with col2:
        if st.button("Check RAM"):
            try:
                response = requests.get(f"{API_URL}/ram", timeout=5)
                if response.status_code == 200:
                    ram_data = response.json()
                    st.metric("RAM Usage", f"{ram_data.get('ram_usage_mb', 0)} MB")
                else:
                    st.error("Failed to get RAM data")
            except:
                st.error("Connection error")
    
    with col3:
        if st.button("Refresh All"):
            st.rerun()

# Customers Tab
with tab2:
    st.header("Customer Database")
    
    # Fetch and display customers
    if st.button("Load Customers"):
        data = fetch_data(f"{API_URL}/customers")
        
        if data:
            df = pd.DataFrame(data)
            
            # Add search and filter
            search_col1, search_col2 = st.columns(2)
            
            with search_col1:
                search_text = st.text_input("Search customers", "")
            
            with search_col2:
                if "Churn" in df.columns:
                    churn_filter = st.selectbox(
                        "Filter by Churn", 
                        ["All"] + list(df["Churn"].unique())
                    )
            
            # Apply filters
            if search_text:
                mask = df.apply(lambda row: row.astype(str).str.contains(search_text, case=False).any(), axis=1)
                df = df[mask]
            
            if "Churn" in df.columns and churn_filter != "All":
                df = df[df["Churn"] == churn_filter]
            
            # Display dataframe
            st.dataframe(df, use_container_width=True)
            
            # Summary statistics
            st.subheader("Summary Statistics")
            if "Churn" in df.columns:
                churn_rate = (df["Churn"] == "Yes").mean() * 100
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Customers", len(df))
                col2.metric("Churn Rate", f"{churn_rate:.1f}%")
                col3.metric("Avg Tenure", f"{df['tenure'].mean():.1f} months")
        else:
            st.warning("No customer data available")

# Add Customer Tab
with tab3:
    st.header("Add New Customer")
    
    with st.form("add_customer_form"):
        # Layout in columns
        col1, col2 = st.columns(2)
        
        with col1:
            gender = st.selectbox("Gender", ["Male", "Female"])
            SeniorCitizen = st.selectbox("Senior Citizen", [0, 1])
            Partner = st.selectbox("Partner", ["Yes", "No"])
            Dependents = st.selectbox("Dependents", ["Yes", "No"])
            tenure = st.number_input("Tenure", min_value=0, value=12)
            PhoneService = st.selectbox("Phone Service", ["Yes", "No"])
            MultipleLines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])
        
        with col2:
            InternetService = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
            OnlineSecurity = st.selectbox("Online Security", ["Yes", "No"])
            OnlineBackup = st.selectbox("Online Backup", ["Yes", "No"])
            DeviceProtection = st.selectbox("Device Protection", ["Yes", "No"])
            TechSupport = st.selectbox("Tech Support", ["Yes", "No"])
            StreamingTV = st.selectbox("Streaming TV", ["Yes", "No"])
            StreamingMovies = st.selectbox("Streaming Movies", ["Yes", "No"])
        
        # Contract and billing
        col3, col4 = st.columns(2)
        
        with col3:
            Contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
            PaperlessBilling = st.selectbox("Paperless Billing", ["Yes", "No"])
        
        with col4:
            PaymentMethod = st.selectbox(
                "Payment Method",
                ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
            )
            MonthlyCharges = st.number_input("Monthly Charges", min_value=0.0, value=50.0)
            TotalCharges = st.number_input("Total Charges", min_value=0.0, value=500.0)
        
        # Submit button
        submitted = st.form_submit_button("Add Customer")
        
        if submitted:
            payload = {
                "gender": gender,
                "SeniorCitizen": SeniorCitizen,
                "Partner": Partner,
                "Dependents": Dependents,
                "tenure": tenure,
                "PhoneService": PhoneService,
                "MultipleLines": MultipleLines,
                "InternetService": InternetService,
                "OnlineSecurity": OnlineSecurity,
                "OnlineBackup": OnlineBackup,
                "DeviceProtection": DeviceProtection,
                "TechSupport": TechSupport,
                "StreamingTV": StreamingTV,
                "StreamingMovies": StreamingMovies,
                "Contract": Contract,
                "PaperlessBilling": PaperlessBilling,
                "PaymentMethod": PaymentMethod,
                "MonthlyCharges": MonthlyCharges,
                "TotalCharges": TotalCharges
            }
            
            try:
                response = requests.post(f"{API_URL}/post", json=payload, timeout=10)
                
                if response.status_code == 201:
                    st.success("Customer added successfully!")
                    # Clear form by rerunning
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Connection error: {e}")

# Predict Tab
with tab4:
    st.header("Predict Customer Churn")
    
    with st.form("predict_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            gender = st.selectbox("Gender", ["Male", "Female"], key="predict_gender")
            SeniorCitizen = st.selectbox("Senior Citizen", [0, 1], key="predict_senior")
            Partner = st.selectbox("Partner", ["Yes", "No"], key="predict_partner")
            Dependents = st.selectbox("Dependents", ["No", "Yes"], key="predict_dependents")
            tenure = st.number_input("Tenure", min_value=0, value=12, key="predict_tenure")
            PhoneService = st.selectbox("Phone Service", ["Yes", "No"], key="predict_phone")
            MultipleLines = st.selectbox("Multiple Lines", ["No phone service", "No", "Yes"], 
                                       key="predict_multilines")
            MonthlyCharges = st.number_input("Monthly Charges", min_value=0.0, value=50.0, 
                                           key="predict_monthly")
        
        with col2:
            InternetService = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"], 
                                         key="predict_internet")
            OnlineSecurity = st.selectbox("Online Security", ["No", "Yes", "No internet service"], 
                                        key="predict_security")
            OnlineBackup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"], 
                                      key="predict_backup")
            DeviceProtection = st.selectbox("Device Protection", ["No", "Yes", "No internet service"], 
                                          key="predict_device")
            TechSupport = st.selectbox("Tech Support", ["No", "Yes", "No internet service"], 
                                     key="predict_tech")
            StreamingTV = st.selectbox("Streaming TV", ["No", "Yes", "No internet service"], 
                                     key="predict_tv")
            StreamingMovies = st.selectbox("Streaming Movies", ["No", "Yes", "No internet service"], 
                                         key="predict_movies")
        
        col3, col4 = st.columns(2)
        
        with col3:
            Contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"], 
                                  key="predict_contract")
            PaperlessBilling = st.selectbox("Paperless Billing", ["Yes", "No"], key="predict_paperless")
        
        with col4:
            PaymentMethod = st.selectbox(
                "Payment Method", 
                ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"], 
                key="predict_payment"
            )
            TotalCharges = st.number_input("Total Charges", min_value=0.0, value=500.0, key="predict_total")
        
        predicted = st.form_submit_button("Predict Churn")
        
        if predicted:
            payload = {
                "gender": gender,
                "SeniorCitizen": SeniorCitizen,
                "Partner": Partner,
                "Dependents": Dependents,
                "tenure": tenure,
                "PhoneService": PhoneService,
                "MultipleLines": MultipleLines,
                "InternetService": InternetService,
                "OnlineSecurity": OnlineSecurity,
                "OnlineBackup": OnlineBackup,
                "DeviceProtection": DeviceProtection,
                "TechSupport": TechSupport,
                "StreamingTV": StreamingTV,
                "StreamingMovies": StreamingMovies,
                "Contract": Contract,
                "PaperlessBilling": PaperlessBilling,
                "PaymentMethod": PaymentMethod,
                "MonthlyCharges": MonthlyCharges,
                "TotalCharges": TotalCharges
            }
            
            try:
                with st.spinner("Predicting..."):
                    response = requests.post(f"{API_URL}/predict", json=payload, timeout=10)
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Display results
                        churn = result.get("churn", "Unknown")
                        probability = float(result.get("probability", 0))
                        
                        st.subheader("Prediction Results")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if churn == "Yes":
                                st.error(f"**Churn Prediction:** {churn}")
                            else:
                                st.success(f"**Churn Prediction:** {churn}")
                        
                        with col2:
                            st.metric("Probability", f"{probability:.1%}")
                        
                        # Show progress bar
                        st.progress(probability)
                        
                        # Risk assessment
                        if probability > 0.7:
                            st.warning(" High churn risk detected")
                        elif probability > 0.4:
                            st.info(" Medium churn risk")
                        else:
                            st.success(" Low churn risk")
                        
                    else:
                        st.error(f"Prediction failed: {response.text}")
                        
            except Exception as e:
                st.error(f"Error: {e}")

# Sidebar for info
with st.sidebar:
    st.header("System Info")
    st.write(f"API URL: {API_URL}")
    st.write("---")
    st.write("**Instructions:**")
    st.write("1. Check API health first")
    st.write("2. View existing customers")
    st.write("3. Add new customers")
    st.write("4. Predict churn for customers")
    
    # Refresh button in sidebar
    if st.button("Refresh App"):
        st.rerun()

# Footer
st.write("---")
st.write('FastAPI (backend API) | Streamlit (frontend UI) | Python (ML model integration)')
st.write('Tech stack: FastAPI for backend, Streamlit for frontend')
st.write('Endpoints: Mention that you support GET, POST, PATCH, PUT for interacting with the ML model')
st.write('Usage: How users can interact (via API calls or Streamlit dashboard).')
st.write("Customer Churn Prediction System : with ml model | made by Samsul | power by streamlit | api construction with fastapi ")