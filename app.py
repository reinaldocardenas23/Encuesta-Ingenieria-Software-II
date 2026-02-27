import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- CONFIGURACIÓN DE BASE DE DATOS LOCAL ---
FILE_DB = "historico_perfiles.csv"

def inicializar_db():
    if not os.path.exists(FILE_DB):
        df = pd.DataFrame(columns=["Nombre", "ID", "Clarificador", "Ideador", "Desarrollador", "Implementador", "Perfil_Dominante"])
        df.to_csv(FILE_DB, index=False)

def guardar_resultado(datos):
    df = pd.read_csv(FILE_DB)
    df = pd.concat([df, pd.DataFrame([datos])], ignore_index=True)
    df.to_csv(FILE_DB, index=False)

# --- LISTA COMPLETA DE PREGUNTAS (Basado en tu imagen) ---
# Estructura: (Texto de la pregunta, Categoría)
# A=Clarificador, B=Ideador, C=Desarrollador, D=Implementador
preguntas_raw = [
    ("Pregunta de ejemplo: ¿Te gusta resolver problemas? (Esta no suma puntos)", "EJEMPLO"), # Pregunta 1 despreciada
    ("Generalmente no me acerco a los problemas de forma creativa", "C"),
    ("Me gusta probar y luego revisar mis ideas antes de generar la solución o producto final", "C"),
    ("Me gusta tomarme el tiempo para clarificar la naturaleza exacta del problema", "A"),
    ("Disfruto de tomar los pasos necesarios para poner mis ideas en acción", "D"),
    ("Me gusta separar un problema amplio en partes para examinarlo desde todos los ángulos", "C"),
    ("Tengo dificultad en tener ideas inusuales para resolver un problema", "B"),
    ("Me gusta identificar los hechos más relevantes relativos al problema", "A"),
    ("No tengo el temperamento para tratar de aislar las causas específicas de un problema", "A"),
    ("Disfruto al generar formas únicas de mirar un problema", "B"),
    ("Me gusta generar todos los pros y los contras de una solución potencial", "C"),
    ("Antes de implementar una solución me gusta separarla en pasos", "C"),
    ("Transformar ideas en acción no es lo que disfruto más", "D"),
    ("Me gusta superar el criterio que puede usarse para identificar la mejor opción o solución", "C"),
    ("Disfruto de pasar tiempo profundizando el análisis inicial del problema", "B"),
    ("Por naturaleza no paso mucho tiempo emocionándome en definir el problema exacto a resolver", "A"),
    ("Me gusta entender una situación al mirar el panorama general", "B"),
    ("Disfruto en trabajar problemas mal definidos y novedosos", "B"),
    ("Cuando trabajo en un problema me gusta encontrar la mejor forma de enunciarlo", "A"),
    ("Disfruto de hacer que las cosas se concreten", "D"),
    ("Me gusta enfocarme en enunciar un problema de forma precisa", "A"),
    ("Disfruto de usar mi imaginación para producir muchas ideas", "B"),
    ("Me gusta enfocarme en la información clave de una situación desafiante", "A"),
    ("Disfruto de tomarme el tiempo para perfeccionar una idea", "C"),
    ("Me resulta difícil implementar mis ideas", "D"),
    ("Disfruto de transformar ideas en bruto en soluciones concretas", "D"),
    ("No paso el tiempo en todas las cosas que necesito hacer para implementar una idea", "D"),
    ("Realmente disfruto de implementar una idea", "D"),
    ("Antes de avanzar me gusta tener una clara comprensión del problema", "A"),
    ("Me gusta trabajar con ideas únicas", "B"),
    ("Disfruto de poner mis ideas en acción", "D"),
    ("Me gusta explorar las fortalezas y debilidades de una solución potencial", "C"),
    ("Disfruto de reunir información para identificar el origen de un problema particular", "A"),
    ("Disfruto el análisis y el esfuerzo que lleva transformar un concepto preliminar en una idea", "C"),
    ("Mi tendencia natural no es generar muchas ideas para los problemas", "B"),
    ("Disfruto de usar metáforas y analogías para generar nuevas ideas para los problemas", "B"),
    ("Encuentro que tengo poca paciencia para el esfuerzo que lleva pulir o refinar una idea", "C"),
    ("Tiendo a buscar una solución rápida y luego implementarla", "D")
]

