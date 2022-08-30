# streamlit_app.py

import streamlit as st

def password_entered():

	if (
		st.session_state["username"] in st.secrets["passwords"]
		and st.session_state["password"]
		== st.secrets["passwords"][st.session_state["username"]] 
	):
		return True

st.session_state["username"] = st.text_input("Username", on_change=(password_entered))
st.session_state["password"] = st.text_input("Password", on_change=(password_entered), type="password")



st.button('logearse',on_click=password_entered)

if password_entered():
	st.write(st.session_state["username"])
