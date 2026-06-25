import streamlit as st
import pandas as pd
from datetime import date
from PIL import Image
import os

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="ULYA - Ultimate Life-course Advancement", page_icon="Logo Ulya-1edit.png", layout="wide")

# --- INISIALISASI SESSION STATE ---
# Session state berguna untuk menyimpan data saat pengguna berpindah halaman
if 'fase' not in st.session_state:
    st.session_state['fase'] = "Belum Pilih"

# --- FUNGSI BANTU MENGHITUNG UMUR ---
def hitung_umur_bulan(tgl_lahir):
    if tgl_lahir:
        hari = (date.today() - tgl_lahir).days
        return round(hari / 30.44, 1)
    return 0

# --- FUNGSI NAVIGASI (SIDEBAR) ---
st.sidebar.title("🧠 Menu ULYA")
st.sidebar.markdown("Navigasi Aplikasi")

menu_pilihan = st.sidebar.radio(
    "Pilih Halaman:",
    ["1. Pengantar", 
     "2. Tentang Aplikasi ULYA", 
     "3. Petunjuk Penggunaan", 
     "4. Login & Pilih Fase", 
     "5. Identitas Pengguna", 
     "6. Data Anak", 
     "7. Pemeriksaan Antropometri", 
     "8. Asupan Makan Ibu", 
     "9. Kuesioner Psikososial", 
     "10. Dashboard & Rekomendasi", 
     "11. Edukasi Gizi & Kognitif", 
     "12. Evaluasi"]
)

# Menentukan Sapaan
panggilan = "Adik/Nona" if "Remaja" in st.session_state.get('fase', '') else "Bunda"
nama_user = st.session_state.get('nama_ibu', '')
sapaan_resmi = f"{panggilan} {nama_user}".strip() if nama_user else panggilan

st.sidebar.divider()
if st.session_state['fase'] != "Belum Pilih":
    st.sidebar.success(f"Status Aktif: **{sapaan_resmi}**\n\nFase: {st.session_state['fase'][:15]}...")

# ==========================================
# HALAMAN 1: PENGANTAR
# ==========================================
if menu_pilihan == "1. Pengantar":
    # Menampilkan Logo jika file tersedia
    try:
        logo = Image.open("Logo Ulya-1edit.png")
        # Menggunakan kolom agar logo berada di tengah dan ukurannya pas
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            #st.image(logo, use_column_width=True)
            st.image(logo, width="stretch")
    except FileNotFoundError:
        st.warning("⚠️ File logo 'Logo Ulya-1edit.png' tidak ditemukan di folder. Tampilan logo dilewati.")
    
    st.title("Selamat Datang di ULYA")
    st.subheader("*Utamakan Langkah Optimalisasi Generasi Hebat Berdaya*")
    st.write("Aplikasi Prediksi Potensi Kecerdasan (FSIQ) Anak Berbasis *Machine Learning* untuk 1000 Hari Pertama Kehidupan.")
    st.info("👈 Silakan gunakan menu di panel sebelah kiri untuk mulai bernavigasi, dimulai dari memilih Fase Kehidupan Anda pada menu **Login**.")

# ==========================================
# HALAMAN 2: TENTANG APLIKASI
# ==========================================
elif menu_pilihan == "2. Tentang Aplikasi ULYA":
    st.title("Tentang ULYA")
    st.write("**ULYA (Utamakan Langkah Optimalisasi Generasi Hebat Berdaya)** adalah hasil penelitian saintifik yang ditranslasikan menjadi sistem peringatan dini kesehatan digital.")
    st.write("Kata *Ulya* berasal dari bahasa Arab yang bermakna 'Puncak' atau 'Keutamaan'. Visi kami adalah membawa potensi kognitif anak Anda mencapai titik tertingginya melalui pendekatan preventif sejak masa pranikah hingga anak usia sekolah.")

