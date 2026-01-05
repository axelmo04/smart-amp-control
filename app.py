import streamlit as st
import paho.mqtt.client as mqtt

# Configuración de comunicación
BROKER = "broker.hivemq.com"
T_POWER = "mecatronic/amp/power"

st.set_page_config(page_title="Control de Audio Pro", page_icon="🔊")

st.title("🔊 Panel de Control Mecatrónico")
st.write("Control de Amplificador mediante Módulo de Relés y ESP32")

# Función para mandar comandos
def mandar_comando(cmd):
    try:
        c = mqtt.Client()
        c.connect(BROKER, 1883, 10)
        c.publish(T_POWER, cmd)
        c.disconnect()
        st.toast(f"Comando {cmd} enviado")
    except Exception as e:
        st.error(f"Error de conexión: {e}")

# Diseño de la página
col1, col2 = st.columns(2)

with col1:
    st.header("Interruptor")
    if st.button("🚀 ENCENDER SISTEMA", use_container_width=True):
        mandar_comando("ON")
    if st.button("🛑 APAGAR SISTEMA", use_container_width=True, type="primary"):
        mandar_comando("OFF")

with col2:
    st.header("Telemetría")
    st.info("La temperatura se muestra en la consola del ESP32 por ahora.")
    # Próximo paso: Agregar un suscriptor aquí para ver la temperatura.

st.divider()
st.caption("Proyecto final - Ingeniería en Mecatrónica")