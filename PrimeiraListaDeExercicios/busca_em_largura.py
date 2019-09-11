from classes import *

LOG = False


def busca_em_largura(problema):
    no = No(problema.estado_inicial)

    if problema.teste_de_objetivo(no.estado):
        return solucao(problema, no), [], []

    borda = [no]
    explorado = []

    while len(borda):
        if LOG:
            print("Borda: ", [
                  no.estado + f" pai {no.pai.estado if no.pai else None} " for no in borda])

        no = borda.pop(0)
        explorado = explorado + [no]

        if LOG:
            print("Explorados: ", [
                  no.estado + f" pai {no.pai.estado if no.pai else None} " for no in explorado])
            print("Nó Explorado:", no.estado)

        for acao in problema.acoes(no):
            if LOG:
                print("Filho: ", acao)

            filho = no_filho(problema, no, acao)

            if (filho not in explorado) and (filho not in borda):
                if problema.teste_de_objetivo(filho):
                    return solucao(problema, filho), [no.estado + f" pai {no.pai.estado if no.pai else None} " for no in explorado], [no.estado + f" pai {no.pai.estado if no.pai else None} " for no in borda]

                borda.append(filho)
    return False
