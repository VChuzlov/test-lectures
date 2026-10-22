---
# ─────────────────────────────────────────────────────────────────────────────
# HEADMATTER -- шапка лекции. Поля title/lecture/topics попадают в оглавление
# сайта (см. tools/build_site.py), поэтому заполняйте их у каждой лекции.
# ─────────────────────────────────────────────────────────────────────────────
routerMode: hash
theme: default
title: Функции
lecture: '08'
topics: функции, def, return, параметры и аргументы, вызов функции, None, несколько результатов, строка документации, локальные переменные, область видимости, изменяемые аргументы, декомпозиция, проверка функций, assert

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

<h2 class="!mt-0">Лекция 8. Функции</h2>

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

# План проверки уравнения

<div class="eqs"><span>C₂H₆ + 3O₂ → 2CO₂ + 3H₂O</span></div>

<div class="lead">
В лекции 7 ошибка в этом уравнении найдена вручную. Задание: записать последовательность действий, по которой уравнение сможет проверить человек, не изучавший химию.
</div>

<v-click>

<ol class="steps">
<li>Разделить уравнение по стрелке на левую и правую части.</li>
<li>Разделить каждую часть по знаку «+» на вещества: C₂H₆ и 3O₂.</li>
<li>Отделить коэффициент от формулы: 3O₂ → 3 и O₂.</li>
<li>Разобрать формулу на элементы: C₂H₆ → C: 2, H: 6.</li>
<li>Сложить атомы каждой части с учётом коэффициентов и сравнить части.</li>
</ol>

<div class="note">
Каждый шаг – отдельная задача с собственным названием. В этой лекции шаги плана становятся функциями, а программа – последовательностью их вызовов.
</div>

</v-click>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

<!--
Дать две минуты, собрать шаги из зала и записать на доске. Чаще всего пропускают шаг 3: коэффициент умножают не на все элементы формулы (3H2O -- это и 6 атомов H, и 3 атома O).
-->

---

# Та же проверка в шесть строк

<div class="cols-2">

<div>

```python
equations = ['CH4 + 2O2 -> CO2 + 2H2O',
             'C2H6 + 3O2 -> 2CO2 + 3H2O',
             'Fe2O3 + 3CO -> 2Fe + 3CO2',
             '4Al + 3O2 -> 2Al2O3',
             '2KClO3 -> 2KCl + 2O2',
             'C3H8 + 5O2 -> 3CO2 + 4H2O']

for eq in equations:
    left, right = eq.split(' -> ')
    if count_atoms(left) == count_atoms(right):
        print('верно ', eq)
    else:
        print('ошибка', eq)
```

</div>

<div>

<pre class="output">верно  CH4 + 2O2 -> CO2 + 2H2O
ошибка C2H6 + 3O2 -> 2CO2 + 3H2O
верно  Fe2O3 + 3CO -> 2Fe + 3CO2
верно  4Al + 3O2 -> 2Al2O3
ошибка 2KClO3 -> 2KCl + 2O2
верно  C3H8 + 5O2 -> 3CO2 + 4H2O</pre>

