from flask import Flask
from flask import request
from flask import render_template
from flask import session
from flask_json import FlaskJSON, JsonError, json_response, as_json

import pymysql


def db_connect():
    return pymysql.connect(host='localhost', user='anggaganteng', password='anggagantengbanget', database='simpati', port=3307)

def verifikasi_username_password(username, password):
    db = db_connect()
    sql = f"select * from simak_mst_mahasiswa where Login={username} and password = SUBSTRING(MD5(MD5('{password}')), 1, 10)"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        if cur.fetchone():
            return True
        return False

app = Flask(__name__)

app.secret_key = 'tescobacoba'




@app.route('/', methods=['GET'])
def login():
    if 'username' in session:
        return render_template('index.html')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_auth():
    username = request.form['username']
    password = request.form['password']
    if verifikasi_username_password(username, password):
        session['username'] = username
        return render_template ('index.html')
    else:
        return 'login gagal'

@app.route('/home')
def home():
    return render_template ('index.html')


@app.route('/nilai_mahasiswa')
def home_nilai():
    if 'username' in session :
        data = nilai_mhs(session['username'])
        return render_template('nilai.html', data_nilai = data, NPM=session['username'])
    else :
        return render_template('login.html')

def nilai_mhs(npm):
    db = db_connect()
    sql = f"select JadwalID, NilaiAkhir, GradeNilai from simak_trn_krs where MhswID ='{npm}'"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        mahasiswa = cur.fetchall()
        if mahasiswa != ():
            data_fix = []
            for i in mahasiswa:
                data = []
                data.append(nama_matkul(i[0]))
                data.append(i[1])
                data.append(i[2])
                data_fix.append(data)
            return data_fix
        return None

def nama_matkul(JadwalID):
    db = db_connect()
    sql = f"select Nama from simak_trn_jadwal where JadwalID ='{JadwalID}'"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        data = cur.fetchone()
        if data:
            return data[0]
        return None


@app.route('/profil')
def home_profil():
    if 'username' in session :
        return nilai_mhs(session['username'])
    else :
        return render_template ('login.html')

@app.route('/profil_mhs')
def profil_mhs():
    if 'username' in session :
        db = db_connect()
        sql = f"select *from simak_mst_mahasiswa where MhswID='{session['username']}'"
        with db:
            cur = db.cursor()
            cur.execute(sql)
            data = cur.fetchall()
            return render_template ('profil.html', data = data)
    else :
        return render_template('login.html')

@app.route('/jadwal')
def jadwal_mhs():
    if 'username' in session :
        db = db_connect()
        sql = f"""select a.HariID, a.JamMulai, a.JamSelesai, a.DosenID, a.Nama, a.MKKode, b.JadwalID,
        c.MhswID 
        from  simak_trn_jadwal as a 
        JOIN 
        simak_trn_krs as b ON a.JadwalID = b.JadwalID 
        JOIN 
        simak_mst_mahasiswa as c ON b.MhswID = c.MhswID 
        WHERE c.MhswID = '{session['username']}'"""
        with db:
            cur = db.cursor()
            cur.execute(sql)
            data = cur.fetchall()
        return render_template ('jadwal.html', data = data)
    else :
        return render_template('login.html')

@app.route('/dosen')
def dosen():
    if 'username' in session :
        db = db_connect()
        sql = f"""select a.Nama,a.MKKode,
        b.Nama, c.MhswID
        from simak_trn_jadwal as a
        INNER JOIN
        simak_mst_dosen as b ON a.DosenID = b.Login
        INNER JOIN
        simak_trn_krs as c ON a.MKKode = c.MKKode
        WHERE c.TahunID = 20201 AND
        c.MhswID = '{session['username']}'"""
        with db:
            cur = db.cursor()
            cur.execute(sql)
            data = cur.fetchall()
        return render_template ('dosen.html', data = data)
    else :
        return render_template('login.html')


app.run(debug=True)



