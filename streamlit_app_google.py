import streamlit as st
import pandas as pd
import os
import numpy as np
from datetime import time, datetime
from deta import Deta
from auth_google import *


if 'usuario' not in st.session_state:
    st.session_state['usuario'] = 'Desconocido'
st.set_page_config(layout="wide")
with open('style.css') as f:
		st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# para animaciones copadas https://www.youtube.com/watch?v=TXSOitGoINE
# https://lottiefiles.com/search?q=handshake&category=animations

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

deta = Deta(DETA_KEY)

db = deta.Base("primera_fase_bwin")
db_r = deta.Base("resultados")

def fetch_df():
	"""Devuelve los usuarios en la base de datos"""
	df = db.fetch()
	return df.items

df = fetch_df()
df = pd.DataFrame.from_dict(df[0])


distintos_paises = tuple(set(df['Pais_b'].append(df['Pais_a'])))


st.title('Prode Mundial')


#st.header('Esto es un header')
#st.subheader('Esto es un subheader')

with st.sidebar:
	st.title('Detalle de Usuario')
	st.write('1) Primero Logeate en Google:')
	st.markdown(body=get_login_str(), unsafe_allow_html=True)
	st.write('')
	st.write('2. Después tocá el botón de entrar')
	st.write('')
	if st.button('Entrar'):
		st.session_state['usuario'] = display_user()
	st.write('')
	st.write('')
	st.write('Usuario: '+st.session_state['usuario'])
	st.write('')
	st.write('')
	add_sidebar = st.selectbox('Ronda',('First Round','2nd'))

