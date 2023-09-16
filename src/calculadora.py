from dataclasses import dataclass
from math import cos, sqrt, pi
import numpy as np

@dataclass
class Ponto:
    ler: float
    pa: float


def calcula_tensao_normal_maxima_metodo_secante(t_esc, ecr2, Ler, E) -> float:

    def _calcula_equacao_da_secante(PsA, ecr2, Ler, E) -> float:
        secante = 1 / cos((Ler/2) * sqrt(PsA / E))
        return PsA * (1 + ecr2 * secante)

    Psa_values = np.arange(0.1, t_esc, 0.1)
    tensoes_calculadas = np.vectorize(_calcula_equacao_da_secante)(Psa_values, ecr2, Ler, E)
    tensao_imediatamente_maior_que_t_esc = tensoes_calculadas[tensoes_calculadas > t_esc].min()
    index = np.where(tensoes_calculadas == tensao_imediatamente_maior_que_t_esc)[0][0]
    return Psa_values[index]

def calcula_tensao_normal_maxima_metodo_euler(E, A, Ler) -> float:
    return (np.pi**2 * E) / (Ler**2)

def calcular_v_max(p_aplicado, p_critico, e):
    secante = 1 / cos( (pi/2) * sqrt(p_aplicado / p_critico) )
    return round(e * (secante - 1),2)

def calcula_tensao_critica(t_esc, ecr2, Ler, A, E):
    if ecr2 == 0:
        return calcula_tensao_normal_maxima_metodo_euler(E, A, Ler)
    else:
        return calcula_tensao_normal_maxima_metodo_secante(t_esc, ecr2, Ler, E)


def calcular_pontos_abaco(t_esc, ecr2, A, E):
    Ler_values = np.arange(0.5, 200.5, 0.5)
    PsA_values = np.vectorize(calcula_tensao_critica)(t_esc, ecr2, Ler_values, A, E)
    pontos = [Ponto(round(Ler, 24), round(PsA, 2)) for Ler, PsA in zip(Ler_values, PsA_values)]
    
    return {ecr2 : pontos}

def calcular_abaco(t_esc, ecr2, A, E, abaco_completo, de, ate, razao):

    if abaco_completo:
        ecr2_values = np.append(np.arange(de, ate+razao, razao), [ecr2])
    else:
        ecr2_values = [ecr2]
    
    abaco = {}

    curvas = np.vectorize(calcular_pontos_abaco)(t_esc, ecr2_values, A, E)
    
    for curva in curvas:
        abaco.update(curva)
    
    return abaco


