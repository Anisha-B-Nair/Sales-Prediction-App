import streamlit as st

st.title("📊 Sales Prediction App")

st.write("Welcome! This is a simple app to predict sales using machine learning.")

# Example input
tv = st.number_input("Enter TV Advertising Spend ($)", min_value=0.0, step=0.1)
radio = st.number_input("Enter Radio Advertising Spend ($)", min_value=0.0, step=0.1)
newspaper = st.number_input("Enter Newspaper Advertising Spend ($)", min_value=0.0, step=0.1)

if st.button("Predict"):
    # dummy prediction for now
    prediction = 2.5*tv + 1.5*radio + 0.5*newspaper  
    st.success(f"Predicted Sales: {prediction:.2f} units")
# code will go here
