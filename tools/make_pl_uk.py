#!/usr/bin/env python3
"""Складывает content/pl.json и content/uk.json.

Ключи берутся из английского словаря: если перевод какого-то ключа забыт,
сборка об этом скажет здесь, а не молча оставит английскую фразу на польской
странице.

Суммы — из тех же демо-наборов, по которым сняты экраны
(`scripts/demo_locales.py`): у польского курс 1, у украинского 11. Совпадение
обязательно: рядом с макетом лежит снимок, и разные числа в них читаются как
подделка.
"""

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / 'content'

# referrer доезжает до Play Console: по нему видно, сколько установок дала
# страница и какой из языков.
PLAY = ('https://play.google.com/store/apps/details?id=dev.charoian.traty'
        '&referrer=utm_source%3Dlanding%26utm_medium%3Dweb%26utm_campaign%3D')
PRIVACY = 'https://scancheck-617d3.web.app/privacy.html'
DELETE = 'https://scancheck-617d3.web.app/delete-account.html'

PL = {
    'meta.title': 'Skaner paragonów: wydatki według kategorii — Traty',
    'meta.description': 'Zrób zdjęcie paragonu: Traty odczyta każdą pozycję — nazwę, cenę, ilość, kategorię — i pokaże, na co idzie miesiąc. Start za darmo, na Androida.',
    'meta.keywords': 'skaner paragonów, aplikacja do paragonów, wydatki domowe, budżet domowy android, zakupy spożywcze, historia cen, wydatki według kategorii',
    'og.title': 'Zrób zdjęcie paragonu. Sam się poukłada.',
    'og.description': 'Traty czyta każdą pozycję paragonu — nazwę, cenę, ilość, kategorię — i zamienia miesiąc zakupów w kilka liczb, które widać na pierwszy rzut oka.',
    'tw.description': 'Każda pozycja wyceniona i przypisana. Nic wpisywane ręcznie.',

    'nav.how': 'Jak to działa',
    'nav.month': 'Twój miesiąc',
    'nav.family': 'Rodzina',
    'nav.privacy': 'Prywatność',
    'nav.pricing': 'Cennik',
    'nav.faq': 'Pytania',
    'nav.cta': 'Pobierz za darmo',

    'hero.eyebrow': 'Skaner paragonów na Androida',
    'hero.h1a': 'Sfotografuj paragon.',
    'hero.h1b': 'Sam się poukłada.',
    'hero.lede': 'Każda pozycja odczytana, wyceniona i przypisana do kategorii — nazwa, ilość, cena, wszystko. Miesiąc papierków zamienia się w budżet domowy, który wypełnia się sam.',
    'cta.play': 'Pobierz z Google Play',
    'hero.cta2': 'Zobacz, jak to działa',
    'hero.trust1': 'Start za darmo',
    'hero.trust2': 'Zdjęcie nie jest przechowywane',
    'hero.trust3': 'Bez reklam',
    'scene.title': 'Poukładane w sekundę',
    'scene.cap': 'Odczytane ze zdjęcia',

    'how.eyebrow': 'Trzy kroki, jakieś pół minuty',
    'how.h2': 'Celujesz aparatem. To cała robota.',
    'how.lede': 'Żadna aplikacja nie sprawiła, by wpisywanie paragonu było przyjemne, więc Traty o to nie prosi. Zrób zdjęcie, a lista przyjdzie już rozbita na pozycje — i każdą można poprawić, jeśli coś odczytało się źle.',
    'how.s1h': 'Zrób zdjęcie',
    'how.s1p': 'Zmięty, wyblakły, absurdalnie długi — po prostu wyceluj i zrób zdjęcie. Długie paragony są cięte na pasy i czytane po kawałku, a i tak liczą się jako jeden odczyt.',
    'how.s1alt': 'Ekran aparatu w Traty wycelowany w papierowy paragon',
    'how.s2h': 'Czyta każdą pozycję',
    'how.s2p': 'Nazwa, ilość, cena jednostkowa i kategoria dla każdej pozycji. Sumę, datę i walutę telefon odczytuje sam.',
    'how.s2alt': 'Rozpoznane pozycje paragonu w Traty: nazwa, ilość, cena i kategoria',
    'how.s3h': 'Miesiąc sam się sumuje',
    'how.s3p': 'Każdy paragon trafia w jeden obraz miesiąca: suma, średnia, wydatek na dzień i dokładnie to, na co poszło.',
    'how.s3alt': 'Pulpit Traty: suma miesiąca, wydatek na dzień i podział na kategorie',

    'month.eyebrow': 'Wydatki według kategorii',
    'month.h2': 'Miesiąc zakupów w sześciu liczbach.',
    'month.p': 'Sterta paragonów nie mówi nic, kształt mówi wszystko. Traty rysuje ten miesiąc na tle tych samych dni poprzedniego, więc przekroczenie widać w pierwszym tygodniu, a nie 30.',
    'month.li1': 'Suma narastająco na tle tych samych dni poprzedniego miesiąca',
    'month.li2': 'Średni paragon, wydatek na dzień, pieniądze zaoszczędzone na promocjach',
    'month.li3': 'Każda kategoria trzyma swój kolor, miesiąc po miesiącu',
    'month.li4': 'Dotknij kategorii, żeby zobaczyć pozycje w środku',
    'dash.demo': 'Dane poglądowe',
    'dash.since': 'Wydane od początku miesiąca',
    'dash.chartalt': 'Suma narastająco we wrześniu jest o 21 procent niższa niż w tych samych dniach sierpnia',
    'dash.avg': 'Średni paragon',
    'dash.perday': 'Na dzień',
    'dash.saved': 'Zaoszczędzono',
    'dash.baralt': 'Udział kategorii w miesiącu',

    'price.eyebrow': 'Historia ceny',
    'price.h2': 'Zauważa, kiedy cena po cichu rośnie.',
    'price.p': 'To samo mleko, ten sam sklep, pięćdziesiąt groszy drożej niż miesiąc temu. Nikt tego nie wyłapie z pamięci. Traty pamięta każdą cenę zapłaconą za produkt i mówi wprost, kiedy nowa jest wyższa.',
    'price.li1': 'Każdy zakup produktu, najtańszy i najdroższy oznaczone',
    'price.li2': 'Porównanie za litr albo za kilogram, nie za opakowanie',
    'price.li3': 'Dwie różne rzeczy liczone jako jeden produkt? Rozdziel je jednym dotknięciem',
    'price.dearest': 'najdrożej',
    'price.cheapest': 'najtaniej',

    'edit.eyebrow': 'Twoje do poprawienia',
    'edit.h2': 'Czyta model. Właścicielem jesteś ty.',
    'edit.p': 'Model czasem źle odczyta rozmazany wiersz, a aplikacja, która udaje, że tak nie jest, jest gorsza od tej, która się do tego przyznaje. Każde pole zostaje do edycji, a paragon pilnuje własnej arytmetyki — w chwili, gdy pozycje przestają się sumować do wydrukowanej sumy, mówi o tym.',
    'edit.li1': 'Dwa dotknięcia, żeby poprawić cenę albo przenieść pozycję do innej kategorii',
    'edit.li2': 'Nie masz aparatu? Wpisz paragon ręcznie — za darmo, zawsze, ile chcesz',
    'edit.li3': 'Miesiąc po miesiącu, grupa po grupie, aż do pojedynczej pozycji',
    'edit.li4': 'Jasny i ciemny motyw, po polsku, angielsku, ukraińsku i rosyjsku',
    'edit.alt1': 'Rozpoznany paragon w Traty, pozycja po pozycji na arkuszu przypominającym papier',
    'edit.alt2': 'Ekran wydatków w Traty: miesiąc po miesiącu, w podziale na kategorie',

    'band.l1': 'kategorii, do których trafiają zakupy',
    'band.l2': 'wbudowane języki',
    'band.l3': 'reklam, nigdy',
    'band.l4': 'paragonów wpisanych ręcznie, za darmo',

    'widget.eyebrow': 'Widżet na ekranie głównym',
    'widget.h2': 'Suma, bez otwierania czegokolwiek.',
    'widget.p': 'Widżet z miesiącem i ostatnimi paragonami. Za darmo na każdym planie — rysuje paragony, które już masz, a branie pieniędzy za podgląd własnych liczb byłoby dziwnym interesem.',
    'widget.li1': 'Suma miesiąca i ostatnie paragony na pierwszy rzut oka',
    'widget.li2': 'Dotknięcie prowadzi prosto do aparatu',
    'widget.li3': 'Dopasowuje się do jasnego albo ciemnego wyglądu aplikacji',
    'widget.alt': 'Widżet Traty na ekranie głównym Androida z sumą miesiąca',

    'fam.eyebrow': 'Jeden plan, pięć osób',
    'fam.h2': 'Rodzina robi zakupy razem. Więc płaci raz.',
    'fam.p': 'Jedna subskrypcja zamiast pięciu: subskrybent zakłada rodzinę i zaprasza do czterech osób, a dołączenie jest darmowe, nawet jeśli nigdy za nic nie zapłaciły.',
    'fam.li1': 'Jedna wspólna baza paragonów — kto by nie robił zakupów, widzą wszyscy',
    'fam.li2': 'Jedna wspólna pula odczytów, z planu subskrybenta',
    'fam.li3': 'Każdy ma swój telefon, swoje konto i swój język',
    'fam.li4': 'Wyjdziesz z rodziny — twoje własne darmowe odczyty zostają twoje',
    'fam.cta': 'Zobacz, ile to kosztuje',
    'fam.card': 'Rodzina · 5 osób',
    'fam.owner': 'właściciel',
    'fam.poolline': 'Odczyty w tym miesiącu, wspólne',
    'fam.poolalt': 'Wykorzystano 63 ze 100 miesięcznych odczytów, na pięć osób',
    'fam.poolfoot': 'Jedna pula, nie pięć. Każdy widzi, ile z niej zostało.',
    'fam.vs1': 'Pięć subskrypcji',
    'fam.vs2': 'Jedna rodzina',

    'priv.eyebrow': 'Co opuszcza telefon',
    'priv.h2': 'Paragon mówi o tobie sporo. My nie zostawiamy z tego prawie nic.',
    'priv.lede': 'Wersja po ludzku. Prawna jest na dole strony i mówi to samo, tylko dłużej.',
    'priv.c1h': 'Zdjęcie nie zostaje',
    'priv.c1p': 'Trafia na serwer tylko po to, żeby je odczytać, i znika. Nic o tobie nie jest sprzedawane ani przekazywane reklamodawcom, bo żadnych reklamodawców nie ma.',
    'priv.c2h': 'Telefon robi swoje',
    'priv.c2p': 'Sumę, datę i walutę odczytuje urządzenie. Serwera potrzebuje tylko lista pozycji i to jedyny powód, dla którego zdjęcie w ogóle opuszcza telefon.',
    'priv.c3h': 'Możesz to wyłączyć',
    'priv.c3p': 'Wyłącz rozpoznawanie, a reszta działa dalej: wpisywanie ręczne, historia, kategorie, widżet. Usunięcie konta i danych to strona, a nie wymiana maili.',

    'pricing.h2': 'Tylko jedna rzecz tu kosztuje.',
    'pricing.lede': 'Odczyt zdjęcia jest płatny od paragonu i to właśnie kupuje subskrypcja. Twoja historia, twoje poprawki, twoje kategorie, twój widżet — to nas nic nie kosztuje i ciebie też nie. A jedna subskrypcja wystarcza na pięcioosobową rodzinę.',
    'plan.free': 'Za darmo',
    'plan.forever': ' / na zawsze',
    'plan.freesub': 'Tyle, żeby sprawdzić, czy pasuje do twojego życia.',
    'plan.f1a': '5 odczytów paragonu',
    'plan.f1b': ' ze zdjęcia',
    'plan.f2': 'Bez limitu paragonów wpisanych ręcznie',
    'plan.f3': 'Pełna historia, edycja, kategorie, zestawienia',
    'plan.f4': 'Historia cen i widżet na ekranie głównym',
    'plan.f5': 'Dołączenie do cudzej rodziny',
    'plan.freecta': 'Zacznij za darmo',
    'plan.plus': 'Traty Plus',
    'plan.month': ' / miesiąc',
    'plan.plussub': 'Dla rodziny, która zbiera paragony.',
    'plan.p1': '20 odczytów dziennie, 100 miesięcznie',
    'plan.p2': 'Rodzina do pięciu osób, jedna wspólna baza',
    'plan.p3': 'Jedna subskrypcja obejmuje całą rodzinę',
    'plan.p4': 'Wszystko z planu darmowego, bez zmian',
    'plan.p5': 'Anulujesz w Google Play, kiedy chcesz',
    'plan.pluscta': 'Pobierz Traty',
    'pricing.note': 'Rozliczane przez Google Play w twojej walucie. Rodzina dzieli jedną pulę, a nie mnoży ją — i właśnie dlatego jedna subskrypcja wystarcza pięciu osobom.',

    'faq.eyebrow': 'Pytania',
    'faq.h2': 'Zanim zainstalujesz',
    'faq.q1': 'Jak Traty czyta paragon?',
    'faq.a1': 'Robisz zdjęcie. Sumę, datę i walutę telefon odczytuje sam. Listę pozycji czyta model na naszym serwerze — to jedyny powód, dla którego zdjęcie opuszcza urządzenie. Bardzo długi paragon jest cięty na pasy i czytany po kawałku, a i tak liczy się jako jeden odczyt.',
    'faq.q2': 'Czy moje zdjęcie paragonu gdzieś zostaje?',
    'faq.a2': 'Nie. Zdjęcie trafia na serwer tylko po to, żeby je odczytać, i nie jest przechowywane. Jeśli wolisz, żeby nic nie opuszczało telefonu, wyłącz rozpoznawanie w ustawieniach: wpisywanie ręczne, historia, kategorie, zestawienia i widżet działają dokładnie tak samo.',
    'faq.q3': 'Czy to naprawdę za darmo?',
    'faq.a3': 'Wpisywanie paragonów ręcznie, ich edycja, cała historia, kategorie, zestawienia, historia cen i widżet są darmowe i bez limitu, tak długo, jak używasz aplikacji. Płatny jest tylko odczyt zdjęcia, bo każdy kosztuje — dlatego plan darmowy zawiera pięć odczytów, a potem subskrypcja to 19,99 zł miesięcznie.',
    'faq.q4': 'A jeśli model źle odczyta pozycję?',
    'faq.a4': 'Popraw ją. Każde pole poprawisz dwoma dotknięciami — nazwa, cena, ilość, kategoria — a aplikacja ostrzega, kiedy pozycje przestają się sumować do wydrukowanej sumy, więc źle odczytana liczba zostaje złapana, a nie po cichu wliczona w miesiąc.',
    'faq.q5': 'Czy rodzina może dzielić jedną subskrypcję?',
    'faq.a5': 'Tak. Subskrybent zakłada rodzinę i zaprasza do czterech osób; dołączenie jest darmowe. Wszyscy widzą te same paragony i korzystają z tej samej miesięcznej puli, więc pięcioosobowa rodzina potrzebuje jednej subskrypcji, a nie pięciu.',
    'faq.q6': 'Jakie języki i waluty obsługuje?',
    'faq.a6': 'Aplikacja mówi po polsku, angielsku, ukraińsku i rosyjsku, a paragony czyta w walucie, która jest na nich wydrukowana — wakacyjny paragon nie zamieni się po cichu w twoje domowe pieniądze.',
    'faq.q7': 'Na jakich telefonach działa?',
    'faq.a7': 'Android, z Google Play. Wersji na iPhone jeszcze nie ma.',

    'final.eyebrow': 'Twój następny paragon',
    'final.h2': 'Przestań zbierać papier. Zacznij czytać liczby.',
    'final.lede': 'Pięć odczytów za darmo, bez karty, bez reklam. Jeśli przez tydzień nie zasłuży na miejsce na twoim ekranie, nic nie tracisz.',

    'foot.made': 'Autor: Oleksii Charoian',
    'foot.privacy': 'Polityka prywatności',
    'foot.delete': 'Usuń swoje dane',

    'marq.1': 'Nazwa, cena, ilość, kategoria',
    'marq.2': '30 kategorii',
    'marq.3': 'Historia ceny produktu',
    'marq.4': 'Widżet na ekranie głównym',
    'marq.5': 'Wspólna rodzina',
    'marq.6': 'English · Polski · Українська · Русский',
    'marq.7': 'Wpisywanie ręczne zawsze za darmo',
    'marq.8': 'Czyta walutę z paragonu',
}