if st.session_state['usuario'] != 'Desconocido':
	
	if add_sidebar == 'First Round':
		grupos = ['A','B','C','D','E','F','G','H']
		colA, colB = st.columns(2)
		dicc = {}
		#resultados = {'usuario': st.session_state['usuario'],'fecha': ahora} #acá tengo que poner el usuario
	# 	if password_entered():
	# 		st.write(st.session_state["username"])
		def subir_resultados():
			st.session_state['fecha']=str(datetime.utcnow().date())+'-'+str(datetime.utcnow().time())
			st.balloons()
			return db_r.put({k: v for k, v in st.session_state.items()})
		st.button('Guardar cambios',on_click=subir_resultados)
		
		for i in range(0,8):	
			with st.expander('Grupo '+grupos[i]):
				dicc[grupos[i]] = df[df['grupo'] == grupos[i]]
				for j in range(0,len(dicc[grupos[i]])):
					col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([3,1,3,1,1,1,3,1,3]) #proporción en el ancho de las columnas
					key_a = (str(i)+str(j))+'a'
					key_b = (str(i)+str(j))+'b'
					with col1:
						st.number_input(label='', min_value=0, max_value=None, value=0, step=1, format=None, key=key_a, help=None, on_change=None, args=None)
					with col2:
						st.markdown(body =
		 						 f"""
		 						 <div class='div_partido'>
								   <p><span class='apuesta'>{dicc[grupos[i]]['win_a'][j]}</span></p>
		 						 </div>
		 						 """
		 						 , unsafe_allow_html=True)
					with col3:
						st.markdown(body =
		 						 f"""
		 						 <div class='div_partido'>
								   <p class='pais'>{dicc[grupos[i]]['Pais_a'][j]}</p>
		 						 </div>
		 						 """
		 						 , unsafe_allow_html=True)
					with col4:
						st.markdown(body =
		 						 f"""
		 						 <div class='div_partido'>
								   <p><span class='vs'>vs</span></p>
		 						 </div>
		 						 """
		 						 , unsafe_allow_html=True)
	
					with col5:
						st.markdown(body =
		 						 f"""
		 						 <div class='div_partido'>
								   <p><span class='apuesta'>{dicc[grupos[i]]['tie'][j]}</span></p>
		 						 </div>
		 						 """
		 						 , unsafe_allow_html=True)
	
					with col6:
						st.markdown(body =
		 						 f"""
		 						 <div class='div_partido'>
								   <p><span class='vs'>vs</span></p>
		 						 </div>
		 						 """
		 						 , unsafe_allow_html=True)
						
					with col7:
						st.markdown(body =
		 						 f"""
		 						 <div class='div_partido'>
								   <p class='pais'>{dicc[grupos[i]]['Pais_b'][j]}</p>
		 						 </div>
		 						 """
		 						 , unsafe_allow_html=True)		
	
					with col8:
						st.markdown(body =
		 						 f"""
		 						 <div class='div_partido'>
								   <p><span class='apuesta'>{dicc[grupos[i]]['win_b'][j]}</span></p>
		 						 </div>
		 						 """
		 						 , unsafe_allow_html=True)
					with col9:
							st.number_input(label='', min_value=0, max_value=None, value=0, step=1, format=None, key=key_b, help=None, on_change=None, args=None)
	 			
	
		st.write(st.session_state)
	# 	
	# 	
	# 	st.subheader('Range slider')
	
	# 	values = st.slider('Esto es para elegir un rango',0.0, 100.0, (25.0, 75.0))
	# 	st.write('Values:', values)
	
	# 	st.subheader('Range time slider')
	# 	
	# 	appointment = st.slider("Schedule your appointment:",value=(time(11, 30), time(12, 45)))
	# 	st.write("You're scheduled for:", appointment)
	# 		
	# 	st.subheader('Datetime slider')
	# 	
	# 	start_time = st.slider(
	# 	     "When do you start?",
	# 	     value=datetime(2020, 1, 1, 9, 30),
	# 	     format="MM/DD/YY - hh:mm")
	# 	st.write("Start time:", start_time)	
	# 	
	# 	color = st.select_slider( #https://docs.streamlit.io/library/api-reference/widgets/st.select_slider
	# 	     'Select a color of the rainbow',
	# 	     options=['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet'])
	# 	st.write('My favorite color is', color)	
	    
	# 	col1, col2 = st.columns(2)
	# 	columns = [col1, col2]
	# 	values = [5,4]
	# 	
	# 	for i in range(0,len(columns)):
	# 		with columns[i]:
	# 			st.metric(label='1', value=values[i],delta= "{:.2%}".format(values[i]/100))
	
	# 	st.dataframe(df)
	# 	
	# 	
	# 	st.header('st.checkbox')
	# 	
	# 	st.write ('What would you like to order?')
	# 	
	# 	icecream = st.checkbox('Ice cream')
	# 	coffee = st.checkbox('Coffee')
	# 	cola = st.checkbox('Cola')
	# 	
	# 	if icecream:
	# 	     st.write("Great! Here's some more 🍦")
	# 	
	# 	if coffee: 
	# 	     st.write("Okay, here's some coffee ☕")
	# 	
	# 	if cola:
	# 	     st.write("Here you go 🥤")
	# 	
	
	
	# if add_sidebar == 'Otra opción':
	# 	st.write('Otra opción')
	# 	pais_select = st.selectbox('Elegi un pais',distintos_paises) #las opciones son una tupla
	# 	
	# 	fig = px.bar(df,x='Pais_a',y='win_a')
	# 	st.plotly_chart(fig)
	# 	
	# 	st.header('st.button')
	# 	
	# 	df2 = pd.DataFrame(np.random.randn(200, 3),columns=['a', 'b', 'c'])
	# 	c = alt.Chart(df2).mark_circle().encode(
	#      x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])
	# 	st.write(c)
	# 	
	# 	options = st.multiselect(
	# 	     'What are your favorite colors',
	# 	     ['Green', 'Yellow', 'Red', 'Blue'],
	# 	     ['Yellow', 'Red'])
	# 	
	# 	st.write('You selected:', options)	
	
	# 	if st.button('Say hello'):
	# 		st.write('Why hello there')
	# 	else:
	# 		st.write('Goodbye')
