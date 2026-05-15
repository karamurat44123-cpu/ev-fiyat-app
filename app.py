import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from scipy.stats import linregress
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from pandas.tseries.offsets import BDay

st.title("📈 BIST Hisse Takip")

# Takip listesi
hisseler = [
    "THYAO.IS",
    "ASTOR.IS",
    "ASELS.IS",
    "KCHOL.IS",
    "SISE.IS",
    "TUPRS.IS",
    "BIMAS.IS",
    "EREGL.IS",
    "AKBNK.IS",
    "GARAN.IS",
    "YKBNK.IS",
    "PETKM.IS",
    "SASA.IS",
    "HEKTS.IS",
    "FROTO.IS",
    "TOASO.IS"
]

hisse = st.selectbox("Takip etmek istediğin hisseyi seç:", hisseler)

tahmin_gunu = st.selectbox(
    "Tahmin süresi seç:",
    [1, 2, 3, 5, 7]
)

st.subheader("🔥 Trend Hisseler")

for hisse_kodu in hisseler:

    try:
        veri_tarama = yf.download(hisse_kodu, period="1mo")

        if not veri_tarama.empty:

            son = veri_tarama["Close"].iloc[-1].iloc[0]

            ma20_tarama = veri_tarama["Close"].rolling(20).mean()

            rsi_degisim = veri_tarama["Close"].diff()

            yukselen = rsi_degisim.where(rsi_degisim > 0, 0).rolling(14).mean()

            dusen = (-rsi_degisim.where(rsi_degisim < 0, 0)).rolling(14).mean()

            rs = yukselen / dusen

            rsi = 100 - (100 / (1 + rs))

            son_rsi = rsi.iloc[-1].iloc[0]

            puan = 50

            if son > ma20_tarama.iloc[-1].iloc[0]:
                puan += 20

            if son_rsi < 30:
                puan += 20

            elif son_rsi > 70:
                puan -= 20

            if puan >= 70:
                st.success(f"{hisse_kodu} → Güçlü Trend (%{puan})")

            elif puan >= 55:
                st.info(f"{hisse_kodu} → İzlenebilir (%{puan})")

            else:
                st.error(f"{hisse_kodu} → Riskli (%{puan})")

    except:
        pass

veri = yf.download(hisse, period="1mo")

if not veri.empty:

    son_fiyat = veri["Close"].iloc[-1].iloc[0]

    st.subheader(f"Güncel Fiyat: {round(son_fiyat,2)} TL")

    ma20 = veri["Close"].rolling(20).mean()

macd_kisa = veri["Close"].ewm(span=12).mean()
macd_uzun = veri["Close"].ewm(span=26).mean()
macd = macd_kisa - macd_uzun
signal = macd.ewm(span=9).mean()

son_macd = macd.iloc[-1].iloc[0]
son_signal = signal.iloc[-1].iloc[0]

puan = 0

# MA20 kontrol
if son_fiyat > ma20.iloc[-1].iloc[0]:
    puan += 2
else:
    puan -= 2

# MACD kontrol
if son_macd > son_signal:
    puan += 2
else:
    puan -= 2

# RSI kontrol
if son_rsi < 30:
    puan += 2
elif son_rsi > 70:
    puan -= 2

x = list(range(len(veri)))
y = veri["Close"].squeeze().values

X = np.array(x).reshape(-1, 1)
Y = np.array(y)

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X, Y)

gelecek_gun = np.array([[len(veri) + tahmin_gunu]])

gelecek_tarih = veri.index[-1] + BDay(tahmin_gunu)

tahmin = model.predict(gelecek_gun)[0]

# AI tahmini kontrol
if tahmin > son_fiyat:
    puan += 2
else:
    puan -= 2

# RSI benzeri momentum hesabı
degisim = veri["Close"].diff()

yukselen = degisim.where(degisim > 0, 0).rolling(14).mean()
dusen = (-degisim.where(degisim < 0, 0)).rolling(14).mean()

rs = yukselen / dusen
rsi = 100 - (100 / (1 + rs))

son_rsi = rsi.iloc[-1].iloc[0]

# Trend gücü
if son_rsi > 70:
    st.warning(f"RSI: {round(son_rsi,2)} → Aşırı Alım")
elif son_rsi < 30:
    st.success(f"RSI: {round(son_rsi,2)} → Aşırı Satım")
else:
    st.info(f"RSI: {round(son_rsi,2)} → Normal Bölge")

slope, intercept, r, p, std = linregress(x, y)

tahmin = intercept + slope * (len(veri) + tahmin_gunu)

st.info(f"Yapay Zeka Tahmini ({tahmin_gunu} Gün Sonra): {round(tahmin,2)} TL")

# Güven skoru hesaplama
guven = 50

if son_fiyat > ma20.iloc[-1].iloc[0]:
    guven += 15

if son_rsi < 30:
    guven += 20

elif son_rsi > 70:
    guven -= 20

# Trend analizi
if tahmin > son_fiyat:
    guven += 15
else:
    guven -= 15

# Limitler
guven = max(0, min(100, guven))

# Risk seviyesi
if guven >= 70:
    risk = "Düşük Risk"
elif guven >= 50:
    risk = "Orta Risk"
else:
    risk = "Yüksek Risk"

st.success(f"Yükseliş İhtimali: %{guven}")

st.warning(f"Risk Seviyesi: {risk}")

# MACD hesaplama
ema12 = veri["Close"].ewm(span=12).mean()
ema26 = veri["Close"].ewm(span=26).mean()

macd = ema12 - ema26
signal = macd.ewm(span=9).mean()

macd_son = macd.iloc[-1].iloc[0]
signal_son = signal.iloc[-1].iloc[0]

if macd_son > signal_son:
    st.success("MACD: YÜKSELİŞ TRENDİ")
else:
    st.error("MACD: DÜŞÜŞ TRENDİ")

# Nihai karar
if puan >= 5:
    st.success("ÇOK GÜÇLÜ AL SİNYALİ")
elif puan >= 2:
    st.success("AL SİNYALİ")
elif puan <= -5:
    st.error("ÇOK GÜÇLÜ SAT SİNYALİ")
elif puan <= -2:
    st.error("SAT SİNYALİ")
else:
    st.warning("BEKLE / KARARSIZ BÖLGE")

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


