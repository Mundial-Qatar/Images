import streamlit as st
import pandas as pd
import pickle
#import os
import plotly.express as px

#os.chdir('C:/Users/fedem/Mis_Documentos/Programación y soft/Web Scrapping/BWIN')
#if os.path.isfile('base_bwin.pickle'): #chequeo que no exista ya el archivo con una bajada de todos los datos
    
with open('base_bwin.pickle', 'rb') as handle:
	diccionario = pd.read_pickle(handle)
	print('se recuperó una versión anterior')
df = diccionario[max(diccionario.keys())]
distintos_paises = tuple(set(df['Pais_b'].append(df['Pais_a'])))



st.title('Titulo')

add_sidebar = st.sidebar.selectbox('Opcion defecto',('Opcion defecto','Otra opción'))

if add_sidebar == 'Opcion defecto':
	st.write('defecto')

    
	col1, col2 = st.columns(2)
	columns = [col1, col2]
	values = [5,4]
	
	for i in range(0,len(columns)):
		with columns[i]:
			st.metric(label='1', value=values[i],delta= "{:.2%}".format(values[i]/100))

	st.dataframe(df)
	


if add_sidebar == 'Otra opción':
	st.write('Otra opción')
	pais_select = st.selectbox('Elegi un pais',distintos_paises) #las opciones son una tupla
	
	fig = px.bar(df,x='Pais_a',y='win_a')
	st.plotly_chart(fig)
	
	st.header('st.button')

	if st.button('Say hello'):
		st.write('Why hello there')
	else:
		st.write('Goodbye')