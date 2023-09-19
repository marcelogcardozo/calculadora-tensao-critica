from src.calculadora import calcula_tensao_critica, calcular_abaco, calcular_v_max
from src.utils import get_footer, set_chart, set_table
import streamlit as st

st.set_page_config(
    page_title="Calculadora",
    page_icon=":coffee:",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(get_footer(), unsafe_allow_html=True)

st.title('Calculadora - Tensão Crítica')

st.markdown("""

Feito por: Marcelo Cardozo  &bull; [![GitHub](https://cdn.pixabay.com/photo/2022/01/30/13/33/github-6980894_1280.png)](https://github.com/marcelogcardozo)
                            &bull; [![LinkedIn](https://scontent.fsdu25-1.fna.fbcdn.net/v/t39.30808-1/267422938_4880673518668256_5792791296770782057_n.png?stp=dst-png_p200x200&_nc_cat=108&ccb=1-7&_nc_sid=754033&_nc_ohc=FzJ49MszpDkAX_b3T44&_nc_ht=scontent.fsdu25-1.fna&cb_e2o_trans=t&oh=00_AfC1YK5ssU0tc3BQcFnYLlPAJFN8jotV5pf9JJc-ANb7pQ&oe=650DDC2B)](https://www.linkedin.com/in/marcelogcardozo/)

Versão: 0.1.0
""")

st.markdown(
    """
    <style>
    img {
        width: 25px; /* Define a largura da imagem */
        height: 25px; /* Define a altura da imagem */
        border-radius: 50%; /* Cria um efeito de círculo */
    }
    </style>
    """,
    unsafe_allow_html=True,
)





st.subheader('Resultados')
st.divider()

# Parâmetros de entrada
st.sidebar.title('Parâmetros de Entrada')

st.sidebar.subheader('Dados do Material')
E = st.sidebar.number_input('Módulo de Elasticidade (GPa)', 0.1, 10000.0, 200.0) * 1000
T_esc = st.sidebar.number_input('Tensão de Escoamento (MPa)', 0.1, 10000.0, 250.0)

st.sidebar.subheader('Dados da Seção Transversal')
A = st.sidebar.number_input('Área (mm²)', 0.1, None, 1900.0)
I = st.sidebar.number_input('Inércia (mm⁴)', 0.0, None, 0.0)
r = st.sidebar.number_input('Raio de Giração (mm)', 0.0, None, 20.76)
c = st.sidebar.number_input('Distância da Linha Neutra (mm)', 0.1, None, 0.1)

st.sidebar.subheader('Dados do caso')
P = st.sidebar.number_input('Carga aplicada (kN)', 0.0, None, 16.0)
Le = st.sidebar.number_input('Comprimento efetivo do elemento (mm)', 0.1, None, 6000.0)
e = st.sidebar.number_input('Excentricidade (mm)', 0.0, None, 0.0)
FS = st.sidebar.number_input('Fator de Segurança', 0.0, None, 1.0)

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

        if (I == 0 and r == 0):
            st.error('Inércia e Raio de Giração não podem ser ambos iguais a 0')
            st.stop()
        elif r == 0:
            r = (I / A) ** (1/2)

        ecr2 = (e*c)/r**2
        Ler = Le/r
   
        tensao_normal_critica = calcula_tensao_critica(T_esc, ecr2, Ler, E)
        pcr = tensao_normal_critica * A / 1000
        
        if (P == 0 and FS > 0):
            P = pcr / FS
        tensao_normal_aplicada = (P * 1000) / A

        v_max = calcular_v_max(P, pcr, e)

        FS = 0 if tensao_normal_aplicada == 0 else tensao_normal_critica / tensao_normal_aplicada

        abaco = calcular_abaco(T_esc, ecr2, E, gerar_abaco_completo, de, ate, razao)

        col1.latex('P_{cr} = '+f'{pcr:.2f} kN')
        col1.latex(f'P = {P:.2f} kN')

        col2.latex('\sigma_{cr} = '+f'{tensao_normal_critica:.2f} MPa')
        col2.latex(f'\sigma = {tensao_normal_aplicada:.2f} MPa')
        col2.latex('V_{max} = '+f'{v_max:.2f} mm')

        col3.latex(f'FS = {FS:.2f}')
        col3.latex(f'Método: {"Euler" if e == 0 else "Secante"}')

        set_chart(col4, ecr2, abaco, gerar_abaco_completo)
        set_table(col5, ecr2, abaco)
