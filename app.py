
import streamlit as st
import pandas as pd
from datetime import datetime
from bias_rules import generate_insights

st.set_page_config(page_title="MoneyMind - Behavioral Insights", layout="wide")

st.title("💰 MoneyMind: Behavioral Finance Copilot")
st.subheader("Upload your transaction CSV to uncover decision-making patterns")

uploaded_file = st.file_uploader("📤 Upload your Plaid transaction CSV", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        df['date'] = pd.to_datetime(df['date'])

        st.success("✅ File uploaded successfully! Analyzing your behavior...")

        insights = generate_insights(df)

        if insights:
            st.subheader("🔍 Detected Insights:")
            for i, insight in enumerate(insights, 1):
                st.markdown(f"""**{i}. {insight['bias']}**  
💡 *{insight['insight']}*  
🧠 _{insight.get('gpt_nudge', '[No AI insight available]')}_""")
        else:
            st.info("No notable behavioral patterns were detected from your data.")

    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info("Please upload a CSV file to begin.")
