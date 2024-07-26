from multiprocessing import Process, Manager


class WarehouseManager:
    def __init__(self):
        self.data = Manager().dict()

    def process_request(self, request):
        name = request[0]
        command = request[1]
        amount = request[2]
        if command == 'receipt':
            if name in self.data.keys():
                self.data[name] += amount
            else:
                self.data[name] = amount
        elif command == 'shipment':
            if name in self.data.keys() and self.data[name] >= amount:
                self.data[name] -= amount

    def run(self, requests):
        actions = []
        for request in requests:
            proc = Process(target=self.process_request, args=(request,))
            actions.append(proc)
            proc.start()
        for proc in actions:
            proc.join()


if __name__ == '__main__':
    manager = WarehouseManager()
    requests = [
        ("product1", "receipt", 100),
        ("product2", "receipt", 150),
        ("product1", "shipment", 30),
        ("product3", "receipt", 200),
        ("product2", "shipment", 50)
    ]
    manager.run(requests)
    print(manager.data)
