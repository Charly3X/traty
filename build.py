#!/usr/bin/env python3
"""Собирает лендинг на трёх языках из одного шаблона.

Зачем сборка, а не три готовых файла: правка текста или числа иначе делалась бы
трижды и однажды разошлась бы. Шаблон — `template.html`, содержимое —
`content/<язык>.json`, картинки — `assets/<язык>/`.

Валюта в макетах совпадает с языком: английская страница показывает евро,
польская — злотые, украинская — гривны. Числа берутся из того же демо-набора,
что и снимки экранов (`scripts/demo_locales.py`), иначе страница показывала бы
одни суммы в вёрстке и другие на снимке.

Запуск:
    python3 landing/build.py            # собрать всё
    python3 landing/build.py --check    # только проверить, что плейсхолдеры закрыты
"""

import argparse
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
TEMPLATE = ROOT / 'template.html'
CONTENT = ROOT / 'content'

#: Язык по умолчанию лежит в корне, остальные — в своих каталогах. Состав
#: языков и корневой язык задаются в `content/site.json`: английскую версию
#: нельзя выкладывать, пока её снимки экрана в злотых, а не в евро.
DEFAULT = 'en'
LANGS = ['en', 'pl', 'uk']
BASE = ''          # префикс пути, если страница живёт не в корне домена
LANG_NAMES = {'en': 'EN', 'pl': 'PL', 'uk': 'UA'}

#: Шрифты — свойство языка, а не содержимого: у Bricolage Grotesque и Courier
#: Prime нет кириллицы, и украинская страница без подмены уезжает в засечки
#: системного запасного шрифта.
FONTS = {
    'latin': {
        'fonts': 'https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Manrope:wght@400;500;600;700&family=Courier+Prime:wght@400;700&display=swap',
        'fontDisplay': '"Bricolage Grotesque",Georgia,serif',
        'fontMono': '"Courier Prime",ui-monospace,SFMono-Regular,monospace',
        'fontTweak': '',
    },
    'cyrillic': {
        'fonts': 'https://fonts.googleapis.com/css2?family=Unbounded:wght@500;700;800&family=Manrope:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap',
        'fontDisplay': '"Unbounded","Manrope",sans-serif',
        'fontMono': '"IBM Plex Mono",ui-monospace,SFMono-Regular,monospace',
        # Unbounded заметно шире Bricolage, а украинские слова длиннее
        # английских: на прежних кеглях заголовок не помещался в 375 px.
        'fontTweak': '''/* ── кегли под Unbounded ──────────────────────────────────────────────── */
h1{font-size:clamp(2.05rem,6.4vw,5rem);letter-spacing:-.045em}
h2{font-size:clamp(1.75rem,3.9vw,3rem);letter-spacing:-.04em}
h3{font-size:clamp(1.12rem,1.8vw,1.4rem)}
.big{font-size:clamp(1.9rem,4vw,2.7rem)}
.plan .price{font-size:clamp(1.9rem,3.4vw,2.5rem)}
.band .v{font-size:clamp(1.6rem,2.9vw,2.3rem)}
.vs .m{font-size:1.4rem}
details summary{font-size:1.02rem}''',
    },
}
SCRIPT = {'en': 'latin', 'pl': 'latin', 'uk': 'cyrillic'}

#: Цвета категорий — те же шестнадцать слотов, что в приложении
#: (`lib/theme/app_colors.dart`), поэтому названы номерами слотов страницы.
COLORS = ['var(--c1)', 'var(--c2)', 'var(--c3)', 'var(--c4)', 'var(--c5)', 'var(--c6)']


def esc(text):
    return html.escape(str(text), quote=True)


# ── блоки ────────────────────────────────────────────────────────────────

