from heapq import heappush, heappop
from itertools import count
import networkx as nx


def dijkstra_algorithm(G, inicio, final, atributo="weight"):
    (distancia_total, camino) = para_un_vertice(G, inicio, final=final, atributo=atributo)
    return camino


def extraer_pesos(G, weight):
    if callable(weight):
        return weight

    if G.is_multigraph():
        return lambda u, v, d: min(attr.get(weight, 1) for attr in d.values())
    return lambda u, v, data: data.get(weight, 1)


def para_un_vertice(G, inicio, final=None, limite=None, atributo="weight"):
    return varios_vertices(
        G, {inicio}, limite=limite, final=final, peso=atributo
    )


def varios_vertices(G, iniciales, final=None, limite=None, peso="weight"):
    if not iniciales:
        raise ValueError("El grafo esta vacio")

    if final in iniciales:
        return (0, [final])
    peso = extraer_pesos(G, peso)
    camino = {inicio: [inicio] for inicio in iniciales}
    distancia = _dijkstra_multisource(
        G, iniciales, peso, caminos=camino, limite=limite, final=final)
    if final is None:
        return (distancia, camino)
    try:
        return (distancia[final], camino[final])
    except KeyError as e:
        raise nx.NetworkXNoPath(f"No path to {final}.") from e


def _dijkstra_multisource(
        G, iniciales, pesos, pred=None, caminos=None, limite=None, final=None
):
    G_succ = G._succ if G.is_directed() else G._adj

    push = heappush
    pop = heappop
    distancia = {}
    visitado = {}
    c = count()
    valores_x_vertice = []
    for vertice_inicial in iniciales:
        if vertice_inicial not in G:
            raise nx.NodeNotFound(f"El vertice origen {vertice_inicial}no es parte del grafo")
        visitado[vertice_inicial] = 0
        push(valores_x_vertice, (0, next(c), vertice_inicial))
    while valores_x_vertice:
        (dist, contador, verti) = pop(valores_x_vertice)
        if verti in distancia:
            continue
        distancia[verti] = dist
        if verti == final:
            break
        for u, e in G_succ[verti].items():
            cost = pesos(verti, u, e)
            if cost is None:
                continue
            vu_dist = distancia[verti] + cost
            if limite is not None:
                if vu_dist > limite:
                    continue
            if u in distancia:
                u_dist = distancia[u]
                if vu_dist < u_dist:
                    raise ValueError("Camino incorrecto:", "pesos negativos invalidos")
                elif pred is not None and vu_dist == u_dist:
                    pred[u].append(verti)
            elif u not in visitado or vu_dist < visitado[u]:
                visitado[u] = vu_dist
                push(valores_x_vertice, (vu_dist, next(c), u))
                if caminos is not None:
                    caminos[u] = caminos[verti] + [u]
                if pred is not None:
                    pred[u] = [verti]
            elif vu_dist == visitado[u]:
                if pred is not None:
                    pred[u].append(verti)

    return distancia
