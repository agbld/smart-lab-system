import sys
sys.path.append('../')
import time
from agent import Agent

class TestAgent(Agent):
    def __init__(self, name: str, port):
        super().__init__(name, port)
        
    def handle_message(self, message: dict):
        # write the received message to file
        with open(f'.received_messages_{self.name}.txt', 'a') as f:
            f.write(f"{message}\n")

test_agent_1 = TestAgent('agenet_1', 5000)

test_agent_2 = TestAgent('agenet_2', 5001)

cnt = 0
while True:
    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    if cnt % 5 == 0:
        test_agent_1.send_message('127.0.0.1', 5001, True, {'ts': time_str, 'context': 'Important message', 'from': f'{test_agent_1.name}'})
    test_agent_1.send_message('127.0.0.1', 5001, False, {'ts': time_str, 'context': 'message', 'from': f'{test_agent_1.name}'})
    cnt += 1
    time.sleep(1)

