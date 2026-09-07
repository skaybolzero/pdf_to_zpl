from collections import defaultdict

# 2. Agrupamento - conta quantas páginas (=unidades) existem de cada SKU
def agrupar_por_sku(registros: list[dict]) -> dict[str, list[dict]]:
    grupos = defaultdict(list)
    for r in registros:
        grupos[r['seller_sku']].append(r)
    return dict(grupos)
