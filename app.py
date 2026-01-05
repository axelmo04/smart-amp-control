import streamlit as st
import paho.mqtt.client as mqtt
import time

# Datos del servidor
BROKER = "broker.hivemq.com"
TOPIC = "mecatronic/amp/power"

st.title("🔊 Control de Audio - Axel")

def enviar_comando(comando):
    try:
        # Creamos el cliente
        client = mqtt.Client()
        
        # Conectamos
        st.write(f"Intentando conectar a {BROKER}...")
        client.connect(BROKER, 1883, 60)
        
        # Publicamos el mensaje
        resultado = client.publish(TOPIC, comando)
        
        # Esperamos un instante para asegurar que el mensaje salga
        if resultado.rc == mqtt.MQTT_ERR_SUCCESS:
            st.success(f"✅ Mensaje '{comando}' enviado al servidor")
        else:
            st.error("❌ El mensaje no pudo salir")
            
        client.disconnect()
    except Exception as e:
        st.error(f"❌ Error de conexión: {e}")

# Botones
if st.button("🚀 ENCENDER", use_container_width=True):
    enviar_comando("ON")

if st.button("🛑 APAGAR", use_container_width=True, type="primary"):
    enviar_comando("OFF")