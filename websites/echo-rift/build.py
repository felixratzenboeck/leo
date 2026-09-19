"""Build the self-contained offline HTML using only Python's standard library."""
from pathlib import Path
import argparse

ROOT = Path(__file__).resolve().parent

def build(destination: Path) -> None:
    source = ROOT / 'public'
    html = (source / 'index.html').read_text(encoding='utf-8')
    css = (source / 'style.css').read_text(encoding='utf-8')
    html = html.replace('<link rel="stylesheet" href="style.css">', '<style>\n' + css + '\n</style>')
    for name in ('engine', 'render', 'network', 'app'):
        js = (source / f'{name}.js').read_text(encoding='utf-8')
        if '</script' in js.lower():
            raise ValueError(f'Unsafe inline script closing sequence in {name}.js')
        html = html.replace(f'<script src="{name}.js"></script>', f'<script>\n{js}\n</script>')
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(html, encoding='utf-8')
    print(f'{destination}: {destination.stat().st_size:,} bytes')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT / 'ECHO-RIFT.html')
    build(parser.parse_args().output)
