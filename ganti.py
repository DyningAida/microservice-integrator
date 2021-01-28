from flask import Flask, url_for, session
from flask import render_template, redirect
from authlib.integrations.flask_client import OAuth


app = Flask(__name__)
app.secret_key = '!secret'
app.config.from_object('config')

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth(app)
oauth.register(
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


@app.route('/')
def homepage():
    user = session.get('user')
    return render_template('home.html')


@app.route('/login')
def login():
    redirect_uri = url_for('authgoogle', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@app.route('/authgoogle')
def authgoogle():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token)
    session['user'] = user
    return redirect('/')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

app.run(debug=True)