def block_head(c, site):
    d, s = c['data'], c['strings']
    base = site.rstrip('/')
    url = base + ('' if c['lang'] == DEFAULT else '/' + c['lang'] + '/')
    if c['lang'] == DEFAULT:
        url += '/'
    alts = '\n'.join(
        '<link rel="alternate" hreflang="%s" href="%s">' % (
            l, base + ('/' if l == DEFAULT else '/%s/' % l))
        for l in LANGS)
    og = base + c['assets'].rstrip('/') + '/og.jpg'
    faq = [{'@type': 'Question', 'name': s['faq.q%d' % i],
            'acceptedAnswer': {'@type': 'Answer', 'text': s['faq.a%d' % i]}}
           for i in range(1, 8)]
    ld = {
        '@context': 'https://schema.org',
        '@graph': [
            {
                '@type': 'SoftwareApplication',
                'name': 'Traty',
                'applicationCategory': 'FinanceApplication',
                'operatingSystem': 'Android',
                'description': s['meta.description'],
                'url': url,
                'installUrl': c['play'],
                'image': og,
                'inLanguage': ['en', 'pl', 'uk', 'ru'],
                'author': {'@type': 'Person', 'name': 'Oleksii Charoian',
                           'email': 'oleksii.charoian@gmail.com'},
                'offers': [
                    {'@type': 'Offer', 'name': s['plan.free'], 'price': '0',
                     'priceCurrency': d['plan']['currency']},
                    {'@type': 'Offer', 'name': s['plan.plus'],
                     'price': d['plan']['plusAmount'],
                     'priceCurrency': d['plan']['currency']},
                ],
            },
            {'@type': 'FAQPage', 'mainEntity': faq},
        ],
    }
    return '''<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
{alts}
<link rel="alternate" hreflang="x-default" href="{base}/">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#0B0B0B">
<meta name="author" content="Oleksii Charoian">
<meta name="keywords" content="{kw}">

<meta property="og:type" content="website">
<meta property="og:site_name" content="Traty">
<meta property="og:title" content="{ogt}">
<meta property="og:description" content="{ogd}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{oglocale}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{ogt}">
<meta name="twitter:description" content="{twd}">
<meta name="twitter:image" content="{og}">

<script type="application/ld+json">
{ld}
</script>

'''.format(title=esc(s['meta.title']), desc=esc(s['meta.description']),
           kw=esc(s['meta.keywords']), url=url, alts=alts, base=base, og=og,
           ogt=esc(s['og.title']), ogd=esc(s['og.description']),
           twd=esc(s['tw.description']), oglocale=c['ogLocale'],
           ld=json.dumps(ld, ensure_ascii=False, indent=2))


def block_langs(c, site):
    out = ['    <div class="langs" role="navigation" aria-label="Language">']
    for l in LANGS:
        href = (BASE + '/') if l == DEFAULT else '%s/%s/' % (BASE, l)
        cls = ' class="on"' if l == c['lang'] else ''
        out.append('      <a href="%s" hreflang="%s"%s>%s</a>' % (href, l, cls, LANG_NAMES[l]))
    out.append('    </div>')
    return '\n'.join(out)


def block_paper(c):
    p = c['data']['paper']
    out = ['<div class="shop">%s</div>' % esc(p['shop']),
           '        <div class="meta">%s</div>' % esc(p['meta']),
           '        <hr>']
    for name, sub, amount in p['rows']:
        out.append('        <div class="p-row"><span>%s</span><span>%s</span></div>'
                   % (esc(name), esc(amount)))
        if sub:
            out.append('        <div class="p-sub">%s</div>' % esc(sub))
    out += ['        <hr>',
            '        <div class="p-total"><span>%s</span><span>%s</span></div>'
            % (esc(p['total'][0]), esc(p['total'][1]))]
    return '\n'.join(out)


def block_sorted(c):
    out = []
    for i, (name, note, amount, slot) in enumerate(c['data']['sorted']):
        out.append(
            '<div class="s-row" style="--d:%.2fs"><i class="dot" style="background:%s"></i>'
            '<b>%s<em>%s</em></b><span class="amt">%s</span></div>'
            % (.5 + i * .35, COLORS[slot], esc(name), esc(note), esc(amount)))
    return ('\n' + ' ' * 8).join(out)


