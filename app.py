from flask import Flask
from flask import request
from flask import render_template, redirect
from flask import session, url_for
from flask_json import FlaskJSON, JsonError, json_response, as_json
from authlib.integrations.flask_client import OAuth
import pymysql
import os
import sys
from datetime import timedelta
import config

sys.path.insert(0, os.path.dirname(__file__))

def db_connect():
    return pymysql.connect(host='localhost', user='micropol_dyning', password='Date290200!', database='micropol_test', port=3306)

def verifikasi_username_password(username, password):
    db = db_connect()
    sql = f"select * from simak_mst_mahasiswa where Login={username} AND password = SUBSTRING(MD5(MD5('{password}')), 1, 10)"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        if cur.fetchone():
            return True
        return False

def isLoggedIN():
    try:
        user = dict(session).get('profile', None)
        if user:
            return True
        else:
            return False
    except Exception:
        return False

app = Flask(__name__)

oauth = OAuth(app)
app.secret_key = 'tes cobacoba'
app.config.from_object('config')
GOOGLE_CLIENT_ID = '613016628391-9e3v2n5on64j70sdr2kslsuhoc8a8fbv.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'BHQ_2O6Kia3Xk_yb4OuVRwVp'
FN_BASE_URL = 'micropoltekpos.xyz'
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth(app)
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_id='613016628391-9e3v2n5on64j70sdr2kslsuhoc8a8fbv.apps.googleusercontent.com',
    client_secret='BHQ_2O6Kia3Xk_yb4OuVRwVp',
    client_kwargs={
        'scope': 'openid email profile'
    }
)


@app.route('/authgoogle')
def authgoogle():
    #oauth.create_client()
    session['_google_authlib_state_'] = request.args.get('state')
    session['_google_authlib_redirect_uri_'] = config.FN_BASE_URL + url_for('authgoogle')
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token)
    session['user'] = user
    session.permanent = True
    #google_provider_cfg = get_google_provider_cfg()
    #authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    #email_google = request.args.get('userinfo.email')
    #email_siap = f"select Email from simak_mst_mahasiswa where Email='{email_google}'"
    #if session['user'] == email_siap:
    return redirect('/home')
    #else:
        #return redirect('/home')
    #    return 'Gunakan Email yang terdaftar di SIAP'

@app.route('/google_login')
def google_login():
    #oauth.create_client('google')
    #Request.args.get(CONF_URL).json()
    redirect_uri = config.FN_BASE_URL + url_for('authgoogle')
    return oauth.google.authorize_redirect(redirect_uri)

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
    #email = dict[session].get('email',None)
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
        sql = f"select * from simak_mst_mahasiswa where MhswID='{session['username']}'"
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
        sql = f"""select a.HariID, a.JamMulai, a.JamSelesai, a.DosenID, a.Nama, a.MKKode, b.JadwalID
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
@app.route('/presensi')
def presensi():
    if 'username' in session:
        db = db_connect()
        sql = f"""SELECT simak_trn_jadwal.Nama, simak_mst_tahun.Nama, simak_trn_presensi_mahasiswa.JenisPresensiID
            from simak_trn_presensi_mahasiswa, simak_trn_jadwal, simak_mst_tahun where simak_trn_presensi_mahasiswa.MhswID = '{session['username']}'"""
        with db:
            cur = db.cursor()
            cur.execute(sql)
            data = cur.fetchall()
        return render_template ('presensi.html', data = data)
    else:
        return 'Maaf halaman tidak dapat diakses'
@app.route('/dosen')
def dosen():
    if 'username' in session :
        db = db_connect()
        sql = f"""select *
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

@app.route('/khs')
def khs():
    if 'username' in session:
        db = db_connect()
        sql = f"select * from simak_trn_khs  where MhswID = {session['username']}"
        with db:
            cur = db.cursor()
            cur.execute(sql)
            data = cur.fetchall()
        return render_template ('khs.html', data = data)
    else :
        return render_template('login.html')

@app.route('/perwalian')
def perwalian():
    if 'username' in session:
        db = db_connect()
        sql = f"select * from simak_trn_krs_perwalian where MhswID = {session['username']}"
        with db:
            cur = db.cursor()
            cur.execute(sql)
            data = cur.fetchall()
        return render_template ('perwalian.html', data = data)
    else :
        return render_template('login.html')

@app.route('/ruangan')
def ruangan():
    if 'username' in session:
        db = db_connect()
        sql = f"select RuangID , Lantai, Kapasitas from simak_mst_ruangan"
        with db:
            cur = db.cursor()
            cur.execute(sql)
            data = cur.fetchall()
        return render_template ('ruangan.html', data = data)
    else :
        return render_template('login.html')
        
@app.route('/struktur')
def struktur():
    if 'username' in session:
        db = db_connect()
        sql = f"select Singkatan, Nama, Urutan from simak_mst_jenis_jabatan"
        with db:
            cur = db.cursor()
            cur.execute(sql)
            data = cur.fetchall()
        return render_template ('struktur.html', data = data)
    else :
        return render_template('login.html')

@app.route('/about')
def about():
    if 'username' in session:
        db = db_connect()
        sql = f"select * from simak_mst_kampus"
        with db:
            cur = db.cursor()
            cur.execute(sql)
            data = cur.fetchall()
        return render_template ('index.html', data = data)
    else :
        return render_template('login.html')

#if __name__ == '__main__'
#    app.run(debug=True)

