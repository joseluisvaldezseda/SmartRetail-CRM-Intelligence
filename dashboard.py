import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Intelligence Dashboard | Quintiles",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. ESTILO CSS PERSONALIZADO (Aesthetic & Minimalist)
st.markdown("""
    <style>
    .main { background-color: #F8F9FB; }
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #E5E7EB;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1F2937;
        margin: 2rem 0 1rem 0;
        padding-bottom: 8px;
        border-bottom: 1.5px solid #F3F4F6;
    }
    .stMultiSelect div[data-baseweb="tag"] {
        background-color: #3B82F6 !important;
        border-radius: 4px !important;
    }
    .sidebar-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #111827;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. CARGA DE DATOS OPTIMIZADA
@st.cache_data
def load_data():
    try:
        df = pd.read_parquet('rfm_churn_ltv.parquet')
        #df = pd.read_csv('Quintiles.csv', sep=None, engine='python', encoding='utf-8-sig')

        df.columns = df.columns.str.strip()
        df = df.replace('Dato no disponible', pd.NA)
        
        numeric_cols = ['Probabilidad_Churn', 'Probabilidad_Compra_90d', 'Monto_Esperado_90d', 'CLV_90dias']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # --- SEGMENTACIÓN ROBUSTA ---
        
        # 1. Propensión de Recompra
        p_col = 'Probabilidad_Compra_90d'
        if p_col in df.columns and df[p_col].notnull().any():
            bins_p = [-0.001, 0.25, 0.50, 0.75, 1.001]
            labels_p = ['Baja Propensión', 'Propensión Media', 'Alta Propensión', 'Muy Alta Propensión']
            df['Segmento_Recompra'] = pd.cut(df[p_col], bins=bins_p, labels=labels_p)
        else:
            df['Segmento_Recompra'] = 'Sin datos'

        # 2. Valor Futuro (Cuartiles)
        v_col = 'CLV_90dias'
        if v_col in df.columns and df[v_col].notnull().any():
            try:
                quantile_labels = ['Valor Bronce', 'Valor Plata', 'Valor Oro', 'Valor Diamante']
                edges = df[v_col].quantile([0, 0.25, 0.5, 0.75, 1.0]).unique()
                if len(edges) > 1:
                    actual_labels = quantile_labels[:len(edges)-1]
                    df['Potencial_Valor'] = pd.cut(df[v_col], bins=edges, labels=actual_labels, include_lowest=True)
                else:
                    df['Potencial_Valor'] = 'Valor Único'
            except:
                df['Potencial_Valor'] = 'Indeterminado'
        else:
            df['Potencial_Valor'] = 'Sin datos'
            
        return df
    except Exception as e:
        st.error(f"Error crítico al cargar el archivo: {e}")
        return None

df_raw = load_data()

# --- 4. BARRA LATERAL (FILTROS) ---
if df_raw is not None:
    # Definir el ordenamiento de RFM solicitado
    segmento_a_calificacion = {
        'Campeones': 1, 'VIPs Leales': 2, 'Alto Potencial': 3, 'VIPs Potenciales': 4,
        'Calidad Reciente': 5, 'Nuevos Grandes Compradores': 6, 'Calidad Regular': 7,
        'Estándar Reciente': 8, 'Estándar': 9, 'Calidad Prometedora': 10,
        'Alto Riesgo - Valiosos': 11, 'Nuevos Clientes': 12, 'Bajo Compromiso': 13,
        'Pasivos': 14, 'Críticos a Retener': 15, 'Necesitan Atención': 16,
        'En Riesgo': 17, 'Baja Prioridad': 18, 'A Punto de Dormir': 19,
        'Hibernando': 20
    }

    with st.sidebar:
        st.markdown('<p class="sidebar-title">🎯 Estrategia CRM</p>', unsafe_allow_html=True)
        
        explicaciones = {
            "Manual / Todos": "Control total de filtros. Sin pre-selecciones automáticas.",
            "Escudo de Oro (Retención VIP)": "🛡️ <b>Objetivo:</b> Evitar fuga de valor. Clientes VIP con alto riesgo.",
            "Caja Rápida (Conversión)": "⚡ <b>Objetivo:</b> Flujo de caja. Clientes con propensión alta.",
            "Diamantes en Bruto (Upselling)": "💎 <b>Objetivo:</b> Crecer cuentas. Clientes nuevos con CLV futuro alto.",
            "Operación Lázaro (Reactivación)": "🔄 <b>Objetivo:</b> Recuperar cuentas. Clientes valiosos inactivos."
        }

        # 1. Listas base de datos
        all_bus = sorted(df_raw['NEGOCIO'].dropna().unique().tolist()) if 'NEGOCIO' in df_raw.columns else []
        all_rec = sorted(df_raw['Segmento_Recompra'].dropna().unique().tolist())
        all_val = sorted(df_raw['Potencial_Valor'].dropna().unique().tolist())
        all_rfm = sorted(df_raw['Segmento_RFM'].dropna().unique().tolist(), key=lambda x: segmento_a_calificacion.get(x, 99))
        all_risk = sorted(df_raw['Categoria_Probabilidad_Abandono'].dropna().unique().tolist())

        # 2. Funciones para forzar el cambio (Callbacks)
        def aplicar_estrategia():
            est = st.session_state.selector_estrategia
            # Reset por defecto a todo
            st.session_state.ms_bus = all_bus
            st.session_state.ms_rec = all_rec
            st.session_state.ms_val = all_val
            st.session_state.ms_rfm = all_rfm
            st.session_state.ms_risk = all_risk

            if est == "Escudo de Oro (Retención VIP)":
                st.session_state.ms_rfm = [s for s in all_rfm if s in ['Campeones', 'VIPs Leales', 'Alto Potencial']]
                st.session_state.ms_risk = [s for s in all_risk if 'Alta' in s or 'Muy alta' in s]
                st.session_state.ms_val = [s for s in all_val if 'Oro' in s or 'Diamante' in s]
            elif est == "Caja Rápida (Conversión)":
                st.session_state.ms_rec = [s for s in all_rec if 'Alta' in s or 'Muy Alta' in s]
                st.session_state.ms_rfm = [s for s in all_rfm if s in ['Calidad Reciente', 'Nuevos Grandes Compradores', 'Estándar Reciente']]
            elif est == "Diamantes en Bruto (Upselling)":
                st.session_state.ms_rfm = [s for s in all_rfm if s in ['Nuevos Clientes', 'Calidad Prometedora', 'Estándar']]
                st.session_state.ms_val = [s for s in all_val if 'Oro' in s or 'Diamante' in s]
            elif est == "Operación Lázaro (Reactivación)":
                st.session_state.ms_rfm = [s for s in all_rfm if s in ['Críticos a Retener', 'En Riesgo', 'A Punto de Dormir']]
                st.session_state.ms_val = [s for s in all_val if 'Oro' in s or 'Plata' in s]

        def toggle_select_all(key_checkbox, key_ms, full_list):
            if st.session_state[key_checkbox]:
                st.session_state[key_ms] = full_list
            else:
                st.session_state[key_ms] = []

        # 3. Selector de Estrategia
        estrategia = st.selectbox(
            "Selecciona un preset de campaña:",
            list(explicaciones.keys()),
            key="selector_estrategia",
            on_change=aplicar_estrategia,
            help="Al elegir una estrategia, los filtros de abajo se ajustarán automáticamente."
        )
        
        st.markdown(f"""<div style="background-color: #F9FAFB; border: 1px solid #E5E7EB; padding: 12px; border-radius: 8px; font-size: 0.82rem; color: #6B7280; line-height: 1.4; margin-bottom: 20px;">{explicaciones[estrategia]}</div>""", unsafe_allow_html=True)
        
        st.divider()
        st.markdown('<p class="sidebar-title">Configuración de Filtros</p>', unsafe_allow_html=True)

        # 4. RENDERIZADO DE FILTROS (Uso de Session State directo)
        
        if 'NEGOCIO' in df_raw.columns:
            with st.expander("Tipo de Negocio", expanded=False):
                st.checkbox("Seleccionar todos", key="chk_bus", value=True, on_change=toggle_select_all, args=("chk_bus", "ms_bus", all_bus))
                if "ms_bus" not in st.session_state: st.session_state.ms_bus = all_bus
                selected_bus = st.multiselect("Negocio", all_bus, key="ms_bus", label_visibility="collapsed")
        
        with st.expander("Propensión de Recompra", expanded=False):
            st.checkbox("Seleccionar todos", key="chk_rec", value=True, on_change=toggle_select_all, args=("chk_rec", "ms_rec", all_rec))
            if "ms_rec" not in st.session_state: st.session_state.ms_rec = all_rec
            selected_recompra = st.multiselect("Recompra", all_rec, key="ms_rec", label_visibility="collapsed")

        with st.expander("Nivel de Valor Futuro", expanded=False):
            st.checkbox("Seleccionar todos", key="chk_val", value=True, on_change=toggle_select_all, args=("chk_val", "ms_val", all_val))
            if "ms_val" not in st.session_state: st.session_state.ms_val = all_val
            selected_valor = st.multiselect("Valor", all_val, key="ms_val", label_visibility="collapsed")

        with st.expander("Segmentos RFM", expanded=False):
            st.checkbox("Seleccionar todos", key="chk_rfm", value=True, on_change=toggle_select_all, args=("chk_rfm", "ms_rfm", all_rfm))
            if "ms_rfm" not in st.session_state: st.session_state.ms_rfm = all_rfm
            selected_rfm = st.multiselect("RFM", all_rfm, key="ms_rfm", label_visibility="collapsed")
        
        with st.expander("Niveles de Riesgo", expanded=False):
            st.checkbox("Seleccionar todos", key="chk_risk", value=True, on_change=toggle_select_all, args=("chk_risk", "ms_risk", all_risk))
            if "ms_risk" not in st.session_state: st.session_state.ms_risk = all_risk
            selected_abandon = st.multiselect("Riesgo", all_risk, key="ms_risk", label_visibility="collapsed")

        if st.button("Limpiar Filtros / Reset"):
            for k in st.session_state.keys():
                if k.startswith("ms_") or k.startswith("chk_") or k == "selector_estrategia":
                    del st.session_state[k]
            st.rerun()


    # --- FILTRADO (Se mantiene igual pero con las variables actualizadas) ---
    mask = (
        (df_raw['Segmento_RFM'].isin(selected_rfm)) &
        (df_raw['Categoria_Probabilidad_Abandono'].isin(selected_abandon)) &
        (df_raw['Segmento_Recompra'].isin(selected_recompra)) &
        (df_raw['Potencial_Valor'].isin(selected_valor))
    )
    if 'NEGOCIO' in df_raw.columns:
        mask = mask & (df_raw['NEGOCIO'].isin(selected_bus))
        
    df_filtered = df_raw[mask].copy()


    # --- 5. CUERPO PRINCIPAL ---
    st.title("Business Insights")
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Cuentas Seleccionadas", f"{len(df_filtered):,}")
    with m2:
        val = df_filtered['Probabilidad_Churn'].mean()
        st.metric("Riesgo Churn Promedio", f"{val:.1%}" if pd.notnull(val) else "0%")
    with m3:
        val = df_filtered['CLV_90dias'].sum()
        st.metric("CLV Total (90d)", f"${val:,.0f}")
    with m4:
        val = df_filtered['Probabilidad_Compra_90d'].mean()
        st.metric("Propensión Compra", f"{val:.1%}" if pd.notnull(val) else "0%")

    # --- 6. GRÁFICOS ---
    #st.markdown('<p class="section-header">Composición y Valor de Cartera</p>', unsafe_allow_html=True)
    
    # FILA 1: Distribución RFM y Distribución de Valor
    c1, c2 = st.columns(2)
    
    with c1:
        # 1. Preparar datos
        df_rfm_counts = df_filtered['Segmento_RFM'].value_counts().reset_index()
        df_rfm_counts.columns = ['Segmento', 'Cantidad']
        
        # 2. Crear Gráfico con Estética Premium
        fig_rfm = px.bar(
            df_rfm_counts, 
            x='Cantidad', 
            y='Segmento', 
            orientation='h',
            title="<b>Distribución por Segmento RFM</b>",
            color='Cantidad',
            color_continuous_scale='Sunsetdark', 
            text_auto='.2s' 
        )
        
        # 3. Personalización Visual Avanzada
        fig_rfm.update_traces(
            marker_line_width=0,
            opacity=0.9,
            textposition='outside',
            textfont=dict(size=12, color='#4B5563')
        )
        
        fig_rfm.update_layout(
            # AQUÍ ESTÁ LA CORRECCIÓN: Todo lo de yaxis en un solo dict
            yaxis=dict(
                categoryorder='total ascending', 
                showgrid=False, 
                title=None
            ),
            
            # Tipografía y títulos
            font=dict(family="Inter, sans-serif", size=13, color="#1F2937"),
            title_font_size=15,
            
            # Limpieza total de fondo y rejillas
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                showgrid=True, 
                gridcolor='#F3F4F6',
                showline=False,
                zeroline=False,
                title="Cuentas"
            ),
            
            # Ocultar barra de color lateral
            coloraxis_showscale=False, 
            
            height=550,
            margin=dict(l=20, r=40, t=70, b=20)
        )

        st.plotly_chart(fig_rfm, use_container_width=True)


    with c2:
        fig_v = px.pie(
            df_filtered, 
            names='Potencial_Valor', 
            title="<b>Cuentas por Nivel de Valor (CLV)</b>", # Agregamos <b> para que sea negrita igual que el otro
            hole=0.5, 
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        
        fig_v.update_layout(
            # --- ESTA ES LA PARTE QUE IGUALA EL DISEÑO ---
            font=dict(family="Inter, sans-serif", size=13, color="#1F2937"),
            title_font_size=15,
            # ---------------------------------------------
            
            legend=dict(orientation="h", yanchor="bottom", y=-0.2),
            height=550, # Igualamos la altura para que las cajas se vean alineadas
            margin=dict(l=20, r=20, t=70, b=20) # Ajustamos márgenes superiores para el título
        )
        st.plotly_chart(fig_v, use_container_width=True)


    # FILA 2: Análisis Predictivo (Scatter Plot)
    st.markdown('<p class="section-header">Relación Propensión vs Valor Esperado</p>', unsafe_allow_html=True)
    
    # Seleccionamos las columnas necesarias para asegurar que existan en el hover
    cols_necesarias = [
        'Probabilidad_Compra_90d', 
        'Monto_Esperado_90d', 
        'CLV_90dias', 
        'Segmento_Recompra', 
        'CUENTA', 
        'Segmento_RFM', 
        'Categoria_Probabilidad_Abandono'
    ]
    
    df_scat = df_filtered.dropna(subset=['Probabilidad_Compra_90d', 'Monto_Esperado_90d']).head(3000)
    
    if not df_scat.empty:
        fig_s = px.scatter(
            df_scat, 
            x='Probabilidad_Compra_90d', 
            y='Monto_Esperado_90d',
            size='CLV_90dias', 
            color='Segmento_Recompra', 
            title="",
            color_discrete_sequence=px.colors.qualitative.Safe,
            hover_name='CUENTA',
            # --- MEJORA DE HOVER AQUÍ ---
            hover_data={
                'Segmento_RFM': True,                               # Añade el Segmento RFM
                'Categoria_Probabilidad_Abandono': True,            # Añade el Riesgo
                'Probabilidad_Compra_90d': ':.2%',                  # Formato porcentaje
                'Monto_Esperado_90d': ':$,.2f',                     # Formato moneda
                'CLV_90dias': ':$,.2f',                             # Formato moneda
                'Segmento_Recompra': False                          # Lo quitamos de aquí porque ya sale en el color
            }
        )
        
        # Personalización adicional para que el hover se vea más limpio
        fig_s.update_layout(
            hoverlabel=dict(
                bgcolor="white",
                font_size=13,
                font_family="Inter"
            ),
            xaxis_title="Probabilidad de Compra (%)",
            yaxis_title="Monto Esperado ($)"
        )
        
        st.plotly_chart(fig_s, use_container_width=True)
    else:
        st.info("Sin datos predictivos suficientes para el gráfico de dispersión.")


    # --- 7. TABLA ---
    st.markdown('<p class="section-header">Explorador</p>', unsafe_allow_html=True)
    
    # MODIFICACIÓN: Buscador de cuenta
    search_query = st.text_input("Buscar cuenta específica:", placeholder="Ingrese ID de cuenta...")
    
    df_table = df_filtered.copy()
    if search_query:
        df_table = df_table[df_table['CUENTA'].astype(str).str.contains(search_query, case=False, na=False)]

    cols_t = ['CUENTA', 'NEGOCIO', 'Segmento_RFM', 'Potencial_Valor', 'Segmento_Recompra', 'CLV_90dias']
    st.dataframe(
        df_table[cols_t], use_container_width=True, height=400,
        column_config={
            "CLV_90dias": st.column_config.NumberColumn("Valor Proyectado", format="$%.2f"),
            "CUENTA": st.column_config.TextColumn("Cuenta")
        }, hide_index=True
    )

    # --- 8. INSIGHTS ---
    st.markdown('<p class="section-header">Resumen</p>', unsafe_allow_html=True)
    i1, i2, i3 = st.columns(3)
    with i1:
        count = len(df_filtered[df_filtered['Potencial_Valor'].astype(str).str.contains('Diamante|Oro', na=False)])
        st.success(f"**Cuentas VIP:**\n\n{count:,} cuentas están en el nivel superior de valor proyectado.")
    with i2:
        count = len(df_filtered[df_filtered['Segmento_Recompra'].astype(str).str.contains('Muy Alta|Alta', na=False)])
        st.info(f"**Venta Próxima:**\n\n{count:,} cuentas tienen propensión alta o muy alta de compra.")
    with i3:
        count = len(df_filtered[df_filtered['Categoria_Probabilidad_Abandono'].astype(str).str.contains('Alta', na=False)])
        st.error(f"**Riesgo Crítico:**\n\n{count:,} cuentas requieren atención inmediata por riesgo de fuga.")
else:
    st.error("Archivo no encontrado o vacío.")