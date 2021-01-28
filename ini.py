from flask import Flask
from flask import request
from flask import render_template, redirect
from flask import session, url_for
from flask_json import FlaskJSON, JsonError, json_response, as_json
from authlib.integrations.flask_client import OAuth
import pymysql
import os
from datetime import timedelta

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
oauth = OAuth(app)
app.secret_key = 'tes cobacoba'
app.config.from_object('config')
#app.secret_key = os.getenv("APP_SECRET_KEY")
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
google = oauth.register(
    name='google',
    client_id='613016628391-9e3v2n5on64j70sdr2kslsuhoc8a8fbv.apps.googleusercontent.com',
    client_secret='Lk-bnNkDzrhaxbADcXC4Eb1Z',
    server_metadata_url=CONF_URL,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params = None,
    authorize_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@app.route('/authgoogle')
def authgoogle():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    #email = google.parse_id_token(token)
    resp = google.get('userinfo')
    user_info = resp.json()
    # do something with the token and profile
    session['email'] = user_info('email')
    #session['email'] = email
    return redirect('/home')

@app.route('/loginauth')
def loginauth():
    google = oauth.create_client('google')
    redirect_uri = url_for('authgoogle', _external=True)
    return google.authorize_redirect(redirect_uri)

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
    email = dict[session].get('email',None)
    return render_template ('index.html', email=email)


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



