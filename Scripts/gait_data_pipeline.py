"""
Clinical Gait Analysis - Data Engineering Pipeline
--------------------------------------------------
Script ini mengekstrak data sinyal mentah (time-series), melakukan pembersihan,
menerapkan Min-Max Normalization pada sensor sEMG, dan menyimpannya 
ke dalam database SQLite untuk analisis agregasi lebih lanjut.
"""

import os
import glob
import pandas as pd
import sqlite3
import logging

# Konfigurasi logging untuk memantau proses
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def min_max_normalize(series):
    """
    Menerapkan Min-Max Normalization (0.0 hingga 1.0) pada Pandas Series.
    """
    col_min = series.min()
    col_max = series.max()
    
    # Menghindari error pembagian dengan nol jika sinyal datar (max == min)
    if col_max == col_min:
        return series * 0.0
        
    return (series - col_min) / (col_max - col_min)

def run_etl_pipeline(raw_data_folder, db_path):
    """
    Mengeksekusi proses Extract, Transform, Load (ETL) pada seluruh file subjek.
    """
    # Mencari semua file CSV di dalam folder data mentah
    file_pattern = os.path.join(raw_data_folder, "*.csv")
    file_list = glob.glob(file_pattern)
    
    if not file_list:
        logging.error("Tidak ada file CSV yang ditemukan di direktori tersebut.")
        return

    # Membuat koneksi ke database SQLite
    conn = sqlite3.connect(db_path)
    table_name = "gait_master_features"
    
    logging.info(f"Memulai pemrosesan untuk {len(file_list)} file subjek...")

    total_rows = 0

    for file_path in file_list:
        # Ekstrak Record ID dari nama file (Asumsi nama file: timeseries_S01.csv)
        filename = os.path.basename(file_path)
        record_id = filename.split('_')[-1].replace('.csv', '')
        
        logging.info(f"Memproses subjek: {record_id}...")

        # EXTRACT: Membaca data mentah
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            logging.error(f"Gagal membaca {filename}: {e}")
            continue

        # Memastikan ada kolom 'record_id'
        df['record_id'] = record_id

        # TRANSFORM: Menerapkan Normalisasi pada kolom sEMG
        semg_columns = [
            'semg LT REC.F', 'semg RT REC.F', 
            'semg LT HAM', 'semg RT HAM'
        ]
        
        for col in semg_columns:
            if col in df.columns:
                norm_col_name = f"{col}_norm"
                df[norm_col_name] = min_max_normalize(df[col])
            else:
                logging.warning(f"Kolom {col} tidak ditemukan di {filename}")

        # Menghapus kolom anomali atau data kosong jika diperlukan (Data Cleaning)
        # Contoh: Eksklusi gonio pinggul kanan akibat saturasi sensor
        if 'gonio RT HIP' in df.columns:
            df = df.drop(columns=['gonio RT HIP'])

        # LOAD: Menyimpan data yang sudah ditransformasi ke SQLite dengan mode 'append'
        # Hal ini mencegah memori laptop penuh saat memproses 15 juta baris
        df.to_sql(table_name, conn, if_exists='append', index=False)
        
        total_rows += len(df)

    conn.close()
    logging.info(f"Proses ETL Selesai! Total baris data diproses: {total_rows:,}")

if __name__ == "__main__":
    # Konfigurasi Path File (Ubah sesuai dengan struktur direktori lokal Anda)
    RAW_DATA_FOLDER = "./data/raw_timeseries/"
    SQLITE_DB_PATH = "./data/gait_analysis_bigdata.db"
    
    # Membuat folder jika belum ada
    os.makedirs(RAW_DATA_FOLDER, exist_ok=True)
    os.makedirs(os.path.dirname(SQLITE_DB_PATH), exist_ok=True)
    
    # Jalankan Pipeline
    run_etl_pipeline(RAW_DATA_FOLDER, SQLITE_DB_PATH)