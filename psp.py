from car import Car, MonsterTruck

def _q_01():
    """
    ============================================================================
    Часть 1
    ----------------------------------------------------------------------------
    >>> apalkoff_car = Car('Tesla', 'Model S')
    >>> apalkoff_car.color
    'Без цвета. Покрась меня.'

    >>> apalkoff_car.paint('чёрный')
    'Цвет Tesla Model S теперь чёрный'

    >>> apalkoff_car.color
    'чёрный'

    ============================================================================
    Часть 2
    ----------------------------------------------------------------------------
    >>> apalkoff_car = Car('Tesla', 'Model S')
    >>> apalkoff_car.model
    'Model S'

    >>> apalkoff_car.gas = 10
    >>> apalkoff_car.drive()
    'Tesla Model S делает врум-врум!'

    >>> apalkoff_car.drive()
    'Tesla Model S не может ехать!'

    >>> apalkoff_car.fill_gas()
    'Количество бензина в Tesla Model S: 20'

    >>> apalkoff_car.gas
    20

    >>> Car.gas
    30

    ============================================================================
    Часть 3
    ----------------------------------------------------------------------------
    >>> Car.headlights
    2

    >>> apalkoff_car.headlights
    2

    >>> Car.headlights = 3
    >>> apalkoff_car.headlights
    3

    >>> apalkoff_car.headlights = 2
    >>> Car.headlights
    3

    ============================================================================
    Часть 4
    ----------------------------------------------------------------------------
    >>> apalkoff_car.wheels = 2
    >>> apalkoff_car.wheels
    2

    >>> Car.num_wheels
    4

    >>> apalkoff_car.drive()
    'Tesla Model S не может ехать!'

    >>> Car.drive()
    Traceback (most recent call last):
      ...
    TypeError: Car.drive() missing 1 required positional argument: 'self'

    >>> Car.drive(apalkoff_car)
    'Tesla Model S не может ехать!'

    ============================================================================
    Часть 5
    ----------------------------------------------------------------------------
    >>> apalkoff_car = MonsterTruck('Монстр', 'Бэтмобиль')
    >>> apalkoff_car.drive()
    ДРЫН-ДЫН-ДЫН! Этот монстр-трак просто огромный!
    'Монстр Бэтмобиль делает врум-врум!'

    >>> Car.drive(apalkoff_car)
    'Монстр Бэтмобиль делает врум-врум!'

    >>> MonsterTruck.drive(apalkoff_car)
    ДРЫН-ДЫН-ДЫН! Этот монстр-трак просто огромный!
    'Монстр Бэтмобиль делает врум-врум!'

    >>> Car.rev(apalkoff_car)
    Traceback (most recent call last):
      ...
    AttributeError: type object 'Car' has no attribute 'rev'
    """
    return 0

# Ниже этого места трогать ничего не нужно.

if __name__ == '__main__':
    import doctest, sys
    finder = doctest.DocTestFinder()
    runner = doctest.DocTestRunner(doctest.OutputChecker(), optionflags=doctest.FAIL_FAST)
    doctest.OutputChecker.output_difference = lambda a, b, c, d: ""
    m = sys.modules.get('__main__')
    for test in finder.find(m, m.__name__):
        if test.name == '__main__': continue
        if test.name.split('.')[1][:2] != '_q': continue
        for example in test.examples: example.options[doctest.SKIP] = False
        if  runner.run(test).failed != 0: break
