# Официальное ридми
## Технологический стек 
+ PyQT5
+ Numba
+ Numpy
+ Python3.6
## Задача
Создание симулятора спутника в атмосфере тела с множеством упрощений, например, равномерностью атмосферы 
## Ход работы
* Создание архитектуры
* Написание графического движка
* Написание математическкой модели
* Связка графического движка и модели
* Улучшение GUI
* Исправление багов
* Переход на numba для учкорения вычислений




# satelliteSimulator
PyQt5 satellite simulator with air resistance (but infinite atmosphere size)

![Example application image](docs/image01.png?raw=true "Example picture of application")

## Installation
Install Python3.6 or newer and PyQt5, which can be installed using pip3

```pip3 install -r requirements.txt```

## Launch
If you have only one python version installed

```python main.py```


Otherwise you need to specify your version, e.g.

```python3 main.py```
