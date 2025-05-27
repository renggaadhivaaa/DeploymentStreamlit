import pickle
import streamlit as st
import numpy as np

# Load model
model = pickle.load(open('model_prediksi_harga_mobil.sav', 'rb'))

# Setup sesi state untuk menyimpan histori
if 'history' not in st.session_state:
    st.session_state.history = []

# Judul Aplikasi
st.title("🚗 Prediksi Harga Mobil")

st.markdown("Masukkan fitur mobil di bawah ini untuk memprediksi harga menggunakan model Machine Learning.")

# ===== Input Fitur =====
enginesize = st.number_input("Ukuran Mesin (enginesize)", min_value=0.0, step=0.1)
horsepower = st.number_input("Tenaga Kuda (horsepower)", min_value=0.0, step=0.1)
citympg = st.number_input("Efisiensi Bahan Bakar Kota (citympg)", min_value=0.0, step=0.1)

# Pilih mata uang
currency = st.selectbox("Tampilkan Harga Dalam:", ["USD", "Rupiah", "Euro"])

# Fungsi konversi mata uang
def convert_currency(amount_usd, target):
    if target == "USD":
        return f"${amount_usd:,.2f}"
    elif target == "Rupiah":
        return f"Rp {amount_usd * 15500:,.0f}"
    elif target == "Euro":
        return f"€{amount_usd * 0.9:,.2f}"

# ===== Tombol Prediksi =====
if st.button("Prediksi Harga"):
    fitur_input = np.array([[enginesize, horsepower, citympg]])
    prediksi = model.predict(fitur_input)
    harga_usd = float(prediksi[0])
    harga_formatted = convert_currency(harga_usd, currency)

    # Tampilkan hasil
    st.success(f"💰 Harga Mobil Diperkirakan: {harga_formatted}")

    # Simpan ke histori
    st.session_state.history.append({
        "enginesize": enginesize,
        "horsepower": horsepower,
        "citympg": citympg,
        "prediksi": harga_formatted
    })

# ===== Tombol Reset =====
if st.button("🔄 Reset Input"):
    st.experimental_rerun()

# ===== Tampilkan Riwayat Prediksi =====
if st.session_state.history:
    st.subheader("📜 Riwayat Prediksi")
    st.table(st.session_state.history)
