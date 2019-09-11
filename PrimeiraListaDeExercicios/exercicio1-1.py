from classes import *
from busca_em_largura import busca_em_largura

# nos do grafo
start_n = ("Start", 0, {"A": 2, "B": 3, "D": 5})
A_n = ("A", 2, {"Start": 2, "C": 2})
B_n = ("B", 5, {"Start": 3, "D": 4})
C_n = ("C", 2, {"A": 2, "D": 1, "Goal": 2})
D_n = ("D", 1, {"Start": 5, "B": 4, "C": 1, "Goal": 5})
goal_n = ("Goal", 0, {"C": 2, "D": 5})

grafo = [start_n, A_n, B_n, C_n, D_n, goal_n]


def funcao_resultado(estado, acao):
    return acao


problema = Problema(grafo, start_n, goal_n, funcao_resultado)

solucao, explorados, borda = busca_em_largura(problema)

print("Solucao:", solucao)
print("Explorados", explorados)
print("Borda", borda)
