import streamlit as st
import paho.mqtt.client as mqtt
import time

# --- MISMOS TÓPICOS QUE EL ESP32 ---
BROKER = "broker.hivemq.com"
T_CONTROL = "axel/mecatronic/control/audio"
T_TEMP = "axel/mecatronic/telemetry/temp"

st.set_page_config(page_title="Control Audio Pro", page_icon="🔊")
st.title("🔊 Control y Telemetría")

# Estado de la temperatura
if 'temp' not in st.session_state:
    st.session_state.temp = "Cargando..."

# --- LÓGICA MQTT ---
def enviar(cmd):
    try:
        c = mqtt.Client()
        c.connect(BROKER, 1883)
        c.publish(T_CONTROL, cmd)
        c.disconnect()
        st.toast(f"Comando {cmd} enviado")
    except Exception as e:
        st.error(f"Error de envío: {e}")

# Receptor de temperatura (corre en segundo plano)
def on_message(client, userdata, message):
    st.session_state.temp = message.payload.decode()

@st.cache_resource
def iniciar_escucha():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(BROKER, 1883)
    client.subscribe(T_TEMP)
    client.loop_start()
    return client

iniciar_escucha()

# --- INTERFAZ ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Energía")
    if st.button("🚀 ENCENDER", use_container_width=True):
        enviar("ON")
    if st.button("🛑 APAGAR", use_container_width=True, type="primary"):
        enviar("OFF")

with col2:
    st.subheader("Temperatura")
    st.metric(label="Disipador", value=f"{st.session_state.temp} °C")
    if st.button("🔄 Refrescar"):
        st.rerun()

st.divider()
st.caption("Proyecto Mecatrónica - Axel")