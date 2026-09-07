import re

import pdfplumber
from pdf2image import convert_from_path
from pyzbar.pyzbar import decode

# 1. Leitura - extrai texto nativo + decodifica o QR de cada página
def scan_barcodes_em_pdf(pdf_path: str, poppler_path: str, dpi: int=300) -> list[dict]:
    '''
    Lê todas as páginas do PDF e devolve, para cada uma, o QRCode decodificado
    junto com o texto nativo (produto, cor, seller_sku, barcode).
    dpi=300 é necessário: em 200 (padrão do pdf2image) parte dos códigos falha.
    '''
    imagens = convert_from_path(pdf_path, poppler_path=poppler_path, dpi=dpi)

    resultado = []
    with pdfplumber.open(pdf_path) as pdf:
        for numero_pagina, (pagina_pdf, imagem) in enumerate(zip(pdf.pages, imagens), start=1):
            registro = _extrair_pagina(pagina_pdf, imagem)
            registro['pagina'] = numero_pagina
            resultado.append(registro)
    return resultado

def _extrair_pagina(pagina_pdfplumber, imagem_pil) -> dict:
    '''Extrai título/cor/SKU/barcode do texto nativo + decodifica o QRCode da mesma página'''
    texto = pagina_pdfplumber.extract_text() or ''
    linhas = [l.strip() for l in texto.split('\n') if l.strip()]

    seller_sku = None
    barcode = None
    whs_skuid = None
    produto_linhas = []

    for linha in linhas:
        m_sku = re.match(r'seller sku:\s*(.+)', linha, re.IGNORECASE)
        m_barcode = re.match(r'barcode:\s*(.+)', linha, re.IGNORECASE)
        m_whs = re.match(r'whs skuid:\s*(.+)', linha, re.IGNORECASE)
        if m_sku:
            seller_sku = m_sku.group(1).strip()
        elif m_barcode:
            barcode = m_barcode.group(1).strip()
        elif m_whs:
            whs_skuid = m_whs.group(1).strip()
        else:
            produto_linhas.append(linha)

    produto_bruto = ' '.join(produto_linhas)

    # separa 'cor/var' do nome
    m_cor = re.search(r'Promoção:\s*(.+)$', produto_bruto, re.IGNORECASE)
    if m_cor:
        cor = m_cor.group(1).strip()
        titulo = produto_bruto[:m_cor.start()].strip()

    else:
        cor = None
        titulo = produto_bruto

    qr_lidos = decode(imagem_pil)
    qr_data = qr_lidos[0].data.decode('utf-8') if qr_lidos else None

    return {
        'seller_sku': seller_sku,
        'titulo': titulo,
        'cor': cor,
        'barcode': barcode,
        'whs_skuid': whs_skuid,
        'qr_data': qr_data,
    }
