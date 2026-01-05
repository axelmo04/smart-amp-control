import streamlit as st
import paho.mqtt.client as mqtt
import time

# USAR EXACTAMENTE ESTE TÓPICO (sin espacios)
TOPICO = "axel/mecatronic/control/audio"
BROKER = "broker.hivemq.com"

def enviar_comando(comando):
    try:
        client = mqtt.Client()
        client.connect(BROKER, 1883, 60)
        
        # Iniciamos el bucle interno de MQTT
        client.loop_start()
        
        # Publicamos y esperamos confirmación real
        publicacion = client.publish(TOPIC, comando, qos=1)
        publicacion.wait_for_publish() # <--- ESTO ASEGURA QUE NO LLEGUE VACÍO
        
        time.sleep(0.5) # Respiro de seguridad
        client.loop_stop()
        client.disconnect()
        st.success(f"✅ ¡Confirmado! '{comando}' llegó al servidor")
    except Exception as e:
        st.error(f"❌ Error de envío: {e}")

st.title("🔊 Control Maestro - Axel")

if st.button("🚀 ENCENDER"):
    enviar_comando("ON")

if st.button("🛑 APAGAR"):
    enviar_comando("OFF")