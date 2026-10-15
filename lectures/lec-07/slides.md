---
# ─────────────────────────────────────────────────────────────────────────────
# HEADMATTER -- шапка лекции. Поля title/lecture/topics попадают в оглавление
# сайта (см. tools/build_site.py), поэтому заполняйте их у каждой лекции.
# ─────────────────────────────────────────────────────────────────────────────
routerMode: hash
theme: default
title: Словари
lecture: '07'
topics: словари, ключи и значения, get(), keys(), values(), items(), генераторы словарей, сортировка по значению, вложенные словари, подсчёт, Counter, группировка, defaultdict

# ГЛАВНОЕ ДЛЯ СВЕТЛОЙ/ТЁМНОЙ ТЕМЫ:
#   auto  -- подхватывает системную тему студента, кнопка/клавиша d переключает
#   dark  -- только тёмная (так было раньше)
#   light -- только светлая
colorSchema: auto

# фон титульного слайда: две версии, выбор -- в самом слайде через <LightOrDark>
transition: slide-left
mdc: true
drawings:
  persist: false
duration: 90min

# Заметки докладчика видны только вам (клавиша p -> presenter mode)
---

<div class="cover-bg"></div>

<div class="cover-body flex flex-col justify-center h-full">

<h1>Основы программирования</h1>

<h2 class="!mt-0">Лекция 7. Словари (dict)</h2>

<div class="cover-rule"></div>

###### Лекторы: 

<p class="text-[var(--ink-2)] mt-8">
1. Вячеслав Алексеевич Чузлов<br>
к.т.н., доцент ОХИ ИШПР ТПУ
</p>
<p class="text-[var(--ink-2)] mt-8">
2. Игорь Михайлович Долганов<br>
к.т.н., доцент ОХИ ИШПР ТПУ
</p>

</div>


---

# Уравнено ли уравнение?

В двух уравнениях из шести ошибка. В каких?

<div class="eqs">
<span><b>1</b>CH₄ + 2O₂ → CO₂ + 2H₂O</span>
<span><b>2</b>C₂H₆ + 3O₂ → 2CO₂ + 3H₂O</span>
<span><b>3</b>Fe₂O₃ + 3CO → 2Fe + 3CO₂</span>
<span><b>4</b>4Al + 3O₂ → 2Al₂O₃</span>
<span><b>5</b>2KClO₃ → 2KCl + 2O₂</span>
<span><b>6</b>C₃H₈ + 5O₂ → 3CO₂ + 4H₂O</span>
</div>

<v-click>

<div class="cols-2 mt-4">

<div>

- Ошибки в № 2 и № 5, обе в кислороде. В № 2 слева 6 атомов O, справа 7. В № 5 слева 6, справа 4.
- Правильно: 2C₂H₆ + 7O₂ → 4CO₂ + 6H₂O и 2KClO₃ → 2KCl + 3O₂.

</div>

<div>

<div class="warn">
Для ответа пришлось составить таблицу «элемент → число атомов» для каждой стороны каждого уравнения. Множество такую таблицу хранить не умеет: оно знает, какие элементы есть, но не сколько.
</div>

</div>

</div>

</v-click>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

<!--
Дать три минуты. Уравнение 2 выглядит правильным: углерод и водород сходятся, ошибку находят только те, кто досчитал кислород до конца.
-->

---

# Элемент → число атомов

```python
left = {'C': 2, 'H': 6, 'O': 6}       # C2H6 + 3O2
right = {'C': 2, 'H': 6, 'O': 7}      # 2CO2 + 3H2O
print(left == right)
for element in left:
    print(element, left[element], right[element])
```

<pre class="output">False
C 2 2
H 6 6
O 6 7</pre>

