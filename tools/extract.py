#!/usr/bin/env python3
"""Одноразовый инструмент: разбирает английскую страницу на шаблон и словарь.

Запускается один раз при заведении многоязычной сборки. Дальше правится
`template.html` и `content/*.json`, а этот файл остаётся как история приёма.

Порядок замен важен: длинные строки идут раньше своих подстрок, иначе внутри
уже подставленного `{{ключ}}` найдётся кусок следующей строки.
"""

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / 'index.html'
TEMPLATE = ROOT / 'template.html'
CONTENT = ROOT / 'content'

# (ключ, точная строка в index.html). Числа и суммы сюда не попадают: они
# приходят из отдельного раздела `data` в json, потому что у каждого языка
# своя валюта.
STRINGS = [
    ('meta.title', 'Traty — snap a receipt, it sorts itself | Receipt scanner for Android'),
    ('meta.description', 'Photograph a paper receipt and Traty reads every line — name, price, quantity, category — then shows where your month actually goes. Free to start on Android. No typing.'),
    ('meta.keywords', 'receipt scanner, receipt app, expense tracker, grocery spending, scan receipt, budget app android, price history, spending by category'),
    ('og.title', 'Snap a receipt. It sorts itself.'),
    ('og.description', 'Traty reads every line of a paper receipt — name, price, quantity, category — and turns a month of shopping into a few numbers you can read at a glance.'),
    ('tw.description', 'Every item priced and sorted. Nothing typed by hand.'),

    ('nav.how', 'How it works'),
    ('nav.month', 'Your month'),
    ('nav.family', 'Family'),
    ('nav.privacy', 'Privacy'),
    ('nav.pricing', 'Pricing'),
    ('nav.faq', 'FAQ'),
    ('nav.cta', 'Get it free'),

    ('hero.eyebrow', 'Receipt scanner for Android'),
    ('hero.h1a', 'Snap a receipt.'),
    ('hero.h1b', 'It sorts itself.'),
    ('hero.lede', 'Every line read, priced and filed into a category — name, quantity, price, the lot. A month of paper becomes a handful of numbers you can actually read.'),
    ('cta.play', 'Get it on Google Play'),
    ('hero.cta2', 'See how it works'),
    ('hero.trust1', 'Free to start'),
    ('hero.trust2', 'Photo never stored'),
    ('hero.trust3', 'No ads'),
    ('scene.title', 'Sorted, in a second'),
    ('scene.cap', 'Read from the photo'),

    ('how.eyebrow', 'Three steps, about ten seconds'),
    ('how.h2', 'You point a camera. That is the whole job.'),
    ('how.lede', 'No app ever made typing a receipt pleasant, so Traty does not ask you to. Photograph it and the list arrives already broken into items — with everything editable if a line came out wrong.'),
    ('how.s1h', 'Photograph it'),
    ('how.s1p', 'Crumpled, faded, absurdly long — point and shoot. Long receipts are cut into strips and read piece by piece, and that still counts as one receipt.'),
    ('how.s1alt', 'Traty camera screen aimed at a paper receipt, with the shutter ready'),
    ('how.s2h', 'It reads every line'),
    ('how.s2p', 'Name, quantity, unit price and a category for each item. The total, the date and the currency are read on the phone itself.'),
    ('how.s2alt', 'Receipt items recognised in Traty: each line with name, quantity, price and category'),
    ('how.s3h', 'The month adds itself up'),
    ('how.s3p', 'Every receipt lands in one picture of the month: total, average, spend per day, and exactly where it all went.'),
    ('how.s3alt', 'Traty dashboard with the month total, spend per day and a breakdown by category'),

    ('month.eyebrow', 'Where the month goes'),
    ('month.h2', 'A month of shopping, in six numbers.'),
    ('month.p', 'A pile of receipts tells you nothing; a shape tells you everything. Traty draws this month against the same days of the last one, so overspending shows up on the 9th instead of on the 30th.'),
    ('month.li1', 'Running total against the same days last month'),
    ('month.li2', 'Average receipt, spend per day, money saved on discounts'),
    ('month.li3', 'Every category keeps its own colour, month after month'),
    ('month.li4', 'Tap a category to see the items inside it'),
    ('dash.demo', 'Demo data'),
    ('dash.since', 'Spent since the 1st'),
    ('dash.chartalt', 'Running total for September is 21 percent below the same days of August'),
    ('dash.avg', 'Average receipt'),
    ('dash.perday', 'Per day'),
    ('dash.saved', 'Saved'),
    ('dash.baralt', 'Share of the month by category'),

    ('price.eyebrow', 'Price history'),
    ('price.h2', 'It notices when a price creeps up.'),
    ('price.p', 'The same milk, the same shop, fifty groszy dearer than last month. Nobody catches that from memory. Traty keeps every price you have paid for a product and says plainly when the new one is higher.'),
    ('price.li1', 'Every purchase of a product, cheapest and dearest marked'),
    ('price.li2', 'Compared per litre or per kilo, not per package'),
    ('price.li3', 'Two different things counted as one product? Split them in a tap'),
    ('price.sparkalt', 'The price held at the old value four times and then rose'),
    ('price.dearest', 'dearest'),
    ('price.cheapest', 'cheapest'),

    ('edit.eyebrow', 'Yours to correct'),
    ('edit.h2', 'Read by a model. Owned by you.'),
    ('edit.p', 'A model misreads a smudged line now and then, and an app that pretends otherwise is worse than one that admits it. Every field stays editable, and the receipt keeps its own arithmetic honest — the moment the lines stop adding up to the printed total, it says so.'),
    ('edit.li1', 'Two taps to fix a price or move an item to another category'),
    ('edit.li2', 'No camera? Type the receipt in by hand — free, always, however many'),
    ('edit.li3', 'Month by month, group by group, down to a single item'),
    ('edit.li4', 'Light and dark, in English, Polish, Ukrainian and Russian'),
    ('edit.alt1', 'A recognised receipt in Traty, line by line on a paper-like sheet, every line editable'),
    ('edit.alt2', 'Traty expenses screen: spending month by month, grouped by category'),

    ('band.l1', 'categories, each with its own colour'),
    ('band.l2', 'languages, built in'),
    ('band.l3', 'ads, ever'),
    ('band.l4', 'receipts typed in by hand, free'),

    ('widget.eyebrow', 'Home screen'),
    ('widget.h2', 'The total, without opening anything.'),
    ('widget.p', 'A widget with the month so far and your latest receipts. Free on every tier — it draws the receipts you already have, and charging a person for sight of their own numbers would be a strange business.'),
    ('widget.li1', 'Month total and recent receipts at a glance'),
    ('widget.li2', 'Tap straight through to the camera'),
    ('widget.li3', 'Follows the light or dark look of your phone'),
    ('widget.alt', 'The Traty widget on an Android home screen showing the month total without opening the app'),

    ('fam.eyebrow', 'One plan, five people'),
    ('fam.h2', 'A family shops together. So it pays once.'),
    ('fam.p', 'Most apps sell you five subscriptions for one household. Traty sells one: a subscriber opens a household and invites up to four people, and joining is free even if they have never paid for anything.'),
    ('fam.li1', 'One shared base of receipts — whoever shopped, everybody sees it'),
    ('fam.li2', "One shared allowance of readings, drawn from the subscriber's plan"),
    ('fam.li3', 'Everyone keeps their own phone, their own login, their own language'),
    ('fam.li4', 'Leave the household and your own free readings are still yours'),
    ('fam.cta', 'See what it costs'),
    ('fam.card', 'Household · 5 people'),
    ('fam.owner', 'owner'),
    ('fam.poolline', 'Readings this month, shared'),
    ('fam.poolalt', '63 of 100 monthly readings used, across five people'),
    ('fam.poolfoot', 'One pool, not five. Everyone sees what is left of it.'),
    ('fam.vs1', 'Five subscriptions'),
    ('fam.vs2', 'One household'),

    ('priv.eyebrow', 'What leaves your phone'),
    ('priv.h2', 'A receipt says a lot about you. We keep almost none of it.'),
    ('priv.lede', 'The plain version. The legal one is linked at the bottom and says the same thing at greater length.'),
    ('priv.c1h', 'The photo is not kept'),
    ('priv.c1p', 'It travels to be read and is gone. Nothing about you is sold or passed to advertisers, because there are no advertisers.'),
    ('priv.c2h', 'The phone does its share'),
    ('priv.c2p', 'The total, the date and the currency are read on the device. Only the item list needs a server, and that is the single reason a photo ever leaves.'),
    ('priv.c3h', 'You can switch it off'),
    ('priv.c3p', 'Turn recognition off and the rest carries on: manual entry, history, categories, the widget. Deleting your account and your data is a page, not an email thread.'),

    ('pricing.eyebrow', 'Pricing'),
    ('pricing.h2', 'Only one thing here costs money.'),
    ('pricing.lede', 'Reading a photograph is paid for per receipt, so that is what a subscription buys. Your history, your edits, your categories, your widget — those cost us nothing and cost you nothing. And one subscription covers a household of five.'),
    ('plan.free', 'Free'),
    ('plan.forever', ' / forever'),
    ('plan.freesub', 'Enough to see whether it fits your life.'),
    ('plan.f1a', '5 receipt readings'),
    ('plan.f1b', ' from a photo'),
    ('plan.f2', 'Unlimited receipts typed in by hand'),
    ('plan.f3', 'Full history, editing, categories, breakdowns'),
    ('plan.f4', 'Price history and the home-screen widget'),
    ('plan.f5', "Join someone else's household"),
    ('plan.freecta', 'Start free'),
    ('plan.plus', 'Traty Plus'),
    ('plan.month', ' / month'),
    ('plan.plussub', 'For a household that shops on paper.'),
    ('plan.p1', '20 readings a day, 100 a month'),
    ('plan.p2', 'A household of up to five, one shared base'),
    ('plan.p3', 'One subscription covers the whole family'),
    ('plan.p4', 'Everything in Free, unchanged'),
    ('plan.p5', 'Cancel in Google Play, any time'),
    ('plan.pluscta', 'Get Traty'),
    ('pricing.note', 'Billed through Google Play in your local currency. A household shares one allowance rather than multiplying it — which is exactly why one subscription is enough for a family of five.'),

    ('faq.eyebrow', 'Questions'),
    ('faq.h2', 'Before you install it'),
    ('faq.q1', 'How does Traty read a receipt?'),
    ('faq.a1', 'You photograph it. The total, the date and the currency are read on the phone itself. The list of items is read by a model on our server — that is the only reason the photograph leaves the device. A very long receipt is cut into strips and read piece by piece, and still counts as one reading.'),
    ('faq.q2', 'Is my receipt photo stored anywhere?'),
    ('faq.a2', 'No. The photograph is sent to be read and is not kept afterwards. If you would rather nothing left the phone at all, turn recognition off in the settings: manual entry, history, categories, breakdowns and the widget keep working exactly as before.'),
    ('faq.q3', 'Is it really free?'),
    ('faq.a3', 'Typing receipts in by hand, editing them, your whole history, categories, breakdowns, price history and the home-screen widget are free and unlimited, for as long as you use the app. Only reading a photograph costs money per receipt, so the free tier includes five readings, and a subscription is $4.99 a month after that.'),
    ('faq.q4', 'What if the model gets a line wrong?'),
    ('faq.a4', 'Fix it. Every field is editable in two taps — name, price, quantity, category — and the app warns you when the lines stop adding up to the printed total, so a misread number is caught rather than quietly folded into your month.'),
    ('faq.q5', 'Can my family share one subscription?'),
    ('faq.a5', 'Yes. A subscriber creates a household and invites up to four people; joining is free. Everyone sees the same receipts and draws on the same monthly allowance, so a family of five needs one subscription rather than five.'),
    ('faq.q6', 'Which languages and currencies does it handle?'),
    ('faq.a6', 'The app speaks English, Polish, Ukrainian and Russian, and reads receipts in the currency printed on them, so a holiday receipt does not quietly turn into your home money.'),
    ('faq.q7', 'Which phones does it run on?'),
    ('faq.a7', 'Android, from Google Play. There is no iPhone version yet.'),

    ('final.eyebrow', 'Your next receipt'),
    ('final.h2', 'Stop filing paper. Start reading numbers.'),
    ('final.lede', 'Five readings free, no card, no ads. If it has not earned its place on your home screen in a week, nothing was lost.'),

    ('foot.made', 'Made by Oleksii Charoian'),
    ('foot.privacy', 'Privacy policy'),
    ('foot.delete', 'Delete your data'),

    ('marq.1', 'Name, price, quantity, category'),
    ('marq.2', '30 categories'),
    ('marq.3', 'Price history per product'),
    ('marq.4', 'Home-screen widget'),
    ('marq.5', 'Shared household'),
    ('marq.6', 'English · Polski · Українська · Русский'),
    ('marq.7', 'Manual entry always free'),
    ('marq.8', 'Reads the currency on the receipt'),
]


def main():
    html = SRC.read_text()
    out = {}
    # Длинные строки первыми: иначе короткая съедает подстроку длинной.
    for key, text in sorted(STRINGS, key=lambda kv: -len(kv[1])):
        if text not in html:
            print(f'НЕ НАЙДЕНО: {key!r} → {text[:60]!r}', file=sys.stderr)
            continue
        html = html.replace(text, '{{%s}}' % key)
        out[key] = text
    TEMPLATE.write_text(html)
    CONTENT.mkdir(exist_ok=True)
    (CONTENT / '_extracted.en.json').write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    left = re.findall(r'>([A-Z][a-z]{3,}[^<{]{12,})<', html)
    print(f'подставлено ключей: {len(out)} из {len(STRINGS)}')
    print('возможно пропущено:', left[:12])


if __name__ == '__main__':
    main()
