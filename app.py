from src.calculadora import calcula_tensao_critica, calcular_abaco, calcular_v_max
from src.utils import get_about, get_footer, set_chart, set_table
import streamlit as st


st.set_page_config(
    page_title="Calculadora",
    page_icon=":coffee:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': get_about()
    }
)

st.markdown(get_footer(), unsafe_allow_html=True)

st.title('Calculadora - Tensão Crítica')

# Parâmetros de entrada
st.sidebar.title('Parâmetros de Entrada')

st.sidebar.subheader('Dados do Material')
E = st.sidebar.number_input('Módulo de Elasticidade (GPa)', 0.0, 1000.0, 200.0) * 1000
T_esc = st.sidebar.number_input('Tensão de Escoamento (MPa)', 0.0, 1000.0, 250.0)

st.sidebar.subheader('Dados da Seção Transversal')
A = st.sidebar.number_input('Área (mm²)', 0.0, 100000.0, 3787.1)
r = st.sidebar.number_input('Raio de Giração (mm)', 0.0, 1000.0, 68.56)
c = st.sidebar.number_input('Distância da Linha Neutra (mm)', 0.0, 1000.0, 78.74)

st.sidebar.subheader('Dados do caso')
P = st.sidebar.number_input('Carga aplicada (kN)', 0.0, 100000.0, 90.0)
Le = st.sidebar.number_input('Comprimento efetivo do elemento (mm)', 0.0, 100000.0, 5000.0)
e = st.sidebar.number_input('Excentricidade (mm)', 0.0, 1000.0, 100.0)

gerar_abaco_completo = st.sidebar.checkbox('Gerar ábaco completo', value=False, key='gerar_abaco')

if gerar_abaco_completo:

    de = st.sidebar.number_input('De', 0.0, 2.0, 0.0)
    ate = st.sidebar.number_input('Até', 0.1, 2.0, 1.0)

    razao = st.sidebar.number_input('Razão', 0.1, 2.0, 0.1)
else:
    de = 0.0
    ate = 1.0
    razao = 0.1

# botao_calcular
if st.sidebar.button('Calcular'):
    
    with st.spinner('Calculando...'):

        col1, col2, col3 = st.columns(3)
        col4, col5 = st.columns([0.85, 0.15])

        ecr2 = (e*c)/r**2
        Ler = Le/r
        
        tensao_normal_critica = calcula_tensao_critica(T_esc, ecr2, Le/r, A, E)
        tensao_normal_aplicada = (P * 1000) / A
        pcr = tensao_normal_critica * A / 1000
        v_max = calcular_v_max(P, pcr, e)

        fator_seguranca = tensao_normal_critica / tensao_normal_aplicada

        abaco = calcular_abaco(T_esc, ecr2, A, E, gerar_abaco_completo, de, ate, razao)

            
        col1.latex('P_{cr} = '+f'{pcr:.2f} kN')
        col1.latex(f'P = {P:.2f} kN')

        col2.latex('\sigma_{cr} = '+f'{tensao_normal_critica:.2f} MPa')
        col2.latex(f'\sigma = {tensao_normal_aplicada:.2f} MPa')
        col2.latex('V_{max} = '+f'{v_max:.2f} mm')

        col3.latex(f'FS = {fator_seguranca:.2f}')
        col3.latex(f'Método: {"Euler" if e == 0 else "Secante"}')

        set_chart(col4, abaco)
        set_table(col5, ecr2, abaco)
