import streamlit as st
import paho.mqtt.client as mqtt

# --- Configuración del Broker ---
# Usamos el mismo broker que el ESP32
BROKER = "broker.hivemq.com"
TOPIC = "mecatronic/amp/power"

# Configuración de la página
st.set_page_config(page_title="Smart Amp Control", page_icon="🔊")

st.title("🔊 Control de Amplificador IoT")
st.subheader("Proyecto Final de Mecatrónica")

# Función para enviar mensajes
def enviar_comando(comando):
    try:
        client = mqtt.Client()
        client.connect(BROKER, 1883, 60)
        client.publish(TOPIC, comando)
        client.disconnect()
        return True
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return False

# Interfaz de usuario
st.write("Presiona los botones para controlar el estado del amplificador:")

col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 ENCENDER", use_container_width=True):
        if enviar_comando("ON"):
            st.success("Comando ON enviado")

with col2:
    if st.button("🛑 APAGAR", use_container_width=True, type="primary"):
        if enviar_comando("OFF"):
            st.warning("Comando OFF enviado")

st.divider()
st.caption("Conectado a través de HiveMQ Public Broker")