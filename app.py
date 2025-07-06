import streamlit as st
import pandas as pd
import numpy as np
import pickle
from utils import calculate_ped, plot_ped_chart, generate_strategy
from cpi_data import get_dynamic_price_index

# Load ML promotion model
ml_model = pickle.load(open("promotions_model.pkl", "rb"))

st.title("📊 Price Elasticity & Retail Strategy Recommender")

# Upload input CSV
uploaded_file = st.file_uploader("Upload your MPCE data", type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("✅ Raw Data Preview:", df.head())

    # CPI adjustment
    cpi_multiplier = st.slider("Adjust CPI Inflation Multiplier", 1.0, 1.5, 1.1)
    df["Rural Price Index"] = 100
    df["Urban Price Index"] = df["Base Urban Index"] * cpi_multiplier

    st.write("📝 Updated Urban Price Index:", df[["Food Item", "Urban Price Index"]])

    # Calculate PED
    results_df = calculate_ped(df)
    st.write("📈 PED Results:", results_df)

    # Plot
    plot_ped_chart(results_df)

    # Predict using ML model
    st.subheader("🤖 Promotion Success Prediction")
    region = st.selectbox("Region", ["Urban", "Rural"])
    season = st.selectbox("Season", ["Summer", "Monsoon", "Winter", "Festival"])

    for idx, row in results_df.iterrows():
        features = np.array([row["PED"], 1 if region=="Urban" else 0, 1 if season=="Summer" else 0]).reshape(1, -1)
        prediction = ml_model.predict(features)
        st.write(f"{row['Food Item']}: {'✅ Likely Effective' if prediction[0]==1 else '⚠️ Less Effective'}")

    # Generate final strategy
    st.subheader("🗂️ Recommended Strategy")
    for idx, row in results_df.iterrows():
        st.write(generate_strategy(row["Food Item"], row["Elasticity"]))

    # Download
    csv = results_df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Results", csv, "results.csv", "text/csv")
