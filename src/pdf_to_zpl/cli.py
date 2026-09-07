import argparse

from .leitura import scan_barcodes_em_pdf
from .agrupamento import agrupar_por_sku
from .zpl import gerar_zpl_por_sku
from .saida import salvar_zpls, limpar_pasta_saida


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Converte um PDF de etiquetas (QR + texto) em arquivos ZPL segmentados por SKU.'
    )
    parser.add_argument('pdf', help='Caminho para o PDF de etiquetas de origem')
    parser.add_argument('--saida', default='saida_zpl', help='Pasta onde os .zpl serão gravados')
    parser.add_argument('--poppler-path', default=None, help='Caminho da pasta bin do Poppler')
    parser.add_argument('--dpi', type=int, default=300, help='Resolução usada na leitura do PDF')
    args = parser.parse_args()

    registros = scan_barcodes_em_pdf(args.pdf, args.poppler_path, dpi=args.dpi)
    print(f'Total de páginas lidas: {len(registros)}')

    divergencias = [r for r in registros if r['qr_data'] != r['barcode']]
    if divergencias:
        print(f'ATENÇÃO: {len(divergencias)} página(s) com QR != barcode do texto — conferir manualmente.')

    grupos = agrupar_por_sku(registros)
    print('\nResumo por SKU:')
    for sku, itens in grupos.items():
        print(f'  SKU {sku} | qtd={len(itens)} | cor={itens[0]["cor"]} | {itens[0]["titulo"]}')

    limpar_pasta_saida(args.saida)
    zpls = gerar_zpl_por_sku(grupos)
    salvar_zpls(zpls, args.saida)


if __name__ == '__main__':
    main()