# --- INTERFAZ STREAMLIT ---
st.set_page_config(page_title="Sistema de Perfiles de Innovación", layout="wide")
inicializar_db()

st.sidebar.title("Acceso al Sistema")
rol = st.sidebar.selectbox("Seleccione su Rol", ["Usuario", "Administrador"])

if rol == "Usuario":
    st.title("📝 Test de Perfil de Innovación")
    st.markdown("Por favor, ingrese sus datos y responda con total sinceridad.")
    
    with st.form("test_form"):
        col_id1, col_id2 = st.columns(2)
        nombre = col_id1.text_input("Nombre Completo")
        cedula = col_id2.text_input("Identificación (ID)")
        
        st.divider()
        
        respuestas_usuario = []
        for i, (pregunta, cat) in enumerate(preguntas_raw):
            st.write(f"**{i+1}.** {pregunta}")
            val = st.radio(f"Ponderación (1 al 10) - Q{i+1}", [1,2,3,4,5,6,7,8,9,10], index=4, horizontal=True, key=f"p{i}")
            respuestas_usuario.append(val)
            st.divider()
            
        enviado = st.form_submit_button("Finalizar y Guardar")
        
        if enviado:
            if nombre and cedula:
                # Cálculo de puntajes
                scores = {"A": 0, "B": 0, "C": 0, "D": 0}
                for i, (pregunta, cat) in enumerate(preguntas_raw):
                    if i == 0: continue # Despreciar pregunta 1
                    if cat in scores:
                        scores[cat] += respuestas_usuario[i]
                
                # Perfil dominante
                perfil_max = max(scores, key=scores.get)
                nombres_perfil = {"A": "Clarificador", "B": "Ideador", "C": "Desarrollador", "D": "Implementador"}
                
                data_to_save = {
                    "Nombre": nombre, "ID": cedula,
                    "Clarificador": scores["A"], "Ideador": scores["B"],
                    "Desarrollador": scores["C"], "Implementador": scores["D"],
                    "Perfil_Dominante": nombres_perfil[perfil_max]
                }
                
                guardar_resultado(data_to_save)
                st.balloons()
                st.success(f"¡Gracias {nombre}! Tu prueba ha sido registrada exitosamente.")
            else:
                st.error("Por favor completa tu Nombre e ID antes de enviar.")

elif rol == "Administrador":
    st.title("🔐 Panel de Control Administrativo")
    passwd = st.sidebar.text_input("Contraseña", type="password")
    
    if passwd == "admin123": # Cambiar por seguridad
        df = pd.read_csv(FILE_DB)
        
        st.subheader("📊 Consolidado de Resultados")
        st.dataframe(df, use_container_width=True)
        
        if not df.empty:
            st.divider()
            st.subheader("📈 Análisis de Perfiles")
            fig = px.histogram(df, x="Perfil_Dominante", color="Perfil_Dominante", 
                               title="Distribución Total de Perfiles en la Empresa")
            st.plotly_chart(fig, use_container_width=True)
            
            st.divider()
            st.subheader("📂 Gestión de Datos")
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button("Exportar Reporte (CSV)", data=csv_data, file_name="reporte_final.csv", mime="text/csv")
            
            uploaded_file = st.file_uploader("Importar Histórico (CSV)", type="csv")
            if uploaded_file:
                new_df = pd.read_csv(uploaded_file)
                new_df.to_csv(FILE_DB, index=False)
                st.success("Histórico actualizado. Recargue la página.")
        else:
            st.info("Aún no hay pruebas registradas.")
    else:
        st.warning("Ingrese la contraseña para ver las métricas.")