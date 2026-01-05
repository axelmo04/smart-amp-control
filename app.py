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


def enviar_comando(comando):
    try:
        client = mqtt.Client()
        client.connect("broker.hivemq.com", 1883, 60)
        
        # Publicamos y guardamos el objeto de información
        info = client.publish("axel/mecatronic/control/audio", comando, qos=1)
        
        # ¡ESTA LÍNEA ES CLAVE! 
        # Obliga al programa a esperar a que el servidor confirme la recepción
        info.wait_for_publish() 
        
        client.disconnect()
        st.success(f"✅ Confirmado: {comando} llegó al servidor")
    except Exception as e:
        st.error(f"❌ Error: {e}")