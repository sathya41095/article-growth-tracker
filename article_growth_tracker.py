
import streamlit as st
import pandas as pd
import datetime
import os
import matplotlib.pyplot as plt

st.set_page_config(page_title="Article Growth Tracker", layout="centered")

st.title("🧭 Article Growth Tracker")

role = st.sidebar.selectbox("Select Role", ["Article", "Mentor"])

if role == "Article":
    st.subheader("📋 Weekly Log Form")

    name = st.text_input("Your Name", placeholder="e.g. Ankit Kumar")
    task = st.selectbox("Task Category", ["Audit", "Tax", "Compliance", "Support", "Internal"])
    description = st.text_area("What did you work on?", placeholder="e.g. Vouching of cash payments for XYZ Ltd.")
    skill = st.text_input("Skill Learned", placeholder="e.g. Sampling logic for vouching")
    mistake = st.text_input("Mistake / Lesson", placeholder="e.g. Missed one invoice during walkthrough")

    st.markdown("### 📚 Study Tracker (Hours per Subject)")
    sfm = st.number_input("SFM (Strategic Financial Management)", min_value=0.0, step=0.5)
    fr = st.number_input("FR (Financial Reporting)", min_value=0.0, step=0.5)
    audit = st.number_input("Audit", min_value=0.0, step=0.5)
    law = st.number_input("Law", min_value=0.0, step=0.5)
    dt = st.number_input("Direct Tax", min_value=0.0, step=0.5)
    idt = st.number_input("Indirect Tax", min_value=0.0, step=0.5)

    client = st.radio("Did you interact with a client?", ["Yes", "No"])
    mood = st.select_slider("Mood Today", ["😞", "😐", "🙂", "😀"])
    submit = st.button("Submit Entry")

    if submit:
        new_entry = pd.DataFrame([{
            "Date": datetime.date.today(),
            "Name": name,
            "Task": task,
            "Description": description,
            "Skill": skill,
            "Mistake": mistake,
            "SFM Hours": sfm,
            "FR Hours": fr,
            "Audit Hours": audit,
            "Law Hours": law,
            "DT Hours": dt,
            "IDT Hours": idt,
            "Client Interaction": client,
            "Mood": mood
        }])

        os.makedirs("data", exist_ok=True)
        try:
            existing = pd.read_csv("data/article_logs.csv")
            df = pd.concat([existing, new_entry], ignore_index=True)
        except FileNotFoundError:
            df = new_entry

        df.to_csv("data/article_logs.csv", index=False)
        st.success("✅ Entry submitted successfully!")

elif role == "Mentor":
    st.subheader("🔒 Mentor Access")
    pwd = st.text_input("Enter Mentor Password", type="password")
    if pwd == "rsaudit123":
        st.success("Access Granted")
        try:
            df = pd.read_csv("data/article_logs.csv")
            st.dataframe(df)

            st.markdown("### 📈 Study Time per Subject (Total)")
            subject_totals = df[[
                "SFM Hours", "FR Hours", "Audit Hours", "Law Hours", "DT Hours", "IDT Hours"
            ]].sum()
            fig, ax = plt.subplots()
            subject_totals.plot(kind='bar', ax=ax)
            ax.set_ylabel("Hours")
            ax.set_title("Study Time Distribution")
            st.pyplot(fig)

        except FileNotFoundError:
            st.warning("No logs submitted yet.")
    elif pwd != "":
        st.error("Incorrect password.")
