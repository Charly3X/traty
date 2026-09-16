#!/usr/bin/env python3
"""Складывает content/en.json: строки из разбора плюс числа в евро.

Суммы — тот же демо-набор, что и на снимках, пересчитанный курсом 0,25
(злотый → евро). Цена за единицу округляется до цента, итог позиции считается
уже от округлённой цены: иначе строка чека не сходилась бы с собственным
умножением.
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / 'content'

RATE = .25


def eur(pln):
    return round(pln * RATE + 1e-9, 2)


def fmt(value):
    # Без разделителя разрядов: так же, как в приложении на снимках.
    return f'{value:.2f}'


# (наименование, количество, цена за единицу в злотых, единица)
ITEMS = [
    ('Chicken thighs', 2, 18.90, 'kg', 1),
    ('Potatoes', 5, 3.49, 'kg', 2),
    ('Milk 2%, 1 l', 6, 4.99, 'l', 0),
    ('Rice, 1 kg', 2, 8.99, 'pcs', 3),
    ('Frozen berries', 2, 14.90, 'pcs', 4),
    ('Juice, 1 l', 4, 7.49, 'pcs', 5),
    ('Cake', 1, 32.90, 'pcs', 1),
]
NOTES = ['Meat', 'Produce', 'Dairy', 'Pantry', 'Frozen', 'Drinks', 'Sweets']

CATEGORIES = [
    ('Rent & bills', '55%', 1450.00),
    ('Fuel', '9%', 246.62),
    ('Services', '6%', 165.00),
    ('Clothing', '5%', 142.90),
    ('Fares', '4%', 110.00),
    ('Other · 11 categories', '20%', 525.88),
]

OVERRIDES = {
    'price.p': 'The same milk, the same shop, a few cents dearer than last month. Nobody catches that from memory. Traty keeps every price you have paid for a product and says plainly when the new one is higher.',
    'faq.a3': 'Typing receipts in by hand, editing them, your whole history, categories, breakdowns, price history and the home-screen widget are free and unlimited, for as long as you use the app. Only reading a photograph costs money per receipt, so the free tier includes five readings, and a subscription is $4.99 a month after that.',
    'dash.chartalt': 'Running total for September is 21 percent below the same days of August',
    'plan.f1b': ' from a photo',
}


def main():
    strings = json.loads((CONTENT / '_extracted.en.json').read_text())
    strings.update(OVERRIDES)

    paper_rows, sorted_rows, total = [], [], 0.0
    for i, (name, qty, unit_pln, unit, slot) in enumerate(ITEMS):
        unit_eur = eur(unit_pln)
        line = round(qty * unit_eur, 2)
        total += line
        sub = '' if qty == 1 else f'{qty} {unit} × {fmt(unit_eur)}'
        paper_rows.append([name, sub, fmt(line)])
        qty_note = f'{qty} {unit}' if qty > 1 else '1 pc'
        sorted_rows.append([name, f'{NOTES[i]} · {qty_note}', fmt(line), slot])

    data = {
        'currency': 'EUR',
        'decimal': '.',
        'month': 'September',
        'prevMonth': 'August',
        'totalRaw': f'{eur(2640.40):.2f}',
        'receipts': '10 receipts',
        'avg': fmt(eur(264.04)),
        'perDay': fmt(eur(240.03)),
        'saved': fmt(eur(13.00)),
        'savedLine': f'Saved on discounts {fmt(eur(13.00))} EUR',
        'categories': [[name, pct, fmt(eur(amount))] for name, pct, amount in CATEGORIES],
        'paper': {
            'shop': 'GROSIK',
            'meta': 'ul. Kwiatowa 12 · 09.09.2026 · 11:20',
            'rows': paper_rows,
            'total': ['TOTAL EUR', fmt(round(total, 2))],
        },
        'sorted': sorted_rows,
        'price': {
            'shop': 'Grosik',
            'item': 'Milk 2%, 1 l',
            'raw': f'{eur(4.99):.2f}',
            'unit': 'EUR per litre',
            'rise': '12% more than 02.08.2026',
            'alt': 'The price held at 1.12 four times and then rose to 1.25',
            'rows': [['09.09.2026', 'top', fmt(eur(4.99))],
                     ['02.09.2026', 'low', fmt(eur(4.49))],
                     ['30.08.2026', 'low', fmt(eur(4.49))],
                     ['09.08.2026', 'low', fmt(eur(4.49))],
                     ['02.08.2026', 'low', fmt(eur(4.49))]],
        },
        'family': {
            'members': [['Alex', 0], ['Marta', 0], ['Kasia', 2], ['Piotr', 4], ['Jan', 1]],
            'used': '63 of 100',
            'share': [['22%', 0], ['16%', 0], ['11%', 2], ['8%', 4], ['6%', 1]],
        },
        # Цена подписки — долларовая для всех рынков (решение владельца,
        # 16.09.2026); демо-суммы в евро её не касаются.
        'plan': {'zero': '$0', 'plus': '$4.99', 'fiveTimes': '$24.95',
                 'currency': 'USD', 'plusAmount': '4.99'},
    }

    out = {
        'lang': 'en',
        'ogLocale': 'en_US',
        'assets': '/assets/en',
        'play': 'https://play.google.com/store/apps/details?id=dev.charoian.traty',
        'privacyUrl': 'https://scancheck-617d3.web.app/privacy.html',
        'deleteUrl': 'https://scancheck-617d3.web.app/delete-account.html',
        'strings': strings,
        'data': data,
    }
    (CONTENT / 'en.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print('записано content/en.json, строк:', len(strings))
    print('итог чека:', data['paper']['total'], '| месяц:', data['totalRaw'])


if __name__ == '__main__':
    main()
