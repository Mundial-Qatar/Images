# streamlit_app.py

import streamlit as st

def check_password():
	def password_entered():

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
		user = st.text_input("Username", on_change=password_entered, key="username")
		st.text_input(
			"Password", type="password", on_change=password_entered, key="password"
		)
		return False, ''
	elif not st.session_state["password_correct"]:
		# Password not correct, show input + error.
		user = st.text_input("Username", on_change=password_entered, key="username")
		st.text_input(
			"Password", type="password", on_change=password_entered, key="password"
		)
		st.error("😕 User not known or password incorrect")
		return False, ''
	else:
		# Password correct.
		return True, user

user = check_password()[1]
if check_password()[0]:
	st.write("Here goes your normal Streamlit app...")
	st.button("Click me")

