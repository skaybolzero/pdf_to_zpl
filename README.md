# pdf-to-zpl

Pipeline em Python que lê PDFs de etiquetas de estoque/armazém exportados pela Shopee (QR Code + texto), agrupa por SKU e gera arquivos ZPL prontos para impressão térmica em lote.

## Contexto

Vendedores da Shopee que usam fulfillment recebem, para cada lote de produtos, um PDF com uma etiqueta por unidade física de estoque — cada página traz um QR Code, o nome/variação do produto e o SKU do vendedor. Um mesmo SKU aparece repetido em várias páginas (uma por unidade).

Este projeto lê esse PDF, identifica quantas unidades existem de cada SKU (contando as páginas repetidas) e gera **um arquivo `.zpl` por SKU**, já com o comando `^PQ<quantidade>` — a própria impressora térmica repete a etiqueta a quantidade certa de vezes, sem precisar duplicar o código no arquivo.

## Estrutura

```
pdf_to_zpl/
├── pyproject.toml
├── README.md
├── .gitignore
├── instalar.bat             # setup automatizado (venv + instalação)
├── executar.bat             # arraste um PDF aqui para gerar os ZPLs
├── abrir_projeto_zpl.bat    # caso o usuário queira abrir o vscode
└── src/
    └── pdf_to_zpl/
        ├── __init__.py
        ├── leitura.py       # extrai texto + decodifica QR de cada página
        ├── agrupamento.py   # agrupa registros por SKU
        ├── zpl.py           # monta o ZPL de cada etiqueta
        ├── saida.py         # limpa a pasta de saída e grava os .zpl
        └── cli.py           # ponto de entrada (linha de comando)
```

## Instalação

### Opção 1 — automatizada (recomendada para quem não usa terminal no dia a dia)

Dê 2 cliques em `instalar.bat`. Ele cria o ambiente virtual e instala tudo sozinho.

### Opção 2 — manual

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -e .
```

### Poppler (dependência externa, não vem via pip)

O `pdf2image` depende do Poppler instalado à parte no sistema.

- **Windows**: baixe em [poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases/), extraia em um caminho fixo (ex: `C:\poppler`).
- **Linux**: `sudo apt install poppler-utils`
- **Mac**: `brew install poppler`

Se for usar o `executar.bat`, edite a linha do `--poppler-path` nele para apontar para onde você extraiu o Poppler.

## Uso

### Modo simples (drag-and-drop)

Arraste o PDF de etiquetas para cima do ícone `executar.bat`. Os `.zpl` aparecem na pasta `saida_zpl`.

### Modo linha de comando

```bash
pdf-to-zpl caminho/para/etiquetas.pdf --saida saida_zpl --poppler-path "C:\poppler\Library\bin"
```

Argumentos:
- `pdf` (obrigatório) — caminho do PDF de origem.
- `--saida` — pasta onde os `.zpl` serão gravados (padrão: `./saida_zpl`; limpa arquivos `.zpl` de execuções anteriores antes de gravar os novos).
- `--poppler-path` — pasta `bin` do Poppler.
- `--dpi` — resolução usada na leitura do PDF (padrão: 300; abaixo disso o QR pode falhar na decodificação).

Saída esperada:

```
Total de páginas lidas: 48
Resumo por SKU:
  SKU 2415 | qtd=12 | cor=Bege | Toalha Banho Dual Air Buddemeyer...
Gravado: saida_zpl/seller_sku_2415.zpl
```

Cada `.zpl` pode ser enviado direto para uma impressora Zebra (ou compatível), ou visualizado antes em [labelary.com/viewer.html](http://labelary.com/viewer.html).

## Notas técnicas

- `dpi=300` é necessário na conversão do PDF para imagem — em 200 (padrão do `pdf2image`) uma parte relevante dos QR Codes falha na decodificação.
- O parser assume o texto no formato `Promoção:<cor>` para separar produto de variação/cor — ajuste a regex em `leitura.py` se o formato do seu PDF for diferente.
- O layout do ZPL (`zpl.py`) foi calibrado para uma etiqueta de `480x320` dots — ajuste `^PW`/`^LL` se sua impressora usar outro tamanho.
- Requer Python 3.10+.

## Privacidade

O `.gitignore` já exclui `*.pdf` e pastas de saída por padrão — não versione PDFs reais de pedidos/clientes.

## Créditos

Boa parte do código deste projeto foi desenvolvida com apoio de IA (Claude, Anthropic), a partir de um caso real de automação de etiquetas de fulfillment.