UK = {
    'meta.title': 'Сканер чеків: витрати за категоріями — Traty',
    'meta.description': 'Сфотографуйте чек: Traty прочитає кожну позицію — назву, ціну, кількість, категорію — і покаже, на що йде місяць. Старт безкоштовний, на Android.',
    'meta.keywords': 'сканер чеків, додаток для чеків, облік витрат, сімейний бюджет android, продукти, історія цін, витрати за категоріями',
    'og.title': 'Сфотографуй чек. Він розкладеться сам.',
    'og.description': 'Traty читає кожну позицію паперового чека — назву, ціну, кількість, категорію — і перетворює місяць покупок на кілька чисел, які видно з одного погляду.',
    'tw.description': 'Кожна позиція з ціною і категорією. Нічого не набирати руками.',

    'nav.how': 'Як це працює',
    'nav.month': 'Ваш місяць',
    'nav.family': "Сім'я",
    'nav.privacy': 'Приватність',
    'nav.pricing': 'Ціна',
    'nav.faq': 'Питання',
    'nav.cta': 'Завантажити',

    'hero.eyebrow': 'Сканер чеків для Android',
    'hero.h1a': 'Сфотографуйте чек.',
    'hero.h1b': 'Він розкладеться сам.',
    'hero.lede': 'Кожен рядок прочитано, оцінено й покладено у свою категорію — назва, кількість, ціна, усе. Місяць паперу перетворюється на облік витрат, який веде себе сам.',
    'cta.play': 'Завантажити в Google Play',
    'hero.cta2': 'Подивитися, як це працює',
    'hero.trust1': 'Старт безкоштовний',
    'hero.trust2': 'Фото не зберігається',
    'hero.trust3': 'Без реклами',
    'scene.title': 'Розкладено за секунду',
    'scene.cap': 'Прочитано з фото',

    'how.eyebrow': 'Три кроки, пів хвилини',
    'how.h2': 'Ви наводите камеру. Це вся робота.',
    'how.lede': 'Жоден додаток не зробив введення чека приємним, тому Traty про це й не просить. Сфотографуйте — і список прийде вже розібраним на позиції, а будь-який рядок можна виправити.',
    'how.s1h': 'Сфотографуйте',
    'how.s1p': 'Зім’ятий, вицвілий, безглуздо довгий — просто наведіть і зніміть. Довгі чеки ріжуться на смуги і читаються частинами, і це однаково одне розпізнавання.',
    'how.s1alt': 'Екран камери Traty, наведений на паперовий чек',
    'how.s2h': 'Він читає кожен рядок',
    'how.s2p': 'Назва, кількість, ціна за одиницю і категорія для кожної позиції. Суму, дату й валюту телефон читає сам.',
    'how.s2alt': 'Розпізнані позиції чека в Traty: назва, кількість, ціна й категорія',
    'how.s3h': 'Місяць складається сам',
    'how.s3p': 'Кожен чек лягає в одну картину місяця: сума, середнє, витрата на день і те, на що саме все пішло.',
    'how.s3alt': 'Головна Traty: сума місяця, витрата на день і розклад за категоріями',

    'month.eyebrow': 'Витрати за категоріями',
    'month.h2': 'Місяць покупок у шести числах.',
    'month.p': 'Купа чеків не говорить нічого, форма — усе. Traty малює цей місяць поверх тих самих днів попереднього, тому перевитрату видно вже на початку місяця, а не наприкінці.',
    'month.li1': 'Сума наростаючим підсумком проти тих самих днів минулого місяця',
    'month.li2': 'Середній чек, витрата на день, зекономлене на знижках',
    'month.li3': 'Кожна категорія тримає свій колір, місяць за місяцем',
    'month.li4': 'Торкніться категорії, щоб побачити позиції всередині',
    'dash.demo': 'Демодані',
    'dash.since': 'Витрачено з початку місяця',
    'dash.chartalt': 'Сума за вересень на 21 відсоток нижча за ті самі дні серпня',
    'dash.avg': 'Середній чек',
    'dash.perday': 'На день',
    'dash.saved': 'Зекономлено',
    'dash.baralt': 'Частка категорій у місяці',

    'price.eyebrow': 'Історія ціни',
    'price.h2': 'Він помічає, коли ціна тихо повзе вгору.',
    'price.p': 'Те саме молоко, той самий магазин, на кілька гривень дорожче, ніж місяць тому. З пам’яті цього не зловити. Traty пам’ятає кожну ціну, яку ви платили за товар, і прямо каже, коли нова вища.',
    'price.li1': 'Кожна покупка товару, найдешевша й найдорожча позначені',
    'price.li2': 'Порівняння за літр або за кілограм, а не за упаковку',
    'price.li3': 'Дві різні речі вважаються одним товаром? Розділіть їх одним дотиком',
    'price.dearest': 'найдорожче',
    'price.cheapest': 'найдешевше',

    'edit.eyebrow': 'Ваше — вам і правити',
    'edit.h2': 'Читає модель. Власник — ви.',
    'edit.p': 'Модель час від часу помиляється на змазаному рядку, і додаток, який удає протилежне, гірший за той, що зізнається. Кожне поле лишається редагованим, а чек стежить за власною арифметикою — щойно рядки перестають складатися в надруковану суму, він про це каже.',
    'edit.li1': 'Два дотики, щоб виправити ціну або перенести позицію в іншу категорію',
    'edit.li2': 'Немає камери? Введіть чек руками — безкоштовно, завжди, скільки завгодно',
    'edit.li3': 'Місяць за місяцем, група за групою, аж до окремої позиції',
    'edit.li4': 'Світла й темна тема, українською, польською, англійською та російською',
    'edit.alt1': 'Розпізнаний чек у Traty, рядок за рядком на аркуші, схожому на папір',
    'edit.alt2': 'Екран витрат у Traty: місяць за місяцем, за категоріями',

    'band.l1': 'категорій, за якими розкладаються покупки',
    'band.l2': 'вбудовані мови',
    'band.l3': 'реклам, ніколи',
    'band.l4': 'чеків, введених руками, безкоштовно',

    'widget.eyebrow': 'Віджет на головному екрані',
    'widget.h2': 'Сума, не відкриваючи нічого.',
    'widget.p': 'Віджет із місяцем і останніми чеками. Безкоштовний на будь-якому тарифі — він малює ті самі чеки, що вже у вас є, а брати гроші за погляд на власні числа було б дивною справою.',
    'widget.li1': 'Сума місяця й останні чеки з одного погляду',
    'widget.li2': 'Дотик веде просто до камери',
    'widget.li3': 'Підлаштовується під світлий або темний вигляд додатка',
    'widget.alt': 'Віджет Traty на головному екрані Android із сумою місяця',

    'fam.eyebrow': "Один тариф, п'ятеро людей",
    'fam.h2': 'Сім’я робить покупки разом. Отже, платить один раз.',
    'fam.p': 'Одна підписка замість п’яти: підписник відкриває сім’ю і запрошує до чотирьох людей, а приєднання безкоштовне, навіть якщо вони ніколи ні за що не платили.',
    'fam.li1': 'Одна спільна база чеків — хто б що не купив, бачать усі',
    'fam.li2': 'Один спільний запас розпізнавань, з тарифу підписника',
    'fam.li3': 'У кожного свій телефон, свій вхід і своя мова',
    'fam.li4': 'Вийдете з сім’ї — власні безкоштовні розпізнавання лишаються вашими',
    'fam.cta': 'Подивитися ціну',
    'fam.card': "Сім'я · 5 людей",
    'fam.owner': 'власник',
    'fam.poolline': 'Розпізнавань цього місяця, спільних',
    'fam.poolalt': "Використано 63 зі 100 місячних розпізнавань, на п'ятьох",
    'fam.poolfoot': "Один запас, а не п'ять. Кожен бачить, скільки лишилося.",
    'fam.vs1': "П'ять підписок",
    'fam.vs2': "Одна сім'я",

    'priv.eyebrow': 'Що залишає телефон',
    'priv.h2': 'Чек говорить про вас багато. Ми не лишаємо з цього майже нічого.',
    'priv.lede': 'Версія людською мовою. Юридична — внизу сторінки, і каже те саме, лише довше.',
    'priv.c1h': 'Фото не зберігається',
    'priv.c1p': 'Воно вирушає лише для того, щоб його прочитали, і зникає. Нічого про вас не продається й не передається рекламодавцям, бо рекламодавців немає.',
    'priv.c2h': 'Телефон робить свою частину',
    'priv.c2p': 'Суму, дату й валюту читає сам пристрій. Сервер потрібен лише для списку позицій — це єдина причина, чому фото взагалі залишає телефон.',
    'priv.c3h': 'Це можна вимкнути',
    'priv.c3p': 'Вимкніть розпізнавання — решта працює далі: ручне введення, історія, категорії, віджет. Видалення акаунта й даних — це сторінка, а не листування.',

    'pricing.h2': 'Тут коштує рівно одна річ.',
    'pricing.lede': 'Читання фотографії оплачується за кожен чек — саме це й купує підписка. Ваша історія, ваші правки, ваші категорії, ваш віджет не коштують нічого ні нам, ні вам. А одна підписка покриває сім’ю з п’ятьох.',
    'plan.free': 'Безкоштовно',
    'plan.forever': ' / назавжди',
    'plan.freesub': 'Достатньо, щоб зрозуміти, чи воно вам підходить.',
    'plan.f1a': '5 розпізнавань чека',
    'plan.f1b': ' з фотографії',
    'plan.f2': 'Скільки завгодно чеків, введених руками',
    'plan.f3': 'Уся історія, правка, категорії, зведення',
    'plan.f4': 'Історія цін і віджет на головному екрані',
    'plan.f5': "Приєднання до чужої сім'ї",
    'plan.freecta': 'Почати безкоштовно',
    'plan.plus': 'Traty Plus',
    'plan.month': ' / місяць',
    'plan.plussub': 'Для родини, яка збирає паперові чеки.',
    'plan.p1': '20 розпізнавань на добу, 100 на місяць',
    'plan.p2': "Сім'я до п'яти осіб, одна спільна база",
    'plan.p3': 'Одна підписка на всю родину',
    'plan.p4': 'Усе з безкоштовного тарифу, без змін',
    'plan.p5': 'Скасування в Google Play, будь-коли',
    'plan.pluscta': 'Встановити Traty',
    'pricing.note': "Оплата через Google Play у вашій валюті. Сім'я ділить один запас, а не множить його — саме тому однієї підписки вистачає на п'ятьох.",

    'faq.eyebrow': 'Питання',
    'faq.h2': 'Перед встановленням',
    'faq.q1': 'Як Traty читає чек?',
    'faq.a1': 'Ви його фотографуєте. Суму, дату й валюту телефон читає сам. Список позицій читає модель на нашому сервері — це єдина причина, чому фотографія залишає пристрій. Дуже довгий чек ріжеться на смуги й читається частинами, і це однаково одне розпізнавання.',
    'faq.q2': 'Чи зберігається десь фото мого чека?',
    'faq.a2': 'Ні. Фотографія вирушає лише для того, щоб її прочитали, і не зберігається. Якщо ви волієте, щоб із телефона не виходило нічого, вимкніть розпізнавання в налаштуваннях: ручне введення, історія, категорії, зведення й віджет працюють так само.',
    'faq.q3': 'Це справді безкоштовно?',
    'faq.a3': 'Введення чеків руками, їх правка, уся історія, категорії, зведення, історія цін і віджет безкоштовні й без обмежень, доки ви користуєтеся додатком. Грошей коштує лише читання фотографії, тому безкоштовний тариф містить п’ять розпізнавань, а далі підписка — 149 ₴ на місяць.',
    'faq.q4': 'А якщо модель помилилася в рядку?',
    'faq.a4': 'Виправте його. Кожне поле редагується двома дотиками — назва, ціна, кількість, категорія — і додаток попереджає, коли рядки перестають складатися в надруковану суму, тож хибне число буде помічене, а не тихо вшите у ваш місяць.',
    'faq.q5': "Чи може сім'я ділити одну підписку?",
    'faq.a5': "Так. Підписник створює сім'ю і запрошує до чотирьох людей; приєднання безкоштовне. Усі бачать ті самі чеки й беруть з того самого місячного запасу, тому родині з п'ятьох потрібна одна підписка, а не п'ять.",
    'faq.q6': 'Які мови й валюти він розуміє?',
    'faq.a6': 'Додаток говорить українською, польською, англійською та російською, а чеки читає у валюті, надрукованій на них, тож чек із відпустки не перетвориться тихо на ваші домашні гроші.',
    'faq.q7': 'На яких телефонах він працює?',
    'faq.a7': 'Android, із Google Play. Версії для iPhone поки немає.',

    'final.eyebrow': 'Ваш наступний чек',
    'final.h2': 'Годі збирати папір. Час читати числа.',
    'final.lede': 'П’ять розпізнавань безкоштовно, без картки, без реклами. Якщо за тиждень додаток не заслужить місце на вашому екрані — ви нічого не втратили.',

    'foot.made': 'Автор — Oleksii Charoian',
    'foot.privacy': 'Політика приватності',
    'foot.delete': 'Видалити свої дані',

    'marq.1': 'Назва, ціна, кількість, категорія',
    'marq.2': '30 категорій',
    'marq.3': 'Історія ціни товару',
    'marq.4': 'Віджет на головному екрані',
    'marq.5': "Спільна сім'я",
    'marq.6': 'English · Polski · Українська · Русский',
    'marq.7': 'Ручне введення завжди безкоштовне',
    'marq.8': 'Читає валюту з чека',
}

