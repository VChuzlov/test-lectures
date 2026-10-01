---
# ─────────────────────────────────────────────────────────────────────────────
# HEADMATTER -- шапка лекции. Поля title/lecture/topics попадают в оглавление
# сайта (см. tools/build_site.py), поэтому заполняйте их у каждой лекции.
# ─────────────────────────────────────────────────────────────────────────────
routerMode: hash
theme: default
title: Последовательности в Python. Списки
lecture: '05'
topics: списки, индексы и срезы, вложенные списки, методы списков, sort() и sorted(), изменяемые и неизменяемые объекты, копия и ссылка, перебор списка, enumerate() и zip(), генераторы списков

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

<h2 class="!mt-0">Лекция 5. Последовательности в Python: списки (list)</h2>

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

# Восемь взвешиваний одной навески

Одну и ту же навеску взвесили восемь раз на аналитических весах. Результаты, г:

<div class="weights">
<span>2,512</span><span>2,508</span><span>2,515</span><span>2,152</span><span>2,511</span><span>2,509</span><span>2,514</span><span>2,510</span>
</div>

<div class="lead mt-4">
Найдите среднее. Одно из измерений ошибочно: какое?
</div>

<v-click>

<div class="cols-2 mt-6">

<div>

- Среднее по всем восьми: **2,4664 г**.
- Семь значений лежат в пределах 2,508...2,515, а среднее ушло от них на 0,045 г. Виновато четвёртое: **2,152** вместо 2,512, две цифры переставлены при записи.
- Среднее без него: **2,5113 г**.

</div>

<div>

<div class="warn">
Восемь чисел ещё можно сложить в телефоне. В лаборатории серия может состоять из тридцати измерений, и ошибочное среди них ищут не на глаз.
</div>

</div>

</div>

</v-click>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

<!--
Дать две минуты. Спросить среднее: ответы разойдутся, промах найдут не все, потому что среднее с ним всё ещё похоже на правду.
-->

---

# Та же задача в семь строк

```python
masses = [2.512, 2.508, 2.515, 2.152, 2.511, 2.509, 2.514, 2.510]
mean = sum(masses) / len(masses)
deviations = [abs(m - mean) for m in masses]
bad = deviations.index(max(deviations))
print(f'среднее по всем: {mean:.4f} г, подозрительное: {masses[bad]} (№ {bad + 1})')
masses.pop(bad)
print(f'среднее без него: {sum(masses) / len(masses):.4f} г')
```

<pre class="output">среднее по всем: 2.4664 г, подозрительное: 2.152 (№ 4)
среднее без него: 2.5113 г</pre>

- Восемь чисел хранятся **вместе**, под одним именем `masses`. К любому из них можно обратиться по индексу, все вместе можно сложить, пересчитать, отсортировать.
- В лекциях 1...4 каждое число жило в своей переменной. Для восьми взвешиваний потребовалось бы восемь имён, для тридцати -- тридцать.

<div class="note">
В этих семи строках есть всё, о чём пойдёт речь: список, <code>sum()</code> и <code>len()</code>, генератор списка, методы <code>index()</code> и <code>pop()</code>. К концу пары каждая строка будет понятна.
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Последовательности в Python

