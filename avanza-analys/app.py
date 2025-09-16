# app.py
import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Leos Portfölj", layout="wide")
st.title("📊 Leos portföljanalys")

# Läs in CSV
try:
    portfolj = pd.read_csv("/Users/leohjernquist/Desktop/Python projekt/avanza-analys/portfolj.csv", sep=";")
    st.write(portfolj.columns)
except FileNotFoundError:
    st.error("CSV-filen 'portfolj.csv' hittades inte.")
    st.stop()

sammanstallning = []

st.info("🔄 Hämtar data från Yahoo Finance...")

for _, rad in portfolj.iterrows():
    ticker = rad['Ticker']
    antal = rad['Antal']
    gav = rad['GAV']  # Total investerad summa

    try:
        aktie = yf.Ticker(ticker)
        pris = aktie.fast_info['last_price']  # Snabbare än .info

        nuvarande_varde = pris * antal
        sedan_kop_kr = nuvarande_varde - gav
        sedan_kop_procent = (sedan_kop_kr / gav) * 100

        sammanstallning.append({
            "Ticker": ticker,
            "Antal": antal,
            "GAV (kr)": round(gav, 2),
            "Nuvarande pris (kr)": round(pris, 2),
            "Totalt värde (kr)": round(nuvarande_varde, 2),
            "Sedan köp (kr)": round(sedan_kop_kr, 2),
            "Sedan köp (%)": round(sedan_kop_procent, 2),
        })

    except Exception as e:
        st.warning(f"Kunde inte hämta data för {ticker}: {e}")

# Visa tabellen
df = pd.DataFrame(sammanstallning)
st.subheader("📋 Portföljsammanställning")
st.dataframe(df, use_container_width=True)

# Visa totalsumma
if not df.empty:
    total_investering = df["GAV (kr)"].sum()
    total_varde = df["Totalt värde (kr)"].sum()
    total_vinst = total_varde - total_investering
    total_avkastning = (total_vinst / total_investering) * 100

    st.markdown("---")
    st.subheader("📈 Total översikt")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total GAV", f"{total_investering:,.0f} kr")
    col2.metric("Nuvarande värde", f"{total_varde:,.0f} kr")
    col3.metric("Vinst/Förlust", f"{total_vinst:,.0f} kr")
    col4.metric("Avkastning (%)", f"{total_avkastning:.2f} %")

# Visa som tabell
st.subheader("📋 Portföljsammanställning")
st.dataframe(pd.DataFrame(sammanstallning))