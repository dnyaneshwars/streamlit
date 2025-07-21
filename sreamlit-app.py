import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
from transformers import pipeline

# Initialize the summarizer once
@st.cache_resource
def get_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = get_summarizer()

# ------------------------------
# 🎯 App Layout
# ------------------------------
st.set_page_config(page_title="Stock Dashboard & Summarizer", layout="wide")
st.title(" Stock Price Dashboard & Text Summarizer")

# Tabs: One for each feature
tab1, tab2 = st.tabs(["Stock Visualization", "Text Summarizer"])

# ------------------------------
# Tab 1: Stock Visualization
# ------------------------------
with tab1:
    st.header("Stock Price Visualization")

    ticker = st.text_input("Enter Stock Symbol (e.g. AAPL, MSFT)", "AAPL")

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", datetime.now())

    if st.button("Fetch Data"):
        try:
            stock_data = yf.download(ticker, start=start_date, end=end_date)
            if stock_data.empty:
                st.warning("No data found for this ticker and date range.")
            else:
                st.subheader(f"Stock Data for {ticker}")
                st.line_chart(stock_data["Close"])
                st.write(stock_data.tail())
        except Exception as e:
            st.error(f"Failed to fetch stock data: {e}")

# ------------------------------
# Tab 2: Text Summarizer
# ------------------------------
with tab2:
    st.header("Stock News / Description Summarizer")

    input_text = st.text_area("Enter stock-related text (e.g. company news, financial summary)", height=250)

    if st.button("Summarize"):
        if not input_text.strip():
            st.warning("Please enter some text.")
        else:
            with st.spinner("Generating summary..."):
                try:
                    summary = summarizer(input_text, max_length=100, min_length=30, do_sample=False)
                    st.subheader("Summary:")
                    st.success(summary[0]['summary_text'])
                except Exception as e:
                    st.error(f"Summarization failed: {e}")
