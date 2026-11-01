---
# ─────────────────────────────────────────────────────────────────────────────
# HEADMATTER -- шапка лекции. Поля title/lecture/topics попадают в оглавление
# сайта (см. tools/build_site.py), поэтому заполняйте их у каждой лекции.
# ─────────────────────────────────────────────────────────────────────────────
routerMode: hash
theme: default
title: 'Функции: передача аргументов и lambda-выражения'
lecture: '09'
topics: именованные аргументы, значения по умолчанию, изменяемое значение по умолчанию, аннотации типов, *args, **kwargs, распаковка при вызове, параметры только по имени, функция как аргумент, lambda

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

<h2 class="!mt-0">Лекция 9. Функции: передача аргументов и lambda-выражения</h2>

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

# Объём газа при разных условиях

Какой объём занимают 2 моль углекислого газа?

<div class="conds">
<span><b>а</b>н. у.: 0 °C, 101,3 кПа</span>
<span><b>б</b>25 °C, 101,3 кПа</span>
<span><b>в</b>25 °C, 202,6 кПа</span>
</div>

<v-click>

<div class="cols-2 mt-4">

<div>

- а) 2 · 22,4 = **44,8 л** -- молярный объём газа при нормальных условиях известен из школьного курса химии.
- б) **48,9 л**, в) **24,5 л** -- по уравнению Менделеева–Клапейрона pV = nRT, откуда V = nRT/p.

</div>

<div>

<div class="note">
Три расчёта различаются только значениями T и p. Нормальные условия встречаются чаще других, поэтому в программе их удобно задать заранее, а при вызове указывать только то, что от них отличается.
</div>

</div>

</div>

</v-click>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

<!--
Дать две минуты. Пункт а) решают почти все, для пунктов б) и в) нужно вспомнить уравнение из курса физики 10 класса и перевести температуру в кельвины.
-->

---

# Та же задача в три вызова

<div class="cols-2">

<div>

```python
R = 8.314                     # Дж/(моль·К)

def gas_volume(n, T=273.15, p=101325):
    """Объём газа, л: pV = nRT."""
    return n * R * T / p * 1000

print(round(gas_volume(2), 1))
print(round(gas_volume(2, T=298.15), 1))
print(round(gas_volume(2, T=298.15, p=202650), 1))
```

<pre class="output">44.8
48.9
24.5</pre>

</div>

<div>

- В заголовке функции у параметров `T` и `p` указаны **значения по умолчанию** -- нормальные условия. Если аргумент не передан, используется это значение.
- При вызове аргументы `T` и `p` указаны **по имени**: из записи видно, какое значение к какому параметру относится.
- Множитель 1000 переводит кубические метры в литры.

</div>

</div>

<div class="note">
Значения по умолчанию, вызов по имени, произвольное число аргументов и функции, которые передают другим функциям, – темы этой лекции.
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---
layout: image-left
class: flex flex-col items-center justify-center
image: /pics/photo_2026-02-19_14-53-38.jpg
---

# Именованные аргументы

---

# Позиционные и именованные аргументы

<!-- <div class="cols-2"> -->

<!-- <div> -->

```python
def final_conc(c1, v1, v2):
    return c1 * v1 / v2

print(final_conc(20, 50, 200))
print(final_conc(c1=20, v1=50, v2=200))
print(final_conc(v2=200, c1=20, v1=50))
print(final_conc(20, v2=200, v1=50))
```

<pre class="output">5.0
5.0
5.0
5.0</pre>

<!-- </div> -->

<!-- <div> -->

