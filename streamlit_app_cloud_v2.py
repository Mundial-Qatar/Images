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
        st.text_input("Username", on_change=password_entered, key="username")
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

	st.write('aca empieza')
	st.write("email" in st.experimental_user)
	st.write(st.experimental_user)
	st.write(st.experimental_user.email)
	st.write(st.session_state["username"])
	st.write('aca termina')


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
