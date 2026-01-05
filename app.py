import streamlit as st
import paho.mqtt.client as mqtt

# --- CONFIGURACIÓN ---
BROKER = "broker.hivemq.com"
T_CONTROL = "axel/mecatronic/control/audio"
T_TEMP = "axel/mecatronic/telemetry/temp"

st.set_page_config(page_title="Master Audio Control", page_icon="🔊")
st.title("🔊 Control y Telemetría del Amplificador")

# Inicializar estado para la temperatura si no existe
if 'temp_actual' not in st.session_state:
    st.session_state.temp_actual = "Cargando..."

# --- CLIENTE MQTT PARA RECIBIR DATOS ---
def on_message(client, userdata, message):
    # Guardamos la temperatura que llega del ESP32
    st.session_state.temp_actual = message.payload.decode()

# Configuración del receptor en segundo plano
@st.cache_resource
def iniciar_receptor():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(BROKER, 1883)
    client.subscribe(T_TEMP)
    client.loop_start()
    return client

iniciar_receptor()

# --- INTERFAZ ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Control de Poder")
    if st.button("🚀 ENCENDER", use_container_width=True):
        c = mqtt.Client(); c.connect(BROKER, 1883)
        c.publish(T_CONTROL, "ON"); c.disconnect()
        st.success("Orden enviada")

    if st.button("🛑 APAGAR", use_container_width=True, type="primary"):
        c = mqtt.Client(); c.connect(BROKER, 1883)
        c.publish(T_CONTROL, "OFF"); c.disconnect()
        st.warning("Orden enviada")

with col2:
    st.subheader("Estado Térmico")
    st.metric(label="Temperatura del Disipador", value=f"{st.session_state.temp_actual} °C")
    
    # Botón para refrescar la pantalla y ver el último dato
    if st.button("🔄 Actualizar Lectura"):
        st.rerun()

st.divider()
st.caption("Axel - Proyecto de Mecatrónica 2024")