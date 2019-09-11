class Problema:
    def __init__(self, grafo, no_grafo_inicial, no_grafo_final, funcao_resultado):
        self.grafo = grafo
        self.estado_inicial = no_grafo_inicial[0]
        self.estado_final = no_grafo_final[0]
        self.funcao_resultado = funcao_resultado

    def teste_de_objetivo(self, estado):
        if estado == self.estado_final:
            return True
        return False

    def __str__(self):
        estados = f""
        for estado in self.estados:
            estados += f"{estado} "
        return estados

    def pega_no_grafo_por_nome(self, estado):
        for no_grafo in self.grafo:
            if estado == no_grafo[0]:
                return no_grafo
        return None

    def acoes(self, estado):
        acoes = []
        no_grafo = self.pega_no_grafo_por_nome(estado)
        proximos_estados = no_grafo[2]
        for e in proximos_estados:
            acoes.append(e)
        return acoes

    def custo_acao(self, estado, acao):
        no_grafo = self.pega_no_grafo_por_nome(estado)
        return no_grafo[2][acao]

    def resultado(self, estado, acao):
        return self.funcao_resultado(estado, acao)


class No:
    def __init__(self, estado, pai=None, acao=None, custo=0):
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo

    def __str__(self):
        return f"Estado: {self.estado} \nPai: {self.pai.estado if self.pai else self.pai}\nCusto: {self.custo} "

    def __eq__(self, other):
        return self.estado == other


def no_filho(problema, pai, acao):
    estado = problema.resultado(pai.estado, acao)
    pai = pai
    acao = acao
    custo = pai.custo + problema.custo_acao(pai.estado, acao)
    return No(estado, pai, acao, custo)


def solucao(problema, no):
    solucao = [no.estado]
    pai = no.pai

    while pai:
        solucao.append(pai.estado)
        pai = pai.pai

    return solucao[::-1]
