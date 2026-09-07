import textwrap

# 2.1 Quebrar título
def quebrar_titulo(titulo: str, largura_max: int = 34, max_linhas: int = 3) -> list[str]:
    linhas = textwrap.wrap(titulo, width=largura_max)
    if len(linhas) > max_linhas:
        linhas = linhas[:max_linhas - 1] + [' '.join(linhas[max_linhas - 1:])]
    return linhas

# 2.2 gerar_zpl_etiqueta
def gerar_zpl_etiqueta(item: dict, quantidade: int) -> str:
    linhas_titulo = quebrar_titulo(item['titulo'])
    campos_titulo = []
    y = 14
    for linha in linhas_titulo:
        campos_titulo.append(f"^FO14,{y}^A0N,20,20^FB452,1,0,C,0^FD{linha}^FS")
        y += 22
    y_qr = y + 4
    bloco_titulo = "\n".join(campos_titulo)
 
    return f"""^XA
^CI28
^PW480
^LL320
^LH0,0
{bloco_titulo}
^FO175,{y_qr}^BQN,2,5^FDQA,{item['qr_data']}^FS
^FO14,224^A0N,22,22^FB452,1,0,C,0^FDCor/Var: {item['cor']}^FS
^FO14,250^A0N,20,20^FB452,1,0,C,0^FDSKU: {item['seller_sku']}^FS
^FO14,274^A0N,16,16^FB452,1,0,C,0^FD{item['barcode']}^FS
^PQ{quantidade}
^XZ
"""

# 3. Geração do ZPL
def gerar_zpl_por_sku(grupos: dict[str, list[dict]]) -> dict[str, str]:
    arquivos = {}
    for sku, itens in grupos.items():
        item = itens[0]
        quantidade = len(itens)
        arquivos[sku] = gerar_zpl_etiqueta(item, quantidade)
    return arquivos
