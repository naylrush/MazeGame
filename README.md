# Игра "Лабиринт".

## Суть игры:
Консольная интерактивная версия игры на бумаге "Лабиринт". Суть игры такова: есть некое поле со стенами, ловушками и выходом,
которые известны только ведущему. Остальные игроки в тайне друг от друга указывают ему координаты стартовой локации
(или позиции выбираются рандомно). Дальше они начинают по очереди ходить по лабиринту, а ведущий сообщает им,
упёрлись они в стену или смогли пройти. Таким образом, игроки исследуют карту, внимательно озираясь по сторонам, думая,
где же расположены ловушки, и пытаясь добраться до выхода раньше соперников. Это продолжается до тех пор,
пока какой-нибудь игрок не наткнётся на выход, имея при себе ключ, и тем самым он победит, заканчивая игру!

## Описание клеток:
- **Пустая клетка**. Встав на неё, с игроком ничего не просиходит. Клетка безвредна.
- **Оглушение**. Игрок, вставший на эту клетку, пропускает следующие несколько ходов. Его извещают о том, куда он попал
и сколько ходов пропустит. В начале его хода сообщается, сколько ещё ходов он пропустит.
- **Резиновая комната**. Игрок может выйти из этой клетки только в одном заданном, известном только ведущему, направлении.
Если он попытается пойти в другую сторону, то просто останется на месте, а ведущий нагло ему соврёт, что он успешно продвинулся.
- **Телепорт**. Игрок, вставший на эту клетку, перенесётся на клетку с заданными, известными только ведущему, координатами.
Игроку сообщается, что его телепортировало, но не сообщается куда.
- **Оружейная**. Если у игрока, пришедшего на эту клетку, меньше 3х патронов (на старте игры их ни у кого нет),
то число патронов в его инвентаре становится равно 3м (максимум). Теперь он может стрелять в заданном направлении.
Если он попадает в другого игрока, тот погибает, и он отправляется на свою стартовую позицию
с пропуском своего следующего хода, а его инвентарь остаётся на позиции, на которой игрока убили.
- **Выход**. Игроку необходим ключ, лежащий где-то на карте. Если игрок двигается из этой клетки в заданном направлении выхода,
имея при себе ключ, он выигрывает, и игра для всех завершается, иначе ведущий сообщает, что игроку нужен ключ, чтобы выйти.

## Формат решения:
**Два режима работы программы:**
1. **check** — проверка поля на достижимость выхода из любой клетки.
2. **game** — сама игра.

В режиме игры запускается игра в интерактивном режиме, то есть игроки будут вводить команды в консоли,
а им туда же будут выводиться ответы "ведущего". В качестве аргумента программа принимает файл с полем — обязательный аргумент,
число игроков и стартовые позиции — опциональные аргументы. Если они не указано число игроков, то игра запустится в одиночном режиме.
Если не указаны стартовые позиции или их недостаточно, то игра запрашивает их в начале игры, сообщив размер поля,
или выбирается рандомно, если установлен флаг ```random_positions```. Когда стартовые позиции заданы, игроки начинают по очереди ходить.

**В свой ход игрок может ввести такие команды:**
- **W/A/S/D** — сходить вверх, влева, вниз, вправо.
- **X <*направление: W/A/S/D*>** — выстрелить в указанном направлении. На это тратится ход. Если у игрока нет патронов,
ведущий сообщает ему об этом вместо выстрела, ход не тратится. Убитый игрок телепортируется на свою стартовую позицию и
пропускает один ход, будучи оглушённым. Инвентарь остаётся на позиции, где игрока пристрелили.
- **E** — посмотреть инвентарь. В базовом варианте сообщается количество патронов у игрока. Ход не тратится.
- **?** - посмотреть список доступных команд с описанием. Ход не тратится.

Когда один из игроков находит выход, ведущий сообщает, что он победитель, и игра для всех завершается.

*Регистр команд неважен.*

**Команды для запуска:**
```
check --map <map_paths/names>
=====
game --map <map_path> --players <players_count> --start_positions <positions as tuple> --random_positions
```
*```--players```, ```--start_positions``` and ```--random_positions``` are optional arguments.*

**Примеры команд:**
```
check --map map.txt
check --map map1.txt map2.txt  <-- you can ckeck multiple maps in a single query
=====
game --map map.txt --start_positions (0,0) <-- starts singleplayer game
game --map map.txt --random_positions <-- starts singleplayer game at a ramdom positions
game --map map.txt --players 2  <-- start positions will be asked before the game starts
game --map map.txt --players 2 --random_positions <-- start positions will be chosen randomly
game --map map.txt --players 2 --start_positions (0,0) --random_positions
game --map map.txt --players 2 --start_positions (0,0) (0,2)
```