# (наименование, количество, цена за единицу в злотых, единица, слот цвета)
ITEMS_PL = [
    ('Udka z kurczaka', 2, 18.90, 'kg', 1),
    ('Ziemniaki', 5, 3.49, 'kg', 2),
    ('Mleko 2%, 1 l', 6, 4.99, 'l', 0),
    ('Ryż, 1 kg', 2, 8.99, 'szt.', 3),
    ('Mrożone owoce leśne', 2, 14.90, 'szt.', 4),
    ('Sok, 1 l', 4, 7.49, 'szt.', 5),
    ('Ciasto', 1, 32.90, 'szt.', 1),
]
NOTES_PL = ['Mięso', 'Warzywa', 'Nabiał', 'Spiżarnia', 'Mrożonki', 'Napoje', 'Słodycze']

ITEMS_UK = [
    ('Курячі стегна', 2, 18.90, 'кг', 1),
    ('Картопля', 5, 3.49, 'кг', 2),
    ('Молоко 2%, 1 л', 6, 4.99, 'л', 0),
    ('Рис, 1 кг', 2, 8.99, 'шт', 3),
    ('Заморожені ягоди', 2, 14.90, 'шт', 4),
    ('Сік, 1 л', 4, 7.49, 'шт', 5),
    ('Торт', 1, 32.90, 'шт', 1),
]
NOTES_UK = ["М'ясо", 'Овочі', 'Молочне', 'Бакалія', 'Заморозка', 'Напої', 'Солодке']