- Шаг 1 выполняет метод `split(' -> ')` ([лекция 4](https://vchuzlov.github.io/test-lectures/lec-04/#/33)), шаги 2–5 -- функция `count_atoms()`: строка `'2CO2 + 3H2O'` → `Counter` «элемент → число атомов» ([лекция 7](https://vchuzlov.github.io/test-lectures/lec-07/#/29)).
- Функции `count_atoms()` в Python нет; её определение составляется в этой лекции.

</div>

</div>

<div class="note">
Без функций программа занимает около двадцати строк с пятью уровнями вложенности. Каждая функция этой лекции занимает около десяти строк.
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---
layout: image-left
class: flex flex-col items-center justify-center
image: /pics/photo_2026-02-19_14-52-25.jpg
---

# Функции

---

# Три копии одного цикла

<div class="cols-2">

<div>

```python
M = {'H': 1.008, 'C': 12.011, 'N': 14.007,
     'O': 15.999, 'K': 39.098}

total = 0
for el, n in {'N': 2, 'H': 4, 'O': 3}.items():
    total += M[el] * n
print('NH4NO3  ', round(total, 3))

for el, n in {'C': 1, 'O': 1, 'N': 2, 'H': 4}.items():
    total += M[el] * n
print('CO(NH2)2', round(total, 3))

total = 0
for el, n in {'K': 1, 'N': 1, 'O': 3}.items():
    total += M[el] * n
print('KNO3    ', round(total, 3))
```

</div>

<div>

<pre class="output">NH4NO3   80.043
CO(NH2)2 140.099
KNO3     101.102</pre>

Молярные массы трёх удобрений; накопитель из [лекции 7](https://vchuzlov.github.io/test-lectures/lec-07/#/15) скопирован трижды. Один результат неверен. Какой и почему?

<v-click>

- Во второй копии нет строки `total = 0`: к массе селитры прибавлена масса карбамида (верно: 60,056).
- Интерпретатор ошибку не обнаруживает: программа выводит правдоподобное число.
- Решение -- записать цикл один раз, дать ему имя и вызывать по имени.

</v-click>

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

<!--
Сначала спросить зал. Ошибку находят прикидкой: C + O + 2N + 4H = 12 + 16 + 28 + 4 = 60, а не 140. Для четвёртого удобрения потребуется четвёртая копия, а исправление формулы придётся вносить в каждую.
-->

---

# Встроенные функции

<div class="small-table">

| Вызов | Результат | Лекция |
|---|---|---|
| `round(80.0432, 2)` | `80.04` | [1](https://vchuzlov.github.io/test-lectures/lec-01/#/32) |
| `math.sqrt(2)` | `1.4142135623730951` | [1](https://vchuzlov.github.io/test-lectures/lec-01/#/28) |
| `len('C6H12O6')` | `7` | [4](https://vchuzlov.github.io/test-lectures/lec-04/#/8) |
| `sum([2, 6, 1])` | `9` | [5](https://vchuzlov.github.io/test-lectures/lec-05/#/8) |
| `max([6.9, 7.4, 7.1])` | `7.4` | [5](https://vchuzlov.github.io/test-lectures/lec-05/#/8) |
| `sorted({'O', 'C', 'H'})` | `['C', 'H', 'O']` | [6](https://vchuzlov.github.io/test-lectures/lec-06/#/25) |
| `divmod(250, 60)` | `(4, 10)` | [6](https://vchuzlov.github.io/test-lectures/lec-06/#/14) |

</div>

<div class="cols-2 mt-2">

<div>

- Функция имеет **имя**, получает **аргументы** в скобках и **возвращает результат**, который подставляется на место вызова. Аргументов может не быть: `input()`.

</div>

<div>

- Для вызова функции достаточно знать её аргументы и результат; устройство `len()` знать не требуется.
- В лекции рассматриваются функции, определяемые в программе.

</div>

</div>

<div class="note">
<code>masses.sort()</code>, <code>'H2O'.lower()</code> – <b>методы</b>: вызываются через точку у объекта. <code>int()</code>, <code>list()</code>, <code>Counter()</code> – <b>типы</b> (классы): вызов создаёт объект.
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Определение функции: `def`

> Функция -- <span class="text-[var(--brand)]">*именованный фрагмент программы*</span>: получает данные, выполняет действия и возвращает результат.

<div class="cols-2">

<div>

```python
M = {'H': 1.008, 'C': 12.011, 'O': 15.999}

def mass(composition):
    total = 0
    for el, n in composition.items():
        total += M[el] * n
    return total

water = {'H': 2, 'O': 1}
glucose = {'C': 6, 'H': 12, 'O': 6}
print(round(mass(water), 3), round(mass(glucose), 3))
```

<pre class="output">18.015 180.156</pre>

</div>

<div>

<FigDevice class="w-full mt-1" />

- Заголовок: `def`, имя, **параметры** в скобках, двоеточие; тело -- с отступом.
- `return` задаёт результат: вызов `mass(water)` заменяется числом `18.015`.
- `total = 0` выполняется при каждом вызове.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Определение и вызов

<div class="cols-2">

<div>

##### `def` только сохраняет функцию

```python
def dilute(c, k):
    print('считаю...')
    return c / k

print('функция определена')
print(dilute(20, 2))
print(dilute(10, 4))
```

<pre class="output">функция определена
считаю...
10.0
считаю...
2.5</pre>

</div>

<div>

##### Вызов до определения

```python
print(dilute(20, 2))

def dilute(c, k):
    return c / k
```

<div class='output'>NameError: name 'dilute' is not defined</div>

Программа выполняется сверху вниз: при выполнении первой строки оператор `def` ещё не выполнен.

</div>

</div>

- `def` создаёт функцию и связывает её с именем, но тело не выполняет: строка «считаю...» при определении не выводится.
- Тело выполняется при каждом **вызове** -- обращении к имени со скобками.
- Поэтому функции определяют в начале программы.

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Параметры и аргументы

<div class="cols-2">

<div>

```python
def final_conc(c1, v1, v2):
    return c1 * v1 / v2

print(final_conc(20, 50, 200))
print(round(final_conc(96, 10, 250), 2))
print(final_conc(20, 200, 50))
final_conc(20, 50)
```

<pre class="output">5.0
3.84
80.0
TypeError: final_conc() missing 1 required positional argument: 'v2'</pre>

</div>

<div>

- c₁·V₁ = c₂·V₂: 50 мл 20 %-го раствора разбавлены до 200 мл, как в [лекции 3](https://vchuzlov.github.io/test-lectures/lec-03/#/2).
- **Параметры** -- имена в заголовке: `c1`, `v1`, `v2`. **Аргументы** -- значения при вызове: `20`, `50`, `200`.
- Аргументы сопоставляются с параметрами **по порядку**. Перестановка объёмов ошибки не вызывает, но даёт неверный результат: 80 % после разбавления 20 %-го раствора.
- Число аргументов должно совпадать с числом параметров, иначе возникает `TypeError`.

</div>

</div>

<div class="note">
Передача аргументов по имени, <code>final_conc(c1=20, v1=50, v2=200)</code>, при которой порядок не важен, – тема лекции 9.
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Что происходит при вызове

<div class="cols-2">

<div>

```python
def final_conc(c1, v1, v2):
    c2 = c1 * v1 / v2
    return c2

c = round(final_conc(20, 50, 200), 1)
print(c)
```

<div class='output'>5.0</div>

<div class="note mt-6">
Вызов функции – выражение. Его значение можно присвоить переменной, вывести через <code>print()</code> или передать в другую функцию, как здесь в <code>round()</code>.
</div>

</div>

<div>

<ol class="steps">
<li>Вычисляются аргументы: <code>20</code>, <code>50</code>, <code>200</code>. Аргументом может быть любое выражение.</li>
<li>Параметры получают значения по порядку, как при присваивании: <code>c1 = 20</code>, <code>v1 = 50</code>, <code>v2 = 200</code>.</li>
<li>Выполняется тело функции до оператора <code>return</code>.</li>
<li>Значение после <code>return</code> подставляется на место вызова: строка принимает вид <code>c = round(5.0, 1)</code>. Выполнение программы продолжается с места вызова.</li>
</ol>

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Оператор `return`

<div class="cols-2">

<div>

```python
def state(t, t_melt, t_boil):
    if t < t_melt:
        return 'твёрдое'
    if t < t_boil:
        return 'жидкое'
    return 'газ'

print(state(25, 0, 100))          # вода
print(state(25, 80.3, 218.0))     # нафталин
print(state(25, -138.3, -0.5))    # бутан
```

<pre class="output">жидкое
твёрдое
газ</pre>

</div>

<div>

- Агрегатное состояние вещества при 25 °C по температурам плавления и кипения.
- `return` возвращает значение и **сразу завершает** функцию: следующие строки в этом вызове не выполняются.
- Поэтому `elif` и `else` не требуются: при `t < t_melt` функция завершается на первом `return`, второй `if` не выполняется.
- В функции может быть несколько операторов `return`; каждый вызов завершается на одном из них.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Оператор `return` в цикле

<div class="cols-2">

<div>

##### Ошибка отступа

```python
def total_mass(masses):
    total = 0
    for m in masses:
        total += m
        return total          # в теле цикла

print(total_mass([2.512, 2.508, 2.515]))
```

<div class='output'>2.512</div>

`return` записан с отступом цикла и выполняется на первом шаге: функция возвращает массу первой навески. Исправление -- записать `return total` с отступом тела функции, после цикла; тогда результат равен `7.535`.

</div>

<div>

##### Досрочный выход при поиске

```python
def first_acidic(ph_values):
    for i, ph in enumerate(ph_values):
        if ph < 7:
            return i
    return None

print(first_acidic([7.4, 7.1, 6.8, 6.2]))
print(first_acidic([7.4, 7.1]))
```

<pre class="output">2
None</pre>

Номер первой кислой пробы. `return` в цикле завершает функцию при первом найденном значении, как `break` в [лекции 3](https://vchuzlov.github.io/test-lectures/lec-03/#/18), и одновременно возвращает результат. Если цикл завершился без `return`, выполняется последняя строка: `return None`.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Что напечатает эта программа?

```python
def mass_fraction(m_part, m_total):
    print(round(m_part / m_total * 100, 2))

w = mass_fraction(28.014, 80.043)        # азот в NH4NO3
print('доля азота, %:', w)
```

<v-click>

<pre class="output">35.0
доля азота, %: None</pre>

<div class="cols-2">

<div>

- Функция **выводит** результат, но **не возвращает** его: оператора `return` в ней нет. Число выведено на экран, а в переменную `w` записано `None`.
- `None` -- значение «отсутствие значения». Его возвращает любая функция без `return`, в том числе `print()`: `r = print('H2O')` записывает в `r` значение `None`.

</div>

<div>

Исправление: функция возвращает результат, вывод выполняется вне функции.

```python
def mass_fraction(m_part, m_total):
    return m_part / m_total * 100

w = mass_fraction(28.014, 80.043)
print(f'доля азота, %: {w:.2f}')
```

<div class='output'>доля азота, %: 35.00</div>

</div>

</div>

</v-click>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

<!--
Сначала спросить зал. Почти все ответят: 35.0 и «доля азота, %: 35.0». Вывод через print и возвращаемое значение на экране выглядят одинаково; различие обнаруживается, когда результат нужен в следующем расчёте.
-->

---

# Строка документации

<div class="cols-2">

<div>

```python
def final_conc(c1, v1, v2):
    """Концентрация раствора после разбавления, %."""
    return c1 * v1 / v2

print(final_conc.__doc__)
help(final_conc)
```

<pre class="output">Концентрация раствора после разбавления, %.
Help on function final_conc in module __main__:

final_conc(c1, v1, v2)
    Концентрация раствора после разбавления, %.</pre>

</div>

<div>

- Строка документации (docstring) -- строковый литерал в тройных двойных кавычках ([лекция 4](https://vchuzlov.github.io/test-lectures/lec-04/#/4)), записанный первой строкой тела функции.
- Интерпретатор сохраняет её в атрибуте функции `__doc__`.
- `help()` выводит заголовок функции и строку документации. В Spyder та же справка выводится на панели Help по сочетанию Ctrl+I (курсор на имени функции).

</div>

</div>

<div class="note">
Комментарий <code>#</code> поясняет, как работает отдельная строка кода. Строка документации описывает, что делает функция и как её вызывать.
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Содержание строки документации

<div class="cols-2">

<div class="code-sm">

```python
def final_conc(c1, v1, v2):
    """Концентрация раствора после разбавления.

    Parameters
    ----------
    c1 : float
        Концентрация исходного раствора, %.
    v1 : float
        Объём исходного раствора, мл.
    v2 : float
        Объём раствора после разбавления, мл.

    Returns
    -------
    float
        Концентрация после разбавления, %.

    Examples
    --------
    >>> final_conc(20, 50, 200)
    5.0
    """
    return c1 * v1 / v2
```

</div>

<div>

- Первая строка -- назначение функции одним предложением; после пустой строки -- подробности.
- Разделы (названия -- на английском): `Parameters` -- параметры, типы, единицы измерения; `Returns` -- возвращаемое значение; `Examples` -- вызов (строка с `>>>`) и результат.
- Это соглашение numpydoc. По нему документированы NumPy и SciPy; Spyder выводит такие строки на панели Help в отформатированном виде.
- Короткой функции достаточно одной строки с описанием и примером.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Несколько результатов

<div class="cols-2">

<div>

```python
def split_coef(term):
    """Отделяет коэффициент: '3O2' -> (3, 'O2')."""
    digits = ''
    for ch in term:
        if not ch.isdigit():
            break
        digits += ch
    formula = term[len(digits):]
    if digits:
        return int(digits), formula
    return 1, formula

print(split_coef('3O2'), split_coef('CH4'))
print(split_coef('25O2'), split_coef('25'))
k, formula = split_coef('3O2')
print(k, formula)
```

<pre class="output">(3, 'O2') (1, 'CH4')
(25, 'O2') (25, '')
3 O2</pre>

</div>

<div>

- Шаг 3 плана: отделение коэффициента от формулы.
- Число повторений известно заранее -- длина строки, поэтому используется цикл `for` ([лекция 3](https://vchuzlov.github.io/test-lectures/lec-03/#/38)). `break` завершает цикл на первом символе, который не является цифрой ([лекция 3](https://vchuzlov.github.io/test-lectures/lec-03/#/18)).
- Срез `term[len(digits):]` -- формула без коэффициента. Строка из одних цифр ошибки не вызывает: формула в этом случае пустая.
- `return int(digits), formula` возвращает **кортеж** из двух значений: кортеж создаёт запятая ([лекция 6](https://vchuzlov.github.io/test-lectures/lec-06/#/7)). Кортеж распаковывается в два имени, как результат `divmod()` ([лекция 6](https://vchuzlov.github.io/test-lectures/lec-06/#/14)).

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

<!--
Коэффициент 25 -- из уравнения горения октана: 2C8H18 + 25O2 -> 16CO2 + 18H2O.
-->

---

# Имя функции

<div class="cols-2">

<div>

- Правила те же, что для переменных ([лекция 1](https://vchuzlov.github.io/test-lectures/lec-01/#/12)): строчные буквы, цифры, `_`, первый символ -- не цифра.
- Имя описывает, **что функция возвращает** или **какое действие выполняет**: `mass`, `final_conc`, `split_coef`, `count_atoms`.
- Функция, возвращающая `True` или `False`, называется утверждением: `is_balanced()`.
- Неинформативные имена: `f`, `calc`, `func1`.

</div>

<div>

##### Имя занято другим значением

```python
sum = 0
for m in [2.512, 2.508]:
    sum += m
print(sum([1, 2]))
```

<div class='output'>TypeError: 'float' object is not callable</div>

```python
def dilute(c, k):
    return c / k

dilute = dilute(20, 2)      # имени присвоено число
print(dilute(10, 4))
```

<div class='output'>TypeError: 'float' object is not callable</div>

</div>

</div>

<div class="warn">
<code>def</code> создаёт переменную, значение которой – функция. После присваивания этому имени другого значения функция недоступна. Так же переопределяются встроенные <code>sum</code>, <code>max</code>, <code>min</code>, <code>len</code>.
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---
layout: image-left
class: flex flex-col items-center justify-center
image: /pics/photo_2026-02-19_14-52-25.jpg
---

# Переменные внутри функции

---

# Локальные переменные

<div class="cols-2">

<div>

```python
M = {'H': 1.008, 'O': 15.999}

def mass(composition):
    total = 0
    for el, n in composition.items():
        total += M[el] * n
    return total

water = {'H': 2, 'O': 1}
print(round(mass(water), 3))
print(total)
```

<pre class="output">18.015
NameError: name 'total' is not defined</pre>

</div>

<div>

- Переменные, созданные внутри функции, -- **локальные**. `total`, `el`, `n` и параметр `composition` создаются при вызове и удаляются после `return`.
- Вне функции они недоступны: после вызова переменной `total` не существует. За пределы функции передаётся только значение после `return`.
- При каждом вызове локальные переменные создаются заново, поэтому ошибка слайда «Три копии одного цикла» внутри функции невозможна.

</div>

</div>

<div class="note">
Функцию можно сравнить с прибором в закрытом корпусе: связь с программой – аргументы на входе и <code>return</code> на выходе.
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Что напечатает эта программа?

```python
c = 20.0                      # концентрация в колбе, %

def dilute(c, k):
    c = c / k
    return c

print(dilute(c, 4), c)
print(dilute(dilute(c, 2), 2))
```

<v-click>

<pre class="output">5.0 20.0
5.0</pre>

- Параметр `c` -- локальная переменная функции. Внешняя переменная `c` -- другая переменная с тем же именем.
- При вызове локальная `c` получила значение `20.0`, внутри функции -- `5.0`. Внешняя `c` не изменилась.
- Во второй строке результат внутреннего вызова (`10.0`) -- аргумент внешнего. Чтобы изменить внешнюю `c`, результат присваивают явно: `c = dilute(c, 4)`.

</v-click>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

<!--
Сначала спросить зал. Частый ответ: 5.0 5.0 в первой строке (раз внутри c изменилась, то и снаружи).
-->

---

# Чтение и присваивание внешних переменных

<div class="cols-2">

<div>

##### Чтение внешней переменной

```python
M = {'H': 1.008, 'O': 15.999}

def water_mass(n):
    return n * (2 * M['H'] + M['O'])

print(round(water_mass(5), 3))
```

<div class='output'>90.075</div>

У функции нет собственной переменной `M`, поэтому интерпретатор ищет её вне функции. Так используют таблицы и константы.

</div>

<div>

##### Присваивание внешней переменной

```python
calls = 0

def water_mass(n):
    calls += 1
    return n * 18.015

water_mass(5)
```

<div class='output'>UnboundLocalError: cannot access local variable 'calls' where it is not associated with a value</div>

Присваивание делает имя `calls` локальным во всей функции, и `+=` обращается к локальной `calls`, у которой ещё нет значения.

</div>

</div>

<div class="note">
Оператор <code>global calls</code> разрешает изменять внешнюю переменную, однако связывает функцию с остальной программой. Рекомендуемый способ: данные передаются через параметры, результат – через <code>return</code>.
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Изменяемый аргумент

<div class="cols-2">

<div>

```python
def add_sample(series, value):
    series.append(value)

def reset(series):
    series = []

masses = [2.512, 2.508]
add_sample(masses, 2.515)
reset(masses)
print(masses)
```

<div class='output'>[2.512, 2.508, 2.515]</div>

</div>

<div>

- Параметр получает **тот же объект**, что и аргумент: `series` -- второе имя списка `masses`, как `b = a` в [лекции 5](https://vchuzlov.github.io/test-lectures/lec-05/#/31).
- Метод `append()` изменяет сам список, поэтому новое значение видно и вне функции.
- `series = []` -- присваивание: локальное имя связывается с новым списком, список `masses` не изменяется.
- Числа, строки и кортежи неизменяемы, для них такой ситуации не возникает.

</div>

</div>

<div class="note">
Функция, изменяющая аргумент, указывает это в строке документации и возвращает <code>None</code>, как метод <code>sort()</code>. В остальных случаях функция работает с копией.
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Что напечатает эта программа?

```python
def hydrate(composition, n):
    """Состав кристаллогидрата с n молекулами воды."""
    composition['H'] = composition.get('H', 0) + 2 * n
    composition['O'] = composition.get('O', 0) + n
    return composition

cuso4 = {'Cu': 1, 'S': 1, 'O': 4}
vitriol = hydrate(cuso4, 5)          # CuSO4·5H2O, медный купорос
print(vitriol)
print(cuso4)
```

<v-click>

<div class="cols-2">

<div>

<pre class="output">{'Cu': 1, 'S': 1, 'O': 9, 'H': 10}
{'Cu': 1, 'S': 1, 'O': 9, 'H': 10}</pre>

Оператор `is` ([лекция 4](https://vchuzlov.github.io/test-lectures/lec-04/#/11)) подтверждает, что функция вернула тот же объект:

```python
print(vitriol is cuso4)
```

<div class='output'>True</div>

</div>

<div>

- `composition` -- второе имя словаря `cuso4`. Функция дописала воду в исходный словарь безводного сульфата меди, а `return` вернул этот же словарь.
- Исправление -- первой строкой тела создать копию ([лекция 7](https://vchuzlov.github.io/test-lectures/lec-07/#/26)) и работать с ней: `composition = composition.copy()`.

</div>

</div>

</v-click>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

<!--
Сначала спросить зал. Почти все ответят, что cuso4 остался {'Cu': 1, 'S': 1, 'O': 4}.
-->

---
layout: image-left
class: flex flex-col items-center justify-center
image: /pics/photo_2026-02-19_14-52-25.jpg
---

# Разбиение задачи на функции

---

# Проектирование сверху вниз

План со слайда 2 преобразуется в функции. Каждая функция решает одну задачу и вызывает функции следующего уровня.

<div class="tree">
<span><b>is_balanced</b>('C2H6 + 3O2 -> 2CO2 + 3H2O')</span><i>шаги 1 и 5: разделить по стрелке, сравнить</i>
<span>└── <b>count_atoms</b>('C2H6 + 3O2')</span><i>шаги 2 и 5: разделить по «+», сложить атомы</i>
<span>    ├── <b>split_coef</b>('3O2') → (3, 'O2')</span><i>шаг 3: отделить коэффициент</i>
<span>    └── <b>parse_formula</b>('C2H6') → C: 2, H: 6</span><i>шаг 4: разобрать формулу</i>
<span>        ├── <b>split_elements</b>('C2H6') → ['C2', 'H6']</span><i>разделить формулу на элементы</i>
<span>        └── <b>split_symbol</b>('C2') → ('C', 2)</span><i>отделить индекс от символа</i>
</div>

<div class="cols-2">

<div>

- Сначала записывается верхний уровень: программа составляется так, будто нужные функции уже определены. Так составлена программа на слайде 3.
- Затем определяется каждая функция следующего уровня.

</div>

<div>

- Каждую функцию можно составить, выполнить и проверить отдельно от остальных.
- `split_coef()` определена на слайде 16. Остаются пять функций.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Что напечатает эта программа?

```python
def report(c1, v1, v2):
    c2 = final_conc(c1, v1, v2)
    return f'{c1} % -> {c2} %'

def final_conc(c1, v1, v2):
    return c1 * v1 / v2

print(report(20, 50, 200))
```

<v-click>

<div class='output'>20 % -> 5.0 %</div>

- Ошибки нет, хотя `report()` вызывает функцию, определённую ниже. При выполнении `def report` тело только сохраняется. Имя `final_conc` ищется при **выполнении** тела, то есть при вызове `report()` в последней строке; к этому моменту выполнены оба оператора `def`.
- Если бы вызов стоял между двумя `def`, возникла бы ошибка:

<div class='output'>NameError: name 'final_conc' is not defined</div>

- Поэтому функции можно записывать в порядке плана: сначала функцию верхнего уровня, затем вспомогательные. Требуется только, чтобы все `def` были выполнены до первого вызова.

</v-click>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

<!--
Сначала спросить зал. Частый ответ: NameError, потому что final_conc определена позже report. Связать со слайдом «Определение и вызов»: там вызов стоял раньше def, здесь -- позже.
-->

---

# Разбор формулы на элементы

<div class="crumb">is_balanced → count_atoms → parse_formula → <b>split_elements</b></div>

<div class="cols-2">

<div>

```python
def split_elements(formula):
    """Элементы: 'KClO3' -> ['K', 'Cl', 'O3']."""
    parts = []
    for ch in formula:
        if ch.isupper():     # новый элемент
            parts.append(ch)
        else:                # строчная буква или цифра
            parts[-1] += ch
    return parts

print(split_elements('KClO3'))
print(split_elements('Fe2O3'), split_elements('C3H8'))
```

<pre class="output">['K', 'Cl', 'O3']
['Fe2', 'O3'] ['C3', 'H8']</pre>

</div>

<div>

- Символ элемента начинается с заглавной буквы; по этому признаку формула делится на части.
- Метод `isupper()` проверяет, является ли символ заглавной буквой. Он относится к той же группе методов строк, что `isdigit()` и `isalpha()` ([лекция 4](https://vchuzlov.github.io/test-lectures/lec-04/#/35)).
- Строчная буква (`Cl`, `Fe`) или цифра индекса присоединяется к последнему элементу списка: `parts[-1] += ch`.
- Функция не обрабатывает ни коэффициенты, ни числа атомов: она только делит формулу на части.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Состав вещества

<div class="crumb">is_balanced → count_atoms → <b>parse_formula</b> → split_elements, <b>split_symbol</b></div>

<div class="cols-2">

<div>

```python
def split_symbol(part):
    """Символ и индекс: 'O3' -> ('O', 3)."""
    symbol = ''
    digits = ''
    for ch in part:
        if ch.isdigit():
            digits += ch
        else:
            symbol += ch
    if digits:
        return symbol, int(digits)
    return symbol, 1

print(split_symbol('O3'), split_symbol('Cl'))
```

<div class='output'>('O', 3) ('Cl', 1)</div>

</div>

<div>

```python
from collections import Counter

def parse_formula(formula):
    """Состав вещества: 'C2H6' -> C: 2, H: 6."""
    atoms = Counter()
    for part in split_elements(formula):
        symbol, n = split_symbol(part)
        atoms[symbol] += n
    return atoms

print(parse_formula('C2H6'))
print(parse_formula('CH3COOH'))
```

<pre class="output">Counter({'H': 6, 'C': 2})
Counter({'H': 4, 'C': 2, 'O': 2})</pre>

</div>

</div>

- `split_symbol()`: буквы накапливаются в `symbol`, цифры -- в `digits`; без индекса атом один.
- `parse_formula()` (шаг 4) вызывает `split_symbol()` для каждой части формулы и складывает атомы в `Counter` ([лекция 7](https://vchuzlov.github.io/test-lectures/lec-07/#/29)).

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Состав стороны уравнения

<div class="crumb">is_balanced → <b>count_atoms</b> → split_coef, parse_formula</div>

<div class="cols-2">

<div>

```python
def count_atoms(side):
    """Атомы: '2CO2 + 3H2O' -> O: 7, H: 6, C: 2."""
    atoms = Counter()
    for term in side.split(' + '):
        k, formula = split_coef(term)
        for symbol, n in parse_formula(formula).items():
            atoms[symbol] += k * n
    return atoms

print(count_atoms('C2H6 + 3O2'))
print(count_atoms('2CO2 + 3H2O'))
```

<pre class="output">Counter({'H': 6, 'O': 6, 'C': 2})
Counter({'O': 7, 'H': 6, 'C': 2})</pre>

</div>

<div>

- Шаги 2 и 5 плана: сторона делится по знакам «+», атомы каждого вещества умножаются на коэффициент и складываются.
- Шаги 3 и 4 выполняют ранее определённые функции `split_coef()` и `parse_formula()`.
- Внутри функции два уровня циклов вместо пяти: перебор символов формулы выполняется в `split_elements()` и `split_symbol()`.
- Слева 6 атомов кислорода, справа 7. Ту же разницу в лекции 7 определили вручную.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Проверка функций на эталонных примерах

<div class="cols-wide">

<div>

```python
assert split_coef('3O2') == (3, 'O2')
assert split_elements('KClO3') == ['K', 'Cl', 'O3']
assert split_symbol('O3') == ('O', 3)
assert parse_formula('C2H6') == {'C': 2, 'H': 6}
assert count_atoms('2CO2 + 3H2O') == {'C': 2, 'O': 7, 'H': 6}
print('все проверки пройдены')
```

<div class='output'>все проверки пройдены</div>

```python
assert count_atoms('CuSO4·5H2O') == {'Cu': 1, 'S': 1,
                                     'O': 9, 'H': 10}
```

<div class='output'>AssertionError</div>

</div>

<div>

- Функцию проверяют на примерах с известным результатом, как прибор -- по стандартному образцу.
- `assert условие`: истинное условие пропускается, ложное останавливает программу с `AssertionError`.
- `Counter` равен словарю с теми же парами.
- Проверки выполняют после каждого изменения функций.

</div>

</div>

<div class="note">
Последняя проверка не пройдена: состав медного купороса определяется неверно (слайд 32).
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Проверка шести уравнений

<div class="crumb"><b>is_balanced</b> → count_atoms → split_coef, parse_formula</div>

<div class="cols-2">

<div>

```python
def is_balanced(equation):
    """Баланс атомов: 'H2 + Cl2 -> 2HCl' -> True."""
    left, right = equation.split(' -> ')
    return count_atoms(left) == count_atoms(right)

for eq in equations:
    if is_balanced(eq):
        print('верно ', eq)
    else:
        print('ошибка', eq)
```

<pre class="output">верно  CH4 + 2O2 -> CO2 + 2H2O
ошибка C2H6 + 3O2 -> 2CO2 + 3H2O
верно  Fe2O3 + 3CO -> 2Fe + 3CO2
верно  4Al + 3O2 -> 2Al2O3
ошибка 2KClO3 -> 2KCl + 2O2
верно  C3H8 + 5O2 -> 3CO2 + 4H2O</pre>

</div>

<div>

- `is_balanced()` -- верхний уровень плана: шаг 1 и сравнение частей. Программа со слайда 3 получила все необходимые функции.
- При проверке шести уравнений функция `parse_formula()` вызывается 22 раза, а определена один раз.
- Разность составов, как в [лекции 7](https://vchuzlov.github.io/test-lectures/lec-07/#/30), показывает элемент, по которому уравнение не сходится:

```python
left, right = equations[1].split(' -> ')
print(count_atoms(right) - count_atoms(left))
```

<div class='output'>Counter({'O': 1})</div>

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Данные изменились: кристаллогидраты

<div class="cols-2">

<div>

```python
print(count_atoms('CuSO4·5H2O'))
```

<div class='output'>Counter({'O·': 45, 'H': 2, 'Cu': 1, 'S': 1, 'O': 1})</div>

Точка не является заглавной буквой, и `split_elements()` присоединила её к части `'O4·5'`, из которой `split_symbol()` выделила «элемент» `O·` с индексом 45.

```python
def count_atoms(side):
    """Атомы: '2CO2 + 3H2O' -> O: 7, H: 6, C: 2."""
    side = side.replace('·', ' + ')   # кристаллогидрат
    atoms = Counter()
    ...                               # без изменений
```

</div>

<div>

```python
eq = 'CuSO4·5H2O -> CuSO4 + 5H2O'
print(is_balanced(eq))
print(count_atoms('CuSO4·5H2O'))
```

<pre class="output">True
Counter({'H': 10, 'O': 9, 'Cu': 1, 'S': 1})</pre>

- По числу атомов CuSO₄·5H₂O равнозначен CuSO₄ + 5H₂O. Исправление -- одна строка в одной функции.
- Остальные функции не изменились. Шесть уравнений проверяются с прежним результатом, все проверки на эталонных примерах проходят.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

<!--
Обезвоживание медного купороса при нагревании -- школьный опыт: синие кристаллы превращаются в белый порошок. Без функций такую правку пришлось бы вносить в каждую копию цикла разбора.
-->

---

# Те же функции -- новая задача

<div class="cols-2">

<div>

```python
M = {'H': 1.008, 'C': 12.011, 'N': 14.007,
     'O': 15.999, 'S': 32.06, 'K': 39.098,
     'Cu': 63.546}

def molar_mass(formula):
    """Молярная масса, г/моль: 'H2O' -> 18.015."""
    return mass(count_atoms(formula))

for f in ['H2O', 'NH4NO3', 'KNO3', 'CuSO4·5H2O']:
    print(f'{f:<11}{molar_mass(f):8.3f}')
```

<pre class="output">H2O          18.015
NH4NO3       80.043
KNO3        101.102
CuSO4·5H2O  249.677</pre>

</div>

<div>

- `molar_mass()` состоит из вызовов двух определённых ранее функций: `count_atoms()` определяет состав вещества, `mass()` со слайда 7 суммирует атомные массы по таблице `M`.
- `count_atoms()` составлена для уравнений, но применима и к отдельному веществу, и к кристаллогидрату.
- Таблица `M` дополнена элементами N, S, K и Cu; функция `mass()` читает её при каждом вызове.

</div>

</div>

<div class="note">
Формулы со скобками, например CO(NH₂)₂, функции разбора не поддерживают. Для их поддержки потребуется изменить только функции разбора формулы; остальные функции программы не изменятся.
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Когда выделять функцию

<div class="small-table">

| Признак | Пример из лекции |
|---|---|
| Фрагмент кода требуется повторно | молярная масса трёх удобрений |
| Фрагмент выполняет действие, которое можно кратко назвать | «отделить коэффициент», «разобрать формулу» |
| Фрагмент можно проверить на примере с известным результатом | `parse_formula('C2H6')` → C: 2, H: 6 |
| Вложенность больше двух уровней | перебор символов формулы внутри перебора веществ |
| Функция не помещается на экран | разделить на функции по шагам плана |

</div>

<div class="cols-2 mt-3">

<div>

- Функция выполняет одну задачу, и её имя описывает эту задачу. Если описание функции содержит союз «и», функцию, как правило, следует разделить.
- Расчёт выполняется в функциях, ввод и вывод -- вне их. Тогда расчётную функцию можно вызвать из любой программы.

</div>

<div>

- Функции позволяют повторять расчёт без копирования кода, вносить исправления в одном месте, заменять подробности именем и проверять программу по частям.
- Программа, разбитая на функции, повторяет план решения: `is_balanced()` выполняет шаги 1–5 со слайда 2.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Частые ошибки

<ol class="steps">
<li><b><code>print</code> вместо <code>return</code>.</b> Функция выводит результат, но возвращает <code>None</code>. Расчёт – через <code>return</code>, вывод – вне функции.</li>
<li><b>Обращение к функции без скобок.</b> <code>mass</code> – сама функция, <code>mass(water)</code> – результат её вызова. Условие <code>if is_balanced:</code> всегда истинно.</li>
<li><b>Вызов до <code>def</code>:</b> <code>NameError</code>. Все операторы <code>def</code> должны быть выполнены до первого вызова.</li>
<li><b>Неверное число аргументов:</b> <code>TypeError: ... missing ... argument</code>. Неверный порядок аргументов ошибки не вызывает, но даёт неверный результат.</li>
<li><b><code>return</code> в теле цикла.</b> Функция завершается на первом шаге цикла. Проверить отступ <code>return</code>.</li>
<li><b>Присваивание внешней переменной внутри функции:</b> <code>UnboundLocalError</code>. Данные передаются через параметры, результат – через <code>return</code>.</li>
<li><b>Изменение списка или словаря, переданного аргументом.</b> Если исходный объект нужен вызывающей программе, функция работает с копией.</li>
<li><b>Имя встроенной функции для переменной:</b> <code>sum = 0</code>, затем <code>sum(...)</code> – <code>TypeError: ... not callable</code>.</li>
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
