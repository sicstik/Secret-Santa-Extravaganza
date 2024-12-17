import ssl
import smtplib
import os
import streamlit as st


def send_email_button(message, receive_email):
    host = "smtp.gmail.com"
    port = 465
    username = "bexelcloud@gmail.com"
    # password = os.getenv("PASSWORD")
    # password_nonEncrypted = "debf ffog aggx evxu"
    password = 'ljudkpucacsjeuef'
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receive_email, message)
    st.toast(f"Email has been sent to {receive_email}")