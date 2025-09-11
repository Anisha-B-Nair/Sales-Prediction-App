import streamlit as st
import pickle
import numpy as np

# Load the saved model
with open("model.pkl", "rb") as file:
    model = pickle.load(file)

st.title("🛍️ Black Friday Sales Prediction")
st.header("Enter Customer & Product Details:")

# Inputs
gender = st.selectbox("Gender", ["M", "F"])
age = st.selectbox("Age", ['0-17', '18-25', '26-35', '36-45', '46-50', '51-55', '55+'])
occupation = st.number_input("Occupation (Code)", min_value=0, step=1)
stay = st.number_input("Years in Current City", min_value=0, step=1)
marital = st.selectbox("Marital Status", ["Single", "Married"])
prod_cat1 = st.number_input("Product Category 1", min_value=0, step=1)
prod_cat2 = st.number_input("Product Category 2", min_value=0, step=1)
prod_cat3 = st.number_input("Product Category 3", min_value=0, step=1)
city = st.selectbox("City Category", ["A", "B", "C"])
user_avg = st.number_input("User Avg Purchase", min_value=0.0, step=1.0)
user_total = st.number_input("User Total Purchase", min_value=0.0, step=1.0)
prod_avg = st.number_input("Product Avg Purchase", min_value=0.0, step=1.0)
user_count = st.number_input("User Purchase Count", min_value=0, step=1)

# Encode inputs the same way as during training
gender = 1 if gender=="M" else 0
age_map = {'0-17':0,'18-25':1,'26-35':2,'36-45':3,'46-50':4,'51-55':5,'55+':6}
age = age_map[age]
marital = 1 if marital=="Married" else 0
city_b = 1 if city=="B" else 0
city_c = 1 if city=="C" else 0

# Create feature array
features = np.array([[gender, age, occupation, stay, marital,
                      prod_cat1, prod_cat2, prod_cat3,
                      city_b, city_c,
                      user_avg, user_total, prod_avg, user_count]])

# Prediction button
if st.button("Predict Purchase Amount"):
    prediction = model.predict(features)
    st.success(f"💰 Predicted Purchase: {prediction[0]:.2f}")

