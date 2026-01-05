import streamlit as st
import paho.mqtt.client as mqtt
import time

# --- CONFIGURACIÓN IDÉNTICA AL ESP32 ---
BROKER = "broker.hivemq.com"
T_CONTROL = "axel/mecatronic/control/audio"
T_TEMP = "axel/mecatronic/telemetry/temp"

st.set_page_config(page_title="Control Audio Pro", page_icon="🔊")
st.title("🔊 Panel de Control Mecatrónico")

# Estado de la temperatura en la interfaz
if 'temp' not in st.session_state:
    st.session_state.temp = "Cargando..."

# --- FUNCIÓN DE ENVÍO CON ESPERA (Publish & Wait) ---
def enviar_comando(comando):
    try:
        client = mqtt.Client()
        client.connect(BROKER, 1883, 60)
        
        # Iniciamos el bucle para procesar el envío
        client.loop_start()
        
        # Publicamos con QoS 1 (asegura entrega)
        msg_info = client.publish(T_CONTROL, comando, qos=1)
        
        # BLOQUEO DE SEGURIDAD: Espera hasta que el mensaje realmente salga
        msg_info.wait_for_publish()
        
        time.sleep(0.5) # Respiro para el servidor
        client.loop_stop()
        client.disconnect()
        st.toast(f"✅ ¡{comando} enviado con éxito!")
    except Exception as e:
        st.error(f"❌ Error de conexión: {e}")

# --- RECEPTOR DE TEMPERATURA ---
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

# --- INTERFAZ DE USUARIO ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Interruptor")
    # Usamos botones grandes para el celular
    if st.button("🚀 ENCENDER", use_container_width=True):
        enviar_comando("ON")
    if st.button("🛑 APAGAR", use_container_width=True, type="primary"):
        enviar_comando("OFF")

with col2:
    st.subheader("Telemetría")
    st.metric(label="Temperatura", value=f"{st.session_state.temp} °C")
    if st.button("🔄 Actualizar"):
        st.rerun()

st.divider()
st.caption("Axel - Control IoT v4.0")