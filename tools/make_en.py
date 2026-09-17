#!/usr/bin/env python3
"""Складывает content/en.json: строки из разбора плюс числа со снимков.

Числа не вычисляются заново, а списаны с экранов, снятых на эмуляторе
17.09.2026 (`store/raw/phone/en/`): рядом с макетом на странице стоит тот же
снимок, и расхождение в цент читалось бы как подделка. Приложение печатает
дробную часть через запятую в любом языке (`formatFixedPoint`), поэтому
запятая и здесь.
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / 'content'

# Чек 09.09 из демо-набора: наименование, количество, единица, цена за единицу,
# сумма, категория (как её прочитала модель), слот цвета.
PAPER = [
    ('Chicken thighs', '2 kg', '4,72', '9,44', 'Meat', 1),
    ('Potatoes', '5 kg', '0,87', '4,35', 'Produce', 2),
    ('Milk 2%, 1 l', '6 l', '1,25', '7,50', 'Dairy', 0),
    ('Rice, 1 kg', '2 pcs', '2,25', '4,50', 'Pantry', 3),
    ('Frozen berries', '2 pcs', '3,72', '7,44', 'Produce', 4),
    ('Juice, 1 l', '4 pcs', '1,87', '7,48', 'Drinks', 5),
    ('Cake', '1 pcs', '8,22', '8,22', 'Bakery', 1),
    ('Weekend discount', '1 pcs', '-2,25', '-2,25', 'Discount', 5),
]

# Разбивка месяца — с экрана «Главной», режим «All categories».
CATEGORIES = [
    ('Rent & bills', '40%', '362,50'),
    ('Electronics', '8%', '74,49'),
    ('Car', '7%', '62,00'),
    ('Fuel', '7%', '61,56'),
    ('Health', '5%', '45,00'),
    ('Other · 17 categories', '33%', '292,56'),
]

OVERRIDES = {
    # Заголовок выдачи: ключевое слово впереди, бренд в конце — Traty никто не
    # ищет по имени, а обрезается заголовок примерно на шестидесяти знаках.
    'meta.title': 'Receipt scanner that sorts spending by category — Traty',
    'meta.description': 'Photograph a paper receipt: Traty reads every line — name, price, quantity, category — and shows where your month goes. Free to start on Android.',
    'hero.lede': 'Every line read, priced and filed into a category — name, quantity, price, the lot. A month of paper turns into an expense tracker that fills itself in.',
    'month.eyebrow': 'Spending by category',
    'widget.eyebrow': 'Home-screen widget',
    # Не «у каждой свой цвет»: цветов шестнадцать на тридцать категорий, слоты
    # повторяются между группами, редкие берут нейтральный (`app_colors.dart`).
    'band.l1': 'categories it sorts your items into',
    # Замерено на съёмке 17.09.2026: от снимка до разобранного списка около
    # двадцати пяти секунд, а не десять.
    'how.eyebrow': 'Three steps, about half a minute',
    'how.s1p': 'Crumpled, faded, absurdly long — point and shoot. Long receipts are cut into strips and read piece by piece, and that still counts as one reading.',
    # Виджет следует теме приложения, а не системы (`WidgetTheme.app`).
    'widget.li3': 'Follows the app’s light or dark look',
    # Без утверждений о чужих приложениях: проверить их мы не можем.
    'fam.p': 'One subscription, not five. A subscriber opens a household and invites up to four people, and joining is free even if they have never paid for anything.',
    'month.p': 'A pile of receipts tells you nothing; a shape tells you everything. Traty draws this month against the same days of the last one, so overspending shows up in the first week instead of on the 30th.',
    'plan.f5': 'Join someone else’s household',
    'fam.li2': 'One shared allowance of readings, drawn from the subscriber’s plan',
    'price.p': 'The same milk, the same shop, a few cents dearer than last month. Nobody catches that from memory. Traty keeps every price you have paid for a product and says plainly when the new one is higher.',
    'faq.a3': 'Typing receipts in by hand, editing them, your whole history, categories, breakdowns, price history and the home-screen widget are free and unlimited, for as long as you use the app. Only reading a photograph costs money per receipt, so the free tier includes five readings, and a subscription is $4.99 a month after that.',
    'dash.chartalt': 'Running total for September is 11 percent below the same days of August',
    'plan.f1b': ' from a photo',
}


def main():
    strings = json.loads((CONTENT / '_extracted.en.json').read_text())
    strings.update(OVERRIDES)

    paper_rows, sorted_rows = [], []
    for name, qty, unit_price, line, category, slot in PAPER:
        paper_rows.append([name, f'{qty} × {unit_price}', line])
        sorted_rows.append([name, f'{category} · {qty}', line, slot])

    data = {
        'currency': 'EUR',
        'decimal': ',',
        'month': 'September',
        'prevMonth': 'August',
        'totalRaw': '898.11',
        'receipts': '16 receipts',
        'avg': '56,13',
        'perDay': '52,83',
        'saved': '3,25',
        'savedLine': 'Saved on discounts 3,25 EUR',
        'trend': '−11%',
        'categories': [list(c) for c in CATEGORIES],
        'paper': {
            'shop': 'HARVEST LANE',
            'meta': '12 Market Street · 09.09.2026 · 11:20',
            'rows': paper_rows,
            'total': ['TOTAL EUR', '46,68'],
        },
        'sorted': sorted_rows,
        'price': {
            'shop': 'Harvest Lane',
            'item': 'Milk 2%, 1 l',
            'raw': '1.25',
            'unit': 'EUR per litre',
            'rise': '12% more than 02.08.2026',
            'alt': 'The price held at 1,12 four times and then rose to 1,25',
            'rows': [['09.09.2026', 'top', '1,25'],
                     ['02.09.2026', 'low', '1,12'],
                     ['30.08.2026', 'low', '1,12'],
                     ['09.08.2026', 'low', '1,12'],
                     ['02.08.2026', 'low', '1,12']],
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
        # referrer доезжает до Play Console: без него не видно, сколько
        # установок пришло со страницы, и воронку нечем мерить.
        'play': 'https://play.google.com/store/apps/details?id=dev.charoian.traty&referrer=utm_source%3Dlanding%26utm_medium%3Dweb%26utm_campaign%3Den',
        'privacyUrl': 'https://scancheck-617d3.web.app/privacy.html',
        'deleteUrl': 'https://scancheck-617d3.web.app/delete-account.html',
        'strings': strings,
        'data': data,
    }
    (CONTENT / 'en.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print('записано content/en.json, строк:', len(strings))


if __name__ == '__main__':
    main()