> Строка ([лекция 4](https://vchuzlov.github.io/test-lectures/lec-04/#/4)) -- *упорядоченная неизменяемая последовательность* символов. Список -- вторая последовательность, и у них много общего.

<div class="cols-2">

<div>

##### Общее для строк и списков

1. Длина: `len()`
2. Проверка вхождения: `in`
3. Индексы и срезы `[i:j:k]`, в том числе отрицательные
4. Конкатенация `+` и повторение `*`
5. Сравнение `==`, `<`, `>`; `min()` и `max()`
6. Перебор в цикле `for`

</div>

<div>

##### Чем список отличается

- Элементы -- **любые объекты**: числа, строки, другие списки. У строки только символы.
- Список <span class="text-[var(--brand)]">*изменяемый*</span>: элемент можно заменить, добавить, удалить. Строку поменять нельзя.
- Методы списка чаще меняют сам список. Методы строки возвращали новую строку.

</div>

</div>

<div class="note">

Индексы и срезы из [лекции 4](https://vchuzlov.github.io/test-lectures/lec-04/#/15) работают для списков без изменений: повторим их только на примерах.

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---
layout: image-left
class: flex flex-col items-center justify-center
image: /pics/photo_2026-01-29_22-47-04.jpg
---

# Списки (`list`)

---

# Списки (`list`)

> Список (тип `list`) -- <span class="text-[var(--brand)]">*упорядоченная изменяемая последовательность*</span> объектов. Элементы записываются через запятую в квадратных скобках `[]`.

```python
masses = [2.512, 2.508, 2.515]             # числа
names = ['вода', 'этанол', 'ацетон']       # строки
row = ['этанол', 'C2H5OH', 46.07, True]    # объекты разных типов
empty = []                                 # пустой список
print(row)
print(len(masses), len(names), len(empty))
```

<pre class="output">['этанол', 'C2H5OH', 46.07, True]
3 3 0</pre>

- Список печатается так же, как записывается в коде: в квадратных скобках, строки в кавычках.
- Пустой список -- нормальный объект. Обычно с него начинают, а потом заполняют в цикле.
- Тип элементов не ограничен, но на практике в одном списке держат однотипные значения: серию масс, набор названий, строки таблицы.

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Список из другого объекта

Функция `list()` собирает список из любой последовательности или итерируемого объекта:

<div class="cols-2">

<div>

```python
print(list('H2SO4'))
print(list(range(1, 6)))
print('2.512 2.508 2.515'.split())
print([0.0] * 5)
print(range(5), list(range(5)))
```

<pre class="output">['H', '2', 'S', 'O', '4']
[1, 2, 3, 4, 5]
['2.512', '2.508', '2.515']
[0.0, 0.0, 0.0, 0.0, 0.0]
range(0, 5) [0, 1, 2, 3, 4]</pre>

</div>

<div>

- `list()` от строки даёт список односимвольных строк.
- `range()` из [лекции 3](https://vchuzlov.github.io/test-lectures/lec-03/#/30) -- не список, а объект последовательности. Список из него получается через `list()`.
- `split()` из [лекции 4](https://vchuzlov.github.io/test-lectures/lec-04/#/33) возвращает список **строк**. Числами они станут после `float()`, об этом ниже.
- `[0.0] * 5` -- заготовка из пяти нулей, когда число элементов известно заранее.

</div>

</div>

<div class="note">
Обратное действие для строки: <code>''.join(['H', '2', 'O'])</code> даёт <code>'H2O'</code>.
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Операции над списками

<div class="cols-2">

<div>

```python
ph = [6.9, 7.1, 7.4, 6.8]
print(len(ph), min(ph), max(ph), sum(ph))
print(ph + [7.0, 7.2])
print([0] * 3 + [1] * 2)
print(sum(ph) / len(ph))
```

<pre class="output">4 6.8 7.4 28.2
[6.9, 7.1, 7.4, 6.8, 7.0, 7.2]
[0, 0, 0, 1, 1]
7.05</pre>

</div>

<div>

- `len()`, `+` и `*` работают как у строк: длина, склейка двух списков в новый, повторение.
- `min()` и `max()` -- наименьший и наибольший элемент.
- `sum()` -- сумма элементов.
- Среднее по серии -- `sum() / len()`, отдельная переменная для накопителя не нужна.

</div>

</div>

<div class="warn">

<code>sum()</code> складывает дробные числа так же, как <code>+</code> в [лекции 2:](https://vchuzlov.github.io/test-lectures/lec-02/#/8) <code>sum([0.1] * 10)</code> даёт <code>0.9999999999999999</code>. Когда важна точность суммы, есть <code>math.fsum()</code>, она даёт <code>1.0</code>.

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Проверка вхождения: `in`

> Для списка оператор `in` сравнивает искомое значение с каждым элементом **целиком**. Подстроки внутри элементов не ищутся.

<div class="cols-2">

<div>

```python
elements = ['Ca', 'Cl', 'Cl']
print('C' in elements)
print('Cl' in elements, 'Na' not in elements)
print('C' in 'CaCl2')
print(7 in [7.0, 8.0])
```

<pre class="output">False
True True
True
True</pre>

</div>

<div>

- В [лекции 4](https://vchuzlov.github.io/test-lectures/lec-04/#/13) `'C' in 'CaCl2'` давало `True`, хотя углерода в хлориде кальция нет: искалась подстрока. Со списком символов элементов ответ верный.
- Сравнение идёт через `==`, поэтому `7` находится среди `[7.0, 8.0]`.
- Для дробных чисел, полученных расчётом, `in` ненадёжен по той же причине, что и `==` в [лекции 2](https://vchuzlov.github.io/test-lectures/lec-02/#/7).

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Сравнение списков

> Списки сравниваются как строки: поэлементно, слева направо, до первого различия.

<div class="cols-2">

<div>

```python
a = [2.512, 2.508]
b = [2.512, 2.508]
print(a == b, a is b)
print([1, 2, 3] < [1, 3])
print([1, 2] == [1.0, 2.0])
print(['проба 10'] < ['проба 9'])
```

<pre class="output">True False
True
True
True</pre>

</div>

<div>

- `==` сравнивает содержимое. `is` проверяет, один ли это объект: два списка, записанные отдельно, всегда разные объекты, даже с одинаковым содержимым.
- `[1, 2, 3] < [1, 3]`: первые элементы равны, вторые `2 < 3`, дальше не сравнивается. Длина роли не играет.
- Элементы-строки сравниваются по кодам символов, со всеми последствиями из <br>[лекции 4](https://vchuzlov.github.io/test-lectures/lec-04/#/10).

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---
layout: image-left
class: flex flex-col items-center justify-center
image: /pics/photo_2026-01-29_22-47-04.jpg
---

# Индексы и срезы

---

# Индексация списков

- Индексы считаются от нуля, отрицательные -- от конца. Наибольший допустимый индекс на единицу меньше длины.
- В отличие от строки, элемент списка -- это не односимвольная строка, а **сам объект**, со своим типом.

```python
ph = [6.9, 7.1, 7.4, 6.8, 7.0]
```

<div class="seq wide">
<table>
<tbody>
<tr class="pos"><th>индекс</th><td>0</td><td>1</td><td>2</td><td>3</td><td>4</td></tr>
<tr class="chr"><th>элемент</th><td>6.9</td><td>7.1</td><td>7.4</td><td>6.8</td><td>7.0</td></tr>
<tr class="neg"><th>индекс с конца</th><td>-5</td><td>-4</td><td>-3</td><td>-2</td><td>-1</td></tr>
</tbody>
</table>
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Индексация в коде

```python
ph = [6.9, 7.1, 7.4, 6.8, 7.0]
print(ph[0], ph[-1], ph[len(ph) - 1])
print(ph[2] * 2)
row = ['этанол', 'C2H5OH', 46.07]
print(row[0].upper(), row[2] / 2)
print(ph[5])
```

<pre class="output">6.9 7.0 7.0
14.8
ЭТАНОЛ 23.035
IndexError: list index out of range</pre>

- `ph[2]` -- число `7.4`, и `ph[2] * 2` его удваивает. В [лекции 4](https://vchuzlov.github.io/test-lectures/lec-04/#/16) `s[1] * 2` повторял символ: там элемент был строкой.
- `row[0]` -- строка, к ней применимы строковые методы. `row[2]` -- число, с ним можно считать. Тип берётся у элемента, а не у списка.
- Индекс `5` для списка из пяти элементов -- ошибка `IndexError`, как и у строк.

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Срезы списков

Правила те же, что для строк: правая граница не входит, границы могут быть отрицательными, третье число -- шаг.

```python
ph = [6.9, 7.1, 7.4, 6.8, 7.0]
print(ph[1:3], ph[-2:], ph[::2], ph[::-1])
print(ph[2], ph[2:3])
print(ph[10:])
```

<pre class="output">[7.1, 7.4] [6.8, 7.0] [6.9, 7.4, 7.0] [7.0, 6.8, 7.4, 7.1, 6.9]
7.4 [7.4]
[]</pre>

- Результат среза -- всегда **новый список**, даже если в нём один элемент или ни одного. `ph[2]` -- число `7.4`, `ph[2:3]` -- список `[7.4]` из одного числа.
- Срез за пределами списка ошибки не даёт: `ph[10:]` -- пустой список `[]`.
- `ph[::-1]` -- копия списка в обратном порядке, исходный список не меняется.

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Вложенные списки

Элементом списка может быть другой список. Так хранят таблицу: строка таблицы -- список, вся таблица -- список строк.

<div class="cols-2">

<div>

```python
table = [['вода',   'H2O',    18.015],
         ['этанол', 'C2H5OH', 46.069],
         ['ацетон', 'C3H6O',  58.080]]
print(table[1])
print(table[1][2])
print(table[-1][0])
print(len(table), len(table[0]))
```

<pre class="output">['этанол', 'C2H5OH', 46.069]
46.069
ацетон
3 3</pre>

</div>

<div>

- Один индекс -- целая строка таблицы, то есть вложенный список.
- Два индекса -- элемент внутри строки: `table[1][2]` -- третий элемент второй строки. Первый индекс всегда номер строки, второй -- номер столбца.
- `len(table)` -- число строк, `len(table[0])` -- число столбцов в первой строке.


</div>

</div>

```python
matrix = [[10, 20, 30],
          [40, 50, 60],
          [70, 80, 90]]
print(matrix[2][0], matrix[1])
```

<div class='output'>70 [40, 50, 60]</div>


<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Что напечатает эта программа?

```python
data = [10, 20, 30, 40, 50]
print(data[1], data[1:2], data[-2:], data[5:])
```

<v-click>

<div class='output'>20 [20] [40, 50] []</div>

- `data[1]` -- второй элемент, число `20`.
- `data[1:2]` -- срез из одного элемента, это список `[20]`, а не число.
- `data[-2:]` -- два последних элемента.
- `data[5:]` -- срез начинается за концом списка. Ошибки нет, результат пустой. Индекс `data[5]` дал бы `IndexError`.

</v-click>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

<!--
Сначала спросить зал. На второй позиции многие скажут 20 без скобок.
-->

---
layout: image-left
class: flex flex-col items-center justify-center
image: /pics/photo_2026-01-29_22-47-04.jpg
---

# Изменение списка

---

# Список можно изменить

В [лекции 4](https://vchuzlov.github.io/test-lectures/lec-04/#/23) присваивание по индексу для строки остановило программу: `acid[-1] = '3'` дало `TypeError`. Для списка это обычная операция.

<div class="cols-2">

<div>

```python
ph = [6.9, 7.1, 7.4, 6.8, 7.0]
before = id(ph)
ph[3] = 6.9
ph[-1] = 7.2
print(ph)
print(id(ph) == before)
```

<pre class="output">[6.9, 7.1, 7.4, 6.9, 7.2]
True</pre>

</div>

<div>

<FigRack class="w-full mt-1" />

</div>

</div>

- Элемент заменяется <span class="text-[var(--brand)]">*на месте*</span>. Новый список не создаётся: `id()` до и после тот же, это тот же объект с другим содержимым. Строку так поменять было нельзя, приходилось собирать новую: <br> `acid[:-1] + '3'`.
- Список похож на штатив с пробирками: гнёзда пронумерованы, в любое можно поставить другую пробирку, а штатив остаётся тем же. Что из этого следует, разберём в отдельном разделе.

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Присваивание срезу и удаление

<div class="cols-2">

<div>

```python
a = [10, 20, 30]
a[1:2] = [4, 5]        # замена: два вместо одного
print(a)
a[1:1] = [60, 70]      # вставка в пустой срез
print(a)
a[1:3] = []            # удаление среза
print(a)
del a[0]               # удаление по индексу
print(a)
del a[1:]              # удаление среза
print(a)
```

<pre class="output">[10, 4, 5, 30]
[10, 60, 70, 4, 5, 30]
[10, 4, 5, 30]
[4, 5, 30]
[4]</pre>

</div>

<div>

- Срезу можно присвоить список другой длины: список растёт или сокращается.
- Пустой срез `a[1:1]` -- это место между элементами. Присваивание в него вставляет, ничего не заменяя.
- `del` -- оператор, а не метод: удаляет элемент или срез, ничего не возвращая.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Методы: добавление и удаление

|Метод|Описание|
|-|-|
|`append(x)`|Добавляет `x` в конец списка|
|`extend(seq)`|Добавляет в конец списка все элементы последовательности `seq`|
|`insert(i, x)`|Вставляет `x` перед элементом с индексом `i`|
|`pop()`, `pop(i)`|Удаляет последний элемент (или элемент с индексом `i`) и возвращает его|
|`remove(x)`|Удаляет первое вхождение `x`; если его нет, ошибка `ValueError`|
|`clear()`|Удаляет все элементы|

<div class="warn">
Все эти методы меняют список <b>на месте</b>. Возвращают они <code>None</code>, кроме <code>pop()</code>, который возвращает удалённый элемент.
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Методы: поиск, порядок, копия

|Метод|Описание|
|-|-|
|`index(x)`|Индекс первого вхождения `x`; если его нет, ошибка `ValueError`|
|`count(x)`|Сколько раз `x` встречается в списке|
|`sort()`|Сортирует список на месте по возрастанию|
|`reverse()`|Переворачивает список на месте|
|`copy()`|Возвращает копию списка|

- `index()` и `count()` есть и у строк, работают так же. Метода `find()` у списка нет: перед `index()` проверяют `in`.
- `sort()`, `reverse()` и все методы с предыдущего слайда изменяют список, у которого вызваны. У строк таких методов не было: строка неизменяема, и `replace()`, `upper()`, `strip()` возвращали новую строку.

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Добавление элементов

<!-- <div class="cols-2"> -->

<!-- <div> -->

```python
ph = [6.9, 7.1]
ph.append(7.4)
print(ph)
ph.extend([6.8, 7.0])
print(ph)
ph.insert(0, 7.2)
print(ph)
ph.append([6.5, 7.3])
print(ph)
```

<pre class="output">[6.9, 7.1, 7.4]
[6.9, 7.1, 7.4, 6.8, 7.0]
[7.2, 6.9, 7.1, 7.4, 6.8, 7.0]
[7.2, 6.9, 7.1, 7.4, 6.8, 7.0, [6.5, 7.3]]</pre>


- `append()` добавляет **один** элемент. Если передать список, он целиком станет одним элементом: последняя строка вывода, вложенный список в конце.
- `extend()` добавляет элементы по одному. То же делает `ph += [6.5, 7.3]`.
- `insert(0, x)` вставляет в начало. Для длинных списков это медленнее, чем `append()`: все элементы сдвигаются.


<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Удаление элементов

<div class="cols-2">

<div>

```python
masses = [2.512, 2.508, 2.515, 2.152, 2.511]
last = masses.pop()
print(last, masses)
bad = masses.pop(3)
print(bad, masses)
masses.remove(2.508)
print(masses)
masses.remove(9.99)
```

<pre class="output">2.511 [2.512, 2.508, 2.515, 2.152]
2.152 [2.512, 2.508, 2.515]
[2.512, 2.515]
ValueError: list.remove(x): x not in list</pre>

</div>

<div>

- `pop()` удаляет **по индексу** и возвращает удалённое: элемент можно сохранить, как здесь в `last` и `bad`.
- `remove()` удаляет **по значению**, только первое вхождение, и ничего не возвращает. Если значения в списке нет, программа останавливается.
- Когда удалённое значение не нужно, годится и `del masses[3]`.


</div>

</div>

<div class="note">
Перед <code>remove()</code> стоит проверить: <code>if x in masses</code>.
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Что напечатает эта программа?

```python
masses = [2.512, 2.508, 2.515]
masses = masses.append(2.511)
print(masses)
```

<v-click>

<div class='output'>None</div>

- `append()` добавил элемент в список и вернул `None`. Присваивание записало этот `None` в имя `masses`, и список с четырьмя значениями потерян: на него больше не ссылается ни одно имя.
- Следующий `masses.append(...)` остановит программу: `AttributeError: 'NoneType' object has no attribute 'append'`.
- Правильно без присваивания: `masses.append(2.511)`. То же с `sort()`: `x = a.sort()` даёт `x` равный `None`.

<div class="warn">

У строк было наоборот: <code>name.replace(...)</code> без присваивания ничего не меняло ([лекция 4](https://vchuzlov.github.io/test-lectures/lec-04/#/31?clicks=1)). У списков присваивание результата метода ломает программу. Правило одно: метод, который меняет список, ничего полезного не возвращает.

</div>

</v-click>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

<!--
Сначала спросить зал. Ожидаемый ответ большинства: список из четырёх чисел.
-->

---

# Сортировка: `sort()` и `sorted()`

<div class="cols-2">

<div>

```python
masses = [2.512, 2.508, 2.515, 2.152, 2.511]
ordered = sorted(masses)
print(ordered)
print(masses)
masses.sort()
print(masses)
masses.sort(reverse=True)
print(masses)
print(sorted('H2SO4'))
```

<pre class="output">[2.152, 2.508, 2.511, 2.512, 2.515]
[2.512, 2.508, 2.515, 2.152, 2.511]
[2.152, 2.508, 2.511, 2.512, 2.515]
[2.515, 2.512, 2.511, 2.508, 2.152]
['2', '4', 'H', 'O', 'S']</pre>

</div>

<div>

- Функция `sorted()` возвращает **новый** отсортированный список, исходный не трогает. Подходит для любой последовательности, в том числе для строки.
- Метод `sort()` сортирует список **на месте** и возвращает `None`.
- `reverse=True` -- по убыванию.
- В отсортированной серии промах оказывается с краю: `masses[0]` или `masses[-1]`.

</div>

</div>

<div class="note">
<code>masses.reverse()</code> просто переворачивает список, не сортируя. Не путать с <code>sort(reverse=True)</code>
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Что можно отсортировать

> Сортируются списки, элементы которых сравнимы друг с другом.

```python
names = ['этанол', 'ацетон', 'Вода', 'бензол']
names.sort()
print(names)
print(sorted([[2, 'б'], [1, 'я'], [2, 'а']]))
print(sorted([1, 'два', 3.0]))
```

<pre class="output">['Вода', 'ацетон', 'бензол', 'этанол']
[[1, 'я'], [2, 'а'], [2, 'б']]
TypeError: '<' not supported between instances of 'str' and 'int'</pre>

- Строки сортируются по кодам символов: заглавная «В» меньше любой строчной буквы, поэтому «Вода» встала первой ([лекция 4](https://vchuzlov.github.io/test-lectures/lec-04/#/10)).
- Вложенные списки сравниваются поэлементно: сначала по первому элементу, при равенстве -- по второму.
- Число и строку сравнить нельзя, смешанный список не сортируется.


<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Сортировка с ключом `key`

Параметр `key` принимает **функцию**. Она вызывается для каждого элемента, а сравниваются её результаты. Сами элементы не меняются.

<div class="cols-2">

<div>

```python
names = ['этанол', 'ацетон', 'Вода', 'бензол']
print(sorted(names, key=str.lower))
print(sorted(names, key=len))
deltas = [0.046, 0.042, -0.314, 0.045]
print(sorted(deltas, key=abs))
print(max(deltas, key=abs), max(deltas))
```

<pre class="output">['ацетон', 'бензол', 'Вода', 'этанол']
['Вода', 'этанол', 'ацетон', 'бензол']
[0.042, 0.045, 0.046, -0.314]
-0.314 0.046</pre>

</div>

<div>

- `key=str.lower`: сравниваются строки в нижнем регистре, и «Вода» встаёт на своё место по алфавиту. В выводе регистр прежний.
- `key=len`: по длине строки. Равные по длине остаются в исходном порядке.
- `key=abs`: по модулю, знак сохраняется. Так же работает `key` у `max()` и `min()`: самое большое **по модулю** отклонение отрицательное.
- Имя функции пишется без скобок: передаётся сама функция, а не результат её вызова.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Поиск: `index()` и `count()`

<div class="cols-2">

<div>

```python
masses = [2.512, 2.508, 2.515, 2.152, 2.511, 2.512]
print(masses.count(2.512))
print(masses.index(2.512))
print(masses.index(max(masses)), masses.index(min(masses)))
print(masses.index(2.5))
```

<pre class="output">2
0
2 3
ValueError: 2.5 is not in list</pre>

</div>

<div>

- `index()` возвращает индекс **первого** вхождения: `2.512` есть на позициях 0 и 5, ответ 0.
- `masses.index(max(masses))` -- позиция наибольшего элемента. Так в задаче о взвешиваниях находится номер промаха: сначала наибольшее отклонение, потом его индекс.

</div>

</div>

- Если значения в списке нет, `index()` останавливает программу. Метода `find()` с ответом `-1` у списков нет.

<div class="warn">

<code>index()</code> ищет через <code>==</code>. Значение, полученное расчётом, может отличаться от записанного в списке в пятнадцатом знаке ([лекция 2](https://vchuzlov.github.io/test-lectures/lec-02/#/8)). Надёжнее искать индекс значения, взятого из самого списка: <code>max(masses)</code>, а не число, набранное руками.

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---
layout: image-left
class: flex flex-col items-center justify-center
image: /pics/photo_2026-01-29_22-47-04.jpg
---

# Изменяемые объекты

---

# Изменяемые и неизменяемые объекты

> <span class="text-[var(--brand)]">*Неизменяемый*</span> объект после создания не меняется: любая операция с ним даёт новый объект. <span class="text-[var(--brand)]">*Изменяемый*</span> объект можно менять на месте, и у него есть операции обоих видов.

<div class="cols-2">

<div>

##### Типы, которые уже встречались

<div class="small-table">

| Неизменяемые | Изменяемые |
|---|---|
| `int`, `float`, `bool`, `str` | `list` |
| кортеж | словарь, множество |

</div>

<div class="muted">Кортеж, словарь и множество: следующая лекция.</div>

</div>

<div>

- У неизменяемых типов нет методов, меняющих объект: `replace()` и `strip()` возвращают новую строку, а `x += 1` создаёт новое число и переводит на него имя `x`.
- У списка операции двух видов, и их надо различать:

</div>

</div>

##### Операции над списком

<div class="small-table">

| Меняют список на месте | Создают новый список |
|---|---|
| `a[i] = x`, `a[i:j] = [...]`, `del a[i]`, `a += b`, `a *= 3` | `a + b`, `a * 3`, `a[i:j]`, `a[:]` |
| `append()`, `extend()`, `insert()`, `pop()`, `remove()`, `clear()` | `a.copy()`, `list(a)`, `sorted(a)` |
| `sort()`, `reverse()` | `[... for x in a]` |

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Два имени, один список

<div class="cols-2">

<div>

```python
proba = [12.1, 12.3, 12.2]
proba_clean = proba        # создали синоним
proba_clean.append(99.9)
print(proba)
print(proba_clean)
print(proba is proba_clean)
```

<pre class="output">[12.1, 12.3, 12.2, 99.9]
[12.1, 12.3, 12.2, 99.9]
True</pre>

</div>

<div>

<svg class="imm" viewBox="0 0 480 262" width="380" xmlns="http://www.w3.org/2000/svg">
<defs><marker id="al-head" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" class="imm-headpath"/></marker></defs>
<text x="0" y="16" class="imm-cap">после proba_clean = proba</text>
<rect x="0" y="28" width="130" height="34" rx="6" class="imm-name"/><text x="65" y="51" class="imm-t">proba</text>
<rect x="0" y="80" width="130" height="34" rx="6" class="imm-name"/><text x="65" y="103" class="imm-t">proba_clean</text>
<rect x="210" y="54" width="270" height="34" rx="6" class="imm-obj"/><text x="345" y="77" class="imm-t">[12.1, 12.3, 12.2]</text>
<path d="M130,45 L208,66" class="imm-arrow" marker-end="url(#al-head)"/>
<path d="M130,97 L208,76" class="imm-arrow" marker-end="url(#al-head)"/>
<line x1="0" y1="130" x2="480" y2="130" class="imm-sep"/>
<text x="0" y="154" class="imm-cap">после proba_clean.append(99.9)</text>
<rect x="0" y="166" width="130" height="34" rx="6" class="imm-name"/><text x="65" y="189" class="imm-t">proba</text>
<rect x="0" y="218" width="130" height="34" rx="6" class="imm-name"/><text x="65" y="241" class="imm-t">proba_clean</text>
<rect x="210" y="192" width="270" height="34" rx="6" class="imm-obj"/><text x="345" y="215" class="imm-t">[12.1, 12.3, 12.2, 99.9]</text>
<path d="M130,183 L208,204" class="imm-arrow" marker-end="url(#al-head)"/>
<path d="M130,235 L208,214" class="imm-arrow" marker-end="url(#al-head)"/>
<text x="212" y="250" class="imm-lbl">тот же объект, новое содержимое</text>
</svg>

</div>

</div>

- Присваивание `proba_clean = proba` не копирует список. Оно даёт тому же объекту **второе имя** ([лекция 1: имя ссылается на объект](https://vchuzlov.github.io/test-lectures/lec-01/#/11)). `append()` изменил объект, и изменение видно под обоими именами.

<div class="danger">
Для строк и чисел второе имя было безобидным: их нельзя изменить. Список изменяем, и правка «копии» портит оригинал. Это самая частая необъяснимая ошибка в работах по спискам.
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Модификация списков

<div class="cols-2">

<div>

```python
a = [1, 2]
b = a
a += [3]          # изменение на месте
print(a, b)
a = a + [4]       # новый объект
print(a, b)
```

<pre class="output">[1, 2, 3] [1, 2, 3]
[1, 2, 3, 4] [1, 2, 3]</pre>


</div>

<div>

<svg class="imm" viewBox="0 0 440 256" width="360" xmlns="http://www.w3.org/2000/svg">
<defs><marker id="ip-head" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" class="imm-headpath"/></marker></defs>
<text x="0" y="16" class="imm-cap">после a += [3]</text>
<rect x="0" y="28" width="60" height="34" rx="6" class="imm-name"/><text x="30" y="51" class="imm-t">a</text>
<rect x="0" y="80" width="60" height="34" rx="6" class="imm-name"/><text x="30" y="103" class="imm-t">b</text>
<rect x="200" y="54" width="150" height="34" rx="6" class="imm-obj"/><text x="275" y="77" class="imm-t">[1, 2, 3]</text>
<path d="M60,45 L198,66" class="imm-arrow" marker-end="url(#ip-head)"/>
<path d="M60,97 L198,76" class="imm-arrow" marker-end="url(#ip-head)"/>
<text x="360" y="77" class="imm-lbl">тот же</text>
<line x1="0" y1="130" x2="440" y2="130" class="imm-sep"/>
<text x="0" y="154" class="imm-cap">после a = a + [4]</text>
<rect x="0" y="166" width="60" height="34" rx="6" class="imm-name"/><text x="30" y="189" class="imm-t">a</text>
<rect x="0" y="218" width="60" height="34" rx="6" class="imm-name"/><text x="30" y="241" class="imm-t">b</text>
<rect x="200" y="166" width="150" height="34" rx="6" class="imm-new"/><text x="275" y="189" class="imm-t">[1, 2, 3, 4]</text>
<rect x="200" y="218" width="150" height="34" rx="6" class="imm-obj"/><text x="275" y="241" class="imm-t">[1, 2, 3]</text>
<path d="M60,183 L198,183" class="imm-arrow" marker-end="url(#ip-head)"/>
<path d="M60,235 L198,235" class="imm-arrow" marker-end="url(#ip-head)"/>
<path d="M60,191 L198,228" class="imm-arrow imm-gone"/>
<text x="360" y="189" class="imm-lbl">новый</text>
<text x="360" y="241" class="imm-lbl">прежний</text>
</svg>

</div>

</div>

- `+=` для списка работает как `extend()`: объект тот же, и `b` видит изменение.
- `a + [4]` собирает **новый** список, а присваивание переводит на него имя `a`. Имя `b` остаётся на прежнем объекте.

<div class="warn">
Одна и та же запись <code>+=</code> означает разное: для списка изменение на месте, для строки и числа новый объект. Тот ли объект остался, проверяют через <code>is</code> или <code>id()</code>.
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Как сделать настоящую копию

<div class="cols-2">

<div>

```python
proba = [12.1, 12.3, 12.2]
copy1 = proba.copy()
copy2 = proba[:]
copy3 = list(proba)
copy1.append(99.9)
print(proba, copy1)
print(proba == copy2, proba is copy2)
```

<pre class="output">[12.1, 12.3, 12.2] [12.1, 12.3, 12.2, 99.9]
True False</pre>

</div>

<div>

Три равноценных способа получить новый список с тем же содержимым:

- метод `copy()`;
- срез целиком `[:]`: срез всегда создаёт новый список;
- функция `list()`.

После копирования `==` даёт `True` (содержимое одинаковое), `is` даёт `False` (объекты разные). Изменение копии оригинал не затрагивает.

</div>

</div>

<div class="note">
Правило: копия нужна тогда, когда список будут <b>менять</b>, а исходный порядок или состав ещё пригодится. Если список только читают, второе имя безопасно.
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Копия вложенного списка

<div class="cols-2">

<div>

```python
table = [[1, 2], [3, 4]]
t2 = table.copy()
t2[0][0] = 99
print(table)
t2[1] = [0, 0]
print(table, t2)
```

<pre class="output">[[99, 2], [3, 4]]
[[99, 2], [3, 4]] [[99, 2], [0, 0]]</pre>

```python
import copy
t3 = copy.deepcopy(table)
t3[0][0] = 1
print(table, t3)
```

<div class='output'>[[99, 2], [3, 4]] [[1, 2], [3, 4]]</div>

</div>

<div>

- `copy()` копирует только **внешний** список. Вложенные списки в копию не переписываются, копия ссылается на те же самые объекты. Поэтому `t2[0][0] = 99` изменил и `table`.
- Замена целой строки `t2[1] = [0, 0]` оригинал не тронула: изменился внешний список, а он у `t2` свой.
- Копия «на всю глубину» -- функция `deepcopy()` из модуля `copy`.

</div>

</div>

<div class="warn">
То же относится к <code>[:]</code> и <code>list()</code>: все три способа делают <i>поверхностную</i> копию.
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Что напечатает эта программа?

```python
x = 5
y = x
x += 1

a = [1, 2]
b = a
c = a[:]
a += [3]

print(x, y)
print(a, b, c)
```

<v-click>

<pre class="output">6 5
[1, 2, 3] [1, 2, 3] [1, 2]</pre>

- Число неизменяемо: `x += 1` создало новое число и перевело на него имя `x`, а `y` осталось на прежнем.
- Список изменяем: `a += [3]` дописал элемент в тот же объект, и `b`, второе имя этого объекта, видит его.
- `c` -- копия, сделанная до изменения. Списков здесь два: `a is b` даёт `True`, `a is c` даёт `False`.

</v-click>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

<!--
Сначала спросить зал. Типичный ответ: 6 5 и [1, 2, 3] [1, 2] [1, 2]: со списком поступают как с числом.
-->

---
layout: image-left
class: flex flex-col items-center justify-center
image: /pics/photo_2026-01-29_22-47-04.jpg
---

# Перебор списка и генераторы

---

# Перебор списка в цикле

<div class="cols-2">

<div>

##### По элементам

```python
ph = [6.9, 7.1, 7.4, 6.8]

acidic = 0
for x in ph:
    if x < 7:
        acidic += 1

print('Количество кислотных проб:', acidic)
```

<div class='output'>Количество кислотных проб: 2</div>

Переменная цикла по очереди принимает значение каждого элемента. Так перебирают, когда элементы только читают.

</div>

<div>

##### По индексам

```python
masses = [2.512, 2.508, 2.515]

for i in range(len(masses)):
    masses[i] = masses[i] * 1000

print(masses)
```

<div class='output'>[2512.0, 2508.0, 2515.0]</div>

`range(len(masses))` перебирает все допустимые индексы. Через индекс элемент можно **заменить** прямо в списке.

</div>

</div>

<div class="warn">
Цикл <code>for m in masses: m = m * 1000</code> список не изменит. Имя <code>m</code> получает копию ссылки на элемент, и присваивание переводит это имя на новое число, а в списке остаётся прежнее. Чтобы изменить элементы, нужен индекс.
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# `enumerate()` и `zip()`

<div class="cols-2">

<div>

##### Номер и элемент вместе

```python
ph = [6.9, 7.1, 7.4]

for i, x in enumerate(ph, 1):
    print(f'проба {i}: pH = {x}')
```

<pre class="output">проба 1: pH = 6.9
проба 2: pH = 7.1
проба 3: pH = 7.4</pre>

`enumerate()` на каждом шаге выдаёт **пару**: номер и элемент. Второй аргумент -- с какого числа нумеровать; по умолчанию с нуля, как индексы.

</div>

<div>

##### Два списка параллельно

```python
names = ['вода', 'этанол', 'ацетон']
M = [18.015, 46.069, 58.080]

for name, m in zip(names, M):
    print(f'{name:<8}{m:8.3f}')
```

<pre class="output">вода      18.015
этанол    46.069
ацетон    58.080</pre>

`zip()` идёт по двум спискам одновременно и выдаёт пары. Останавливается на более коротком.

</div>

</div>

<div class="note">
Пара, которую выдают <code>enumerate()</code> и <code>zip()</code>, называется <b>кортежем</b>: последовательность, как список, только неизменяемая. Подробнее в лекции о словарях. Здесь достаточно того, что пару можно распаковать в две переменные, как <code>M_C, M_H = 12.011, 1.008</code>.
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Список растёт в цикле

Накопитель из [лекции 3](https://vchuzlov.github.io/test-lectures/lec-03/#/10) может быть списком: начинается с `[]`, а `append()` дописывает по элементу за проход.

<div class="cols-2">

<div>

```python
M_C, M_H = 12.011, 1.008
masses = []                  # пустой накопитель
for n in range(1, 11):
    masses.append(n * M_C + (2 * n + 2) * M_H)

print(masses[0], masses[-1])
print(len(masses), max(masses))
print(masses[4])
```

<pre class="output">16.043 142.286
10 142.286
72.151</pre>

</div>

<div>

- В [лекции 3](https://vchuzlov.github.io/test-lectures/lec-03/#/32) таблица алканов печаталась строка за строкой, и после цикла от неё ничего не оставалось.
- Теперь все десять молярных масс сохранены. К любой можно вернуться: `masses[4]` -- пентан, C₅H₁₂.
- Число элементов заранее знать не нужно: список растёт сам.

</div>

</div>

<div class="note">
Если число значений известно, годится и заготовка <code>[0.0] * 10</code> с присваиванием по индексу. Но <code>append()</code> короче и не ошибётся в длине.
</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Серия измерений из строки

Пользователь вводит серию через пробел. `split()` даёт список строк, числами их делает `float()` в цикле:

<div class="cols-2">

<div>

```python
line = input('массы, г: ')     # 2.512 2.508 2.515 2.152
masses = []
for item in line.split():
    masses.append(float(item))

print(masses)
print(f'среднее: {sum(masses) / len(masses):.3f} г')
```

<pre class="output">[2.512, 2.508, 2.515, 2.152]
среднее: 2.422 г</pre>

</div>

<div>

- Без преобразования ничего не посчитать: `sum(line.split())` даёт `TypeError`, строки не складываются с числом.
- В обратную сторону так же: `join()` со списком чисел даёт `TypeError`, он склеивает только строки. Числа сначала превращают в строки, удобнее всего f-строкой.
- Три строки с накопителем -- типовой приём. На следующем слайде он же в одну строку.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Генераторы списков (list comprehension)

> <span class="text-[var(--brand)]">*Генератор списка*</span> -- запись нового списка через выражение, которое применяется к каждому элементу последовательности:

<div class="cols-2">

<div>

```python
xlist = [1, 2, 3, 4, 5, 6]
x2list = [x ** 2 for x in xlist]
print(x2list)
```

<div class='output'>[1, 4, 9, 16, 25, 36]</div>

То же самое циклом с накопителем:

```python
x2list = []
for x in xlist:
    x2list.append(x ** 2)
```

</div>

<div>

```python
line = '2.512 2.508 2.515 2.152'
masses = [float(item) for item in line.split()]
print(masses)
print([m * 1000 for m in masses])
print(', '.join([f'{m:.3f}' for m in masses]))
```

<pre class="output">[2.512, 2.508, 2.515, 2.152]
[2512.0, 2508.0, 2515.0, 2152.0]
2.512, 2.508, 2.515, 2.152</pre>

</div>

</div>

- Читается справа налево: «для каждого `x` из `xlist` взять `x ** 2`». Результат -- новый список, исходный не меняется.
- Генератор короче цикла и выполняется чуть быстрее. В сложных случаях цикл `for` читается лучше, и тогда лучше он.

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Генераторы с условием

<div class="cols-2">

<div>

##### Отбор: `if` после `for`

```python
ph = [6.9, 7.1, 7.4, 6.8]
print([x for x in ph if x < 7])
xlist = [1, 2, 3, 4, 5, 6]
print([x ** 2 for x in xlist if x % 2])
```

<pre class="output">[6.9, 6.8]
[1, 9, 25]</pre>

В новый список попадают только элементы, для которых условие истинно. `x % 2` истинно для нечётных: ненулевой остаток считается за `True` ([лекция 2](https://vchuzlov.github.io/test-lectures/lec-02/#/28)).

</div>

<div>

##### Выбор значения: `if ... else` перед `for`

```python
print(['кислая' if x < 7 else 'щелочная' for x in ph])
print([x ** 2 if x % 2 else x ** 3 for x in xlist])
```

<pre class="output">['кислая', 'щелочная', 'щелочная', 'кислая']
[1, 8, 9, 64, 25, 216]</pre>

Элементов столько же, сколько в исходном списке, но каждому подбирается своё выражение.

</div>

</div>

Источником может быть любая последовательность, не только список: `range()`, строка.

```python
print([x ** 3 for x in range(1, 8)], [w.upper() for w in 'abc'])
```

<div class='output'>[1, 8, 27, 64, 125, 216, 343] ['A', 'B', 'C']</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Генераторы и вложенные списки

<div class="cols-2">

<div>

##### Столбец таблицы

```python
table = [['вода',   'H2O',    18.015],
         ['этанол', 'C2H5OH', 46.069],
         ['ацетон', 'C3H6O',  58.080]]
names = [row[0] for row in table]
print(names)
print(max([row[2] for row in table]))
```

<pre class="output">['вода', 'этанол', 'ацетон']
58.08</pre>

Перебираются строки таблицы, из каждой берётся элемент с нужным индексом. Так из таблицы вынимают столбец.

</div>

<div>

##### Таблица из нулей

```python
grid = [[0] * 3 for _ in range(3)]
grid[0][0] = 1
print(grid)
```

<div class='output'>[[1, 0, 0], [0, 0, 0], [0, 0, 0]]</div>

```python
grid = [[0] * 3] * 3
grid[0][0] = 1
print(grid)
```

<div class='output'>[[1, 0, 0], [1, 0, 0], [1, 0, 0]]</div>

Второй вариант повторяет **один и тот же** вложенный список три раза: те же два имени на один объект, что и в разделе про изменяемые объекты. Генератор создаёт три разных списка. Имя `_` принято для переменной цикла, значение которой не используется.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Что напечатает эта программа?

Отбраковываем всё, что меньше 2,4 г:

```python
masses = [2.512, 2.152, 2.215, 2.508]
for m in masses:
    if m < 2.4:
        masses.remove(m)
print(masses)
```

<v-click>

<div class='output'>[2.512, 2.215, 2.508]</div>

- После удаления `2.152` элемент `2.215` сдвинулся на его место, на индекс 1. А цикл перешёл к индексу 2, и `2.215` остался непроверенным.
- Ошибки нет, программа отработала и выдала неверный результат. Список, по которому идёт цикл, **менять нельзя**.
- Правильно: собрать новый список из подходящих элементов.

```python
masses = [m for m in masses if m >= 2.4]
```

<div class='output'>[2.512, 2.508]</div>

</v-click>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

<!--
Сначала спросить зал. Почти все ответят [2.512, 2.508]. Разобрать по шагам с индексами.
-->

---

# Возвращаемся к задаче о взвешиваниях

<div class="cols-2">

<div>

```python
masses = [2.512, 2.508, 2.515, 2.152,
          2.511, 2.509, 2.514, 2.510]
mean = sum(masses) / len(masses)
print(f'среднее по всем: {mean:.4f} г')
for i, m in enumerate(masses, 1):
    print(f'{i}  {m:.3f}  {m - mean:+.3f}')

deviations = [abs(m - mean) for m in masses]
bad = deviations.index(max(deviations))
print(f'промах: № {bad + 1}, {masses[bad]} г')

masses.pop(bad)
print(f'среднее без него: {sum(masses) / len(masses):.4f} г')
```

</div>

<div>

<pre class="output">среднее по всем: 2.4664 г
1  2.512  +0.046
2  2.508  +0.042
3  2.515  +0.049
4  2.152  -0.314
5  2.511  +0.045
6  2.509  +0.043
7  2.514  +0.048
8  2.510  +0.044
промах: № 4, 2.152 г
среднее без него: 2.5113 г</pre>

- Отклонения через генератор, номер промаха через `index(max())`, удаление через `pop()`.
- Таблица отклонений печатается через `enumerate()`. `+.3f` выводит знак и у положительных чисел.

</div>

</div>

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Данные изменились

Измерений не восемь, а **тридцать**, и правило другое: отбросить **все** значения, которые отличаются от среднего больше чем на 0,1 г.

```python
masses = [2.512, 2.508, 2.515, 2.152, 2.511, 2.509, 2.514, 2.510, 2.513, 2.507,
          2.510, 2.512, 2.509, 2.511, 2.514, 2.508, 2.510, 2.513, 2.215, 2.511,
          2.509, 2.512, 2.510, 2.507, 2.513, 2.511, 2.508, 2.512, 2.510, 2.509]
mean = sum(masses) / len(masses)
clean = [m for m in masses if abs(m - mean) <= 0.1]
print([m for m in masses if abs(m - mean) > 0.1])
print(len(masses), len(clean))
print(f'среднее: {mean:.4f} -> {sum(clean) / len(clean):.4f} г')
```

<pre class="output">[2.152, 2.215]
30 28
среднее: 2.4888 -> 2.5106 г</pre>

- Промахов оказалось два, и программа нашла оба. Вариант с `index(max())` нашёл бы только один: он ищет **самое большое** отклонение, а не **все большие**.
- Расчётная часть не зависит от длины списка. Для тридцати чисел и для трёх тысяч она одна и та же, меняются только данные.

<div class="slide-no">Слайд {{ $nav.currentPage }} / {{ $nav.total }}</div>

---

# Частые ошибки

<ol class="steps">
<li><b>Результат метода присвоен.</b> <code>a = a.sort()</code> или <code>a = a.append(x)</code> записывают в <code>a</code> значение <code>None</code>. Методы, которые меняют список, вызывают без присваивания.</li>
<li><b>Копия через <code>=</code>.</b> <code>b = a</code> даёт списку второе имя, и правка <code>b</code> меняет <code>a</code>. Копия: <code>a.copy()</code> или <code>a[:]</code>.</li>
<li><b><code>append()</code> вместо <code>extend()</code>.</b> <code>a.append([1, 2])</code> добавляет один элемент, и это вложенный список.</li>
<li><b>Замена элементов в цикле по элементам.</b> <code>for m in a: m = m * 1000</code> список не меняет. Нужен цикл по индексам или генератор.</li>
<li><b>Удаление из списка во время перебора по нему.</b> Соседние элементы пропускаются без всякой ошибки. Собирайте новый список с условием.</li>
<li><b>Строки вместо чисел.</b> После <code>split()</code> и <code>input()</code> в списке строки: <code>sum()</code> остановится с <code>TypeError</code>. Сначала <code>float()</code>.</li>
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
