from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from openpyxl import load_workbook
from datetime import datetime
import os
import json

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from io import BytesIO
from app import app

app = Flask(__name__)
app.secret_key = 'your_secret_key'



PENGUNJUNG_SHEET = 'Pengunjung' #Nama sheet di file excel yang digunakan untuk menyimpan data visitor
KUNJUNGAN_SHEET = 'Kunjungan' #Nama sheet di file excel yang digunakan untuk merekam data kunjungan visitor

#Konfigurasi Google Drive
# Muat kredensial dari environment variable
google_credentials = json.loads(os.environ['GOOGLE_CREDENTIALS'])

# Simpan kredensial sementara ke file
with open('credentials.json', 'w') as cred_file:
    json.dump(google_credentials, cred_file)

# Autentikasi Google Drive
gauth = GoogleAuth()
gauth.LoadCredentialsFile(google_credentials)
if not gauth.credentials or gauth.credentials.invalid:
    gauth.LocalWebserverAuth()  # Membuka autentikasi di browser
    gauth.SaveCredentialsFile(google_credentials)

drive = GoogleDrive(gauth)

# ID file Google Drive
FILE_ID = '1qTz1QNwRu3wvTlM_EL43FvnU_dKQ6Qpc'  # Ganti dengan file ID dari file Excel di Google Drive

def load_excel_file():
    """Download dan baca file Excel dari Google Drive."""
    file = drive.CreateFile({'id': FILE_ID})
    file.GetContentFile('temp.xlsx')  # Unduh file sebagai sementara
    workbook = load_workbook('temp.xlsx')
    return workbook

def save_excel_file(workbook):
    """Simpan file Excel ke Google Drive."""
    with BytesIO() as output:
        workbook.save(output)  # Simpan workbook ke BytesIO
        output.seek(0)
        file = drive.CreateFile({'id': FILE_ID})
        file.SetContentString(output.getvalue().decode('latin1'))  # Update konten file di Drive
        file.Upload()

@app.route("/")
def index():
    return redirect(url_for("home"))

@app.route("/visilog", methods=["POST", "GET"])
def home():
    if request.method == 'POST':
        id_pengunjung = request.form.get('id_pengunjung')

        try:
            # Load workbook dari Google Drive
            wb = load_excel_file()
            pengunjung_sheet = wb[PENGUNJUNG_SHEET]
            kunjungan_sheet = wb[KUNJUNGAN_SHEET]

            # Cari data pengunjung berdasarkan ID
            pengunjung = None
            for row in pengunjung_sheet.iter_rows(min_row=2, values_only=True):
                if str(row[0]) == id_pengunjung:  # Kolom pertama adalah ID
                    pengunjung = row
                    break

            if pengunjung:
                # Rekam kunjungan
                TANGGAL_KUNJUNGAN = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                kunjungan_sheet.append([pengunjung[0], pengunjung[1], pengunjung[2], TANGGAL_KUNJUNGAN])
                save_excel_file(wb)  # Simpan workbook kembali ke Google Drive

                return jsonify({
                    'success': True,
                    'nama': pengunjung[1],
                    'redirect': url_for('home')
                })

            else:
                return jsonify({
                    'success': False,
                    'redirect': url_for('home')
                })
            
        except Exception as e:
            flash(f"Terjadi kesalahan: {e}", 'danger')

        return redirect(url_for('home'))

    return render_template('visitor-log.html')



if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5555)
