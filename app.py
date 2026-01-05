import streamlit as st
import paho.mqtt.client as mqtt
import time

# --- CONFIGURACIÓN IDÉNTICA AL ESP32 ---
BROKER = "broker.hivemq.com"
T_CONTROL = "axel/mecatronic/control/audio"
T_TEMP = "axel/mecatronic/telemetry/temp"

st.set_page_config(page_title="Control Audio Pro", page_icon="🔊")
st.title("🔊 Panel de Control y Telemetría")

# Inicializamos el estado de la temperatura
if 'lectura' not in st.session_state:
    st.session_state.lectura = "Cargando..."

# --- LÓGICA DE RECEPCIÓN ---
def al_recibir_mensaje(client, userdata, message):
    # Guardamos el dato en la memoria del navegador
    st.session_state.lectura = message.payload.decode()

@st.cache_resource
def iniciar_conexion():
    cliente = mqtt.Client()
    cliente.on_message = al_recibir_mensaje
    cliente.connect(BROKER, 1883)
    cliente.subscribe(T_TEMP)
    cliente.loop_start()
    return cliente

iniciar_conexion()

# --- INTERFAZ ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Control")
    if st.button("🚀 ENCENDER", use_container_width=True):
        c = mqtt.Client(); c.connect(BROKER, 1883)
        c.publish(T_CONTROL, "ON"); c.disconnect()
    if st.button("🛑 APAGAR", use_container_width=True, type="primary"):
        c = mqtt.Client(); c.connect(BROKER, 1883)
        c.publish(T_CONTROL, "OFF"); c.disconnect()

with col2:
    st.subheader("Telemetría")
    # Este cuadro se actualizará cuando cambie st.session_state.lectura
    st.metric(label="Temperatura Actual", value=f"{st.session_state.lectura} °C")
    
    # BOTÓN DE REFRESCADO MANUAL
    if st.button("🔄 Forzar Actualización"):
        st.rerun()

st.divider()
st.info("El sistema recibe datos cada 5-10 segundos desde el ESP32.")