import streamlit as st
import pandas as pd
import os
import numpy as np
from datetime import time, datetime
from deta import Deta
from auth_google import *
import asyncio
import altair as alt


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
db_log = deta.Base("usuarios_db")
db_s = deta.Base("semi")
db_puntos = deta.Base("tabla_puntos")
db_torneo = deta.Base("torneo_amigos")

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
df_s = fetch_df(db_s)
df_s = pd.DataFrame.from_dict(df_s)

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

grupos = ['A','B','C','D','E','F','G','H']
grupos_paises = {'A':['Catar', 'Ecuador','Senegal','Países Bajos'],
		   'B':['Inglaterra', 'Irán','Estados Unidos','Gales'],
		   'C':['Argentina', 'Arabia Saudita','México','Polonia'],
		   'D':['Francia', 'Dinamarca','Túnez','Australia'],
		   'E':['España', 'Alemania','Japón','Costa Rica'],
		   'F':['Bélgica', 'Canadá','Marruecos','Croacia'],
		   'G':['Brasil', 'Serbia','Suiza','Camerún'],
		   'H':['Portugal', 'Ghana','Uruguay','Corea del Sur']		   
		   }

paises = {'Catar':51, 'Ecuador':17,'Senegal':11,'Países Bajos':3.5,
		  'Inglaterra':2.5, 'Irán':67,'Estados Unidos':13,'Gales':17,
		  'Argentina':2.5, 'Arabia Saudita':151,'México':17,'Polonia':15,
		  'Francia':2.5, 'Dinamarca':5,'Túnez':51,'Australia':41,
		  'España':2.85, 'Alemania':3,'Japón':29,'Costa Rica':151,
		  'Bélgica':3.5, 'Canadá':51,'Marruecos':19,'Croacia':8,
		  'Brasil':2.25, 'Serbia':13,'Suiza':11,'Camerún':29,
		  'Portugal':3.75, 'Ghana':41,'Uruguay':7.5,'Corea del Sur':34		   
		   }

df_paises = pd.DataFrame.from_dict(paises,orient='index').reset_index()
df_paises.columns = ['pais','ratio']
df_paises = df_paises.sort_values('ratio').reset_index()



col_a , col_b = st.columns([10,4])
with col_a:
	st.title('Prode Qatar 2022')
with col_b:
	seccion = st.selectbox('Ronda',('Fase de grupos','Semifinalistas','Simulador','Posiciones','Torneo de amigos'),key='params_key') #

st.markdown(body =
 						 f"""
					
					<img alt="logo_mundial_qatar" class="logomundial" src="https://github.com/Mundial-Qatar/Prode/blob/main/BANNER-LOGO.jpg?raw=true">
 						 """
 						 , unsafe_allow_html=True)


