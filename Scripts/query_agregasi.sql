/*
=============================================================================
Clinical Gait Analysis - Feature Aggregation Query
=============================================================================
Deskripsi: 
Kueri ini mengekstrak dan menghitung nilai rata-rata dari metrik kelistrikan 
otot (sEMG), kinematika sendi mekanik (Goniometer), dan tekanan plantar (Basograph)
dari tabel master data mentah (gait_master_features). 

Hasil dari kueri ini digunakan sebagai sumber data utama (data source) untuk 
visualisasi dashboard makro di Looker Studio.
=============================================================================
*/

SELECT 
    record_id,
    COUNT(*) AS total_baris_data,
    
    -- 1. Metrik Kelistrikan Otot (sEMG) - Dinormalisasi
    ROUND(AVG("semg LT REC.F_norm"), 4) AS rata_paha_depan_kiri,
    ROUND(AVG("semg RT REC.F_norm"), 4) AS rata_paha_depan_kanan,
    ROUND(AVG("semg LT HAM_norm"), 4) AS rata_paha_belakang_kiri,
    ROUND(AVG("semg RT HAM_norm"), 4) AS rata_paha_belakang_kanan,
    
    -- 2. Metrik Sudut Sendi (Goniometer) - Derajat Mekanik
    ROUND(AVG("gonio RT KNEE_sync"), 2) AS rata_sudut_lutut_kanan,
    
    -- Catatan Kualitas Data: 
    -- gonio RT HIP_sync (Pinggul Kanan) dieksklusi dari kueri ini 
    -- akibat adanya anomali saturasi sensor (clipping) pada subjek S21.
    
    -- 3. Metrik Tekanan Pijakan Kaki (Basograph)
    ROUND(AVG("baso LT FOOT_sync"), 2) AS rata_tekanan_kaki_kiri,
    ROUND(AVG("baso RT FOOT_sync"), 2) AS rata_tekanan_kaki_kanan

FROM 
    gait_master_features
    
GROUP BY 
    record_id
    
ORDER BY 
    record_id ASC;
