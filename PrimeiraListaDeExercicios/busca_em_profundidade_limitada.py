from classes import *

LOG = True

explorado = []
borda = []


def busca_em_profundidade_limitada(problema, limite):
    no = No(problema.estado_inicial)
    borda.append(no)
    return busca_em_profundidade_limitada_recursiva(no, problema, limite)


def busca_em_profundidade_limitada_recursiva(no, problema, limite):
    if LOG:
        print("Borda:", [
            no.estado + f" pai {no.pai.estado if no.pai else None} " for no in borda])
        print("Explorados: ", [
            no.estado + f" pai {no.pai.estado if no.pai else None} " for no in explorado])

    borda.remove(no)
    explorado.append(no)

    if problema.teste_de_objetivo(no.estado):
        return solucao(problema, no), [no.estado + f" pai {no.pai.estado if no.pai else None} " for no in explorado], [no.estado + f" pai {no.pai.estado if no.pai else None} " for no in borda]
    else:
        if limite == 0:
            return "corte"
        else:
            CORTE_OCORREU = False

        for acao in problema.acoes(no.estado):
            filho = no_filho(problema, no, acao)
            borda.append(filho)

            resultado = busca_em_profundidade_limitada_recursiva(
                filho, problema, limite - 1)

            if resultado == "corte":
                CORTE_OCORREU = True
            else:
                if resultado != "erro":
                    return resultado
                if CORTE_OCORREU:
                    return "corte"
                else:
                    return "erro"
