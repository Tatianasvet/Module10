from threading import Thread
from time import sleep
from queue import Queue

TABLE_COUNT = 3
CUSTOMER_COUNT = 20
SERVE_TIME = 5


class Table:
    def __init__(self, number):
        self.number = number
        self.is_busy = False


class Customer(Thread):
    def __init__(self, number):
        self.num = number
        self.table = None
        super().__init__()

    def run(self):
        self.table.is_busy = True
        print(f'Посетитель номер {self.num} сел за стол номер {self.table.number}')
        sleep(SERVE_TIME)
        print(f'Посетитель номер {self.num} покушал и ушёл.')
        self.table.is_busy = False


class Cafe:
    def __init__(self, tables):
        self.queue = Queue()
        self.tables = tables
        self.is_open = False
        self.customer_list = []

    def free_table_search(self):
        for table in self.tables:
            if not table.is_busy:
                return table
        return None

    def queue_manager(self):
        while self.is_open or not self.queue.empty():
            table = self.free_table_search()
            if table is not None and not self.queue.empty():
                customer = self.queue.get()
                customer.table = table
                customer.start()
                self.customer_list.append(customer)
        for customer in self.customer_list:
            customer.join()

    def customer_arrival(self):
        self.is_open = True
        queue_manager_thread = Thread(target=self.queue_manager)
        queue_manager_thread.start()
        for n in range(1, CUSTOMER_COUNT + 1):
            cust = Customer(n)
            print(f'Посетитель номер {n} прибыл')
            self.serve_customer(cust)
            sleep(1)
        self.is_open = False
        queue_manager_thread.join()

    def serve_customer(self, customer):
        table = self.free_table_search()
        if table is not None and self.queue.empty():
            customer.table = table
            customer.start()
            self.customer_list.append(customer)
        else:
            print(f'Посетитель номер {customer.num} ожидает свободный стол')
            self.queue.put(customer)


tables = [Table(n) for n in range(1, TABLE_COUNT + 1)]
cafe = Cafe(tables)

customer_arrival_thread = Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()
customer_arrival_thread.join()
