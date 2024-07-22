from threading import Thread
from time import sleep


class Knight(Thread):
    def __init__(self, name, power):
        self.knight_name = name
        self.power = power
        super().__init__()
        self.enemy_count = 100

    def run(self):
        print(f'{self.knight_name}, на нас напали!')
        days = 0
        while self.enemy_count > 0:
            self.enemy_count -= self.power
            days += 1
            sleep(1)
            print(f'{self.knight_name} сражается {days} день(дня)..., осталось {self.enemy_count} войнов.\n', end="")
        print(f'{self.knight_name} одержал победу спустя {days} дней(дня)!')


first_knight = Knight('Sir Lancelot', 10)
second_knight = Knight("Sir Galahad", 20)

first_knight.start()
second_knight.start()

first_knight.join()
second_knight.join()

print('Все битвы закончились!')
