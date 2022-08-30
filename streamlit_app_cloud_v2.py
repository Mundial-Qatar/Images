import streamlit as st
import pandas as pd
import pickle
#import os
import plotly.express as px

def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
	global usuario
	usuario = st.text_input("Username", on_change=password_entered, key="username")	
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():

	#os.chdir('C:/Users/fedem/Mis_Documentos/Programación y soft/Web Scrapping/BWIN')
	#if os.path.isfile('base_bwin.pickle'): #chequeo que no exista ya el archivo con una bajada de todos los datos

	with open('base_bwin.pickle', 'rb') as handle:
		diccionario = pd.read_pickle(handle)
		print('se recuperó una versión anterior')
	df = diccionario[max(diccionario.keys())]
	distintos_paises = tuple(set(df['Pais_b'].append(df['Pais_a'])))



	st.title('Titulo')

	st.write('aca empieza v2')
	st.write(usuario)
	st.write('aca termina')


	add_sidebar = st.sidebar.selectbox('Opcion defecto',('Opcion defecto','Otra opción'))

	if add_sidebar == 'Opcion defecto':
		st.write('defecto')

	if add_sidebar == 'Otra opción':
		st.write('Otra opción')
		
