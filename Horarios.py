from itertools import combinations, product
from Logica_checkpoint import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from types import MethodType
import sys

sys.setrecursionlimit(10000)

# ---------------------------------------------------------------
# Dominios. El índice de cada lista es el que usa el Descriptor.
# ---------------------------------------------------------------
CURSOS = ['Lógica', 'Cálculo', 'Programación', 'Álgebra']
PROFES = ['Kurt', 'Bertrand', 'Alan']
BLOQUES = ['Bloque 1', 'Bloque 2', 'Bloque 3']
SALONES = ['Salón 101', 'Salón 102']

NC, NP, NH, NS = len(CURSOS), len(PROFES), len(BLOQUES), len(SALONES)


def escribir_horarios(self, literal):
    if '-' in literal:
        atomo = literal[1:]
        neg = ' no'
    else:
        atomo = literal
        neg = ''
    c, p, h, s = self.unravel(atomo)
    return f"{CURSOS[c]}{neg} es dictada por {PROFES[p]} en el {BLOQUES[h]}, {SALONES[s]}"


class Horarios:

    '''
    Clase para representar el problema de asignar
    asignaturas a profesores, bloques y salones.
    '''

    def __init__(self):
        self.A = Descriptor([NC, NP, NH, NS])
        self.A.escribir = MethodType(escribir_horarios, self.A)
        r1 = self.regla1()
        r2 = self.regla2()
        r3 = self.regla3()
        r4 = self.regla4()
        self.reglas = [r1, r2, r3, r4]

    # Atajo para no escribir ravel([...]) todo el tiempo
    def a(self, c, p, h, s):
        return self.A.ravel([c, p, h, s])

    def regla1(self):
        combos = list(product(range(NP), range(NH), range(NS)))
        # Al menos una asignación por curso
        lista_min = []
        for c in range(NC):
            lista_min.append(Otoria([self.a(c, *k) for k in combos]))
        minimo = Ytoria(lista_min)
        # A lo sumo una asignación por curso
        lista_max = []
        for c in range(NC):
            for k in combos:
                otros = [self.a(c, *o) for o in combos if o != k]
                lista_max.append('(' + self.a(c, *k) + '>-' + Otoria(otros) + ')')
        maximo = Ytoria(lista_max)
        return '(' + minimo + 'Y' + maximo + ')'

    def regla2(self):
        lista = []
        for p in range(NP):
            for h in range(NH):
                for c1, c2 in combinations(range(NC), 2):
                    for s1, s2 in product(range(NS), repeat=2):
                        lista.append('-(' + self.a(c1, p, h, s1) + 'Y' + self.a(c2, p, h, s2) + ')')
        return Ytoria(lista)

    def regla3(self):
        lista = []
        for s in range(NS):
            for h in range(NH):
                for c1, c2 in combinations(range(NC), 2):
                    for p1, p2 in product(range(NP), repeat=2):
                        lista.append('-(' + self.a(c1, p1, h, s) + 'Y' + self.a(c2, p2, h, s) + ')')
        return Ytoria(lista)

    def regla4(self):
        kurt = PROFES.index('Kurt')
        bertrand = PROFES.index('Bertrand')
        lista = []
        # Kurt solo dicta Lógica o Programación
        for c in [CURSOS.index('Cálculo'), CURSOS.index('Álgebra')]:
            for h in range(NH):
                for s in range(NS):
                    lista.append('-' + self.a(c, kurt, h, s))
        # Bertrand no está disponible en el Bloque 1
        for c in range(NC):
            for s in range(NS):
                lista.append('-' + self.a(c, bertrand, 0, s))
        return Ytoria(lista)

    def base_conocimiento(self):
        return Ytoria(self.reglas)

    def imprimir(self, I):
        for l in I:
            if I[l]:
                print(self.A.escribir(l))

    def visualizar(self, I):
        fig, axes = plt.subplots(figsize=(3 * NS + 1, 2 * NH))
        ancho = 1. / NS
        alto = 1. / NH
        # Cuadrícula: filas = bloques, columnas = salones
        for h in range(NH):
            for s in range(NS):
                color = 'cornsilk' if (h + s) % 2 == 0 else 'lightgrey'
                axes.add_patch(patches.Rectangle((s * ancho, 1 - (h + 1) * alto), ancho, alto,
                                                 facecolor=color, edgecolor='black', linewidth=2))
        # Texto de cada asignación verdadera
        for l in I:
            if I[l]:
                c, p, h, s = self.A.unravel(l)
                axes.text(s * ancho + ancho / 2, 1 - h * alto - alto / 2,
                          f'{CURSOS[c]}\n{PROFES[p]}',
                          ha='center', va='center', size=14)
        axes.set_xlim(0, 1)
        axes.set_ylim(0, 1)
        axes.set_xticks([ancho * (s + .5) for s in range(NS)])
        axes.set_xticklabels(SALONES)
        axes.xaxis.tick_top()
        axes.set_yticks([1 - alto * (h + .5) for h in range(NH)])
        axes.set_yticklabels(BLOQUES)
        axes.tick_params(length=0)
        plt.show()


