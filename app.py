import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.title("📈 BIST Hisse Takip")

hisse = st.text_input("Hisse kodu gir (örnek: THYAO.IS)", "THYAO.IS")

veri = yf.download(hisse, period="1mo")

if not veri.empty:

    son_fiyat = veri["Close"].iloc[-1].iloc[0]

    st.subheader(f"Güncel Fiyat: {round(son_fiyat,2)} TL")

    ma20 = veri["Close"].rolling(20).mean()

if son_fiyat > ma20.iloc[-1].iloc[0]:
    st.success("AL SİNYALİ")
else:
    st.error("SAT SİNYALİ")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=veri.index,
            y=veri["Close"],
            mode="lines",
            name="Fiyat"
        )
    )

    st.plotly_chart(fig)