- **Позиционный аргумент** сопоставляется с параметром по порядку: первый -- с первым.
- **Именованный аргумент** записывается как `имя=значение` и сопоставляется с параметром по имени. Порядок именованных аргументов значения не имеет.
- Оба способа можно сочетать: сначала позиционные, затем именованные.
- Ошибка со слайда 9 [лекции 8](https://vchuzlov.github.io/test-lectures/lec-08/#/9) -- перестановка объёмов -- при вызове по имени исключена.

<!-- </div> -->

<!-- </div> -->

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Именованные аргументы встроенных функций

<div class="small-table">

| Вызов | Результат | Назначение параметра |
|---|---|---|
| `print('H2O', 'CO2', sep=', ')` | `H2O, CO2` | `sep` -- разделитель выводимых значений |
| `round(2.4664, ndigits=2)` | `2.47` | `ndigits` -- число знаков после запятой |
| `sorted([7.4, 6.9, 7.1], reverse=True)` | `[7.4, 7.1, 6.9]` | `reverse` -- упорядочение по убыванию |
| `max([], default=0)` | `0` | `default` -- результат, если элементов нет |

</div>

<div class="cols-2 mt-3">

<div>

```python
help(print)
```

<pre class="output">Help on built-in function print in module builtins:

print(*args, sep=' ', end='\n', file=None, flush=False)
    Prints the values to a stream, or to sys.stdout by default.</pre>

</div>

<div>

- `end=' '` в `print()` ([лекция 3](https://vchuzlov.github.io/test-lectures/lec-03/#/11)) и `reverse=True` в `sorted()` ([лекция 5](https://vchuzlov.github.io/test-lectures/lec-05/#/25)) -- именованные аргументы.
- Имена параметров и значения по умолчанию указаны в справке: `help()` или панель Help в Spyder (Ctrl+I).

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

<!--
Справка print() выведена не полностью: показаны заголовок и первая строка описания. Запись *args в заголовке -- тема второй половины лекции.
В таблице только функции. Именованные аргументы принимают и методы (метод split() строки: sep=';'), и типы (enumerate -- класс: start=1), но на этом слайде они не показываются, чтобы не смешивать понятия.
-->

---

# Правила записи вызова

<div class="cols-2">

<div>

##### Позиционный аргумент после именованного

```python
final_conc(c1=20, 50, 200)
```

<div class='output'>SyntaxError: positional argument follows keyword argument</div>

##### Два значения одному параметру

```python
final_conc(20, 50, c1=20)
```

<div class='output'>TypeError: final_conc() got multiple values for argument 'c1'</div>

</div>

<div>

##### Неизвестное имя параметра

```python
final_conc(20, 50, V2=200)
```

<div class='output'>TypeError: final_conc() got an unexpected keyword argument 'V2'. Did you mean 'v2'?</div>

- Позиционные аргументы записываются перед именованными.
- Позиционный аргумент `20` уже связан с `c1`, поэтому `c1=20` -- второе значение того же параметра.
- Имя аргумента должно совпадать с именем параметра, включая регистр букв. Подсказка «Did you mean» выводится начиная с Python 3.13.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Что напечатает эта программа?

```python
def final_conc(c1, v1, v2):
    return c1 * v1 / v2

print(final_conc(20, v2=50, v1=200))
```

<v-click>

<div class='output'>80.0</div>

- Позиционный аргумент `20` связан с `c1`. Именованные аргументы связаны по именам: `v1 = 200`, `v2 = 50`.
- Порядок именованных аргументов в вызове значения не имеет: `v2=50` записан раньше `v1=200`, но это не делает 50 объёмом `v1`.
- Результат 20 · 200 / 50 = 80 соответствует концентрированию раствора, а не разбавлению: имена аргументов в вызове нужно сверять с их смыслом.

</v-click>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

<!--
Сначала спросить зал. Частый ответ: 5.0 -- по привычке аргументы сопоставляют по порядку записи.
-->

---
layout: image-left
class: flex flex-col items-center justify-center
image: /pics/photo_2026-02-19_14-53-38.jpg
---

# Значения по умолчанию

---

# Параметры со значениями по умолчанию

<div class="cols-2">

<div>

```python
def gas_volume(n, T=273.15, p=101325):
    """Объём газа, л: pV = nRT."""
    return n * R * T / p * 1000

print(round(gas_volume(2), 2))
print(round(gas_volume(2, 298.15), 2))
print(round(gas_volume(2, p=202650), 2))
```

<pre class="output">44.83
48.93
22.41</pre>

</div>

<div>

<FigKnobs class="w-full mt-1" />

</div>

</div>

- `n` -- **обязательный** параметр, `T` и `p` -- **необязательные**: при отсутствии аргумента используется значение из заголовка.
- Чтобы изменить давление, оставив температуру по умолчанию, `p` передают по имени: позиционный аргумент на втором месте был бы температурой.
- Значение по умолчанию можно сравнить с заводской настройкой прибора: её меняют только при необходимости.

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Порядок параметров в заголовке

<!-- <div class="cols-2"> -->

<!-- <div> -->

```python
def gas_volume(T=273.15, n, p=101325):
    return n * R * T / p * 1000
```

<div class='output'>SyntaxError: parameter without a default follows parameter with a default</div>

```python
help(round)
```

<pre class="output">Help on built-in function round in module builtins:

round(number, ndigits=None)
    Round a number to a given precision in decimal digits.</pre>

<!-- </div> -->

<!-- <div> -->

- Параметры без значения по умолчанию записываются **перед** параметрами со значением по умолчанию. Иначе при позиционном вызове нельзя определить, к какому параметру относится аргумент.
- Обязательными делают параметры, без которых расчёт не имеет смысла: количество вещества. Значения по умолчанию задают для типичных условий.
- Так устроены встроенные функции: у `round()` второй параметр необязательный, и `round(2.4664)` возвращает `2`.

<!-- </div> -->

<!-- </div> -->

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Что напечатает эта программа?

```python
def add_sample(value, series=[]):
    series.append(value)
    return series

print(add_sample(2.512))
print(add_sample(2.508))
```

<v-click>

<div class="cols-2">

<div>

<pre class="output">[2.512]
[2.512, 2.508]</pre>

- Значение по умолчанию вычисляется **один раз** -- при выполнении `def`. Все вызовы без второго аргумента получают один и тот же список.
- Первый вызов дописал в него 2.512, второй -- 2.508. Изменяемый аргумент ведёт себя так же, как в [лекции 8](https://vchuzlov.github.io/test-lectures/lec-08/#/22).

</div>

<div>

Исправление: значение по умолчанию `None`, новый список -- при каждом вызове.

```python
def add_sample(value, series=None):
    if series is None:
        series = []
    series.append(value)
    return series

print(add_sample(2.512))
print(add_sample(2.508))
```

<pre class="output">[2.512]
[2.508]</pre>

</div>

</div>

</v-click>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

<!--
Сначала спросить зал. Почти все ответят [2.512] и [2.508]. Правило: значением по умолчанию не делают список, словарь или множество.
-->

---
layout: image-left
class: flex flex-col items-center justify-center
image: /pics/photo_2026-02-19_14-53-38.jpg
---

# Аннотации типов

---

# Аннотации типов

<div class="cols-2">

<div>

```python
def gas_volume(n: float, T: float = 273.15,
               p: float = 101325) -> float:
    """Объём газа, л: pV = nRT."""
    return n * R * T / p * 1000

print(gas_volume.__annotations__)
help(gas_volume)
```

<pre class="output">{'n': &lt;class 'float'&gt;, 'T': &lt;class 'float'&gt;, 'p': &lt;class 'float'&gt;, 'return': &lt;class 'float'&gt;}
Help on function gas_volume in module __main__:

gas_volume(n: float, T: float = 273.15, p: float = 101325) -> float
    Объём газа, л: pV = nRT.</pre>

</div>

<div>

- **Аннотация** -- указание ожидаемого типа: после имени параметра через двоеточие, тип результата -- после `->` в конце заголовка.
- У параметра с аннотацией и значением по умолчанию знак `=` отделяется пробелами: `T: float = 273.15`.
- Аннотации хранятся в атрибуте `__annotations__` и выводятся в справке: `help()` и панель Help в Spyder.
- Аннотация сообщает тип, строка документации -- смысл и единицы измерения ([лекция 8](https://vchuzlov.github.io/test-lectures/lec-08/#/15)). Одно другое не заменяет.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Типы в аннотациях

<div class="cols-2">

<div>

```python
def split_coef(term: str) -> tuple[int, str]:
    """Отделяет коэффициент: '3O2' -> (3, 'O2')."""
    ...

def mass(composition: dict[str, int]) -> float:
    """Молярная масса по составу, г/моль."""
    ...

def mean(values: list[float]) -> float:
    """Среднее значение серии измерений."""
    return sum(values) / len(values)

def report(name: str, value: float) -> None:
    """Выводит строку отчёта."""
    print(f'{name}: {value:.3f}')
```

</div>

<div class="small-table">

| Аннотация | Значение |
|---|---|
| `int`, `float`, `str`, `bool` | число, строка, логическое значение |
| `list[float]` | список чисел |
| `tuple[int, str]` | кортеж: число и строка |
| `dict[str, int]` | словарь: строка → число |
| `set[str]` | множество строк |
| `None` | функция ничего не возвращает |

</div>

</div>

- В квадратных скобках указывают тип элементов коллекции. Такая запись доступна с Python 3.9.
- Функции `split_coef()` и `mass()` -- из [лекции 8](https://vchuzlov.github.io/test-lectures/lec-08/#/16); тело заменено на `...`, изменились только заголовки.

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Что напечатает эта программа?

```python
def moles(m: float, M: float) -> int:
    """Количество вещества, моль."""
    return m / M

print(moles(10, 40))
print(moles('10', 40))
```

<v-click>

<pre class="output">0.25
TypeError: unsupported operand type(s) for /: 'str' and 'int'</pre>

- Интерпретатор аннотации **не проверяет**: аннотация `-> int` не мешает вернуть `0.25`, аннотация `m: float` не мешает передать строку.
- Ошибка во второй строке возникает при делении строки на число, то есть в теле функции, а не при проверке аннотации.
- Несоответствие типов до запуска находят программы статического анализа кода, например mypy. Для интерпретатора аннотации -- только сведения для человека и инструментов.

</v-click>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

<!--
Сначала спросить зал. Частые ответы: 0 (раз результат объявлен целым) или ошибка уже в первой строке.
-->

---
layout: image-left
class: flex flex-col items-center justify-center
image: /pics/photo_2026-02-19_14-53-38.jpg
---

# Произвольное число аргументов

---

# `*args`: позиционные аргументы в кортеж

<div class="cols-2">

<div>

```python
def total_moles(*amounts: float) -> float:
    """Суммарное количество вещества, моль."""
    print(amounts)
    return sum(amounts)

print(total_moles(1.5, 0.5, 2.0))
print(total_moles(0.25))
print(total_moles())
```

<pre class="output">(1.5, 0.5, 2.0)
4.0
(0.25,)
0.25
()
0</pre>

</div>

<div>

- Звёздочка перед именем параметра собирает все позиционные аргументы в **кортеж**. Аргументов может быть любое число, в том числе ни одного.
- Имя параметра произвольное; по соглашению используют `args`, если более точного названия нет.
- Аннотация `*amounts: float` задаёт тип **каждого** аргумента; сам `amounts` -- кортеж чисел.
- Так устроена `print()`: она принимает любое число аргументов.
- В распаковке присваиванием ([лекция 6](https://vchuzlov.github.io/test-lectures/lec-06/#/15)) имя со звёздочкой получает список, в заголовке функции -- кортеж.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Параметры только по имени

<div class="cols-2">

<div>

```python
R = 8.314                          # Дж/(моль·К)

def gas_volume(n: float, *, T: float = 273.15,
               p: float = 101325) -> float:
    """Объём газа, л: pV = nRT."""
    return n * R * T / p * 1000

def mixture_volume(*amounts: float, T: float = 273.15,
                   p: float = 101325) -> float:
    """Объём смеси газов, л."""
    return gas_volume(sum(amounts), T=T, p=p)

print(round(mixture_volume(0.78, 0.21, 0.01), 2))
print(round(mixture_volume(0.78, 0.21, 0.01,
                           T=298.15), 2))
print(gas_volume(2, 298.15))
```

<pre class="output">22.41
24.46
TypeError: gas_volume() takes 1 positional argument but 2 were given</pre>

</div>

<div>

- Параметры после одиночной `*` (`T`, `p`) получают значения **только по имени**. Позиционный параметр один -- `n`, поэтому `gas_volume(2, 298.15)` завершается ошибкой.
- После `*amounts` параметры тоже передаются только по имени: позиционные аргументы собраны в кортеж.
- Параметр после `*` нельзя перепутать с соседним, как объёмы в [лекции 8, слайд 9](https://vchuzlov.github.io/test-lectures/lec-08/#/9); параметр до `*` (`n`) передаётся по позиции.
- Объём смеси -- по суммарному количеству вещества (закон Авогадро, слайд 29).

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Что напечатает эта программа?

```python
def total_moles(*amounts: float) -> float:
    print('аргументов:', len(amounts))
    return sum(amounts)

mixture = [1.5, 0.5, 2.0]
print(total_moles(*mixture))
print(total_moles(mixture))
```

<v-click>

<pre class="output">аргументов: 3
4.0
аргументов: 1
TypeError: unsupported operand type(s) for +: 'int' and 'list'</pre>

- `total_moles(*mixture)`: звёздочка в **вызове** распаковывает список на отдельные аргументы -- то же, что `total_moles(1.5, 0.5, 2.0)`.
- `total_moles(mixture)`: передан один аргумент -- сам список. Кортеж `amounts` содержит один элемент, и `sum()` пытается сложить 0 со списком. Аннотация `float` этому не препятствует: она не проверяется (слайд 16).
- Звёздочка в заголовке собирает аргументы, звёздочка в вызове -- распаковывает.

</v-click>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

<!--
Сначала спросить зал. Частый ответ: 4.0 в обоих случаях.
-->

---

# Распаковка при вызове

<div class="cols-2">

<div>

```python
point = (2, 298.15, 202650)
print(round(gas_volume(*point), 1))

conditions = {'T': 298.15, 'p': 202650}
print(round(gas_volume(2, **conditions), 1))

series = [2.512, 2.508, 2.515]
print(*series)
print(*series, sep='; ')
```

<pre class="output">24.5
24.5
2.512 2.508 2.515
2.512; 2.508; 2.515</pre>

</div>

<div>

- `*` перед списком или кортежем в вызове передаёт его элементы как отдельные **позиционные** аргументы, по порядку.
- `**` перед словарём передаёт его пары как **именованные** аргументы: ключ -- имя параметра, значение -- аргумент.
- `print(*series)` выводит элементы списка через пробел, без скобок и запятых.

</div>

</div>

<div class="note">
Здесь <code>gas_volume()</code> со слайда 14 (с аннотациями, без <code>*</code>): все три параметра можно передать позиционно.
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# `**kwargs`: именованные аргументы в словарь

<div class="cols-2">

<div>

```python
def composition(**atoms: int) -> dict[str, int]:
    return atoms

print(composition(C=2, H=6))

M = {'H': 1.008, 'C': 12.011, 'O': 15.999}

def molar_mass(**atoms: int) -> float:
    """Молярная масса по составу, г/моль."""
    total = 0
    for el, n in atoms.items():
        total += M[el] * n
    return total

print(round(molar_mass(C=6, H=12, O=6), 3))
```

<pre class="output">{'C': 2, 'H': 6}
180.156</pre>

</div>

<div>

- Две звёздочки перед именем параметра собирают все именованные аргументы, не совпавшие с другими параметрами, в **словарь**: имя аргумента -- ключ.
- По соглашению параметр называют `kwargs` (keyword arguments), если более точного названия нет.
- Аннотация `**atoms: int` задаёт тип **значения** каждого аргумента; ключи -- всегда строки, поэтому `composition()` возвращает `dict[str, int]`.
- Запись `molar_mass(C=6, H=12, O=6)` соответствует `dict(C=6, H=12, O=6)` из [лекции 7](https://vchuzlov.github.io/test-lectures/lec-07/#/17), ограничение то же: имя аргумента -- допустимое имя переменной.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

<!--
Пример ограничения: ключ 'мм рт. ст.' нельзя передать как именованный аргумент -- это не имя переменной.
-->

---

# Виды параметров в заголовке

<div class="small-table">

| Запись в заголовке | Вид параметра | Как передаётся аргумент |
|---|---|---|
| `def f(a)` | обязательный | по позиции или по имени |
| `def f(a=1)` | со значением по умолчанию | по позиции или по имени; можно не передавать |
| `def f(*args)` | сбор позиционных аргументов | любое число позиционных аргументов → кортеж |
| `def f(*, a)`, `def f(*args, a)` | только по имени | только `a=...` |
| `def f(**kwargs)` | сбор именованных аргументов | любые `имя=значение` → словарь |
| `def f(a, /)` | только по позиции | только по позиции, имя указывать нельзя |

</div>

<div class="cols-2 mt-3">

<div>

```python
help(sorted)
```

<pre class="output">Help on built-in function sorted in module builtins:

sorted(iterable, /, *, key=None, reverse=False)
    Return a new list containing all items from the iterable in ascending order.</pre>

</div>

<div>

- В справке встроенных функций встречаются `/` и `*`. У `sorted()` первый аргумент передаётся только по позиции, а `key` и `reverse` -- только по имени: `sorted(data, len)` вызывает ошибку.
- Порядок в заголовке: обязательные, со значением по умолчанию, `*args`, только по имени, `**kwargs`.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---
layout: image-left
class: flex flex-col items-center justify-center
image: /pics/photo_2026-02-19_14-53-38.jpg
---

# Функции без имени: `lambda`

---

# Функция как аргумент

<div class="cols-wide">

<div>

```python
formulas = ['C2H6', 'CH4', 'C10H22']
print(sorted(formulas, key=len))

substances = [('вода', 100.0), ('этанол', 78.4),
              ('ацетон', 56.1)]

def boiling_point(item: tuple[str, float]) -> float:
    return item[1]

print(sorted(substances, key=boiling_point))
print(max(substances, key=boiling_point))
```

<pre class="output">['CH4', 'C2H6', 'C10H22']
[('ацетон', 56.1), ('этанол', 78.4), ('вода', 100.0)]
('вода', 100.0)</pre>

</div>

<div>

- Параметр `key` получает **функцию**, а не результат её вызова: `key=len` записано без скобок ([лекция 5](https://vchuzlov.github.io/test-lectures/lec-05/#/27)).
- `sorted()` вызывает эту функцию для каждого элемента и сравнивает полученные значения.
- Собственная функция передаётся так же: `boiling_point()` возвращает температуру кипения из пары «вещество, Tкип».
- Имя функции -- переменная, значением которой является функция ([лекция 8](https://vchuzlov.github.io/test-lectures/lec-08/#/17)), поэтому её можно передать как любое значение.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Выражение `lambda`

<div class="cols-wide">

<div>

```python
print(sorted(substances, key=lambda item: item[1]))
print(min(substances, key=lambda item: item[1]))

Tb = {'вода': 100.0, 'этанол': 78.4, 'ацетон': 56.1}
print(sorted(Tb.items(), key=lambda pair: pair[1],
             reverse=True))
```

<pre class="output">[('ацетон', 56.1), ('этанол', 78.4), ('вода', 100.0)]
('ацетон', 56.1)
[('вода', 100.0), ('этанол', 78.4), ('ацетон', 56.1)]</pre>

</div>

<div>

- `lambda параметры: выражение` создаёт функцию без имени. Она возвращает значение выражения, оператор `return` не пишется.
- `lambda item: item[1]` выполняет то же, что `boiling_point()` со слайда 25, но записана на месте вызова.
- Тело `lambda` -- одно выражение. Циклы, присваивания и несколько строк в нём недопустимы.
- Аннотации и строку документации в выражении `lambda` записать нельзя.

</div>

</div>

<div class="note">
Третий вызов упорядочивает пары словаря по убыванию значения. В <a href="https://vchuzlov.github.io/test-lectures/lec-07/#/19">лекции 7</a> по значениям упорядочены ключи: в <code>key</code> передан метод словаря <code>Tb.get</code>.
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Что напечатает эта программа?

```python
formulas = ['C2H6', 'CH4', 'C10H22']
print(sorted(formulas, key=len))
print(sorted(formulas, key=len()))
```

<v-click>

<pre class="output">['CH4', 'C2H6', 'C10H22']
TypeError: len() takes exactly one argument (0 given)</pre>

- `key=len` передаёт функцию: `sorted()` вызывает её сама для каждой формулы.
- `key=len()` сначала **вызывает** `len` без аргумента, и ошибка возникает ещё до сортировки.
- Та же ошибка с собственной функцией: `key=boiling_point()` -- `TypeError: boiling_point() missing 1 required positional argument: 'item'`.

</v-click>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

<!--
Сначала спросить зал. Частый ответ: оба вывода одинаковые. Это ошибка «вызов вместо функции» из списка частых ошибок лекции 8.
-->

---

# `lambda` или `def`

<div class="cols-2">

<div>

##### `lambda` -- короткая функция на месте вызова

```python
metals = [('медь', 8.96), ('алюминий', 2.70),
          ('железо', 7.87)]        # плотность, г/см³
print(min(metals, key=lambda m: m[1]))
```

<div class='output'>('алюминий', 2.7)</div>

</div>

<div>

##### `def` -- функция, которая нужна повторно

```python
def density(metal: tuple[str, float]) -> float:
    """Плотность, г/см³: ('медь', 8.96) -> 8.96."""
    return metal[1]

print(min(metals, key=density))
print(max(metals, key=density))
```

<pre class="output">('алюминий', 2.7)
('медь', 8.96)</pre>

</div>

</div>

- `lambda` уместна, если функция состоит из одного выражения и нужна в одном месте: как `key` в `sorted()`, `min()`, `max()`.
- `def` нужен, если функция используется несколько раз, требует аннотаций, строки документации или нескольких строк кода.
- Присваивать `lambda` имени не рекомендуется: `density = lambda m: m[1]` -- то же, что `def`, но без имени в сообщениях об ошибках, без аннотаций и без строки документации. Это правило записано в руководстве по стилю [PEP 8](https://peps.python.org/pep-0008/#programming-recommendations) (раздел Programming Recommendations).

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Объём воздуха при разных температурах

<div class="cols-2">

<div>

```python
R = 8.314                          # Дж/(моль·К)

def gas_volume(n: float, *, T: float = 273.15,
               p: float = 101325) -> float:
    """Объём газа, л: pV = nRT."""
    return n * R * T / p * 1000

def mixture_volume(*amounts: float, T: float = 273.15,
                   p: float = 101325) -> float:
    """Объём смеси газов, л."""
    return gas_volume(sum(amounts), T=T, p=p)

air = [0.78, 0.21, 0.01]           # N2, O2, Ar, моль
for t in [0, 25, 100]:
    v = mixture_volume(*air, T=t + 273.15)
    print(f'{t:>3} °C {v:6.2f} л')
```

</div>

<div>

<pre class="output">  0 °C  22.41 л
 25 °C  24.46 л
100 °C  30.62 л</pre>

- `T` и `p` в обеих функциях передаются только по имени.
- `mixture_volume()` собирает количества газов в кортеж, `*air` распаковывает список при вызове.
- По закону Авогадро при одинаковых T и p равные количества любых газов занимают равные объёмы. Поэтому объём смеси определяется суммой 0,78 + 0,21 + 0,01 = 1&nbsp;моль и не зависит от того, какие газы её составляют. Воздух при этих условиях близок к идеальному газу.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

<!--
Если спросят, почему состав смеси не учитывается: объёмы компонентов по отдельности [round(gas_volume(n), 2) for n in air] -> [17.48, 4.71, 0.22], сумма 22.41 л -- столько же, сколько 1 моль любого газа. Молярная масса газов на объём не влияет, она нужна для массы смеси.
-->

---

# Данные изменились: давление в атмосферах

<div class="cols-2">

<div>

```python
TO_PA = {'Па': 1, 'кПа': 1000, 'атм': 101325}

def gas_volume(n: float, *, T: float = 273.15,
               p: float = 101325,
               unit: str = 'Па') -> float:
    """Объём газа, л; давление p в единицах unit."""
    return n * R * T / (p * TO_PA[unit]) * 1000

print(round(gas_volume(2), 1))
print(round(gas_volume(2, T=298.15, p=2,
                       unit='атм'), 1))
print(round(mixture_volume(0.78, 0.21, 0.01), 2))
```

<pre class="output">44.8
24.5
22.41</pre>

</div>

<div>

- В справочнике давление задано в атмосферах. В функцию добавлен параметр `unit` со значением по умолчанию `'Па'`; множители -- из таблицы перевода единиц [лекции 7](https://vchuzlov.github.io/test-lectures/lec-07/#/16).
- Прежние вызовы работают без изменений: `unit` в них не указан и принимает значение по умолчанию. `mixture_volume()` не изменилась.
- Новый параметр со значением по умолчанию расширяет функцию, не нарушая программ, которые её уже вызывают.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Как составить заголовок функции

<div class="small-table">

| Задача | Средство | Пример |
|---|---|---|
| параметр необходим для расчёта | обязательный параметр | `n` в `gas_volume()` |
| у параметра есть типичное значение | значение по умолчанию | `T=273.15`, `unit='Па'` |
| аргументы легко перепутать | параметры только по имени: `*` | `gas_volume(n, *, T, p)` |
| число однотипных аргументов заранее неизвестно | `*args` | `mixture_volume(*amounts)` |
| набор именованных значений заранее неизвестен | `**kwargs` | `molar_mass(**atoms)` |
| нужен изменяемый объект по умолчанию | `None` и проверка `is None` | `add_sample(value, series=None)` |
| тип параметров и результата | аннотации | `n: float`, `-> float` |

</div>

<div class="note">
Функция удобна, если по её вызову понятно, какое значение к чему относится, а для типичного случая достаточно указать только обязательные аргументы.
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Частые ошибки

<ol class="steps">
<li><b>Позиционный аргумент после именованного:</b> <code>SyntaxError</code>. Сначала позиционные аргументы, затем именованные.</li>
<li><b>Параметр без значения по умолчанию после параметра со значением:</b> <code>SyntaxError</code>. Обязательные параметры – первыми.</li>
<li><b>Изменяемое значение по умолчанию.</b> <code>series=[]</code> – один список на все вызовы. Значение по умолчанию <code>None</code>, список – в теле функции.</li>
<li><b>Неверное имя аргумента:</b> <code>TypeError: ... unexpected keyword argument</code>. Имя совпадает с именем параметра, включая регистр.</li>
<li><b>Список вместо распакованных аргументов:</b> <code>total_moles(mixture)</code> вместо <code>total_moles(*mixture)</code>.</li>
<li><b>Позиционный аргумент для параметра только по имени:</b> <code>TypeError: ... positional argument</code>.</li>
<li><b>Вызов вместо функции:</b> <code>key=len()</code> вместо <code>key=len</code>.</li>
<li><b>Расчёт на проверку аннотаций.</b> Интерпретатор их не проверяет.</li>
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