CATEGORIES_PL = [
    ('Czynsz i rachunki', '55%', 1450.00),
    ('Paliwo', '9%', 246.62),
    ('Usługi', '6%', 165.00),
    ('Odzież', '5%', 142.90),
    ('Przejazdy', '4%', 110.00),
    ('Pozostałe · 11 kategorii', '20%', 525.88),
]
CATEGORIES_UK = [
    ('Оренда і рахунки', '55%', 1450.00),
    ('Пальне', '9%', 246.62),
    ('Послуги', '6%', 165.00),
    ('Одяг', '5%', 142.90),
    ('Проїзд', '4%', 110.00),
    ('Решта · 11 категорій', '20%', 525.88),
]


def curly(table):
    """Апостроф в украинском — типографский (’), а не машинописный.

    Строки набраны и так, и так, потому что часть из них в python-исходнике
    заключена в одинарные кавычки; выравнивание здесь одно на весь словарь.
    """
    return {k: v.replace("\'", "\u2019") if isinstance(v, str) else v
            for k, v in table.items()}


def money(value, rate):
    """Сумма демо-набора в валюте языка, как её показывает приложение.

    Разряды не разделяются: приложение их не разделяет, и снимок рядом с
    макетом показал бы «29044,40» против «29 044,40».
    """
    return f'{value * rate:.2f}'.replace('.', ',')