def block_dash(c):
    d, s = c['data'], c['strings']
    bar = ''.join('<i style="--w:%s;background:%s"></i>' % (pct, COLORS[i])
                  for i, (_, pct, _) in enumerate(d['categories']))
    rows = '\n'.join(
        '        <div class="row"><i class="dot" style="background:%s"></i><span>%s</span>'
        '<span class="pc">%s</span><span class="am tabular">%s</span></div>'
        % (COLORS[i], esc(name), pct, esc(amount))
        for i, (name, pct, amount) in enumerate(d['categories']))
    return '''<div class="card rv" data-d="2" id="dash" style="position:relative">
      <span class="tag">{demo}</span>
      <p class="k">{month}</p>
      <p class="big tabular"><span data-count="{totalraw}">0</span><small>{cur}</small></p>
      <p class="muted" style="font-size:.92rem">{receipts}</p>

      <div class="chartbox">
        <p class="k" style="margin-bottom:.5rem">{since}</p>
        <svg viewBox="0 0 620 190" role="img" aria-label="{chartalt}">
          <defs>
            <linearGradient id="fill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0" stop-color="#F97316" stop-opacity=".38"/>
              <stop offset="1" stop-color="#F97316" stop-opacity="0"/>
            </linearGradient>
          </defs>
          <line x1="0" y1="176" x2="620" y2="176" stroke="rgba(255,255,255,.12)"/>
          <path class="area" d="M6,172 L58,166 L110,160 L162,152 L214,146 L266,132 L318,116 L318,176 L6,176 Z" fill="url(#fill)" opacity="0"/>
          <path class="draw dash" d="M6,168 L58,158 L110,150 L162,140 L214,128 L266,116 L318,74 L370,58 L422,46 L474,34 L526,26 L578,20"
                fill="none" stroke="#7A7974" stroke-width="2" stroke-dasharray="1 7" stroke-linecap="round"/>
          <path class="draw solid" d="M6,172 L58,166 L110,160 L162,152 L214,146 L266,132 L318,116"
                fill="none" stroke="#F97316" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
          <circle class="pt" cx="318" cy="116" r="5.5" fill="#F97316" opacity="0"/>
        </svg>
        <div class="legend">
          <span style="color:#F97316"><i></i><span style="color:var(--ink-2)">{month}</span></span>
          <span class="pill">↘ −21%</span>
          <span style="color:#7A7974"><i style="border-top-style:dotted;border-top-width:3px"></i><span style="color:var(--ink-2)">{prev}</span></span>
        </div>
      </div>

      <div class="statrow">
        <div><p class="k">{avgl}</p><p class="v tabular">{avg}</p></div>
        <div><p class="k">{perdayl}</p><p class="v tabular">{perday}</p></div>
        <div><p class="k">{savedl}</p><p class="v tabular">{saved}</p></div>
      </div>

      <div class="bar" role="img" aria-label="{baralt}">{bar}</div>

      <div class="brk">
{rows}
      </div>
      <p class="saved">{savedline}</p>
    </div>'''.format(
        demo=esc(s['dash.demo']), month=esc(d['month']), prev=esc(d['prevMonth']),
        totalraw=d['totalRaw'], cur=esc(d['currency']), receipts=esc(d['receipts']),
        since=esc(s['dash.since']), chartalt=esc(s['dash.chartalt']),
        avgl=esc(s['dash.avg']), avg=esc(d['avg']), perdayl=esc(s['dash.perday']),
        perday=esc(d['perDay']), savedl=esc(s['dash.saved']), saved=esc(d['saved']),
        baralt=esc(s['dash.baralt']), bar=bar, rows=rows,
        savedline=esc(d['savedLine']))


def block_price(c):
    d, s = c['data'], c['strings']
    p = d['price']
    rows = '\n'.join(
        '        <div class="h"><span class="tabular">%s</span><span class="lab">%s</span><b>%s</b></div>'
        % (esc(date), esc(s['price.dearest'] if kind == 'top' else s['price.cheapest']), esc(value))
        for date, kind, value in p['rows'])
    return '''<div class="card rv pricecard" style="position:relative">
      <span class="tag">{demo}</span>
      <p class="k">{shop}</p>
      <div class="row2">
        <div>
          <h3 style="font-family:var(--body);font-weight:600;font-size:1.05rem;margin:.3rem 0 .5rem">{item}</h3>
          <p class="big tabular"><span data-count="{raw}">0</span><small>{unit}</small></p>
          <p class="rise" style="margin-top:.5rem">{rise}</p>
        </div>
        <svg viewBox="0 0 220 90" width="220" height="90" role="img" aria-label="{alt}">
          <path class="draw spark" d="M8,66 L58,66 L108,66 L158,66 L208,24" fill="none" stroke="#FB923C" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
          <circle class="pt" cx="208" cy="24" r="5" fill="#FB923C" opacity="0"/>
        </svg>
      </div>
      <div class="hist">
{rows}
      </div>
    </div>'''.format(demo=esc(s['dash.demo']), shop=esc(p['shop']), item=esc(p['item']),
                     raw=p['raw'], unit=esc(p['unit']), rise=esc(p['rise']),
                     alt=esc(p['alt']), rows=rows)


