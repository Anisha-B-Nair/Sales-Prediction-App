import streamlit as st
import pickle
import pandas as pd
import numpy as np
import os

# ===============================
# Load model and feature objects
# ===============================
BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "black_friday_model.pkl")
FEATURES_PATH = os.path.join(BASE_DIR, "features.pkl")

# Load model
try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.error("❌ black_friday_model.pkl not found! Please put it in the same folder as app.py.")
    st.stop()

# Load features
try:
    with open(FEATURES_PATH, "rb") as f:
        feature_objects = pickle.load(f)
except FileNotFoundError:
    st.error("❌ features.pkl not found! Please put it in the same folder as app.py.")
    st.stop()

# ===============================
# Page setup
# ===============================
st.set_page_config(page_title="Black Friday Sales Prediction", layout="wide")
st.title("🛍️ Black Friday Sales Prediction App")
st.write("Predict the purchase amount for a customer based on their profile and product details.")

# ===============================
# Product Category Mapping
# ===============================
product_mapping = {
    1: "Clothing",
    2: "Footwear",
    3: "Electronics",
    4: "Home & Kitchen",
    5: "Beauty & Personal Care",
    6: "Toys & Games",
    7: "Sports",
    8: "Books",
    9: "Other"
}

# ===============================
# Input Section
# ===============================
st.header("Customer & Product Details")
col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox("Gender", ["M", "F"])
    age = st.selectbox("Age", ['0-17', '18-25', '26-35', '36-45', '46-50', '51-55', '55+'])
    occupation = st.number_input("Occupation Code", min_value=0, step=1)
    stay = st.number_input("Years in Current City", min_value=0, step=1)
    marital = st.selectbox("Marital Status", ["Single", "Married"])
    city = st.selectbox("City Category", ["A", "B", "C"])

with col2:
    prod_cat1_label = st.selectbox("Product Category 1", list(product_mapping.values()))
    prod_cat2_label = st.selectbox("Product Category 2", list(product_mapping.values()))
    prod_cat3_label = st.selectbox("Product Category 3", list(product_mapping.values()))
    user_avg = st.number_input("User Avg Purchase", min_value=0.0, step=1.0)
    user_total = st.number_input("User Total Purchase", min_value=0.0, step=1.0)
    prod_avg = st.number_input("Product Avg Purchase", min_value=0.0, step=1.0)
    user_count = st.number_input("User Purchase Count", min_value=0, step=1)

# ===============================
# Convert product labels back to numbers
# ===============================
inv_mapping = {v: k for k, v in product_mapping.items()}
prod_cat1 = inv_mapping[prod_cat1_label]
prod_cat2 = inv_mapping[prod_cat2_label]
prod_cat3 = inv_mapping[prod_cat3_label]

# ===============================
# Encode Inputs
# ===============================
gender_encoded = feature_objects['Gender_Encoder'].transform([gender])[0] if 'Gender_Encoder' in feature_objects else (1 if gender=="M" else 0)
age_encoded = feature_objects['Age_Map'][age] if 'Age_Map' in feature_objects else {'0-17':0,'18-25':1,'26-35':2,'36-45':3,'46-50':4,'51-55':5,'55+':6}[age]
marital_encoded = 1 if marital=="Married" else 0
city_b = 1 if city=="B" else 0
city_c = 1 if city=="C" else 0

# ===============================
# Prepare input DataFrame
# ===============================
input_df = pd.DataFrame([{
    'Gender': gender_encoded,
    'Age': age_encoded,
    'Occupation': occupation,
    'Stay_In_Current_City_Years': stay,
    'Marital_Status': marital_encoded,
    'Product_Category_1': prod_cat1,
    'Product_Category_2': prod_cat2,
    'Product_Category_3': prod_cat3,
    'City_Category_B': city_b,
    'City_Category_C': city_c,
    'User_Avg_Purchase': user_avg,
    'User_Total_Purchase': user_total,
    'Product_Avg_Purchase': prod_avg,
    'User_Purchase_Count': user_count
}])

# Reorder columns if stored in features.pkl
if 'columns_order' in feature_objects:
    input_df = input_df[feature_objects['columns_order']]

# ===============================
# Prediction
# ===============================
if st.button("Predict Purchase Amount"):
    prediction = model.predict(input_df)
    st.success(f"💰 Predicted Purchase Amount: {prediction[0]:.2f}")

# Optional: show input data
with st.expander("Show Input Data"):
    st.write(input_df)
