import streamlit as st
from sklearn.linear_model import LinearRegression

st.title("🏠 Ev Fiyat Tahmini")

X = [[50], [60], [70], [80]]
y = [150000, 180000, 210000, 240000]

model = LinearRegression()
model.fit(X, y)

metrekare = st.number_input("Metrekare gir:", min_value=0)

if st.button("Tahmin Et"):
    sonuc = model.predict([[metrekare]])
    st.success("Tahmini fiyat: " + str(int(sonuc[0])) + " TL")