if Corrio == 'OK':
	
	####----Cálculos que quiero hacer para este usuario-----------------------------------------------------------
	
	#st.session_state['usuario']
	def puntos_segun_fecha_usuario(fecha='2022-12-18',usuario=st.session_state['usuario']):
		fecha_parametro_date = datetime.strptime(fecha, '%Y-%m-%d')
		puntos_player = 0
		dicc = {}
		for i in range(0,8):
			dicc[grupos[i]] = df[df['grupo'] == grupos[i]]
			for j in range(0,len(dicc[grupos[i]])):
				key_a = str(i)+'-'+str(j)+'a'
				key_b = str(i)+'-'+str(j)+'b'
				rec_a = 0
				rec_b = 0
				try: #Este try es por si la base de datos de resultados está vacía. En ese caso df_r['usuario'] falla
					if usuario in [x for x in df_r['usuario']]:
						max_fecha = df_r[(df_r['usuario'] == usuario)]['fecha'].max()
						row = df_r[(df_r['usuario'] == usuario)&(df_r['fecha'] == max_fecha)]
						rec_a = [x for x in row[key_a]][0]
						rec_b = [x for x in row[key_b]][0]
				except:
					pass
				fecha_partido_str_hora = dicc[grupos[i]]['Fecha_partido'][j]
				#fecha_partido_str_hora = dicc[grupos[0]]['Fecha_partido'][0]
				fecha_partido_date_hora = datetime.strptime(fecha_partido_str_hora, '%Y-%m-%d %H:%M:%S')
				fecha_partido_str = fecha_partido_date_hora.strftime('%Y-%m-%d')
				fecha_partido_date = datetime.strptime(fecha_partido_str, '%Y-%m-%d')
				
				key_a = str(i)+'-'+str(j)+'a'
				key_b = str(i)+'-'+str(j)+'b'
				rec_a_real = 0
				rec_b_real = 0
				try: #Este try es por si la base de datos de resultados está vacía. En ese caso df_r['usuario'] falla
					max_fecha = df_r[(df_r['usuario'] == 'mazzafedeitalia@gmail.com')]['fecha'].max()
					row_real = df_r[(df_r['usuario'] == 'mazzafedeitalia@gmail.com')&(df_r['fecha'] == max_fecha)]
					rec_a_real = [x for x in row_real[key_a]][0]
					rec_b_real = [x for x in row_real[key_b]][0]
				except:
					pass
				
				rec_a = 0
				rec_b = 0
				try: #Este try es por si la base de datos de resultados está vacía. En ese caso df_r['usuario'] falla
					max_fecha = df_r[(df_r['usuario'] == usuario)]['fecha'].max()
					row = df_r[(df_r['usuario'] == usuario)&(df_r['fecha'] == max_fecha)]
					rec_a = [x for x in row[key_a]][0]
					rec_b = [x for x in row[key_b]][0]
				except:
					pass						
				
				if fecha_partido_date <= fecha_parametro_date:
				
					puntos_ganador = 0
					puntos_marcador = 0
					puntos_partido = 0
					
					formato_ganador = 'class-pendiente'
					formato_marcador = 'class-pendiente'
					formato_total = 'class-pendiente'
		
					if rec_a_real == 99:
						rec_a_real = 'X'
						rec_b_real = 'X'
						estado_resultado = 'Todavía no se cargó el resultado'
					else:
						if rec_a_real > rec_b_real:
							outcome_real = 'Gana A'
						elif rec_a_real < rec_b_real:
							outcome_real = 'Gana B'
						else:
							outcome_real = 'Empate'
						
						if rec_a > rec_b:
							outcome_pronostico = 'Gana A'
							ratio_ganador = float(dicc[grupos[i]]['win_a'][j])
						elif rec_a < rec_b:
							outcome_pronostico = 'Gana B'
							ratio_ganador = float(dicc[grupos[i]]['win_b'][j])
						else:
							outcome_pronostico = 'Empate'
							ratio_ganador = float(dicc[grupos[i]]['tie'][j])
						
						if outcome_real == outcome_pronostico:
							puntos_ganador = ratio_ganador
							formato_ganador = 'class-ganador'
							puntos_partido = puntos_ganador
						else:
							puntos_ganador = 0
							formato_ganador = 'class-perdedor'
							formato_marcador = 'class-perdedor'
						
						if (rec_a == rec_a_real) & (rec_b == rec_b_real):
							if rec_a + rec_b >2.5:
								puntos_partido = round(2*puntos_ganador,3)
								formato_marcador = 'class-ganador'
							else:
								puntos_partido = round(1.5*puntos_ganador,3)
								formato_marcador = 'class-ganador'
							puntos_marcador = round(puntos_partido - puntos_ganador,3)
						else:
							puntos_marcador = 0
						
						puntos_player = puntos_player + puntos_partido
						
		return puntos_player
				 
	
	
	st.session_state['puntos_player'] = puntos_segun_fecha_usuario()
	
	
	
	####----Función que evalua resultados-----------------------------------------------------------
	
	def función_resultados_totales():
		fechas_string = ['2022-11-20','2022-11-21','2022-11-22','2022-11-23','2022-11-24',
					 '2022-11-25','2022-11-26','2022-11-27','2022-11-28','2022-11-29',
					 '2022-11-30','2022-12-01','2022-12-02']
