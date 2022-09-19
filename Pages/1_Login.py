import streamlit as st
from auth_google import *

st.set_page_config(layout="wide")
with open('style.css') as f:
		st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

if os.path.isfile('my_secrets.py'): #Con esto chequeo si estoy en entorno local
	import my_secrets as ms
	DETA_KEY = ms.DETA_KEY
	CLIENT_ID = ms.CLIENT_ID
	CLIENT_SECRET = ms.CLIENT_SECRET
	REDIRECT_URI = ms.REDIRECT_URI
	print('Entorno local')
else:
	DETA_KEY = st.secrets["KEYS"]['DETA_KEY']
	CLIENT_ID = st.secrets["KEYS"]['CLIENT_ID']
	CLIENT_SECRET = st.secrets["KEYS"]['CLIENT_SECRET']
	REDIRECT_URI = st.secrets["KEYS"]['REDIRECT_URI']
	print('En producción')

if 'usuario' not in st.session_state:
	try:
		st.session_state['usuario'] = display_user()
	except:
	    st.session_state['usuario'] = 'Desconocido'

if st.session_state['usuario'] == 'Desconocido':
	st.title('Detalle de Usuario')
	st.write('1) Primero Logeate en Google:')
	st.markdown(get_login_str(),unsafe_allow_html=True)
else:
	st.write('Estas logeado como: '+st.session_state['usuario'])
	def nav_to():
		nav_script = """
		<meta http-equiv="refresh" content="0; url='%s'">
		""" % (REDIRECT_URI)
		st.write(nav_script, unsafe_allow_html=True)
	nav_to()


# st.write('')
# st.write('2. Después tocá el botón de entrar')
# if st.button('Entrar'):
# 	st.session_state['usuario'] = display_user()
# st.write('')
# st.write('')
# st.write('Usuario: '+st.session_state['usuario'])
# st.write('')
# st.write('')
# add_sidebar = st.selectbox('Ronda',('First Round','2nd'))