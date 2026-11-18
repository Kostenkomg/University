class Car(object):
    num_wheels = 4
    gas = 30
    headlights = 2
    size = 'Малышка'

    def __init__(self, make, model):
        self.make = make
        self.model = model
        self.color = 'Без цвета. Покрась меня.'
        self.wheels = Car.num_wheels
        self.gas = Car.gas

    def paint(self, color):
        self.color = color
        return 'Цвет ' + self.make + ' ' + self.model + ' теперь ' + color

    def drive(self):
        if self.wheels < Car.num_wheels or self.gas <= 0:
            return self.make + ' ' + self.model + ' не может ехать!'
        self.gas -= 10
        return self.make + ' ' + self.model + ' делает врум-врум!'

    def pop_tire(self):
        if self.wheels > 0:
            self.wheels -= 1

    def fill_gas(self):
        self.gas += 20
        return 'Количество бензина в ' + self.make + ' ' + self.model + ': ' + str(self.gas)


class MonsterTruck(Car):
    size = 'Монстр'

    def rev(self):
        print('ДРЫН-ДЫН-ДЫН! Этот монстр-трак просто огромный!')

    def drive(self):
        self.rev()
        return Car.drive(self)


# --- Пример выполнения кода (создание объектов и вызов методов) ---
my_car = Car('Tesla', 'Model S')
print(my_car.paint('красный'))
print(my_car.drive())
my_car.pop_tire()
print(my_car.drive())
print(my_car.fill_gas())

print('-' * 30)

monster = MonsterTruck('Bigfoot', 'F-250')
print(monster.size)
print(monster.drive())
