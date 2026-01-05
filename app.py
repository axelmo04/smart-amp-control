import streamlit as st
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

# --- CONFIGURACIÓN ---
BROKER = "broker.hivemq.com"
T_CONTROL = "axel/mecatronic/control/audio"
T_TEMP = "axel/mecatronic/telemetry/temp"

st.set_page_config(page_title="Smart Amp Axel", page_icon="🔊")
st.title("🔊 Sistema de Control y Telemetría")

# Inicializamos el estado de la temperatura
if 'temp_val' not in st.session_state:
    st.session_state.temp_val = "---"

# --- RECEPTOR DE TEMPERATURA (Escuchando a la nube) ---
def on_message(client, userdata, message):
    st.session_state.temp_val = message.payload.decode()

@st.cache_resource
def iniciar_receptor():
    cliente = mqtt.Client()
    cliente.on_message = on_message
    cliente.connect(BROKER, 1883)
    cliente.subscribe(T_TEMP)
    cliente.loop_start()
    return cliente

iniciar_receptor()

# --- INTERFAZ DE USUARIO ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Control de Relé")
    # Usamos el método 'publish.single' que confirmamos que funciona
    if st.button("🚀 ENCENDER", use_container_width=True):
        publish.single(T_CONTROL, "ON", hostname=BROKER)
        st.success("Orden: ON")

    if st.button("🛑 APAGAR", use_container_width=True, type="primary"):
        publish.single(T_CONTROL, "OFF", hostname=BROKER)
        st.error("Orden: OFF")

with col2:
    st.subheader("Telemetría")
    st.metric(label="Temperatura Disipador", value=f"{st.session_state.temp_val} °C")
    
    if st.button("🔄 Actualizar Pantalla"):
        st.rerun()

st.divider()
st.caption("Axel - Ingeniería Mecatrónica 2026")