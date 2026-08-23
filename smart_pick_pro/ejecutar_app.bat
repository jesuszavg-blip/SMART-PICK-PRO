@echo off
chcp 65001 > nul
title Smart Pick Pro - Iniciador VIP
color 0A
echo ============================================================
echo 🏆 INICIANDO SMART PICK PRO VIP...
echo ============================================================
cd /d "C:\Users\Dell\.gemini\antigravity\scratch\smart_pick_pro"

echo 🛑 Liberando puerto 8501 y procesos anteriores...
taskkill /F /IM python.exe > nul 2>&1
timeout /t 1 /nobreak > nul

set NPY_DISABLE_CPU_FEATURES=X86_V2 AVX2 FMA3 AVX512F
set OPENBLAS_CORETYPE=generic

echo 📦 Verificando/Instalando dependencias necesarias...
python -m pip install numpy==1.26.4 pandas streamlit requests plotly scipy bcrypt python-dotenv openpyxl > nul 2>&1

echo 🚀 Encendiendo el servidor web Smart Pick Pro...
python -m streamlit run app.py --server.port 8501

pause
