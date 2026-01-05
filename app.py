import streamlit as st
import paho.mqtt.client as mqtt
import time

# --- CONFIGURACIÓN ---
BROKER = "broker.hivemq.com"
T_CONTROL = "axel/mecatronic/control/audio"
T_TEMP = "axel/mecatronic/telemetry/temp"

st.set_page_config(page_title="Control Audio Axel", page_icon="🔊")
st.title("🔊 Control Maestro y Telemetría")

# --- FUNCIONES ---
def enviar(comando):
    try:
        client = mqtt.Client()
        client.connect(BROKER, 1883, 60)
        client.publish(T_CONTROL, comando, qos=1)
        client.disconnect()
        st.toast(f"Comando {comando} enviado")
    except Exception as e:
        st.error(f"Error: {e}")

# --- INTERFAZ ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Poder")
    if st.button("🚀 ENCENDER", use_container_width=True):
        enviar("ON")
    if st.button("🛑 APAGAR", use_container_width=True, type="primary"):
        enviar("OFF")

with col2:
    st.subheader("Estado")
    # Para la temperatura, usaremos un truco: leer el "último mensaje" del broker
    if st.button("🌡️ VER TEMPERATURA"):
        # Esta parte se conecta solo un segundo para ver qué hay en el canal
        def on_msg(c, u, m):
            st.session_state.temp = m.payload.decode()
            c.disconnect()
            
        temp_client = mqtt.Client()
        temp_client.on_message = on_msg
        temp_client.connect(BROKER, 1883)
        temp_client.subscribe(T_TEMP)
        temp_client.loop_start()
        time.sleep(1) # Espera a que llegue el dato
        temp_client.loop_stop()
        
    if 'temp' in st.session_state:
        st.metric("Temperatura actual", f"{st.session_state.temp} °C")
    else:
        st.write("Presiona el botón para leer")

st.divider()
st.caption("Axel - Ingeniería Mecatrónica")