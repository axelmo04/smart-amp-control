import streamlit as st
import paho.mqtt.client as mqtt

# USAREMOS ESTE TÓPICO ÚNICO
TOPICO_UNICO = "axel/mecatronic/control/audio"
BROKER = "broker.hivemq.com"

def enviar_comando(comando):
    client = mqtt.Client()
    client.connect(BROKER, 1883)
    # Publicamos con "Retain=True" para que el mensaje se quede guardado en el servidor
    client.publish(TOPICO_UNICO, comando, retain=True) 
    client.disconnect()

st.title("🔊 Control Maestro - Axel")

if st.button("🚀 ENCENDER"):
    enviar_comando("ON")
    st.success("Enviado al canal único: ON")

if st.button("🛑 APAGAR"):
    enviar_comando("OFF")
    st.error("Enviado al canal único: OFF")