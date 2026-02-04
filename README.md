# End-to-End Customer Churn Prediction App

machine learning application for predicting customer churn.  
built with [FastAPI] (backend CRUD API), [Streamlit] (frontend UI), and real_time ML inference.  
data is stored in JSON format, and the system supports deployment with docker.


Features
   FastAPI backend with CRUD endpoints
   Streamlit dashboard for interactive predictions
   Real-time machine learning inference
   JSON-based storage for customer data
   Dockerized for easy deployment

Structure

    customer_churn/
      |--data/data.py    # data svaing and data loading
      |--ml_model/
      |           |-- ml_model_v3.pkl   # ml model
      |           |--predictor.py       # predict intent
      |--streamlit/
      |           |--test.py              # ui front
      |--validation /
      |              |--priority.py       # sorting priority
      |              |--schema.py           # pydantic validation 
      |-- customer_churn_prediction.ipnb         
      |--customer.json
      |-- main.py             # fastapi endpot 
      | -- readme.md          # project documentation



      git clone https://github.com/deathsamsul/End-to-End-Customer-Churn-Prediction-App.git
      python -m venv venv
      \venv\Scripts\activate   # Windows
      pip install -r requirements.txt
      uvicorn app.main:app --reload
      streamlit run streamlit/test.py


---

Installation
```bash
git clone https://github.com/deathsamsul/End-to-End-Customer-Churn-Prediction-App.git
python -m venv venv
\venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
streamlit run streamlit/test.py

