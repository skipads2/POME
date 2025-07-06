import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def calculate_ped(df):
    df["Rural Qty"] = df["Rural MPCE"] / df["Rural Price Index"]
    df["Urban Qty"] = df["Urban MPCE"] / df["Urban Price Index"]
    df["%ΔQ"] = (df["Urban Qty"] - df["Rural Qty"]) / ((df["Urban Qty"] + df["Rural Qty"]) / 2)
    df["%ΔP"] = (df["Urban Price Index"] - df["Rural Price Index"]) / ((df["Urban Price Index"] + df["Rural Price Index"]) / 2)
    df["PED"] = df["%ΔQ"] / df["%ΔP"]
    df["Elasticity"] = df["PED"].apply(classify_elasticity)
    return df

def classify_elasticity(ped):
    if abs(ped) > 1:
        return "Elastic"
    elif abs(ped) < 1:
        return "Inelastic"
    else:
        return "Unit Elastic"

def generate_strategy(item, elasticity):
    if elasticity == "Inelastic":
        return f"{item}: Maintain stable pricing; focus on trust, consistent supply, and value packs."
    elif elasticity == "Elastic":
        return f"{item}: Use aggressive promotions, combos, dynamic pricing to drive volume."
    else:
        return f"{item}: Adjust pricing cautiously; monitor market trends closely."

def plot_ped_chart(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x="Food Item", y="PED", data=df, palette="coolwarm", ax=ax)
    plt.xticks(rotation=45)
    plt.axhline(1, color="grey", linestyle="--", label="Elasticity = 1")
    plt.title("Price Elasticity of Demand by Food Item")
    plt.legend()
    st.pyplot(fig)