## Формат описания поля:
**Пример:**
```
3 3
.|S E
. . _
S . L
. . .
A R .
E Exit(UP)
S Stun(2)
A Armory()
R RubberRoom(RIGHT)
L RubberRoom(LEFT)
```

*Для простоты I/O поля отсчёт идёт построчно и посимвольно, то есть ноль слева-сверху, оси — вниз и вправо.
Например, клетка "A - Armory" находится по координатам (3, 0).*

В первой строчке — размер поля, в данном случае 3x3, дальше — описание поля. На нечётных линиях описаны клетки и вертикальные стены,
на чётных линиях — горизонтальные стены. На нечётной линии нечётные символы задают клетки: "." — обычная пустая клетка,
а буква — особая клетка, значение которой описано ниже. Чётные символы нечётной линии задают вертикальные стены:
пробел — отсутствие стены, а "|" означает, что стена есть. На чётной линии чётный символы ничего не задают,
а нечётные задают горизонтальные стены: пробел означает отсутствие стены, а "\_" означает, что стена есть.
В данном примере, стена есть между левым верхним углом (0, 0) и соседней справа клеткой (0, 1)
и между правым верхним углом (0, 2) и соседней снизу клеткой (1, 2).

Затем идет описание особых клеток, где каждая буква описывается на отдельной строчке. В этих строчках идет буква,
а дальше вызов класса особой клетки с необходимыми ему аргументами. В примере одну из клеток (0, 2) сделали выходом,
причём, чтобы выйти, нужно пойти наверх, другие — оглушение на два хода ((0, 1) и (1, 0)) и так далее.

## Команды для описания особых клеткок с примерами:
**Оглушение:**
```
S Stun(duration)
=====
S Stun(2)
```

**Резиновая комната:**
```
R RubberRoom(direction)
=====
R RubberRoom(RIGHT)
L RubberRoom(LEFT)
```

**Телепорт:**
```
T Teleport(destination)
=====
1 Teleport((0, 2))
2 Teleport((3, 1))
```

**Оружейная:**
```
A Armory()
```

**Выход:**
```
E Exit(direction)
=====
E Exit(LEFT)
```

*Особая клетка может задаваться любым символом. Направления: UP, LEFT, DOWN, RIGHT.*

## Бонусы:
- **0.6 балла**. Новая клетка - сон. Когда игрок переходит на неё,  он “засыпает” и переносится на другое поле. Разумеется, ему об этом не сообщают. Следующие несколько ходов он, ничего не подозревая, будет бродить по другому полю. Там тоже могут быть стены, ловушки, там можно найти ключ, можно умереть, ведь другие игроки заснув попадают на ту же карту, или даже выиграть! Но чтобы с вами не случилось, когда вы проснетесь, по истечению времени или из-за смерти или победы во сне, ваш инвентарь вернется к состоянию, в котором он был до сна, и вы вновь окажетесь на исходной карте, в той точке, где уснули. Ведущий сообщает, что игрок проснулся и что находится у него в инвентаре на самом деле, но не говорит, сколько ходов игрок проспал и где он находится. Пока игрок спит, его настоящее тело продолжает стоять на месте. Это значит, что во время сна игрока могут застрелить и наяву. Иными словами, по сну на самом деле ходит не сам игрок, а его “дух”. Теперь, как задать карту для сна? Это делается следующим образом:
    ```
    2
    2 2
    . E
    Z .
    1 1
    .
    E Exit(1)
    Z Sleep(2, (1, 0, 0))
    ```
    В первой строчке задаётся число полей, дальше размер первого (нулевого вернее), затем его описание, а потом размер следующего поля и так далее. Координаты становятся трехмерными, первый индекс - индекс поля. Стартовые позиции игроков по-прежнему двумерные, они начинают на поле с нулевым индексом. В данном примере клетка сна на два хода переносит “дух” игрока на поле с индексом 1 в точку с координатами (0, 0). Обратите внимание, что внутри сна может быть другой сон! Единственное ограничение - между разными полями не должно быть циклов, в частности из сна не должно быть переходов обратно на “настоящее” поле.
- **1 балл**. Еще один режим работы: случайная генерация карты. На вход принимаем размер карты, файл, куда нужно записать созданное поле, и опционально random seed для возможности воспроизвести результат. В лабиринте должны с какой-то вероятностью появляться особые клетки разных типов. Алгоритм можете выбрать какой хотите, главное чтобы в итоге из любой точки можно было дойти до выхода. Вот несколько источников, где можно почитать про методы генерации обычных лабиринтов:
    - https://en.wikipedia.org/wiki/Maze_generation_algorithm
    - http://www.astrolog.org/labyrnth/algrithm.htm
    - https://habr.com/ru/post/262345/
    - https://habr.com/ru/post/176671/
    - https://habr.com/ru/post/319532/