def tseitin(formula):
    '''
    Convierte una fórmula (string inorder) a forma clausal con la
    transformación de Tseitin. Devuelve (ids, clausulas) donde ids
    mapea cada letra proposicional a un entero positivo y cada cláusula
    es una lista de enteros (negativo = literal negado).
    '''
    arbol = inorder_to_tree(formula)
    ids = {}
    clausulas = []
    contador = [0]

    def nueva():
        contador[0] += 1
        return contador[0]

    def codificar(f):
        if type(f) == Letra:
            if f.letra not in ids:
                ids[f.letra] = nueva()
            return ids[f.letra]
        if type(f) == Negacion:
            return -codificar(f.subf)
        a = codificar(f.left)
        b = codificar(f.right)
        x = nueva()
        if f.conectivo == 'Y':
            clausulas.extend([[-x, a], [-x, b], [x, -a, -b]])
        elif f.conectivo == 'O':
            clausulas.extend([[-x, a, b], [x, -a], [x, -b]])
        elif f.conectivo == '>':
            clausulas.extend([[-x, -a, b], [x, a], [x, -b]])
        elif f.conectivo == '=':
            clausulas.extend([[-x, -a, b], [-x, a, -b], [x, a, b], [x, -a, -b]])
        return x

    raiz = codificar(arbol)
    clausulas.append([raiz])
    return ids, clausulas


def dpll(clausulas, asignacion):
    '''
    DPLL con propagación unitaria. Devuelve un dict var -> bool
    o None si las cláusulas son insatisfacibles.
    '''
    while True:
        unidades = set()
        restantes = []
        for c in clausulas:
            pendientes = []
            satisfecha = False
            for l in c:
                v = asignacion.get(abs(l))
                if v is None:
                    pendientes.append(l)
                elif v == (l > 0):
                    satisfecha = True
                    break
            if satisfecha:
                continue
            if not pendientes:
                return None
            if len(pendientes) == 1:
                unidades.add(pendientes[0])
            restantes.append(pendientes)
        clausulas = restantes
        if not unidades:
            break
        if any(-l in unidades for l in unidades):
            return None
        asignacion = dict(asignacion)
        for l in unidades:
            asignacion[abs(l)] = l > 0
    if not clausulas:
        return asignacion
    # Ramificación sobre un literal de la cláusula más corta
    literal = min(clausulas, key=len)[0]
    for valor in (literal > 0, literal < 0):
        nueva_asig = dict(asignacion)
        nueva_asig[abs(literal)] = valor
        res = dpll(clausulas, nueva_asig)
        if res is not None:
            return res
    return None


def resolver(formula):
    '''
    SAT solver: Tseitin + DPLL sobre las fórmulas de Logica.py.
    Devuelve una interpretación (dict átomo -> bool) o None
    si la fórmula es insatisfacible.
    '''
    ids, clausulas = tseitin(formula)
    res = dpll(clausulas, {})
    if res is None:
        return None
    return {letra: res.get(v, False) for letra, v in ids.items()}


if __name__ == '__main__':
    h = Horarios()
    I = resolver(h.base_conocimiento())
    if I is None:
        print('La base de conocimiento es insatisfacible: no hay horario válido')
    else:
        h.imprimir(I)
        h.visualizar(I)

        