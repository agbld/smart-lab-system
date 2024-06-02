#%%

import sys
sys.path.append('..')
import time
from agent import Agent
import hardware

class TestAgent(Agent):
    def __init__(self, name: str, port: int = 5000, recipients: list = [], state: dict = {}, seat_id_to_rgb_pin: dict = {}):
        super().__init__(name, port, recipients, state, seat_id_to_rgb_pin)
        
    def handle_message(self, message: dict):
        # write the received message to file
        with open(f'.received_messages_{self.name}.txt', 'a') as f:
            f.write(f"{message}\n")

# test_agent_1 = TestAgent('agenet_1', 5000)

state = {
    "member": [
        {
            "name": "agbld",
            "status": 0,
            "seat_id": 0,
        },
        {
            "name": "shawn ",
            "status": 0,
            "seat_id": 1,
        }
    ]
}

recipients = [
    # {'ip_address': '127.0.0.1', 'port': 5000},
]

# face_rec_agent = TestAgent('agenet_2', port=5001, recipients=recipients, state=state, seat_id_to_led_pin=hardware.seat_id_to_led_pin)

test_agent_2 = TestAgent('agenet_2', port=5000, recipients=recipients, state=state, seat_id_to_rgb_pin=hardware.SEAT_ID_TO_RGB_PIN)
#%%
# cnt = 0
# while True:
#     time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
#     if cnt % 5 == 0:
#         test_agent_1.send_message('127.0.0.1', 5001, True, {'ts': time_str, 'context': 'Important message', 'from': f'{test_agent_1.name}'})
#     test_agent_1.send_message('127.0.0.1', 5001, False, {'ts': time_str, 'context': 'message', 'from': f'{test_agent_1.name}'})
#     cnt += 1
#     time.sleep(1)