# ==========================================
# HALAMAN 3: PETUNJUK
# ==========================================
elif menu_pilihan == "3. Petunjuk Penggunaan":
    st.title("Petunjuk Penggunaan")
    st.markdown("""
    1. **Login:** Pilih fase kehidupan Anda saat ini. Sistem akan menyesuaikan pertanyaan secara otomatis.
    2. **Isi Data:** Lengkapi identitas, riwayat asupan makan, antropometri, dan kuesioner di menu yang tersedia.
    3. **Lewati Jika Tidak Relevan:** Jika Anda remaja, menu Data Anak tidak perlu diisi.
    4. **Dashboard:** Setelah semua data terisi, buka menu *Dashboard & Rekomendasi* untuk melihat Prediksi FSIQ.
    """)

# ==========================================
# HALAMAN 4: LOGIN / PILIH FASE
# ==========================================
elif menu_pilihan == "4. Login & Pilih Fase":
    st.title("🔑 Halaman Login (Pilih Fase)")
    st.write("Untuk menyajikan perhitungan akurat, mari sesuaikan profil Anda.")
    
    fase_pilihan = st.radio(
        "Di fase manakah Anda saat ini?",
        ["A. Remaja / Calon Pengantin / Merencanakan Kehamilan", 
         "B. Sedang Hamil", 
         "C. Memiliki Anak (Usia Balita hingga 8 Tahun)"],
        key="fase"
    )
    
    st.text_input("Nama Panggilan (Boleh singkatan):", key="nama_ibu", placeholder="Contoh: Rina")
    st.success("Profil Anda telah tersimpan! Silakan lanjut ke menu **5. Identitas Pengguna** di panel kiri.")

