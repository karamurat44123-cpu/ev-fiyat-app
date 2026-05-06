import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.title("📈 BIST Hisse Takip")

hisse = st.text_input("Hisse kodu gir (örnek: THYAO.IS)", "THYAO.IS")

veri = yf.download(hisse, period="1mo")

if not veri.empty:

    son_fiyat = veri["Close"].iloc[-1]

    st.subheader(f"Güncel Fiyat: {round(float(son_fiyat),2)} TL")

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

else:
    st.error("Hisse bulunamadı")
