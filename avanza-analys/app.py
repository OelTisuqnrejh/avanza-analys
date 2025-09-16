# fil app.py
import streamlit as st
import yfinance as yf

st.title("Leos aktieanalys med Yahoo Finance")

# Ange aktiens ticker-symbol (t.ex. AAPL för Apple):
ticker = st.text_input("AAPL")

if ticker:
    # Hämta aktiedata från Yahoo Finance
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")
    st.write(hist)
    
    # Visa aktiedata
    st.subheader(f"Historisk data för {ticker}")
    st.line_chart(hist['Close'])

    # Visa grundläggande information om aktien
    st.subheader(f"Grundläggande information om {ticker}")
    info = stock.info
    st.write(f"Namn: {info.get('longName', 'N/A')}")
    st.write(f"Sektor: {info.get('sector', 'N/A')}")
    st.write(f"Marknadsvärde: {info.get('marketCap', 'N/A')}")
    st.write(f"P/E-tal: {info.get('trailingPE', 'N/A')}")
    st.write(f"Utdelning: {info.get('dividendYield', 'N/A')}")