# ==========================================
# HALAMAN 5: IDENTITAS PENGGUNA (IBU/REMAJA)
# ==========================================
elif menu_pilihan == "5. Identitas Pengguna":
    st.title(f"👩 Identitas {panggilan}")
    if st.session_state['fase'] == "Belum Pilih":
        st.warning("Mohon pilih fase Anda terlebih dahulu di menu Login.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.date_input("Tanggal Lahir Anda", min_value=date(1970, 1, 1), max_value=date.today(), key="tgl_lahir_ibu")
            st.number_input("Berat Badan (kg)", 30.0, 150.0, 55.0, key="bb_ibu")
            st.number_input("Tinggi Badan (cm)", 130.0, 190.0, 155.0, key="tb_ibu")
            if st.session_state.get('bb_ibu') and st.session_state.get('tb_ibu'):
                imt = round(st.session_state['bb_ibu'] / ((st.session_state['tb_ibu']/100)**2), 1)
                st.info(f"Kalkulasi Indeks Massa Tubuh (IMT): **{imt}**")
        
        with col2:
            st.selectbox("Tingkat Pendidikan Tuntas", ["SD", "SMP", "SMA", "Diploma", "S1", "S2/S3"], key="pendidikan_tuntas")
            st.number_input("Total Lama Pendidikan (Termasuk yang sedang dijalani, dalam tahun)", 6, 25, 12, key="pendidikan_lama")
            st.selectbox("Perkiraan Pendapatan Keluarga per Bulan:", ["< Rp 2 Juta", "Rp 2 - 3 Juta", "> Rp 3 Juta"], key="pendapatan")

# ==========================================
# HALAMAN 6: DATA ANAK
# ==========================================
elif menu_pilihan == "6. Data Anak":
    if "A." in st.session_state['fase'] or st.session_state['fase'] == "Belum Pilih":
        st.info("Halaman ini khusus untuk Bunda yang sudah memiliki anak (Fase C).")
    else:
        st.title("🧒 Data Diri Anak")
        st.text_input("Nama Anak:", key="nama_anak")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Tempat Lahir:", key="tempat_lahir_anak")
            st.selectbox("Jenis Kelamin:", ["Laki-laki", "Perempuan"], key="jk_anak")
        with col2:
            st.date_input("Tanggal Lahir Anak", min_value=date(2015, 1, 1), max_value=date.today(), key="tgl_lahir_anak")
            umur = hitung_umur_bulan(st.session_state.get('tgl_lahir_anak'))
            st.info(f"Kalkulasi Usia Sistem: **{umur} Bulan**")

# ==========================================
# HALAMAN 7: ANTROPOMETRI
# ==========================================
elif menu_pilihan == "7. Pemeriksaan Antropometri":
    if "C." not in st.session_state.get('fase', ''):
        st.info("Halaman ini khusus untuk Bunda yang sudah memiliki anak (Fase C).")
    else:
        st.title("📏 Pemeriksaan Antropometri & Z-Score")
        umur_bln = hitung_umur_bulan(st.session_state.get('tgl_lahir_anak', date.today()))
        
        st.markdown("**Data Saat Lahir**")
        st.number_input("Berat Badan Lahir Anak (gram)", 1000, 5000, 3000, key="bb_lahir")
        
        st.markdown("**Pengukuran Terkini (Hari Ini)**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("Berat Badan (kg)", 3.0, 40.0, 15.0, key="bb_anak")
        with col2:
            st.number_input("Tinggi Badan (cm)", 40.0, 150.0, 100.0, key="tb_anak")
        with col3:
            st.number_input("Lingkar Kepala (cm)", 30.0, 60.0, 50.0, key="lk_anak")
            
        # Kalkulator Z-Score Dummy (Bayangan)
        z_bb = round((st.session_state['bb_anak'] - (3.3 + (0.2 * umur_bln))) / 1.5, 2)
        z_tb = round((st.session_state['tb_anak'] - (50 + (0.5 * umur_bln))) / 4.0, 2)
        z_lk = round((st.session_state['lk_anak'] - (35 + (0.15 * umur_bln))) / 1.2, 2)
        
        st.success(f"📊 **Kalkulasi Z-Score:** BB/U ({z_bb}), TB/U ({z_tb}), LK/U ({z_lk})")

# ==========================================
# HALAMAN 8: ASUPAN MAKAN IBU
# ==========================================
elif menu_pilihan == "8. Asupan Makan Ibu":
    if "A." in st.session_state.get('fase', '') or st.session_state['fase'] == "Belum Pilih":
        st.info("Halaman ini untuk Bunda yang sedang hamil (Fase B) atau mengevaluasi riwayat hamil (Fase C).")
    else:
        st.title("🍽️ Asupan Makan (Makronutrien)")
        st.write("Berdasarkan riwayat porsi harian, sistem akan memproyeksikan asupan protein Anda per trimester.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Porsi sumber hewani per hari (Daging/Ikan/Ayam/Telur):", 0, 15, 3, key="porsi_hewani")
        with col2:
            st.number_input("Porsi sumber nabati per hari (Tahu/Tempe/Kacang):", 0, 15, 2, key="porsi_nabati")
            
        prot_estimasi = (st.session_state['porsi_hewani'] * 15) + (st.session_state['porsi_nabati'] * 5)
        st.session_state['protein_t1'] = prot_estimasi
        st.info(f"✅ Proyeksi Asupan Protein Trimester 1 Anda: **{prot_estimasi} gram/hari**")

# ==========================================
# HALAMAN 9: KUESIONER
# ==========================================
elif menu_pilihan == "9. Kuesioner Psikososial":
    if "A." in st.session_state.get('fase', '') or st.session_state['fase'] == "Belum Pilih":
        st.info("Halaman ini untuk Bunda di Fase B dan C.")
    else:
        st.title("📝 Kuesioner Psikososial Ibu")
        st.markdown("### Instrumen MAAPs (Efikasi Diri)")
        st.slider("Skor keyakinan diri Anda dalam mengasuh & mengelola stres (36-74):", 36, 74, 56, key="skor_maaps")
        
        if "C." in st.session_state.get('fase', ''):
            st.markdown("### Instrumen PBDQ (Dimensi Pengasuhan)")
            st.slider("Skor *Emotional Warmth* (Kehangatan Emosi saat mendampingi anak, 8-36):", 8, 36, 29, key="skor_ew")

# ==========================================
# HALAMAN 10: DASHBOARD & REKOMENDASI
# ==========================================
elif menu_pilihan == "10. Dashboard & Rekomendasi":
    st.title("📊 Dashboard Hasil & Rekomendasi ULYA")
    
    if st.session_state['fase'] == "Belum Pilih":
        st.warning("Data belum lengkap. Silakan Login dan isi data di menu sebelumnya.")
    else:
        if st.button("🚀 Prediksi FSIQ Anak Saya Sekarang!", use_container_width=True):
            st.snow()
            
            # Mengambil data dari session state
            edu = st.session_state.get('pendidikan_lama', 12)
            imt = round(st.session_state.get('bb_ibu', 55) / ((st.session_state.get('tb_ibu', 155)/100)**2), 1)
            prot = st.session_state.get('protein_t1', 77)
            maaps = st.session_state.get('skor_maaps', 56)
            umur_bln = hitung_umur_bulan(st.session_state.get('tgl_lahir_anak', date.today()))
            ztb = round((st.session_state.get('tb_anak', 100) - (50 + (0.5 * umur_bln))) / 4.0, 2)
            zlk = round((st.session_state.get('lk_anak', 50) - (35 + (0.15 * umur_bln))) / 1.2, 2)
            
            # Simulasi ML (Dummy Weights based on Ridge Regression findings)
            base_score = 62.1
            d_edu = (edu - 11.5) * 1.5
            d_imt = 0 if (18.5 <= imt <= 24.9) else -3.0
            d_prot = (prot - 77) * 0.1
            d_maaps = (maaps - 56) * 0.5
            d_tb = ztb * 5.0
            d_lk = zlk * 4.5
            
            skor_akhir = int(max(30, min(95, base_score + d_edu + d_imt + d_prot + d_maaps + d_tb + d_lk)))
            
            # Menampilkan Hasil
            st.metric(label="🌟 Prediksi Skor Kognitif (FSIQ)", value=f"{skor_akhir} Poin")
            
            st.subheader("Rekomendasi Pintar untuk Anda:")
            if "A." in st.session_state['fase']:
                st.info("Kapasitas Prediksi: 8,66% (Potensi Awal). Jaga IMT dan tingkatkan literasi gizi prabikah.")
            elif "B." in st.session_state['fase']:
                st.info("Kapasitas Prediksi: 17,07% (Fetal Neurogenesis). Pertahankan asupan protein Trimester 1 Anda!")
            else:
                st.info("Kapasitas Prediksi: 56,82% (Full Model).")
                if skor_akhir >= 80:
                    st.success("Pertumbuhan linier anak dan pengasuhan Anda sangat promotif! Pertahankan Z-Score hijau.")
                else:
                    st.error("Terdapat indikasi potensi penurunan Z-score antropometri. Segera intervensi asupan energi dan stimulasi!")

# ==========================================
# HALAMAN 11: EDUKASI
# ==========================================
elif menu_pilihan == "11. Edukasi Gizi & Kognitif":
    st.title("📚 Pusat Edukasi")
    st.write("Pelajari lebih lanjut mengenai sains di balik kecerdasan anak.")
    with st.expander("Mengapa Protein di Trimester 1 Sangat Penting?"):
        st.write("Trimester pertama adalah masa kritis *Neurogenesis* di mana sel-sel saraf otak bayi dibentuk...")
    with st.expander("Apa Hubungan Tinggi Badan dan Kecerdasan?"):
        st.write("Kegagalan pertumbuhan fisik kronis (*stunting*) berjalan beriringan dengan hambatan kognitif...")

# ==========================================
# HALAMAN 12: EVALUASI
# ==========================================
elif menu_pilihan == "12. Evaluasi":
    st.title("⭐ Evaluasi Aplikasi ULYA")
    st.write("Bantu kami menyempurnakan aplikasi ini!")
    st.slider("Berapa bintang untuk pengalaman penggunaan aplikasi ini?", 1, 5, 5)
    st.text_area("Masukan dan Saran:")
    if st.button("Kirim Evaluasi"):
        st.success("Terima kasih atas masukannya!")