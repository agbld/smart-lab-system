from agent import Agent
import hardware

class MessageLoggerAgent(Agent):
    def __init__(self, name: str, port: int = 5000, recipients: list = [], state: dict = {}, seat_id_to_rgb_pin: dict = {}):
        super().__init__(name, port, recipients, state, seat_id_to_rgb_pin)
        
    def handle_message(self, message: dict):
        # write the received message to file
        with open(f'.received_messages_{self.name}.txt', 'a') as f:
            f.write(f"{message}\n")

state = {
    "member": [
        {
            "name": "agbld",
            "status": 0,
            "seat_id": 0,
            "ip_address": "127.0.0.1",
            "port": 9999,
        },
        {
            "name": "shawn ",
            "status": 0,
            "seat_id": 1,
            "ip_address": "127.0.0.1",
            "port": 9999,
        }
    ]
}

recipients = [
    # {'ip_address': '127.0.0.1', 'port': 5000},
]

test_agent_2 = MessageLoggerAgent('agenet_2', port=5000, recipients=recipients, state=state, seat_id_to_rgb_pin=hardware.SEAT_ID_TO_RGB_PIN)
