"""Search local gallery metadata; write an attributed contact sheet. No network."""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import re
from PIL import Image, ImageDraw, ImageFont


def tokens(text):
    return re.findall(r'[a-z0-9]+', text.lower())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--gallery', type=Path, required=True)
    parser.add_argument('--query', required=True)
    parser.add_argument('--pattern', choices=['architecture', 'framework', 'pipeline', 'conceptual', 'teaser', 'taxonomy'])
    parser.add_argument('--venue', help='Comma-separated venue names, e.g. iclr,neurips,cvpr')
    parser.add_argument('--limit', type=int, default=12)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if not 1 <= args.limit <= 30:
        parser.error('--limit must be between 1 and 30')
    root = args.gallery.resolve()
    raw = json.loads((root / 'data/figures.json').read_text(encoding='utf-8-sig'))
    figures = raw if isinstance(raw, list) else raw['figures']
    docs = [Counter(tokens(f.get('title', '') + ' ' + ' '.join(f.get('authors', [])) + ' ' + f.get('pattern', ''))) for f in figures]
    avg = sum(sum(doc.values()) for doc in docs) / max(1, len(docs))
    query = set(tokens(args.query))
    frequency = {word: sum(word in doc for doc in docs) for word in query}
    venues = set(args.venue.lower().split(',')) if args.venue else None
    ranked = []
    for figure, doc in zip(figures, docs):
        if args.pattern and figure.get('pattern') != args.pattern:
            continue
        if venues and figure.get('venue') not in venues:
            continue
        score = 0.0
        for word in query:
            tf = doc.get(word, 0)
            idf = math.log(1 + (len(docs) - frequency[word] + .5) / (frequency[word] + .5))
            score += idf * tf * 2.2 / (tf + 1.2 * (.25 + .75 * sum(doc.values()) / avg)) if tf else 0
        ranked.append((score, figure))
    ranked.sort(key=lambda pair: (-pair[0], pair[1]['id']))
    args.output.mkdir(parents=True, exist_ok=True)
    results = []
    for score, figure in ranked[:args.limit]:
        item = {**figure, 'retrieval_score': round(score, 4), 'absolute_image': str(root / figure['image'])}
        results.append(item)
    if not results:
        raise SystemExit('No references match these filters. Broaden the pattern or venue filter.')
    cell_w, cell_h = 520, 340
    columns = min(3, len(results))
    canvas = Image.new('RGB', (columns * cell_w, math.ceil(len(results) / columns) * cell_h), 'white')
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype('arial.ttf', 15) if Path('C:/Windows/Fonts/arial.ttf').exists() else ImageFont.load_default()
    for index, figure in enumerate(results):
        x, y = (index % columns) * cell_w, (index // columns) * cell_h
        with Image.open(figure['absolute_image']) as original:
            thumb = original.convert('RGB')
            thumb.thumbnail((cell_w - 24, 258))
            canvas.paste(thumb, (x + (cell_w - thumb.width) // 2, y + 8 + (258 - thumb.height) // 2))
        draw.rectangle((x, y, x + cell_w - 1, y + cell_h - 1), outline='#DCE1E8')
        label = f'{index + 1}. {figure["id"]} | {figure.get("pattern", "")}'
        while len(label) > 12 and font.getlength(label) > cell_w - 24:
            label = label[:-4] + '...'
        draw.text((x + 12, y + 273), label, fill='#182337', font=font)
        title = figure['title']
        lines = []
        while title and len(lines) < 2:
            cutoff = min(len(title), 65)
            if len(title) > cutoff:
                cutoff = max(title.rfind(' ', 0, cutoff), 25)
            lines.append(title[:cutoff])
            title = title[cutoff:].strip()
        for line_no, line in enumerate(lines):
            draw.text((x + 12, y + 295 + 19 * line_no), line, fill='#4C596B', font=font)
    canvas.save(args.output / 'reference-contact-sheet.png')
    (args.output / 'references.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'matches': len(results), 'contact_sheet': str((args.output / 'reference-contact-sheet.png').resolve()), 'metadata': str((args.output / 'references.json').resolve())}, ensure_ascii=False))


if __name__ == '__main__':
    main()
