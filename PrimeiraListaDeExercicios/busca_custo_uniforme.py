from classes import *

LOG = False


def busca_custo_uniforme(problema):
    no = No(problema.estado_inicial)

    borda = [no]
    explorado = []

    while len(borda):
        if LOG:
            print("Borda:", [
                  no.estado + f" pai {no.pai.estado if no.pai else None} " for no in borda])

        no = None
        for n in borda:
            if no == None:
                no = n
                continue
            if n.custo < no.custo:
                no = n
        borda.remove(no)

        if problema.teste_de_objetivo(no.estado):
            return solucao(problema, no), [no.estado + f" pai {no.pai.estado if no.pai else None} " for no in explorado], [no.estado + f" pai {no.pai.estado if no.pai else None} " for no in borda]

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
                borda.append(filho)
            else:
                if filho in borda:
                    no_de_mesmo_estado = None
                    for no in borda:
                        if no == filho:
                            no_de_mesmo_estado = no
                    if no_de_mesmo_estado.custo > filho.custo:
                        borda.remove(no_de_mesmo_estado)
                        borda.append(filho)
    return False
