import streamlit as st
import paho.mqtt.publish as publish

# CONFIGURACIÓN IDÉNTICA
BROKER = "broker.hivemq.com"
T_CONTROL = "axel/mecatronic/control/audio"

st.title("🔊 Control de Emergencia - Axel")

# Función simplificada al máximo
def mandar(comando):
    try:
        # Esto envía el mensaje en un solo intento
        publish.single(T_CONTROL, comando, hostname=BROKER)
        st.success(f"✅ COMANDO {comando} ENVIADO")
    except Exception as e:
        st.error(f"❌ ERROR DE RED: {e}")

# BOTONES GRANDES
if st.button("🚀 ENCENDER", use_container_width=True):
    mandar("ON")

if st.button("🛑 APAGAR", use_container_width=True, type="primary"):
    mandar("OFF")

st.info("Si al picar sale el mensaje verde pero HiveMQ sigue vacío, el problema es tu Firewall.")