import streamlit as st
import paho.mqtt.client as mqtt

st.title("🔊 Master Control - Smart Audio")

def enviar(comando):
    client = mqtt.Client()
    client.connect("broker.hivemq.com", 1883)
    client.publish("mecatronic/amp/power", comando)
    client.disconnect()

if st.button("🚀 ENCENDER"):
    enviar("ON")
    st.success("Señal enviada: ON")

if st.button("🛑 APAGAR"):
    enviar("OFF")
    st.error("Señal enviada: OFF")