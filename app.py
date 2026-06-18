import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
from datetime import datetime, timedelta


def generate_synthetic_data(num_records=1000):
    np.random.seed(42)
    random.seed(42)
    
    data = {
        'Patient ID': [f"PID-{i:04d}" for i in range(1, num_records + 1)],
        'Age': np.random.normal(45, 20, num_records).astype(int),
        'Gender': np.random.choice(['Male', 'Female'], num_records),
        'Arrival Hour': np.random.randint(0, 24, num_records), 
        'Heart Rate': np.random.normal(85, 25, num_records),
        'Oxygen Level': np.random.normal(95, 8, num_records),
        'Temperature': np.random.normal(98.6, 2, num_records),
        'Severity Score': np.random.randint(1, 11, num_records),
        'Waiting Time': np.random.exponential(30, num_records).astype(int),
    }
    
    df = pd.DataFrame(data)
    
   
    df.loc[10:15, 'Age'] = -5 
    df.loc[20:25, 'Oxygen Level'] = 150
    df.loc[30:35, 'Heart Rate'] = 10
    df.loc[40:45, 'Severity Score'] = np.nan
    
    return df


def clean_data(df):
    df.loc[df['Age'] < 0, 'Age'] = df['Age'].median()
    
    df.loc[(df['Oxygen Level'] < 0) | (df['Oxygen Level'] > 100), 'Oxygen Level'] = df['Oxygen Level'].median()
    
    df.loc[(df['Heart Rate'] < 20) | (df['Heart Rate'] > 250), 'Heart Rate'] = df['Heart Rate'].median()
    
    df.fillna(df.median(numeric_only=True), inplace=True)
    
    return df

def calculate_priority(row):
    score = 0
    if row['Oxygen Level'] < 90: score += 30
    if row['Heart Rate'] > 120: score += 20
    if row['Temperature'] > 102: score += 15
    if row['Age'] > 65: score += 10
    score += (row['Severity Score'] * 5)
    return score

def categorize_priority(score):
    if score <= 25: return 'Normal'
    elif score <= 50: return 'Moderate'
    elif score <= 75: return 'High Priority'
    else: return 'Critical'

def generate_excel(df, filename="hospital_analytics_report.xlsx"):
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name="Patient Records", index=False)
        priority_summary = df['Priority Category'].value_counts().reset_index()
        priority_summary.to_excel(writer, sheet_name="Priority Analysis", index=False)

def main():
    st.set_page_config(page_title="Smart ER Analytics", layout="wide")
    st.title("🏥 Smart Hospital Emergency Room Analytics System")
    
    raw_df = generate_synthetic_data(1000)
    df = clean_data(raw_df.copy())
    df['Priority Score'] = df.apply(calculate_priority, axis=1)
    df['Priority Category'] = df['Priority Score'].apply(categorize_priority)
    df['Treatment Required'] = df['Priority Category'].apply(lambda x: 'Yes' if x in ['Critical', 'High Priority'] else 'No')
    
    generate_excel(df)

    st.header("1. Real-Time Hospital KPIs")
    col1, col2, col3, col4 = st.columns(4)
    
    total_patients = len(df)
    critical_patients = len(df[df['Priority Category'] == 'Critical'])
    avg_wait = df['Waiting Time'].mean()
    doctors_needed = int(np.ceil(total_patients / 20)) # 20 patients per doctor
    beds_needed = int(np.ceil(total_patients * 0.30)) # 30% admission rate
    
    col1.metric("Total Patients Today", total_patients)
    col2.metric("Critical Patients", critical_patients)
    col3.metric("Avg Waiting Time (mins)", f"{avg_wait:.1f}")
    col4.metric("Doctors Required (Daily)", doctors_needed)

    st.header("2. Emergency Alert Status")
    if critical_patients < 20:
        st.success("🟢 GREEN ALERT: Normal Operations. Critical patient volume is manageable.")
    elif critical_patients <= 50:
        st.warning("🟡 YELLOW ALERT: Elevated risk. Monitor ICU bed availability.")
    elif critical_patients <= 100:
        st.error("🟠 ORANGE ALERT: High stress. Call in backup emergency staff.")
    else:
        st.error("🔴 RED ALERT: CRITICAL OVERLOAD. Divert non-critical ambulances.")

    st.header("3. Clinical Visualizations")
    colA, colB = st.columns(2)
    
    with colA:
        st.subheader("Priority Distribution")
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        sns.countplot(data=df, x='Priority Category', order=['Normal', 'Moderate', 'High Priority', 'Critical'], palette='viridis', ax=ax1)
        st.pyplot(fig1)

    with colB:
        st.subheader("Hourly Patient Arrivals (Peak Hour Detection)")
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        sns.histplot(data=df, x='Arrival Hour', bins=24, kde=True, color='crimson', ax=ax2)
        st.pyplot(fig2)

    st.header("4. Statistical & Queue Analysis")
    colC, colD = st.columns(2)
    
    with colC:
        st.write("**Patient Wait Times by Priority**")
        wait_summary = df.groupby('Priority Category')['Waiting Time'].mean().reset_index()
        st.dataframe(wait_summary)
        
    with colD:
        st.write("**Resource Forecasting (Next 24h)**")
        st.write(f"- **Est. Ward Beds Required:** {beds_needed}")
        st.write(f"- **Peak Hour Detected:** {df['Arrival Hour'].mode()[0]}:00")
        st.write(f"- **Minimum Doctors at Peak:** {int(np.ceil((len(df[df['Arrival Hour'] == df['Arrival Hour'].mode()[0]])) / 5))}")

    st.header("5. Automated System Recommendations")
    recs = [
        "✅ **Resource Allocation:** Deploy 3 additional doctors during the detected peak arrival hour.",
        f"✅ **Bed Management:** Prepare {beds_needed} ward beds based on the 30% admission trend.",
        "✅ **Triage Efficiency:** Fast-track 'High Priority' patients to reduce their average waiting time.",
        "✅ **Staffing:** Activate on-call respiratory therapists due to elevated low-oxygen patient volume.",
        "✅ **Infrastructure:** Export the generated 'hospital_analytics_report.xlsx' to the administration network for daily logging."
    ]
    for rec in recs:
        st.write(rec)

if __name__ == "__main__":
    main()