def block_band(c):
    s = c['strings']
    return '''<div class="band rv">
      <div><p class="v tabular"><span data-count="30">0</span></p><p class="l">{l1}</p></div>
      <div><p class="v tabular"><span data-count="4">0</span></p><p class="l">{l2}</p></div>
      <div><p class="v">0</p><p class="l">{l3}</p></div>
      <div><p class="v">∞</p><p class="l">{l4}</p></div>
    </div>'''.format(l1=esc(s['band.l1']), l2=esc(s['band.l2']),
                     l3=esc(s['band.l3']), l4=esc(s['band.l4']))


def block_fam(c):
    d, s = c['data'], c['strings']
    f = d['family']
    who = '\n'.join(
        '        <span class="who"><i style="background:%s">%s</i>%s%s</span>'
        % (COLORS[slot] if i else 'var(--accent)', esc(name[0]), esc(name),
           '<span class="tiny">%s</span>' % esc(s['fam.owner']) if i == 0 else '')
        for i, (name, slot) in enumerate(f['members']))
    track = ''.join('<i style="--w:%s;background:%s"></i>'
                    % (w, 'var(--accent)' if i == 0 else COLORS[slot])
                    for i, (w, slot) in enumerate(f['share']))
    return '''<div class="card rv" data-d="2">
      <span class="sub">{plus} · <b>{price}</b>{per}</span>
      <p class="k" style="margin-top:1.4rem">{card}</p>
      <div class="members">
{who}
      </div>

      <div class="pool">
        <div class="line"><span>{poolline}</span><span class="tabular">{used}</span></div>
        <div class="track" role="img" aria-label="{poolalt}">{track}</div>
        <p class="foot">{poolfoot}</p>
      </div>

      <div class="vs">
        <div><p class="t">{vs1}</p><p class="m strike">{five}</p></div>
        <div><p class="t">{vs2}</p><p class="m">{price}</p></div>
      </div>
    </div>'''.format(plus=esc(s['plan.plus']), price=esc(d['plan']['plus']),
                     per=esc(s['plan.month']), card=esc(s['fam.card']), who=who,
                     poolline=esc(s['fam.poolline']), used=esc(f['used']),
                     poolalt=esc(s['fam.poolalt']), track=track,
                     poolfoot=esc(s['fam.poolfoot']), vs1=esc(s['fam.vs1']),
                     vs2=esc(s['fam.vs2']), five=esc(d['plan']['fiveTimes']))


def _tick(text, bold=None):
    inner = ('<b>%s</b>%s' % (esc(bold), esc(text))) if bold else esc(text)
    return ('          <li><svg viewBox="0 0 24 24" aria-hidden="true">'
            '<path d="M4 12.5l5 5L20 6.5"/></svg><span>%s</span></li>' % inner)


def block_plans(c):
    d, s = c['data'], c['strings']
    free = '\n'.join([_tick(s['plan.f1b'], s['plan.f1a']), _tick(s['plan.f2']),
                      _tick(s['plan.f3']), _tick(s['plan.f4']), _tick(s['plan.f5'])])
    plus = '\n'.join([_tick('', s['plan.p1']), _tick(s['plan.p2']), _tick(s['plan.p3']),
                      _tick(s['plan.p4']), _tick(s['plan.p5'])])
    return '''<div class="plans">
      <div class="card plan free rv" data-d="1">
        <p class="k">{freen}</p>
        <p class="price">{zero}<span>{forever}</span></p>
        <p class="muted" style="font-size:.95rem">{freesub}</p>
        <ul>
{free}
        </ul>
        <a class="btn btn-ghost" href="{{{{play}}}}" rel="noopener">{freecta}</a>
      </div>

      <div class="card plan hot rv" data-d="2">
        <p class="k" style="color:var(--accent-2)">{plusn}</p>
        <p class="price">{plusp}<span>{month}</span></p>
        <p class="muted" style="font-size:.95rem">{plussub}</p>
        <ul>
{plus}
        </ul>
        <a class="btn btn-primary" href="{{{{play}}}}" rel="noopener">{pluscta}</a>
      </div>
    </div>'''.format(freen=esc(s['plan.free']), zero=esc(d['plan']['zero']),
                     forever=esc(s['plan.forever']), freesub=esc(s['plan.freesub']),
                     free=free, freecta=esc(s['plan.freecta']),
                     plusn=esc(s['plan.plus']), plusp=esc(d['plan']['plus']),
                     month=esc(s['plan.month']), plussub=esc(s['plan.plussub']),
                     plus=plus, pluscta=esc(s['plan.pluscta']))