- Фигурные скобки, внутри пары `ключ: значение`: это **словарь**. `left['O']` -- не номер, а имя: «сколько атомов кислорода слева».
- Словари равны, если совпадают все пары. В [лекции 6](https://vchuzlov.github.io/test-lectures/lec-06/#/44) множество не заметило, что CH₄ + O₂ → CO₂ + H₂O не уравнено; словарь видит разницу в числе атомов.

<div class="note">
Атомы здесь посчитаны руками. Во второй половине пары <code>Counter</code> сравнит эти же две стороны и покажет, чего и с какой стороны больше.
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Коллекции в Python

<div class="small-table">

| | Строка `str` | Список `list` | Кортеж `tuple` | Множество `set` | Словарь `dict` |
|---|---|---|---|---|---|
| Пример | `'H2SO4'` | `[6.9, 7.1]` | `('Na+', 'Cl-')` | `{'Na+', 'Cl-'}` | `{'C': 2, 'H': 6}` |
| Как достать элемент | по индексу | по индексу | по индексу | никак, только `in` | **по ключу** |
| Повторы | есть | есть | есть | нет | ключи -- нет, значения -- есть |
| Можно изменить | нет | да | нет | да | да |
| Лекция | [4](https://vchuzlov.github.io/test-lectures/lec-04/#/3) | [5](https://vchuzlov.github.io/test-lectures/lec-05/#/6) | [6](https://vchuzlov.github.io/test-lectures/lec-06/#/6) | [6](https://vchuzlov.github.io/test-lectures/lec-06/#/23) | сегодня |

</div>

<div class="cols-2 mt-4">

<div>

- Словарь -- это множество ключей, к каждому из которых привязано значение.
- Для ключей действуют те же правила, что для элементов множества: они уникальны и неизменяемы ([лекция 6](https://vchuzlov.github.io/test-lectures/lec-06/#/36)).

</div>

<div>

- Значения -- любые объекты: числа, строки, списки, другие словари.
- Во второй половине пары -- два словаря из модуля `collections`: `Counter` для подсчёта и `defaultdict` для группировки.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---
layout: image-left
class: flex flex-col items-center justify-center
image: /pics/photo_2026-02-19_14-53-38.jpg
---

# Словари (`dict`)

---

# Словари (`dict`)

> Словарь (тип `dict`) -- <span class="text-[var(--brand)]">*изменяемая коллекция пар «ключ: значение»*</span>. Значение находят по ключу, а не по номеру.

<div class="cols-2">

<div>

```python
M = {'H': 1.008, 'C': 12.011, 'O': 15.999}
print(M)
print(M['C'], len(M))
print('O' in M, 'N' in M)
print(M['N'])
```

<pre class="output">{'H': 1.008, 'C': 12.011, 'O': 15.999}
12.011 3
True False
KeyError: 'N'</pre>

</div>

<div>

<FigJars class="w-full mt-1" />

</div>

</div>

- Пары записываются через запятую в фигурных скобках, ключ и значение -- через двоеточие. `len()` -- число пар. `M['C']` -- значение по ключу.
- `in` проверяет **ключи**. Обращение к ключу, которого нет, останавливает программу: `KeyError`.
- Список -- штатив с пронумерованными гнёздами, словарь -- полка с банками реактивов: банку ищут не по номеру места, а по этикетке.

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Ключи и значения

<div class="cols-2">

<div>

```python
d = {'H': 1.008, 'O': 15.999, 'H': 1.0}
print(d)
salts = {('Na+', 'Cl-'): 'NaCl', ('K+', 'Br-'): 'KBr'}
print(salts[('K+', 'Br-')])
bad = {['Na+', 'Cl-']: 'NaCl'}
```

<pre class="output">{'H': 1.0, 'O': 15.999}
KBr
TypeError: cannot use 'list' as a dict key (unhashable type: 'list')</pre>

</div>

<div>

- Ключи **уникальны**. Повторный ключ не добавляет новую пару, а заменяет значение: остаётся последнее.
- Ключом может быть только хешируемый объект: число, строка, кортеж, `frozenset`. Словарь находит ключ по хешу так же, как множество -- элемент ([лекция 6](https://vchuzlov.github.io/test-lectures/lec-06/#/37)).
- Значения -- любые и могут повторяться: два вещества с одинаковой молярной массой -- нормальная ситуация.

</div>

</div>

<div class="warn">
До Python 3.14 сообщение короче: <code>TypeError: unhashable type: 'list'</code>.
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Изменение словаря

<div class="cols-2">

<div>

```python
M = {'H': 1.008, 'C': 12.011}
M['O'] = 15.999          # новый ключ - новая пара
M['H'] = 1.0             # старый ключ - новое значение
print(M)
del M['H']
x = M.pop('C')
print(x, M)
M.update({'N': 14.007, 'S': 32.06})
print(M)
print(M.pop('Ar', None))
```

<pre class="output">{'H': 1.0, 'C': 12.011, 'O': 15.999}
12.011 {'O': 15.999}
{'O': 15.999, 'N': 14.007, 'S': 32.06}
None</pre>

</div>

<div>

- Присваивание по ключу работает в обе стороны: нового ключа нет -- пара добавляется, ключ есть -- значение заменяется. Ошибки не бывает ни в одном случае.
- `del` удаляет пару. `pop()` удаляет и возвращает значение, как у списка ([лекция 5](https://vchuzlov.github.io/test-lectures/lec-05/#/23)), только по ключу, а не по индексу.
- `pop(ключ, x)` для отсутствующего ключа возвращает `x` вместо `KeyError`.
- `update()` дописывает пары из другого словаря; совпавшие ключи получают новые значения.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Порядок ключей

<div class="cols-2">

<div>

```python
M = {'O': 15.999, 'H': 1.008}
M['C'] = 12.011
print(M)
print(list(M))

ions = ['Na+', 'Cl-', 'Na+', 'K+', 'Cl-', 'Mg2+']
print(list(dict.fromkeys(ions)))
print(sorted(set(ions)))
```

<pre class="output">{'O': 15.999, 'H': 1.008, 'C': 12.011}
['O', 'H', 'C']
['Na+', 'Cl-', 'K+', 'Mg2+']
['Cl-', 'K+', 'Mg2+', 'Na+']</pre>

</div>

<div>

- Словарь помнит порядок, в котором добавлялись ключи. Печать и перебор идут в этом порядке при любом запуске, в отличие от множества ([лекция 6](https://vchuzlov.github.io/test-lectures/lec-06/#/25)).
- `dict.fromkeys(ions)` -- словарь, ключи которого -- элементы списка без повторов, а значения `None`. `list()` от него -- список без повторов **в исходном порядке**.
- Это и есть способ, обещанный в лекции 6: `list(set(...))` убирает повторы, но порядок теряет.

</div>

</div>

<div class="note">
Порядок вставки сохраняется с Python 3.7. Индексов у словаря при этом нет: <code>M[0]</code> ищет ключ <code>0</code>, а не первую пару.
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Словарь вместо цепочки `if`

<div class="cols-2">

<div>

##### Цепочка `if` ... `elif`

```python
name = 'медный купорос'
if name == 'поваренная соль':
    formula = 'NaCl'
elif name == 'питьевая сода':
    formula = 'NaHCO3'
elif name == 'медный купорос':
    formula = 'CuSO4·5H2O'
else:
    formula = '?'
print(formula)
```

<div class='output'>CuSO4·5H2O</div>

</div>

<div>

##### Словарь

```python
trivial = {'поваренная соль': 'NaCl',
           'питьевая сода': 'NaHCO3',
           'медный купорос': 'CuSO4·5H2O',
           'негашёная известь': 'CaO'}
print(trivial['медный купорос'])
print('гипс' in trivial)
trivial['гипс'] = 'CaSO4·2H2O'
print(len(trivial))
```

<pre class="output">CuSO4·5H2O
False
5</pre>

</div>

</div>

- Когда выбор сводится к «по названию найти значение», словарь короче цепочки из [лекции 2](https://vchuzlov.github.io/test-lectures/lec-02/#/26): данные лежат отдельно от кода, а не размазаны по веткам.
- Новый вариант -- одна пара в словаре, причём её можно добавить прямо во время работы программы. В цепочку `if` новую ветку добавляют только правкой кода.

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Что напечатает эта программа?

```python
M = {'H': 1.008, 'C': 12.011, 'O': 15.999}
print('C' in M, 12.011 in M)
M['O'] = 16.0
M['o'] = 16.0
M['C'] = M['C'] * 2
print(len(M), M['C'])
```

<v-click>

<pre class="output">True False
4 24.022</pre>

- `in` проверяет ключи, а не значения. `12.011` -- значение, среди ключей его нет. Для значений есть `12.011 in M.values()`.
- `'O'` и `'o'` -- разные строки, значит, разные ключи. `M['O'] = 16.0` заменил значение, `M['o'] = 16.0` добавил четвёртую пару.
- `M['C'] = M['C'] * 2` читает старое значение и записывает новое под тем же ключом.

</v-click>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

<!--
Сначала спросить зал. Частые ответы: True True (in ищет и в значениях) и 3 (регистр ключа не учитывают).
-->

---
layout: image-left
class: flex flex-col items-center justify-center
image: /pics/photo_2026-02-19_14-53-38.jpg
---

# Перебор  элементов словаря

---

# Метод `get()`

<div class="cols-2">

<div>

```python
M = {'H': 1.008, 'C': 12.011, 'O': 15.999}
print(M.get('C'), M.get('N'))
print(M.get('N', 0.0))
print(M)

element = 'N'
if element in M:
    print(M[element])
else:
    print('нет в таблице:', element)
```

<pre class="output">12.011 None
0.0
{'H': 1.008, 'C': 12.011, 'O': 15.999}
нет в таблице: N</pre>

</div>

<div>

- `get(ключ)` возвращает значение или `None`, если ключа нет. Программа при этом не останавливается.
- `get(ключ, x)` вместо `None` возвращает `x`: значение по умолчанию.
- `get()` ничего не добавляет в словарь: после него в `M` по-прежнему три пары.
- Если при отсутствии ключа нужно сделать что-то другое, а не подставить значение, -- проверка `in` и ветвление.

</div>

</div>

<div class="note">
<code>get()</code> понадобится дважды: для подсчёта (вторая половина пары) и для сложения двух словарей, где ключ есть только в одном из них.
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Методы `keys()`, `values()`, `items()`

<div class="cols-2">

<div>

```python
glucose = {'C': 6, 'H': 12, 'O': 6}
print(list(glucose.keys()))
print(list(glucose.values()))
print(list(glucose.items()))

for element in glucose:
    print(element, end=' ')
print()
for element, n in glucose.items():
    print(f'{element}{n}', end=' ')
print()
print('всего атомов:', sum(glucose.values()))
```

<pre class="output">['C', 'H', 'O']
[6, 12, 6]
[('C', 6), ('H', 12), ('O', 6)]
C H O 
C6 H12 O6 
всего атомов: 24</pre>

</div>

<div>

- `for` по словарю перебирает **ключи**.
- `items()` выдаёт пары-кортежи «ключ, значение». В цикле их распаковывают в два имени, как строки таблицы в [лекции 6](https://vchuzlov.github.io/test-lectures/lec-06/#/16).
- `values()` -- значения: их удобно отдать в `sum()`, `max()`, `min()`.
- `keys()`, `values()` и `items()` возвращают не списки, а «представления» словаря. Их можно перебирать в цикле, а список из них делает `list()`.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Молярная масса по составу

<div class="cols-2">

<div>

```python
M = {'H': 1.008, 'C': 12.011, 'N': 14.007, 'O': 15.999}
nitrate = {'N': 2, 'H': 4, 'O': 3}           # NH4NO3

mass = 0
for element, n in nitrate.items():
    mass += M[element] * n
print(round(mass, 3))

total = sum([M[el] * n for el, n in nitrate.items()])
print(round(total, 3))

w_N = M['N'] * nitrate['N'] / mass * 100
print(f'доля азота: {w_N:.2f} %')
```

<pre class="output">80.043
80.043
доля азота: 35.00 %</pre>

</div>

<div>

- Два словаря: атомные массы и состав вещества. Ключи у них общие -- символы элементов, поэтому `M[element]` находит массу для каждого элемента состава.
- Азот в NH₄NO₃ записан дважды, в составе оба атома посчитаны вместе: `'N': 2`.
- Сумма -- накопителем из [лекции 3](https://vchuzlov.github.io/test-lectures/lec-03/#/10) или генератором списка из [лекции 5](https://vchuzlov.github.io/test-lectures/lec-05/#/41). Результат один.
- Таблицу атомных масс достаточно составить один раз: для селитры, глюкозы и любого другого вещества нужен только состав.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Перевод единиц давления

<div class="cols-2">

<div>

```python
to_Pa = {'Па': 1, 'кПа': 1000, 'бар': 100000,
         'атм': 101325, 'мм рт. ст.': 133.322}

p, unit = 2.5, 'атм'
p_Pa = p * to_Pa[unit]
for u, k in to_Pa.items():
    print(f'{p_Pa / k:12.2f} {u}')
```

<pre class="output">   253312.50 Па
      253.31 кПа
        2.53 бар
        2.50 атм
     1900.01 мм рт. ст.</pre>

</div>

<div>

- Словарь хранит, сколько паскалей в одной единице. Любое давление сначала переводится в паскали, потом в нужную единицу: `p * to_Pa[из] / to_Pa[в]`.
- Пять единиц -- пять пар. Между ними двадцать направлений перевода, и ни одно не надо программировать отдельно.
- Новая единица, например торр, -- одна строка в словаре. Остальная программа не меняется.

</div>

</div>

<div class="note">
Ключ-строка может содержать пробелы и точки: <code>'мм рт. ст.'</code> – такой же ключ, как <code>'Па'</code>.
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Словарь из других объектов

<div class="cols-2">

<div>

```python
symbols = ['H', 'C', 'N', 'O']
masses = [1.008, 12.011, 14.007, 15.999]
M = dict(zip(symbols, masses))
print(M)

print(dict([('Na', 22.990), ('Cl', 35.45)]))
print(dict(H=1.008, O=15.999))
print(list(M), list(M.items())[1])
```

<pre class="output">{'H': 1.008, 'C': 12.011, 'N': 14.007, 'O': 15.999}
{'Na': 22.99, 'Cl': 35.45}
{'H': 1.008, 'O': 15.999}
['H', 'C', 'N', 'O'] ('C', 12.011)</pre>

</div>

<div>

- `dict(zip(ключи, значения))` -- словарь из двух параллельных списков. `zip()` из [лекции 5](https://vchuzlov.github.io/test-lectures/lec-05/#/38) выдаёт пары, `dict()` делает из пар словарь.
- `dict()` от любой последовательности пар -- то же самое.
- `dict(H=1.008)` -- короткая запись, если ключи -- строки, похожие на имена переменных. `'мм рт. ст.'` так не записать.
- В обратную сторону: `list(M)` -- список ключей, `list(M.items())` -- список пар.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Генераторы словарей

> Генератор словаря записывается как генератор множества из [лекции 6](https://vchuzlov.github.io/test-lectures/lec-06/#/28), только на каждом шаге получается пара `ключ: значение`.

<div class="cols-2">

<div>

```python
alkanes = {n: f'C{n}H{2 * n + 2}' for n in range(2, 6)}
print(alkanes)

M = {'H': 1.008, 'C': 12.011, 'N': 14.007,
     'O': 15.999, 'S': 32.06}
print({el: m for el, m in M.items() if m > 14})

by_formula = {f: n for n, f in alkanes.items()}
print(by_formula['C4H10'])
```

<pre class="output">{2: 'C2H6', 3: 'C3H8', 4: 'C4H10', 5: 'C5H12'}
{'N': 14.007, 'O': 15.999, 'S': 32.06}
4</pre>

</div>

<div>

- Первый пример строит словарь «число атомов углерода → формула алкана», как таблица алканов в [лекции 3](https://vchuzlov.github.io/test-lectures/lec-03/#/32), только теперь по ней можно искать.
- Условие `if` после `for` отбирает пары, как в генераторе списка.
- Поменять местами ключ и значение -- обратный словарь «формула → число атомов». Если значения повторяются, останется последний ключ.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Сортировка и поиск по значению

<div class="cols-2">

<div>

```python
Tb = {'вода': 100.0, 'этанол': 78.4,
      'ацетон': 56.1, 'бензол': 80.1}
print(sorted(Tb))
print(sorted(Tb, key=Tb.get))
print(max(Tb, key=Tb.get), max(Tb.values()))

for name in sorted(Tb, key=Tb.get, reverse=True):
    print(f'{name:<8}{Tb[name]:6.1f}')
```

<pre class="output">['ацетон', 'бензол', 'вода', 'этанол']
['ацетон', 'этанол', 'бензол', 'вода']
вода 100.0
вода     100.0
бензол    80.1
этанол    78.4
ацетон    56.1</pre>

</div>

<div>

- `sorted()` от словаря сортирует **ключи**, по алфавиту.
- `Tb.get` -- функция «ключ → значение». Переданная в `key` ([лекция 5](https://vchuzlov.github.io/test-lectures/lec-05/#/27)), она заставляет сравнивать не названия, а температуры кипения.
- `max(Tb, key=Tb.get)` -- ключ с наибольшим значением: **кто** кипит выше всех. `max(Tb.values())` -- само значение: **при какой** температуре.
- Сам словарь при сортировке не меняется.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Ключи словаря как множество

<div class="cols-2">

<div>

```python
lab1 = {'HCl': 2, 'NaOH': 1, 'KOH': 3}
lab2 = {'HCl': 1, 'H2SO4': 2, 'NaOH': 4}
print(sorted(lab1.keys() & lab2.keys()))
print(sorted(lab1.keys() - lab2.keys()))

everything = lab1.keys() | lab2.keys()
total = {k: lab1.get(k, 0) + lab2.get(k, 0)
         for k in sorted(everything)}
print(total)
```

<pre class="output">['HCl', 'NaOH']
['KOH']
{'H2SO4': 2, 'HCl': 3, 'KOH': 3, 'NaOH': 5}</pre>

</div>

<div>

- В двух лабораториях реактивы: название → число банок. Какие есть в обеих, какие только в первой, сколько всего?
- `keys()` поддерживает операции множеств из [лекции 6](https://vchuzlov.github.io/test-lectures/lec-06/#/31): `&`, `|`, `-`, `^`. Ключи и правда ведут себя как множество: они уникальны.
- `values()` таких операций не поддерживает: значения могут повторяться.
- В сумме `get(k, 0)`: реактива, которого в лаборатории нет, там ноль банок.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Методы словаря

<div class="small-table">

|Запись|Что делает|
|-|-|
|`d[k]`|значение по ключу; если ключа нет, `KeyError`|
|`d.get(k)`, `d.get(k, x)`|значение по ключу; если ключа нет, `None` или `x`|
|`k in d`|есть ли ключ `k`|
|`d[k] = v`|добавить пару или заменить значение|
|`del d[k]`, `d.pop(k)`, `d.pop(k, x)`|удалить пару; `pop()` возвращает значение|
|`d.setdefault(k, x)`|ключ `k` есть -- его значение; нет -- добавить пару `k: x` и вернуть `x`|
|`d.update(d2)`, `d \| d2`|дописать пары из `d2`: в `d` на месте / в новый словарь|
|`d.keys()`, `d.values()`, `d.items()`|ключи, значения, пары «ключ, значение»|
|`d.copy()`, `d.clear()`|копия; удалить все пары|

</div>

<div class="cols-2 mt-2">

<div>

```python
M = {'H': 1.008}
print(M.get('C', 12.011), M)
print(M.setdefault('C', 12.011), M)
print(M.setdefault('C', 0.0), M)
```

<pre class="output">12.011 {'H': 1.008}
12.011 {'H': 1.008, 'C': 12.011}
12.011 {'H': 1.008, 'C': 12.011}</pre>

</div>

<div>

- `get()` только читает: углерод в словаре не появился.
- `setdefault()` ключа `'C'` не нашёл и добавил пару. Второй вызов ключ нашёл: вернул старое значение, `0.0` не записан.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Что напечатает эта программа?

Убираем из учёта реактивы, которые закончились:

```python
stock = {'HCl': 2, 'NaOH': 0, 'H2SO4': 1, 'KOH': 0}
for name in stock:
    if stock[name] == 0:
        del stock[name]
print(stock)
```

<v-click>

<div class='output'>RuntimeError: dictionary changed size during iteration</div>

- Цикл перебирает ключи словаря, а `del` в это время меняет число пар. Python останавливает программу на следующем шаге цикла.
- В [лекции 5](https://vchuzlov.github.io/test-lectures/lec-05/#/44) список в той же ситуации молча пропускал элементы. Словарь хотя бы сообщает об ошибке.
- Правильно -- собрать новый словарь или перебирать копию ключей:

```python
stock = {k: v for k, v in stock.items() if v > 0}
print(stock)
```

<div class='output'>{'HCl': 2, 'H2SO4': 1}</div>

</v-click>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

<!--
Сначала спросить зал. Почти все ответят {'HCl': 2, 'H2SO4': 1}. Второй вариант исправления: for name in list(stock): -- перебирается список ключей, а не сам словарь.
-->

---
layout: image-left
class: flex flex-col items-center justify-center
image: /pics/photo_2026-02-19_14-53-38.jpg
---

# Словари внутри словарей

---

# Справочник: словарь словарей

```python
props = {
    'вода':   {'formula': 'H2O',    'M': 18.015, 'Tb': 100.0},
    'этанол': {'formula': 'C2H5OH', 'M': 46.069, 'Tb': 78.4},
    'ацетон': {'formula': 'C3H6O',  'M': 58.080, 'Tb': 56.1},
}
print(props['этанол']['M'])
props['бензол'] = {'formula': 'C6H6', 'M': 78.114, 'Tb': 80.1}
props['вода']['density'] = 0.998
for name, p in props.items():
    print(f"{name:<8}{p['formula']:<8}{p['Tb']:6.1f}")
```

<div class="cols-2">

<div>

<pre class="output">46.069
вода    H2O      100.0
этанол  C2H5OH    78.4
ацетон  C3H6O     56.1
бензол  C6H6      80.1</pre>

</div>

<div>

- Первый ключ -- вещество, второй -- свойство: `props['этанол']['M']`.
- Добавить можно и новое вещество, и новое свойство одному веществу. У именованного кортежа ([лекция 6](https://vchuzlov.github.io/test-lectures/lec-06/#/19)) набор полей задан раз и навсегда.
- В f-строке внешние кавычки двойные: внутри стоят ключи в одинарных.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Ключ -- кортеж или `frozenset`

<div class="cols-2">

<div>

##### Таблица с двумя входами

```python
density = {('вода', 20): 0.998, ('вода', 80): 0.972,
           ('этанол', 20): 0.789, ('этанол', 60): 0.754}
print(density[('этанол', 20)], density['вода', 80])
print([t for name, t in density if name == 'вода'])
```

<pre class="output">0.789 0.972
[20, 80]</pre>

Плотность, г/см³, зависит от вещества и температуры. Ключ -- пара `(вещество, °C)`. В `density['вода', 80]` скобки не нужны: кортеж создаёт запятая ([лекция 6](https://vchuzlov.github.io/test-lectures/lec-06/#/7)).

</div>

<div>

##### Пара без порядка

```python
products = {
    frozenset({'HCl', 'NaOH'}): 'NaCl + H2O',
    frozenset({'AgNO3', 'NaCl'}): 'AgCl + NaNO3',
    frozenset({'BaCl2', 'Na2SO4'}): 'BaSO4 + 2NaCl',
}
print(products[frozenset({'NaOH', 'HCl'})])
pair = frozenset({'NaCl', 'KNO3'})
print(products.get(pair, 'не реагируют'))
```

<pre class="output">NaCl + H2O
не реагируют</pre>

Что получится, если слить два раствора. Порядок веществ не важен, поэтому ключ -- `frozenset` ([лекция 6](https://vchuzlov.github.io/test-lectures/lec-06/#/38)).

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Второе имя и копия

<div class="cols-2">

<div>

```python
stock = {'HCl': 2, 'NaOH': 1}
backup = stock
backup['HCl'] = 0
print(stock)

snapshot = stock.copy()
stock['KOH'] = 5
print(snapshot)
print(stock)
```

<pre class="output">{'HCl': 0, 'NaOH': 1}
{'HCl': 0, 'NaOH': 1}
{'HCl': 0, 'NaOH': 1, 'KOH': 5}</pre>

</div>

<div>

```python
import copy
book = {'вода': {'Tb': 100.0}}
shallow = book.copy()
deep = copy.deepcopy(book)
book['вода']['Tb'] = 99.97
print(shallow['вода'], deep['вода'])
```

<div class='output'>{'Tb': 99.97} {'Tb': 100.0}</div>

</div>

</div>

- Словарь изменяем, и всё сказанное о списках в [лекции 5](https://vchuzlov.github.io/test-lectures/lec-05/#/31) верно и для него: `backup = stock` -- второе имя того же словаря, а не копия.
- `copy()` копирует только внешний словарь. Вложенные словари у копии общие с оригиналом, и правка в справочнике видна через `shallow`. Полная копия -- `copy.deepcopy()`.

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---
layout: image-left
class: flex flex-col items-center justify-center
image: /pics/photo_2026-02-19_14-53-38.jpg
---

# Подсчёт элементов коллекции

---

# Словарь-счётчик

<div class="cols-2">

<div>

```python
found = ['Na+', 'Cl-', 'K+', 'Cl-', 'Na+',
         'Cl-', 'Mg2+', 'SO4 2-', 'Na+', 'Cl-']
counts = {}
for ion in found:
    counts[ion] = counts.get(ion, 0) + 1
print(counts)
print([ion for ion, n in counts.items() if n == 1])
print(max(counts, key=counts.get))
```

<pre class="output">{'Na+': 3, 'Cl-': 4, 'K+': 1, 'Mg2+': 1, 'SO4 2-': 1}
['K+', 'Mg2+', 'SO4 2-']
Cl-</pre>

</div>

<div>

- `found` -- ионы, найденные в десяти пробах воды. Сколько раз встретился каждый?
- `counts.get(ion, 0) + 1`: ион встретился впервые -- ключа ещё нет, `get()` даёт 0, записывается 1. Встретился снова -- к старому счёту прибавляется 1.
- Список проходится **один раз**. В [лекции 6](https://vchuzlov.github.io/test-lectures/lec-06/#/43) `count()` проходил весь список заново для каждого иона.

</div>

</div>

<div class="note">
Ключи счётчика – разные ионы, как в <code>set(found)</code>, но к каждому привязано число. Это и есть таблица «что → сколько раз», которой не хватало множеству.
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>


---

# `Counter`: словарь для подсчёта

<div class="cols-2">

<div>

```python
from collections import Counter

found = ['Na+', 'Cl-', 'K+', 'Cl-', 'Na+',
         'Cl-', 'Mg2+', 'SO4 2-', 'Na+', 'Cl-']
counts = Counter(found)
print(counts)
print(counts['Cl-'], counts['Br-'])
print(counts.most_common(2))

atoms = Counter()
atoms['C'] += 2
atoms['H'] += 6
print(atoms, atoms.total())
```

<pre class="output">Counter({'Cl-': 4, 'Na+': 3, 'K+': 1, 'Mg2+': 1, 'SO4 2-': 1})
4 0
[('Cl-', 4), ('Na+', 3)]
Counter({'H': 6, 'C': 2}) 8</pre>

</div>

<div>

- `Counter` из модуля `collections` -- словарь, у которого отсутствующий ключ даёт **0**, а не `KeyError`. Поэтому `atoms['C'] += 2` работает без `get()`.
- `Counter(список)` считает элементы списка в одну строку: тот же результат, что цикл на предыдущем слайде.
- `most_common(2)` -- два самых частых. Печатается счётчик тоже по убыванию счёта.
- `counts['Br-']` даёт 0, но в счётчик ключ не добавляет.

</div>

</div>

<div class="warn">
<code>Counter('CH3COOH')</code> считает <b>символы</b> строки: <code>C</code>, <code>H</code> и <code>O</code> по два раза и <code>'3'</code> один раз.
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Операции над `Counter`

<div class="cols-2">

<div>

```python
left = Counter({'C': 2, 'H': 6, 'O': 6})
right = Counter({'C': 2, 'H': 6, 'O': 7})
print(left == right)
print(right - left, left - right)
print(left + right)
print(Counter('HHO') + Counter('OO'))
```

<pre class="output">False
Counter({'O': 1}) Counter()
Counter({'O': 13, 'H': 12, 'C': 4})
Counter({'O': 3, 'H': 2})</pre>

</div>

<div class="small-table">

|Запись|Результат|
|-|-|
|`a + b`|сумма счётов|
|`a - b`|разность; только счёты больше 0|
|`a == b`|все счёты равны|
|`a.total()`|сумма всех счётов|
|`a.most_common(k)`|`k` самых частых|

</div>

</div>

- `right - left` -- чего справа больше, чем слева: одного атома кислорода. `left - right` пуст: слева ничего не в избытке. Это ответ не только на вопрос «уравнено ли», но и на вопрос «что не так».
- При сравнении `==` ключ с нулевым счётом и отсутствующий ключ -- одно и то же.

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Что напечатает эта программа?

```python
from collections import Counter
a = Counter({'H': 4, 'O': 2})
b = Counter({'H': 2, 'O': 3})
print(a - b, b - a)
print(len(a - b) + len(b - a))
```

<v-click>

<pre class="output">Counter({'H': 2}) Counter({'O': 1})
2</pre>

- `a - b` по водороду даёт 2, по кислороду -1. Отрицательный и нулевой счёт `Counter` при вычитании **отбрасывает**: в результате остаётся только водород.
- `b - a` по той же причине содержит только кислород.
- Поэтому разницу между двумя сторонами уравнения смотрят в обе стороны: `left - right` и `right - left`.

</v-click>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

<!--
Сначала спросить зал. Частый ответ: Counter({'H': 2, 'O': -1}) и Counter({'H': -2, 'O': 1}), сумма длин 4.
-->

---
layout: image-left
class: flex flex-col items-center justify-center
image: /pics/photo_2026-02-19_14-53-38.jpg
---

# Группировка элементов коллекции

---

# Группировка: словарь списков

<div class="cols-2">

<div>

```python
salts = [('Na+', 'Cl-'), ('K+', 'SO4 2-'),
         ('Na+', 'NO3-'), ('Mg2+', 'Cl-'),
         ('K+', 'Br-'), ('Na+', 'Br-')]
by_cation = {}
for cation, anion in salts:
    if cation not in by_cation:
        by_cation[cation] = []
    by_cation[cation].append(anion)
print(by_cation)
```

<pre class="output">{'Na+': ['Cl-', 'NO3-', 'Br-'], 'K+': ['SO4 2-', 'Br-'], 'Mg2+': ['Cl-']}</pre>

```python
by_cation = {}
for cation, anion in salts:
    by_cation.setdefault(cation, []).append(anion)
print(by_cation['K+'])
```

<div class='output'>['SO4 2-', 'Br-']</div>

</div>

<div>

- Задача: разложить соли по катионам. Ключ -- катион, значение -- **список** анионов.
- Катион встретился впервые -- для него заводится пустой список. Дальше анион дописывается в список этого катиона.
- `setdefault(ключ, [])` делает то же в одну строку: если ключа нет, добавляет пару с пустым списком, и в любом случае возвращает список, в который можно дописывать.
- Счётчик отвечал на вопрос «сколько», группировка -- на вопрос «какие именно».

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Зачем нужен `defaultdict`

<div class="cols-2">

<div>

##### Обычный словарь

```python
groups = {}
groups['Na+'].append('Cl-')
```

<div class='output'>KeyError: 'Na+'</div>

Ключа `'Na+'` нет -- нет и списка, куда дописать анион. Его приходится заводить заранее: проверкой `in` или через `setdefault()`.

</div>

<div>

##### `defaultdict`

```python
from collections import defaultdict
groups = defaultdict(list)
groups['Na+'].append('Cl-')
groups['Na+'].append('Br-')
print(dict(groups))
```

<div class='output'>{'Na+': ['Cl-', 'Br-']}</div>

Ключа нет -- `defaultdict` сам вызывает `list()` и записывает под этот ключ пустой список. В остальном это обычный словарь.

</div>

</div>

<div class="small-table">

| Создание | Новый ключ получает | Зачем |
|---|---|---|
| `defaultdict(list)` | `[]` | группировка: ключ → список |
| `defaultdict(int)` | `0` | подсчёт: `d[k] += 1` |
| `defaultdict(set)` | `set()` | группировка без повторов |

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

<!--
В скобках при создании -- сама функция, без скобок, как key=len в лекции 5: defaultdict вызывает её для каждого нового ключа. list() даёт [], int() даёт 0, set() -- пустое множество.
-->

---

# `defaultdict`: группировка и подсчёт

<div class="cols-2">

<div>

```python
from collections import defaultdict

by_cation = defaultdict(list)
for cation, anion in salts:
    by_cation[cation].append(anion)
print(by_cation['Mg2+'], len(by_cation))
print(dict(by_cation))

counts = defaultdict(int)
for ion in ['Na+', 'Cl-', 'Na+']:
    counts[ion] += 1
print(dict(counts))
```

<pre class="output">['Cl-'] 3
{'Na+': ['Cl-', 'NO3-', 'Br-'], 'K+': ['SO4 2-', 'Br-'], 'Mg2+': ['Cl-']}
{'Na+': 2, 'Cl-': 1}</pre>

</div>

<div>

- Та же группировка солей по катионам, что на слайде со словарём списков, но без проверки `if cation not in ...` и без `setdefault()`.
- `defaultdict(int)` для подсчёта: `counts[ion] += 1` работает и для иона, который встретился впервые, -- его счёт начинается с 0.
- `dict()` превращает его в обычный словарь: так он аккуратнее печатается.

</div>

</div>

<div class="small-table">

| Нужно | Берём |
|---|---|
| найти значение по ключу | `dict` |
| посчитать, сколько раз | `Counter` |
| разложить по группам | `defaultdict(list)` |

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Группировка по составу

Какие вещества состоят из одних и тех же элементов?

<div class="cols-2">

<div>

```python
from collections import defaultdict

formulas = ['H2O', 'CO2', 'CH4', 'H2O2',
            'C2H5OH', 'CO', 'C2H6', 'CH3COOH']
groups = defaultdict(list)
for f in formulas:
    els = frozenset({ch for ch in f if ch.isalpha()})
    groups[els].append(f)

for key in sorted(groups, key=sorted):
    print(sorted(key), groups[key])
```

<pre class="output">['C', 'H'] ['CH4', 'C2H6']
['C', 'H', 'O'] ['C2H5OH', 'CH3COOH']
['C', 'O'] ['CO2', 'CO']
['H', 'O'] ['H2O', 'H2O2']</pre>

</div>

<div>

- Ключ -- набор элементов вещества. Обычное множество ключом быть не может, поэтому `frozenset` ([лекция 6](https://vchuzlov.github.io/test-lectures/lec-06/#/36)).
- Значение -- список веществ с таким набором.
- В [лекции 6](https://vchuzlov.github.io/test-lectures/lec-06/#/40) мы только посчитали, сколько разных наборов. Словарь показывает, какие вещества попали в каждый.
- `key=sorted`: группы печатаются в порядке отсортированных списков элементов, иначе порядок `frozenset` менялся бы от запуска к запуску.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Что напечатает эта программа?

```python
from collections import defaultdict
groups = defaultdict(list)
print('Na+' in groups, len(groups))
if groups['Na+']:
    print('есть соли натрия')
print('Na+' in groups, len(groups))
```

<v-click>

<pre class="output">False 0
True 1</pre>

- `groups['Na+']` в условии `if` только читает, но для `defaultdict` чтение отсутствующего ключа -- уже создание: появилась пара `'Na+': []`.
- Пустой список ложен, поэтому строка про соли натрия не напечаталась. А ключ остался.
- Проверять, есть ли ключ, надо через `in` или `get()`: они ничего не создают. `Counter` в той же ситуации ключ не добавляет.

</v-click>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

<!--
Сначала спросить зал. Почти все ответят False 0 оба раза.
-->

---

# Какую коллекцию выбрать

<div class="small-table">

| Что нужно | Тип | Пример из лекций |
|---|---|---|
| Серия однотипных значений, порядок важен | `list` | массы навесок, серия pH |
| Запись из заданного числа разных полей | `tuple`, `namedtuple` | вещество: название, формула, M |
| Уникальные значения, быстрая проверка «есть ли» | `set` | ионы в растворе |
| Найти значение по имени | `dict` | атомные массы, перевод единиц |
| Посчитать, сколько раз встречается | `Counter` | ионы в пробах, атомы в уравнении |
| Разложить по группам | `defaultdict(list)` | соли по катиону, вещества по составу |
| Ключ из нескольких частей | `tuple`, `frozenset` | (вещество, температура), пара реагентов |

</div>

<div class="note">
Вопрос, с которого начинают: <b>как будут искать данные?</b> По номеру – список или кортеж. По наличию – множество. По имени – словарь.
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Частые ошибки

<ol class="steps">
<li><b>Обращение к ключу, которого нет:</b> <code>KeyError</code>. Если ключа может не быть, – <code>get()</code> или проверка <code>in</code>.</li>
<li><b><code>in</code> по значениям.</b> <code>x in d</code> ищет среди ключей. Среди значений – <code>x in d.values()</code>.</li>
<li><b>Удаление пар во время перебора словаря:</b> <code>RuntimeError</code>. Собрать новый словарь или перебирать <code>list(d)</code>.</li>
<li><b>Список в качестве ключа:</b> <code>TypeError: ... unhashable</code>. Вместо списка – кортеж, вместо множества – <code>frozenset</code>.</li>
<li><b>Копия через <code>=</code>.</b> <code>b = a</code> даёт словарю второе имя. Копия – <code>a.copy()</code>, для вложенных словарей – <code>copy.deepcopy(a)</code>.</li>
<li><b>Проверка <code>defaultdict</code> чтением.</b> <code>if d[k]:</code> создаёт ключ <code>k</code>. Проверять через <code>k in d</code>.</li>
<li><b>Разность счётчиков в одну сторону.</b> <code>a - b</code> отбрасывает отрицательные счёты. Нужна и <code>b - a</code>.</li>
</ol>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---
layout: image-left
image: /pics/photo_2025-11-10_15-42-35.jpg
class: flex flex-col items-center justify-center
---

<LightOrDark>
  <template #dark>
    <img src='./pics/logo_dark.png'>
  </template>
  <template #light>
    <img src='./pics/logo_light.svg'>
  </template>
</LightOrDark>

<br><br><br>

# Благодарю за внимание!
