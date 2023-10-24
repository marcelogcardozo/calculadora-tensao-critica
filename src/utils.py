import plotly.graph_objects as go

from math import sqrt
import numpy as np

def reset_config(st) -> None:

    def _get_footer():
        style = """
            <style>
                # MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                .stApp { bottom: 0px; }
            </style>
        """
        return style
    
    st.set_page_config(
        page_title="Calculadora",
        page_icon=":coffee:",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items = {
            'Get Help': 'mailto:marcelo.cardozo.cg@gmail.com?subject=Ajuda%20-%20Calculadora%20de%20Tensão%20Crítica',
            'Report a bug': 'mailto:marcelo.cardozo.cg@gmail.com?subject=BUG%20-%20Calculadora%20de%20Tensão%20Crítica',
        },
    )

    st.markdown(_get_footer(), unsafe_allow_html=True)

def set_basic_info(st) -> None:

    st.title('Calculadora - Tensão Crítica')
    st.markdown("""
    Feito por: Marcelo Cardozo  &bull; [GitHub](https://github.com/marcelogcardozo)
                                &bull; [LinkedIn](https://www.linkedin.com/in/marcelogcardozo/)

    Versão: 1.0
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

def set_sidebar_and_get_params(st) -> tuple:

    def _set_dados_do_material() -> tuple:

        st.sidebar.subheader('Dados do Material')
        E = st.sidebar.number_input('Módulo de Elasticidade (E) [GPa]', 0.0, None, 200.0) * 1000
        T_esc = st.sidebar.number_input('Tensão de Escoamento ($\sigma_{y}$) [MPa]', 0.0, None, 250.0)

        return E, T_esc

    def _set_dados_secao_transversal() -> tuple:

        st.sidebar.subheader('Dados da Seção Transversal')
        A = st.sidebar.number_input('Área (A) [mm²]', 0.0, None, 0.0)
        col1, col2 = st.sidebar.columns([0.4, 0.6])
        select_box_I_r = col1.selectbox('Inércia ou Raio de Giração', ['I [mm⁴]', 'r [mm]'], label_visibility='collapsed')
        value_I_r = col2.number_input('uma_label_qualquer', 0.0, None, 0.0, label_visibility='collapsed')
        
        if select_box_I_r == 'I [mm⁴]':
            I = value_I_r
            try:
                r = sqrt(I / A)
            except ZeroDivisionError:
                r = 0.0
        else:
            r = value_I_r
            I = A * r**2
        
        c = st.sidebar.number_input('Dist. da LN à Fibra de Maior Compressão (c) [mm]', 0.0, None, 0.0)

        return A, I, r, c

    def _set_dados_do_caso() -> tuple:

        st.sidebar.subheader('Dados do caso')

        col1, col2 = st.sidebar.columns([0.4, 0.6])

        sbox_P = col1.selectbox('uma_label', ['P [kN]', 'FS'], label_visibility='collapsed') #st.sidebar.number_input('Carga aplicada (P) [kN]', 0.0, None, 0.0)
        value_P = col2.number_input('uma_label2', 0.0, None, 0.0, label_visibility='collapsed')

        if sbox_P == 'P [kN]':
            P = value_P
            FS = 0
        else:
            FS = value_P
            P = 0

        col1, col2 = st.sidebar.columns([0.4, 0.6])
        sbox_Le = col1.selectbox('Comprimento efetivo do elemento (Le)', ['Le [mm]', 'L [mm]'], label_visibility='collapsed')
        value_Le = col2.number_input('uma_label_qualquer2', 0.0, None, 0.0, label_visibility='collapsed')

        if sbox_Le == 'L [mm]':
            k = st.sidebar.select_slider('Coeficiente de Flambagem (k)', [str(round(i,2)) for i in np.arange(0.5, 2.05, 0.05)])
            Le = float(k) * value_Le
        else:
            Le = value_Le
            k = 1.0

        e = st.sidebar.number_input('Excentricidade (e) [mm]', 0.0, None, 0.0)

        return P, FS, Le, k, e

    def _set_gerar_abaco_completo_params() -> tuple:

        gerar_abaco_completo = st.sidebar.checkbox('Gerar ábaco completo', value=False, key='gerar_abaco')

        if gerar_abaco_completo:

            faixa_ecr2 = st.sidebar.slider(r'Faixa do $ec/r²$', 0.0, 2.0, (0.0, 1.0), 0.1)
            de = faixa_ecr2[0]
            ate = faixa_ecr2[1]

            razao = st.sidebar.number_input('Razão', 0.1, 2.0, 0.1)
        else:
            de = 0.0
            ate = 1.0
            razao = 0.1

        return gerar_abaco_completo, de, ate, razao

    # Parâmetros de entrada
    st.sidebar.title('Parâmetros de Entrada')

    E, T_esc = _set_dados_do_material()
    A, I, r, c = _set_dados_secao_transversal()
    P, FS, Le, k, e = _set_dados_do_caso()
    abaco_completo, de, ate, razao = _set_gerar_abaco_completo_params()

    return E, T_esc, A, I, r, c, P, FS, Le, k, e, abaco_completo, de, ate, razao

def set_resultados(st, pcr, P, tensao_normal_critica, tensao_normal_aplicada, v_max, FS, e, ecr2, Ler, abaco, gerar_abaco_completo) -> None:

    def set_chart(col_widget, ecr2_base: float, abaco: dict, gerar_abaco_completo: bool) -> None:
        
        fig = go.Figure()
            
        for ecr2, pontos in abaco.items():
            
            xs = [p.ler for p in pontos]
            ys = [p.pa for p in pontos]

            dash = 'dash' if (ecr2 == ecr2_base and gerar_abaco_completo) else None
            line_trace = go.Scatter(x=xs, y=ys, name=f"{ecr2:.2f}", mode='lines', line=dict(dash=dash))

            fig.add_trace(line_trace)

        fig.update_layout(
            title= 'Ábaco de Euler e Secante',
            xaxis_title="Le/r",
            yaxis_title="P/A",
            legend_title="Ecr2",
            yaxis_range=[0, 300.1],
            xaxis_range=[0, 200.1],
        )

        col_widget.plotly_chart(fig, use_container_width=True)

    def set_table(col_widget, ecr2, abaco) -> None:

        data_for_dataframe = {
            'Le/r': [round(p.ler, 2) for p in abaco[ecr2]],
            'P/A': [round(p.pa, 2) for p in abaco[ecr2]],
        }

        col_widget.dataframe(data_for_dataframe)
        
    col1, col2, col3 = st.columns(3)
    col4, col5 = st.columns([0.85, 0.15])

    col1.latex('P_{cr} = ' + f'{pcr:.2f} kN')
    col1.latex('P_{apl} = '+ f'{P:.2f} kN')
    col1.latex('ec/r^2 = '+f'{ecr2:.2f}')

    col2.latex('\sigma_{cr} = '  + f'{tensao_normal_critica:.2f} MPa')
    col2.latex('\sigma_{apl} = ' + f'{tensao_normal_aplicada:.2f} MPa')
    col2.latex(f'Le/r = {Ler:.2f}')

    col3.latex(f'FS = {FS:.2f}')
    col3.latex('V_{max} = '+ f'{v_max:.2f} mm')
    col3.latex(f'Método: {"Euler" if e == 0 else "Secante"}')

    

    set_chart(col4, ecr2, abaco, gerar_abaco_completo)
    set_table(col5, ecr2, abaco)



