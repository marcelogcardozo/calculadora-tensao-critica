from src.utils import reset_config, set_basic_info, set_sidebar_and_get_params, set_resultados
from src.calculadora import calcula_tensao_critica, calcular_abaco, calcular_v_max
import streamlit as st

reset_config(st)

set_basic_info(st)

E, T_esc, A, I, r, c, P, FS, Le, k, e, gerar_abaco_completo, de, ate, razao = set_sidebar_and_get_params(st)

# botao_calcular
if st.sidebar.button('Calcular'):
    
    with st.spinner('Calculando...'):
    
        if A == 0:
            st.error('A área (A) não pode ser iguao a zero.')
            st.stop()
        elif (e > 0 and c == 0):
            st.error('A distância do centroide à fibra mais comprimida (c) não podem ser iguais a zero quando a excentricidade (e) for maior do que zero.')
            st.stop()
        elif (r == 0 and I == 0):
            st.error('O raio de giração (r) ou o momento de inércia (I) devem ser diferentes de zero.')
            st.stop()
        elif (Le == 0):
            st.error('O comprimento efetivo de flambagem (Le) não pode ser igual a zero.')
            st.stop()

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

        set_resultados(st, pcr, P, tensao_normal_critica, tensao_normal_aplicada, v_max, FS, e, ecr2, Ler, abaco, gerar_abaco_completo)

