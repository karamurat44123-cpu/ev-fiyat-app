import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from scipy.stats import linregress

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

    x = list(range(len(veri)))
y = veri["Close"].squeeze().values

slope, intercept, r, p, std = linregress(x, y)

tahmin = intercept + slope * (len(veri) + 1)

st.info(f"Yapay Zeka Tahmini (Yarın): {round(tahmin,2)} TL")

fig = go.Figure()

fig.update_layout(
    title=hisse + " Fiyat Grafiği",
    xaxis_title="Tarih",
    yaxis_title="Fiyat",
    template="plotly_dark"
)

    fig.add_trace(
        go.Scatter(
            x=veri.index,
            y=veri["Close"].squeeze(),
            mode="lines",
            name="Fiyat"
        )
    )

    st.plotly_chart(fig)