def block_footlinks(c):
    s = c['strings']
    return ('<nav class="right">\n'
            '      <a href="%s">%s</a>\n'
            '      <a href="%s">%s</a>\n'
            '      <a href="mailto:oleksii.charoian@gmail.com">oleksii.charoian@gmail.com</a>\n'
            '    </nav>' % (c['privacyUrl'], esc(s['foot.privacy']),
                            c['deleteUrl'], esc(s['foot.delete'])))


# ── сборка ───────────────────────────────────────────────────────────────

def render(c, site):
    page = TEMPLATE.read_text()
    blocks = {
        '{{@head}}': block_head(c, site),
        '{{@langs}}': block_langs(c, site),
        '{{@paper}}': block_paper(c),
        '{{@sorted}}': block_sorted(c),
        '{{@dash}}': block_dash(c),
        '{{@price}}': block_price(c),
        '{{@band}}': block_band(c),
        '{{@fam}}': block_fam(c),
        '{{@plans}}': block_plans(c),
        '{{@footlinks}}': block_footlinks(c),
    }
    for marker, value in blocks.items():
        if marker not in page:
            sys.exit('в шаблоне нет маркера %s' % marker)
        page = page.replace(marker, value)

    page = page.replace('{{lang}}', c['lang'])
    page = page.replace('{{decimal}}', c['data']['decimal'])
    fonts = FONTS[SCRIPT[c['lang']]]
    for key, value in fonts.items():
        page = page.replace('{{%s}}' % key, value)
    page = page.replace('{{assets}}', BASE + c['assets'])
    page = page.replace('{{base}}', BASE)
    page = page.replace('{{play}}', c['play'])
    for key, value in c['strings'].items():
        page = page.replace('{{%s}}' % key, value)

    left = re.findall(r'\{\{[^}]{1,40}\}\}', page)
    if left:
        sys.exit('незакрытые плейсхолдеры в %s: %s' % (c['lang'], sorted(set(left))))
    return page


def sitemap(site):
    base = site.rstrip('/')
    urls = '\n'.join(
        '  <url>\n    <loc>%s</loc>\n    <changefreq>monthly</changefreq>\n'
        '    <priority>%s</priority>\n  </url>'
        % (base + ('/' if l == DEFAULT else '/%s/' % l), '1.0' if l == DEFAULT else '0.9')
        for l in LANGS)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            '%s\n</urlset>\n' % urls)


def main():
    global DEFAULT, LANGS, BASE
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='только проверить сборку')
    args = ap.parse_args()

    conf = json.loads((CONTENT / 'site.json').read_text())
    site = conf['site']
    LANGS = conf.get('langs', LANGS)
    DEFAULT = conf.get('default', LANGS[0])
    BASE = conf.get('base', '').rstrip('/')
    for lang in LANGS:
        c = json.loads((CONTENT / ('%s.json' % lang)).read_text())
        page = render(c, site)
        if args.check:
            print('%s: ок, %d символов' % (lang, len(page)))
            continue
        target = ROOT / 'index.html' if lang == DEFAULT else ROOT / lang / 'index.html'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page)
        print('собрано: %s' % target.relative_to(ROOT))
    if not args.check:
        (ROOT / 'sitemap.xml').write_text(sitemap(site))
        (ROOT / 'robots.txt').write_text(
            'User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n' % site.rstrip('/'))
        print('собрано: sitemap.xml, robots.txt')


if __name__ == '__main__':
    main()
