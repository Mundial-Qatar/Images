import streamlit as st
import pandas as pd
import os
import numpy as np
from datetime import time, datetime
from deta import Deta
from auth_google import *
import asyncio


# from streamlit_option_menu import option_menu

# para animaciones copadas https://www.youtube.com/watch?v=TXSOitGoINE
# https://lottiefiles.com/search?q=handshake&category=animations

#url: https://fedemazza-fdchi-test-google-streamlit-app-google-jpwo6d.streamlitapp.com/
print()
print()
print()
print('Corre todo el script de nuevo')

if os.path.isfile('my_secrets.py'): #Con esto chequeo si estoy en entorno local
	import my_secrets as ms
	DETA_KEY = ms.DETA_KEY
	CLIENT_ID = ms.CLIENT_ID
	CLIENT_SECRET = ms.CLIENT_SECRET
	REDIRECT_URI = ms.REDIRECT_URI
else:
	DETA_KEY = st.secrets["KEYS"]['DETA_KEY']
	CLIENT_ID = st.secrets["KEYS"]['CLIENT_ID']
	CLIENT_SECRET = st.secrets["KEYS"]['CLIENT_SECRET']
	REDIRECT_URI = st.secrets["KEYS"]['REDIRECT_URI']

st.set_page_config(layout="wide")
with open('style.css') as f:
		st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


print('Carga bases de datos')
deta = Deta(DETA_KEY)

db = deta.Base("primera_fase_bwin")
db_r = deta.Base("resultados")

def fetch_df(db):
	"""Devuelve la info de la base de datos"""
	df = db.fetch()
	return df.items

df = fetch_df(db)
df = pd.DataFrame.from_dict(df[0])
df['Fecha_partido'] = df['Fecha_partido'].apply(lambda x: datetime.strptime(x, '%d/%m/%y %H:%M'))
df = df.sort_values('Fecha_partido')
df['Fecha_partido'] = df['Fecha_partido'].apply(lambda x: str(x))
df_r = fetch_df(db_r)
df_r = pd.DataFrame.from_dict(df_r)


def set_user():
	st.session_state['usuario'] = display_user()

def nav_to():
	nav_script = """
	<meta http-equiv="refresh" content="0; url='%s'">
	""" % (REDIRECT_URI+'Login')
	st.write(nav_script, unsafe_allow_html=True)

if 'usuario' not in st.session_state:
    try:
        set_user()
        Corrio = 'OK'
        print('Corrio = OK, set user')
        print('el valor de session es '+st.session_state['usuario'])
    except:
        Corrio = 'NOK'
        print('Error No Corrio')
        nav_to()
        print('NO corrio el set user numero 1, mando a logear')
else:
 	Corrio = 'OK'
 	print('Corrio = OK')
 	st.session_state['params'] = st.experimental_get_query_params()
	
	
st.title('Prode Mundial')


with st.sidebar:
	add_sidebar = st.selectbox('Ronda',('First Round','2nd'),key='params_key') #

	
if Corrio == 'OK':
	
	st.write('Hola '+st.session_state['usuario']+'!')
	if add_sidebar == 'First Round':
		grupos = ['A','B','C','D','E','F','G','H']
		colA, colB = st.columns(2)
		dicc = {}
		def subir_resultados():
			st.session_state['fecha']=str(datetime.utcnow().date())+'-'+str(datetime.utcnow().time())
			st.balloons()
			return db_r.put({k: v for k, v in st.session_state.items()})
		st.button('Guardar cambios',on_click=subir_resultados)
		
		
		for i in range(0,8):
			with st.expander('Grupo '+grupos[i]):
				dicc[grupos[i]] = df[df['grupo'] == grupos[i]]
				for j in range(0,len(dicc[grupos[i]])):
					col1, col2, col3= st.columns([2,8,2]) #proporción en el ancho de las columnas
					key_a = str(i)+'-'+str(j)+'a'
					key_b = str(i)+'-'+str(j)+'b'
					rec_a = 0
					rec_b = 0
					try: #Este try es por si la base de datos de resultados está vacía. En ese caso df_r['usuario'] falla
						if st.session_state['usuario'] in [x for x in df_r['usuario']]:
							max_fecha = df_r[(df_r['usuario'] == st.session_state['usuario'])]['fecha'].max()
							row = df_r[(df_r['usuario'] == st.session_state['usuario'])&(df_r['fecha'] == max_fecha)]
							rec_a = [x for x in row[key_a]][0]
							rec_b = [x for x in row[key_b]][0]
					except:
						pass
					
					text_hover = dicc[grupos[i]]['Fecha_partido'][j]
					
					with col1:        #Espacio para resultado 1er Equipo
						st.number_input(label='', min_value=0, max_value=None, value=rec_a, step=1, format=None, key=key_a, help=None, on_change=None, args=None)
					
					with col3:                  #Espacio para resultado 2do equipo
							st.number_input(label='', min_value=0, max_value=None, value=rec_b, step=1, format=None, key=key_b, help=None, on_change=None, args=None)
					
					apuesta_a, apuesta_b, apuesta_tie = 'apuesta','apuesta','apuesta'
					if st.session_state[key_a]>st.session_state[key_b]:
						apuesta_a = 'apuesta_elegida'
					elif st.session_state[key_a]<st.session_state[key_b]:
						apuesta_b = 'apuesta_elegida'
					else:
						apuesta_tie = 'apuesta_elegida'
						
						
					with col2:        #Score BWIN 1er Equipo
						st.markdown(body =
		 						 f"""
								  <div class='middle container'>
			 						 <div class='div_partido_prueba'>
										 <p style="width: 10%;"><span class={apuesta_a}>{dicc[grupos[i]]['win_a'][j]}</span></p>
									     <img src="https://github.com/Mundial-Qatar/Prode/blob/main/Flags/{dicc[grupos[i]]['Pais_a'][j]}.png?raw=true" alt="Bandera {dicc[grupos[i]]['Pais_a'][j]}"> 
									     <p class='pais' style="width: 20%;">{dicc[grupos[i]]['Pais_a'][j]}<span class="tooltiptext">{text_hover}</span></p>							     
										 <p style="width: 10%;"><span class={apuesta_tie}>{dicc[grupos[i]]['tie'][j]}</span></p>
										 <p class='pais' style="width: 20%;">{dicc[grupos[i]]['Pais_b'][j]}<span class="tooltiptext">{text_hover}</span></p>
										 <img src="https://github.com/Mundial-Qatar/Prode/blob/main/Flags/{dicc[grupos[i]]['Pais_b'][j]}.png?raw=true" alt="Bandera {dicc[grupos[i]]['Pais_a'][j]}">
										 <p style="width: 10%;"><span class={apuesta_b}>{dicc[grupos[i]]['win_b'][j]}</span></p>
								   	 </div>
								  </div>
		 						 """
		 						 , unsafe_allow_html=True)
					
					

					

	 			
else:
	st.write('Usuario es desconocido')  