def build(lang, strings, items, notes, categories, cfg):
    rate = cfg['rate']
    paper_rows, sorted_rows, total = [], [], 0.0
    for i, (name, qty, unit_pln, unit, slot) in enumerate(items):
        unit_price = unit_pln * rate
        line = qty * unit_price
        total += line
        sub = '' if qty == 1 else f'{qty} {unit} × {money(unit_pln, rate)}'
        paper_rows.append([name, sub, money(line / rate, rate)])
        qty_note = f'{qty} {unit}' if qty > 1 else f'1 {unit}'
        sorted_rows.append([name, f'{notes[i]} · {qty_note}', money(line / rate, rate), slot])

    data = {
        'currency': cfg['currency'],
        'decimal': ',',
        'month': cfg['month'],
        'prevMonth': cfg['prevMonth'],
        'totalRaw': f'{2640.40 * rate:.2f}',
        'receipts': cfg['receipts'],
        'avg': money(264.04, rate),
        'perDay': money(240.03, rate),
        'saved': money(13.00, rate),
        'savedLine': cfg['savedLine'],
        'trend': '−21%',
        'categories': [[n, p, money(a, rate)] for n, p, a in categories],
        'paper': {
            'shop': cfg['shop'],
            'meta': cfg['meta'],
            'rows': paper_rows,
            'total': [cfg['totalLabel'], money(total / rate, rate)],
        },
        'sorted': sorted_rows,
        'price': {
            'shop': cfg['priceShop'],
            'item': items[2][0],
            'raw': f'{4.99 * rate:.2f}',
            'unit': cfg['perLitre'],
            'rise': cfg['rise'],
            'alt': cfg['sparkAlt'],
            'rows': [['09.09.2026', 'top', money(4.99, rate)],
                     ['02.09.2026', 'low', money(4.49, rate)],
                     ['30.08.2026', 'low', money(4.49, rate)],
                     ['09.08.2026', 'low', money(4.49, rate)],
                     ['02.08.2026', 'low', money(4.49, rate)]],
        },
        'family': {
            'members': cfg['members'],
            'used': cfg['used'],
            'share': [['22%', 0], ['16%', 0], ['11%', 2], ['8%', 4], ['6%', 1]],
        },
        'plan': cfg['plan'],
    }
    return {
        'lang': lang,
        'ogLocale': cfg['ogLocale'],
        'assets': '/assets/%s' % lang,
        'play': PLAY + lang,
        'privacyUrl': PRIVACY,
        'deleteUrl': DELETE,
        'strings': strings,
        'data': data,
    }


