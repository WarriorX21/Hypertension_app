
import streamlit as st
import pickle
import pandas as pd

# Load model
model = pickle.load(open("hypertension_model.pkl", "rb"))

# Title
st.title("🩺 Hypertension Risk Predictor")

st.markdown("Enter your health data to estimate your 5-year hypertension risk.")

# Inputs
age = st.slider("Age", 18, 80, 30)
gender = st.selectbox("Gender", ["Male", "Female"])
bmi = st.slider("BMI", 15.0, 45.0, 25.0)
glucose = st.slider("Glucose (mg/dL)", 70, 200, 100)
systolic_bp = st.slider("Systolic BP", 90, 180, 120)
diastolic_bp = st.slider("Diastolic BP", 60, 120, 80)
smoker = st.selectbox("Smoker", ["Yes", "No"])
alcohol_intake = st.selectbox("Alcohol Intake", ["Yes", "No"])
physical_activity = st.selectbox("Physical Activity", ["Low", "Medium", "High"])
family_history = st.selectbox("Family History of Hypertension", ["Yes", "No"])
stress_level = st.selectbox("Stress Level", ["Low", "Medium", "High"])

# Encode manually (must match training format)
input_dict = {
    "age": age,
    "gender": 1 if gender == "Male" else 0,
    "bmi": bmi,
    "glucose": glucose,
    "systolic_bp": systolic_bp,
    "diastolic_bp": diastolic_bp,
    "smoker": 1 if smoker == "Yes" else 0,
    "alcohol_intake": 1 if alcohol_intake == "Yes" else 0,
    "physical_activity": {"Low": 0, "Medium": 1, "High": 2}[physical_activity],
    "family_history": 1 if family_history == "Yes" else 0,
    "stress_level": {"Low": 0, "Medium": 1, "High": 2}[stress_level]
}

input_df = pd.DataFrame([input_dict])

# Predict
if st.button("Predict Risk"):
    risk = model.predict_proba(input_df)[0][1]
    st.metric("Predicted Hypertension Risk (%)", f"{risk*100:.2f}%")

    # Explanation (rule-based)
    st.markdown("### 🧠 Top Risk Contributors")
    if age > 50: st.write("- High age")
    if bmi > 30: st.write("- High BMI")
    if glucose > 130: st.write("- High blood glucose")
    if systolic_bp > 140 or diastolic_bp > 90: st.write("- High blood pressure")
    if smoker == "Yes": st.write("- Smoking habit")
    if alcohol_intake == "Yes": st.write("- Alcohol intake")
    if physical_activity == "Low": st.write("- Low physical activity")
    if family_history == "Yes": st.write("- Family history")
    if stress_level == "High": st.write("- High stress")