# 						,'2022-12-03','2022-12-04',
# 					 '2022-12-05','2022-12-06','2022-12-07','2022-12-08','2022-12-09',
# 					 '2022-12-10','2022-12-11','2022-12-12','2022-12-13','2022-12-14',
# 					 '2022-12-15','2022-12-16','2022-12-17','2022-12-18',]
		
		usuarios_con_pronosticos = df_r['usuario'].unique()
		def pasar_a_fecha(fecha):
			return datetime.strptime(fecha, '%Y-%m-%d')
		
		df_pnts = pd.DataFrame(columns=['user','fecha', 'puntos'])
		for user in usuarios_con_pronosticos:
			for fecha in fechas_string:
				puntos = puntos_segun_fecha_usuario(fecha=fecha,usuario=user)
				#puntos = 92
				df_puntos_append = pd.DataFrame({'user':user,'fecha':fecha,'puntos':puntos}, index=[0])	
				df_pnts = df_pnts.append(df_puntos_append)
		df_pnts_dict = df_pnts.to_dict('list')
		return db_puntos.put({'df_puntos': df_pnts_dict,'fecha':datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')})
	


	####---------------------------------------------------------------
	
		
	
	
	
	
	if seccion == 'Fase de grupos':
		if (st.session_state['usuario'] != 'mazzafedeitalia@gmail.com')&(st.session_state['usuario'] != 'mazzafede@gmail.com'):
			db_log.put({'user': st.session_state['usuario'], 'fecha': str(datetime.utcnow().date())+'-'+str(datetime.utcnow().time())})
		colA, colB = st.columns(2)
		dicc = {}
		def subir_resultados():
			st.session_state['fecha']=str(datetime.utcnow().date())+'-'+str(datetime.utcnow().time())
			st.balloons()
			if (st.session_state['usuario'] == 'mazzafedeitalia@gmail.com'):
				función_resultados_totales()    #acá quiero que corra una función que evalúa resultados para todos
				print('esto corrio')
			return db_r.put({k: v for k, v in st.session_state.items()})
		print('hay cartel?')
		col_usuario, col_guardar = st.columns([1,1])
		with col_usuario:
			st.write('Hola '+st.session_state['usuario']+'!')
		with col_guardar:
			st.button('Guardar cambios',on_click=subir_resultados, key=1)
		
		ratio_columnas = [2,6,2,4,5]
		for i in range(0,8):
			with st.expander('Grupo '+grupos[i]):
				dicc[grupos[i]] = df[df['grupo'] == grupos[i]]
				col11, col12, col13, col14, col15 = st.columns(ratio_columnas) #proporción en el ancho de las columnas
				with col11:
					st.markdown(body =
			 						 f"""
					          <div class='div_partido_prueba'>
								  <p class='Titulosreco'><span class=Titulos></span></p>
							  </div>	  
							  <div class='middle container'>
			 						 <div class='div_partido_prueba'>
									 <p><span class=Titulos>Equipo A</span></p>
									 </div>
							  </div>
			 						 """
			 						 , unsafe_allow_html=True)
				with col13:
					st.markdown(body =
			 						 f"""
					          <div class='div_partido_prueba'>
								  <p class='Titulosreco'><span class=Titulos></span></p>
							  </div>	  
							  <div class='middle container'>
			 						 <div class='div_partido_prueba'>
									 <p><span class=Titulos>Equipo B</span></p>
									 </div>
							  </div>
			 						 """
			 						 , unsafe_allow_html=True)
				with col12:
					st.markdown(body =
			 						 f"""
		
								  <div class='middle container'>
									  <div class='div_partido_prueba'>
										  <p style="width: 15%;"><span class=Titulos></span></p>
			  						      <p style="width: 30%;"><span class=Titulos></span></p>
										  <p style="width: 15%;"><span class=Titulos></span></p>
										  <p style="width: 30%;"><span class=Titulos></span></p>
									      <p style="width: 15%;"><span class=Titulos></span></p>
									  </div>
							      </div>
			 						 """
			 						 , unsafe_allow_html=True)	
					
		
		
				with col14:			
					st.markdown(body =
			 						 f"""
				  <div class='Titulos'>
					  <div class='div_partido_prueba'>
						  <p class='Titulosreco'><span class=Titulos>Recompensas (Bwin)</span></p>
					  </div>
					  <div class='div_partido_prueba'>
						  <p class='Titulosreco'><span class=Titulos>Gana A</span></p>
						  <p class='Titulosreco'><span class=Titulos>Emp</span></p>
						  <p class='Titulosreco'><span class=Titulos>Gana B</span></p>
					  </div>
				  </div>
			 						 """
			 						 , unsafe_allow_html=True)	
		
				with col15:			
					st.markdown(body =
			 						 f"""
				  <div class='Titulos'>
					  <div class='div_partido_prueba'>
						  <p class='Titulosmarca'><span class=Titulos>Marcador exacto</span></p>
					  </div>
					  <div class='div_partido_prueba'>
						  <p class='Titulosmarca'><span class=Titulos>< 2.5 goles (x1.5)</span></p>
						  <p class='Titulosmarca'><span class=Titulos>> 2.5 goles (x2)</span></p>
					  </div>
				  </div>
			 						 """
			 						 , unsafe_allow_html=True)		
					
				
				st.markdown(body =
			 						 f"""
									<hr>
			 						 """
			 						 , unsafe_allow_html=True)
				
				for j in range(0,len(dicc[grupos[i]])):
					col1, col2, col3, col4, col5 = st.columns(ratio_columnas) #proporción en el ancho de las columnas
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
						st.number_input(label='', min_value=0, max_value=100, value=rec_a, step=1, format=None, key=key_a, help=None, on_change=None, args=None)
					
					with col3:                  #Espacio para resultado 2do equipo
							st.number_input(label='', min_value=0, max_value=100, value=rec_b, step=1, format=None, key=key_b, help=None, on_change=None, args=None)
					
					apuesta_a, apuesta_b, apuesta_tie, apuesta_low, apuesta_high = 'apuesta','apuesta','apuesta','apuesta','apuesta'
					if st.session_state[key_a]>st.session_state[key_b]:
						apuesta_a = 'apuesta_elegida'
						apuesta_definida = dicc[grupos[i]]['win_a'][j]
					elif st.session_state[key_a]<st.session_state[key_b]:
						apuesta_b = 'apuesta_elegida'
						apuesta_definida = dicc[grupos[i]]['win_b'][j]
					else:
						apuesta_tie = 'apuesta_elegida'
						apuesta_definida = dicc[grupos[i]]['tie'][j]
						
					suma_goles = st.session_state[key_a]+st.session_state[key_b]
					if suma_goles < 2.5:
						apuesta_low = 'apuesta_elegida'
					else:
						apuesta_high = 'apuesta_elegida'
						
						
					with col2:        #Score BWIN 1er Equipo
						st.markdown(body =
		 						 f"""
								  <div class='middle container'>
			 						 <div class='div_partido_prueba'>
									     <img src="https://github.com/Mundial-Qatar/Prode/blob/main/Flags/{dicc[grupos[i]]['Pais_a'][j]}.png?raw=true" alt="Bandera {dicc[grupos[i]]['Pais_a'][j]}"> 
									     <p class='pais' style="width: 20%;">{dicc[grupos[i]]['Pais_a'][j]}<span class="tooltiptext">{text_hover}</span></p>							     
									     <p class='pais' style="width: 5%;">-<span class="tooltiptext">{text_hover}</span></p>							     
										 <p class='pais' style="width: 20%;">{dicc[grupos[i]]['Pais_b'][j]}<span class="tooltiptext">{text_hover}</span></p>
										 <img src="https://github.com/Mundial-Qatar/Prode/blob/main/Flags/{dicc[grupos[i]]['Pais_b'][j]}.png?raw=true" alt="Bandera {dicc[grupos[i]]['Pais_a'][j]}">
								   	 </div>
								  </div>
		 						 """
		 						 , unsafe_allow_html=True)
					
					with col4:			
						st.markdown(body =
				 						 f"""
					  <div class='Titulos'>
						  <div class='div_partido_prueba'>
							  <p><span class={apuesta_a}>{dicc[grupos[i]]['win_a'][j]}</span></p>
							  <p><span class={apuesta_tie}>{dicc[grupos[i]]['tie'][j]}</span></p>
							  <p><span class={apuesta_b}>{dicc[grupos[i]]['win_b'][j]}</span></p>
						  </div>
					  </div>
				 						 """
				 						 , unsafe_allow_html=True)
							
					with col5:			
						st.markdown(body =
				 						 f"""
					  <div class='Titulos'>
						  <div class='div_partido_prueba'>
							  <p><span class={apuesta_low}>{round(float(apuesta_definida)*1.5,3)}</span></p>
							  <p><span class={apuesta_high}>{round(float(apuesta_definida)*2,3)}</span></p>
						  </div>
					  </div>
				 						 """
				 						 , unsafe_allow_html=True)
		st.button('Guardar cambios',on_click=subir_resultados, key=2)	




####-------------------------------------------------------------------------------------------------------------------------------------






			
	elif seccion == 'Simulador':
		puntos_player = 0
		st.title('Puntos (simulador): '+str(round(st.session_state['puntos_player'],2)))
		st.write('Esta sección todavía está en construcción')
		if st.session_state['usuario'] in [x for x in df_r['usuario']]:

			now = datetime.utcnow()
			now = datetime.strptime('2022-11-25 13:00:00', '%Y-%m-%d %H:%M:%S')
			for i in range(0,8):
				with st.expander('Grupo '+grupos[i]):
					dicc = {}
					dicc[grupos[i]] = df[df['grupo'] == grupos[i]]
					
					proporcion_cols = [4,2,3]
					col_tit1, col_tit2, col_tit3 = st.columns(proporcion_cols)
	
					with col_tit1:        
	
						st.markdown(body =
		 						 f"""
							     <div class='middle container'>
			 						 <div class='div_partido_prueba'>
									     <p class='pais' style="width: 25%;">Fecha</p>								 
										 <p class='pais' style="width: 20%;">Equipo A</p>
										 <p class='pais' style="width: 35%;"> </p>							     
										 <p class='pais' style="width: 20%;">Equipo B</p>								 
								   	 </div>
								 </div>
		 						 """
		 						 , unsafe_allow_html=True)		

					with col_tit3:        
	
						st.markdown(body =
		 						 f"""
							     <div class='middle container'>
			 						 <div class='div_partido_prueba'>
									     <p class='pais' style="width: 33%;">Puntos Ganador</p>								 
										 <p class='pais' style="width: 33%;">Puntos Marcador</p>						     
										 <p class='pais' style="width: 34%;">Puntos Partido</p>								 
								   	 </div>
								 </div>
		 						 """
		 						 , unsafe_allow_html=True)							
					
					
					for j in range(0,len(dicc[grupos[i]])):
						text_hover = dicc[grupos[i]]['Fecha_partido'][j]
						col_p1, col_p2, col_p3 = st.columns(proporcion_cols) #proporción en el ancho de las columnas
						
						
						
						key_a = str(i)+'-'+str(j)+'a'
						key_b = str(i)+'-'+str(j)+'b'
						rec_a_real = 0
						rec_b_real = 0
						try: #Este try es por si la base de datos de resultados está vacía. En ese caso df_r['usuario'] falla
							max_fecha = df_r[(df_r['usuario'] == 'mazzafedeitalia@gmail.com')]['fecha'].max()
							row_real = df_r[(df_r['usuario'] == 'mazzafedeitalia@gmail.com')&(df_r['fecha'] == max_fecha)]
							rec_a_real = [x for x in row_real[key_a]][0]
							rec_b_real = [x for x in row_real[key_b]][0]
						except:
							pass
						
						rec_a = 0
						rec_b = 0
						try: #Este try es por si la base de datos de resultados está vacía. En ese caso df_r['usuario'] falla
							max_fecha = df_r[(df_r['usuario'] == st.session_state['usuario'])]['fecha'].max()
							row = df_r[(df_r['usuario'] == st.session_state['usuario'])&(df_r['fecha'] == max_fecha)]
							rec_a = [x for x in row[key_a]][0]
							rec_b = [x for x in row[key_b]][0]
						except:
							pass						
						
						
						fecha_formato_fecha = datetime.strptime(text_hover, '%Y-%m-%d %H:%M:%S')

						puntos_ganador = 0
						puntos_marcador = 0
						puntos_partido = 0
						
						formato_ganador = 'class-pendiente'
						formato_marcador = 'class-pendiente'
						formato_total = 'class-pendiente'

						if rec_a_real == 99:
							rec_a_real = 'X'
							rec_b_real = 'X'
							estado_resultado = 'Todavía no se cargó el resultado'
						else:
							if rec_a_real > rec_b_real:
								outcome_real = 'Gana A'
							elif rec_a_real < rec_b_real:
								outcome_real = 'Gana B'
							else:
								outcome_real = 'Empate'
							
							if rec_a > rec_b:
								outcome_pronostico = 'Gana A'
								ratio_ganador = float(dicc[grupos[i]]['win_a'][j])
							elif rec_a < rec_b:
								outcome_pronostico = 'Gana B'
								ratio_ganador = float(dicc[grupos[i]]['win_b'][j])
							else:
								outcome_pronostico = 'Empate'
								ratio_ganador = float(dicc[grupos[i]]['tie'][j])
							
							if outcome_real == outcome_pronostico:
								puntos_ganador = ratio_ganador
								formato_ganador = 'class-ganador'
								puntos_partido = puntos_ganador
							else:
								puntos_ganador = 0
								formato_ganador = 'class-perdedor'
								formato_marcador = 'class-perdedor'
							
							if (rec_a == rec_a_real) & (rec_b == rec_b_real):
								if rec_a + rec_b >2.5:
									puntos_partido = round(2*puntos_ganador,3)
									formato_marcador = 'class-ganador'
								else:
									puntos_partido = round(1.5*puntos_ganador,3)
									formato_marcador = 'class-ganador'
								puntos_marcador = round(puntos_partido - puntos_ganador,3)
							else:
								puntos_marcador = 0
							
							puntos_player = puntos_player + puntos_partido 
							estado_resultado = 'Resultado disponible'
							
						
						
						
						with col_p1:        
	
							st.markdown(body =
			 						 f"""
								     <div class='middle container'>
				 						 <div class='div_partido_prueba'>
										     <p class='pais' style="width: 25%;">{text_hover}<span class="tooltiptext">{text_hover}</span></p>								 
											 <p class='pais' style="width: 5%;"><span class="tooltiptext">{text_hover}</span></p>
										     <img src="https://github.com/Mundial-Qatar/Prode/blob/main/Flags/{dicc[grupos[i]]['Pais_a'][j]}.png?raw=true" alt="Bandera {dicc[grupos[i]]['Pais_a'][j]}"> 
										     <p class='pais' style="width: 15%;">{dicc[grupos[i]]['Pais_a'][j]}<span class="tooltiptext">{text_hover}</span></p>							     
										     <p class='pais' style="width: 10%;">{rec_a_real}<span class="tooltiptext">{text_hover}</span></p>
											 <p class='pais' style="width: 5%;">-<span class="tooltiptext">{text_hover}</span></p>							     
											 <p class='pais' style="width: 10%;">{rec_b_real}<span class="tooltiptext">{text_hover}</span></p>
											 <p class='pais' style="width: 15%;">{dicc[grupos[i]]['Pais_b'][j]}<span class="tooltiptext">{text_hover}</span></p>
											 <img src="https://github.com/Mundial-Qatar/Prode/blob/main/Flags/{dicc[grupos[i]]['Pais_b'][j]}.png?raw=true" alt="Bandera {dicc[grupos[i]]['Pais_a'][j]}">
									   	 </div>
									 </div>
			 						 """
			 						 , unsafe_allow_html=True)
						


							
						
						with col_p2:					
							st.markdown(body =
			 						 f"""
								     <div class='middle container'>
				 						 <div class='div_partido_prueba'>
										     <p class='pais' style="width: 100%;">{estado_resultado}<span class="tooltiptext">{text_hover}</span></p>								 
									   	 </div>
									 </div>
			 						 """
			 						 , unsafe_allow_html=True)
						
						
						
						with col_p3:					
							st.markdown(body =
			 						 f"""
								     <div class='middle container'>
				 						 <div class='div_partido_prueba'>
										     <p class='{formato_ganador}' style="width: 33%;">{puntos_ganador}</p>								 
											 <p class='{formato_marcador}' style="width: 33%;">{puntos_marcador}</p>						     
											 <p class='{formato_ganador}' style="width: 34%;">{puntos_partido}</p>	
									   	 </div>
									 </div>
			 						 """
			 						 , unsafe_allow_html=True)
		else:
			st.write('tenés que tener resultados guardados para poder usar esta sección')	
			
####-------------------------------------------------------------------------------------------------------------------------------------
			
			
	elif seccion == 'Semifinalistas':
		st.markdown(body = '<br>', unsafe_allow_html=True)
		options = []
		try: #Este try es por si la base de datos de resultados está vacía. En ese caso df_r['usuario'] falla
			if st.session_state['usuario'] in [x for x in df_s['usuario']]:
				max_fecha = df_s[(df_s['usuario'] == st.session_state['usuario'])]['fecha'].max()
				row = df_s[(df_s['usuario'] == st.session_state['usuario'])&(df_s['fecha'] == max_fecha)]
				options = list(row['semis'])[0]
		except:
			pass
		
		def subir_resultados_semis():
			if len(options)!=4:
				return
			st.session_state['fecha']=str(datetime.utcnow().date())+'-'+str(datetime.utcnow().time())
			st.balloons()
			return db_s.put({k: v for k, v in st.session_state.items()})
		st.button('Guardar cambios',on_click=subir_resultados_semis, key=3)
		options = st.multiselect('Elegí 4 paises que pienses que pasan a la semi',df_paises['pais'],default=options)
		col_semi1,col_semi2,col_semi3,col_semi4 = st.columns([1,1,1,1])
		
		a = 0
		with col_semi1:
			for i in range(a,a+8):
				st.markdown(body =
			 						 f"""
								     <div class='middle container'>
				 						 <div class='div_partido_semis'>
											  <img src="https://github.com/Mundial-Qatar/Prode/blob/main/Flags/{df_paises['pais'][i]}.png?raw=true" alt="Bandera {df_paises['pais'][i]}">
											  <p class='pais' style="width: 30%;">{df_paises['pais'][i]}</p>
											  <p class='pais' style="width: 10%;"></p>
											  <p class='pais' style="width: 30%;">{str(df_paises['ratio'][i])}</p>
									   	 </div>
									 </div>
			 						 """
			 						 , unsafe_allow_html=True)

		a = a + 8
		with col_semi2:
			for i in range(a,a+8):
				st.markdown(body =
			 						 f"""
								     <div class='middle container'>
				 						 <div class='div_partido_semis'>
											  <img src="https://github.com/Mundial-Qatar/Prode/blob/main/Flags/{df_paises['pais'][i]}.png?raw=true" alt="Bandera {df_paises['pais'][i]}">
											  <p class='pais' style="width: 30%;">{df_paises['pais'][i]}</p>
											  <p class='pais' style="width: 10%;"></p>
											  <p class='pais' style="width: 30%;">{str(df_paises['ratio'][i])}</p>
											</div>
									 </div>
			 						 """
			 						 , unsafe_allow_html=True)

			
		a = a + 8
		with col_semi3:
			for i in range(a,a+8):
				st.markdown(body =
			 						 f"""
								     <div class='middle container'>
				 						 <div class='div_partido_semis'>
											  <img src="https://github.com/Mundial-Qatar/Prode/blob/main/Flags/{df_paises['pais'][i]}.png?raw=true" alt="Bandera {df_paises['pais'][i]}">
											  <p class='pais' style="width: 30%;">{df_paises['pais'][i]}</p>
											  <p class='pais' style="width: 10%;"></p>
											  <p class='pais' style="width: 30%;">{str(df_paises['ratio'][i])}</p>
									   	 </div>
									 </div>
			 						 """
			 						 , unsafe_allow_html=True)

				
		a = a + 8
		with col_semi4:
			for i in range(a,a+8):
				st.markdown(body =
			 						 f"""
								     <div class='middle container'>
				 						 <div class='div_partido_semis'>
											  <img src="https://github.com/Mundial-Qatar/Prode/blob/main/Flags/{df_paises['pais'][i]}.png?raw=true" alt="Bandera {df_paises['pais'][i]}">
											  <p class='pais' style="width: 30%;">{df_paises['pais'][i]}</p>
											  <p class='pais' style="width: 10%;"></p>
											  <p class='pais' style="width: 30%;">{str(df_paises['ratio'][i])}</p>
									   	 </div>
									 </div>
			 						 """
			 						 , unsafe_allow_html=True)
		
		st.session_state['semis'] = options
		
		
		
####-----Posiciones----------------------------------------------------------------------------------------------------------------
					
		
	elif seccion == 'Posiciones':
		df_torneo = fetch_df(db_torneo)
		df_torneo = pd.DataFrame.from_dict(df_torneo)
		mis_torneos = []
		for i in range(0,len(df_torneo)):
			if st.session_state['usuario'] in df_torneo.iloc[i]['friends_list']:
				mis_torneos.append(df_torneo.iloc[i]['friends_name'])
		mis_torneos.append('No estoy en ningún torneo')
		friends_name = st.selectbox('Si estás en algún torneo elegilo',options=mis_torneos)
		if friends_name != 'No estoy en ningún torneo':
			max_fecha = df_torneo[df_torneo['friends_name']==friends_name]['fecha'].max()
			torneo_existente = df_torneo[(df_torneo['friends_name']==friends_name)&(df_torneo['fecha']==max_fecha)]
			participantes = list(torneo_existente['friends_list'])[0]
		else:
			participantes = [st.session_state['usuario']]
	
		def pasar_a_fecha_2(fecha):
			return datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
		def pasar_a_fecha_3(fecha):
			return datetime.strptime(fecha, '%Y-%m-%d')		
		df_puntos = fetch_df(db_puntos)
		max_fecha = pasar_a_fecha_2('2020-11-05 19:33:00')
		for i in range(0,len(df_puntos)):
			if pasar_a_fecha_2(df_puntos[i]['fecha']) > max_fecha:
				max_fecha = pasar_a_fecha_2(df_puntos[i]['fecha'])
				df_puntos_aux = df_puntos[i]['df_puntos']
		print(max_fecha)
		df_puntos = df_puntos_aux.copy()
		df_puntos = pd.DataFrame.from_dict(df_puntos)
		df_puntos = df_puntos[df_puntos['user'].isin(participantes)]
		
		df_puntos['puntos'] = df_puntos['puntos'].astype(float)
		df_puntos['fecha_date'] = df_puntos['fecha'].apply(lambda x: pasar_a_fecha_3(x))
		max_puntos = df_puntos['puntos'].max()
		
		selection = alt.selection(type='single', fields=['user'], bind='legend')
		
		graph = alt.Chart(df_puntos).mark_line().encode(
		    #y = alt.Y('fecha',scale=alt.Scale(domain=(0.3, 0.7))),
			x = alt.X('fecha'),
		    y = alt.Y('puntos',scale=alt.Scale(domain=(0, max_puntos))),
			#size='Winrate_budget_ratio',
			#text = 'Team2',
			#color=alt.Color('user', scale=None),
			color = 'user',
			#tooltip='Team2:N'
		).properties(width=1700,height=600).add_selection(selection)
		
		
		marks = alt.Chart(df_puntos).mark_circle(size=100,opacity=1).encode(
		    #y = alt.Y('fecha',scale=alt.Scale(domain=(0.3, 0.7))),
			x = alt.X('fecha'),
		    y = alt.Y('puntos'),
			#text = 'Team2',
			#color=alt.Color('user', scale=None),
			color = 'user:N',
			#tooltip='Team2:N'
		).properties(width=1700,height=600)
		
				
		
# 		import altair_viewer
# 		altair_viewer.display(graph)
		
		st.altair_chart((graph+marks).interactive(), use_container_width=False)

####------Torneo de amigos-------------------------------------------------------------------------------------------------------------------------------


	elif seccion == 'Torneo de amigos':		
		print('vuelve a correr la pagina torneo de amigos')
		
		df_torneo = fetch_df(db_torneo)
		df_torneo = pd.DataFrame.from_dict(df_torneo)
		def subir_torneo():
			if friends_name in list(df_torneo['friends_name']):
				max_fecha = df_torneo[df_torneo['friends_name']==friends_name]['fecha'].max()
				torneo_existente = df_torneo[(df_torneo['friends_name']==friends_name)&(df_torneo['fecha']==max_fecha)]
				owner = str(list(df_torneo[df_torneo['friends_name']==friends_name]['owner'])[0])			
				if st.session_state['usuario'] == owner:
					db_torneo.put({'friends_name':friends_name,'friends_list':friends_list,'owner':st.session_state['usuario'],'fecha':datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')})
					st.balloons()
				else:
					st.error('El creador de este torneo es'+owner+'. tenés que ser el creador del torneo para poder editarlo')			
			else:
				db_torneo.put({'friends_name':friends_name,'friends_list':friends_list,'owner':st.session_state['usuario'],'fecha':datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')})
				st.balloons()
				
		st.markdown(body = '<br>', unsafe_allow_html=True)		
		st.button('Guardar cambios',on_click=subir_torneo, key=5)
		
		friends_name = st.text_input(label='Ponele nombre a tu torneo', value="", key='valor_input')

		pre_list = ''
		if 'valor_input' in st.session_state:
			print('corre el if valor input')
			print(df_torneo['friends_name'])
			if friends_name in list(df_torneo['friends_name']):
				print('corre el if friends name')
				max_fecha = df_torneo[df_torneo['friends_name']==friends_name]['fecha'].max()
				torneo_existente = df_torneo[(df_torneo['friends_name']==friends_name)&(df_torneo['fecha']==max_fecha)]
				owner = str(list(df_torneo[df_torneo['friends_name']==friends_name]['owner'])[0])				
				if st.session_state['usuario'] == owner:
					print('corre el if owner')
					st.session_state['friends'] = list(df_torneo[df_torneo['friends_name']==friends_name]['friends_list'])[0]
					for i in st.session_state['friends']:
						pre_list = (pre_list +' '+i).strip()

				else:
 					st.error('Este nombre de torneo ya está usado por '+owner)
		
		friends = st.text_input(label='Arma tu equipo de amigos: Agregá las direcciones de mail con el que llenaron el prode separandolos entre sí con un espacio', value=pre_list)
		friends_list = friends.strip().split(" ")
		print(friends_list)
		friends_to_choose = st.multiselect(label='Acá va a ir apareciendo la lista completa',options= friends_list,default= friends_list)#,default=friends_to_choose
		
		
		st.markdown(body = '<br>', unsafe_allow_html=True)
		st.markdown(body = '<br>', unsafe_allow_html=True)	
		st.markdown(body = '<br>', unsafe_allow_html=True)	
		st.markdown(body = '<br>', unsafe_allow_html=True)	
		st.markdown(body = '<br>', unsafe_allow_html=True)	
		st.markdown(body = '<br>', unsafe_allow_html=True)		
		
else:
	st.write('Usuario es desconocido')  