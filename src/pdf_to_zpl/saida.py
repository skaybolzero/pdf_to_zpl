from pathlib import Path

def limpar_pasta_saida(pasta_saida: str) -> None:
    '''Remove os .zpl de execuções anteriores'''
    pasta = Path(pasta_saida)
    if pasta.exists():
        for arquivo in pasta.glob('*.zpl'):
            arquivo.unlink()

def salvar_zpls(arquivos: dict[str, str], pasta_saida:str) -> None:
    pasta = Path(pasta_saida)
    pasta.mkdir(parents=True, exist_ok=True)
    for sku, conteudo in arquivos.items():
        caminho = pasta / f'seller_sku_{sku}.zpl'
        caminho.write_text(conteudo, encoding='utf-8')
        print(f'Gravado: {caminho}')