PL_CFG = {
    'rate': 1, 'currency': 'PLN', 'month': 'Wrzesień', 'prevMonth': 'Sierpień',
    'receipts': '10 paragonów', 'savedLine': 'Zaoszczędzono na promocjach 13,00 PLN',
    'shop': 'GROSIK', 'meta': 'ul. Kwiatowa 12 · 09.09.2026 · 11:20',
    'totalLabel': 'SUMA PLN', 'priceShop': 'Grosik', 'perLitre': 'PLN za litr',
    'rise': '11% więcej niż 02.08.2026',
    'sparkAlt': 'Cena cztery razy trzymała się 4,49 i wzrosła do 4,99',
    'ogLocale': 'pl_PL', 'used': '63 ze 100',
    'members': [['Alex', 0], ['Marta', 0], ['Kasia', 2], ['Piotr', 4], ['Jan', 1]],
    'plan': {'zero': '0 zł', 'plus': '19,99 zł', 'fiveTimes': '99,95 zł',
             'currency': 'PLN', 'plusAmount': '19.99'},
}

UK_CFG = {
    'rate': 11, 'currency': 'UAH', 'month': 'Вересень', 'prevMonth': 'Серпень',
    'receipts': '10 чеків', 'savedLine': 'Зекономлено на знижках 143,00 UAH',
    'shop': 'КОШИК', 'meta': 'вул. Квіткова 12 · 09.09.2026 · 11:20',
    'totalLabel': 'РАЗОМ UAH', 'priceShop': 'Кошик', 'perLitre': 'UAH за літр',
    'rise': '11% більше ніж 02.08.2026',
    'sparkAlt': 'Ціна чотири рази трималася на 49,39 і зросла до 54,89',
    'ogLocale': 'uk_UA', 'used': '63 зі 100',
    'members': [['Олег', 0], ['Марта', 0], ['Катя', 2], ['Петро', 4], ['Іван', 1]],
    'plan': {'zero': '0 ₴', 'plus': '149 ₴', 'fiveTimes': '745 ₴',
             'currency': 'UAH', 'plusAmount': '149'},
}


def main():
    en = json.loads((CONTENT / 'en.json').read_text())['strings']
    bad = False
    for name, table in (('pl', PL), ('uk', UK)):
        missing = set(en) - set(table) - {'pricing.eyebrow'}
        extra = set(table) - set(en)
        # pricing.h2 у английского зовётся иначе — сверяем по факту наличия ключа
        missing = {k for k in missing if k in en}
        if missing or extra:
            print('%s: не переведено %s, лишние %s' % (name, sorted(missing), sorted(extra)),
                  file=sys.stderr)
            bad = bool(missing)
    if bad:
        sys.exit(1)

    (CONTENT / 'pl.json').write_text(json.dumps(
        build('pl', PL, ITEMS_PL, NOTES_PL, CATEGORIES_PL, PL_CFG),
        ensure_ascii=False, indent=2) + '\n')
    (CONTENT / 'uk.json').write_text(json.dumps(
        build('uk', curly(UK), ITEMS_UK, NOTES_UK, CATEGORIES_UK, curly(UK_CFG)),
        ensure_ascii=False, indent=2) + '\n')
    print('записано content/pl.json и content/uk.json')


if __name__ == '__main__':
    main()
