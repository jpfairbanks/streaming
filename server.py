import msgpackrpc
import time

class SumServer(object):
    def sum(self, x, y):
        return x + y
    def sleepy_sum(self, x, y):
        time.sleep(1)
        return x + y
server = msgpackrpc.Server(SumServer())
server.listen(msgpackrpc.Address("localhost", 18800))
server.start()
