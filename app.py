import streamlit as st
import paho.mqtt.client as mqtt
import time

# --- CONFIGURACIÓN ---
# Asegúrate de que este nombre sea EXACTAMENTE igual en el ESP32
TOPIC = "axel/mecatronic/control/audio" 
BROKER = "broker.hivemq.com"

def enviar_comando(comando):
    try:
        client = mqtt.Client()
        client.connect(BROKER, 1883, 60)
        
        # Iniciamos el sistema de envío
        client.loop_start()
        
        # Publicamos usando la variable 'TOPIC' (ya corregida)
        publicacion = client.publish(TOPIC, comando, qos=1)
        publicacion.wait_for_publish() 
        
        time.sleep(0.2) 
        client.loop_stop()
        client.disconnect()
        st.success(f"✅ Enviado al canal: {comando}")
    except Exception as e:
        st.error(f"❌ Error de envío: {e}")

# --- INTERFAZ ---
st.title("🔊 Control Maestro - Axel")

if st.button("🚀 ENCENDER"):
    enviar_comando("ON")

if st.button("🛑 APAGAR"):
    enviar_comando("OFF")