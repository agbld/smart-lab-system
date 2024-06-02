from agent import Agent
import hardware

class MessageLoggerAgent(Agent):
    def __init__(self, name: str, port: int = 5000, recipients: list = [], state: dict = {}, seat_id_to_rgb_pin: dict = {}):
        super().__init__(name, port, recipients, state, seat_id_to_rgb_pin)
        
    def handle_message(self, message: dict):
        # write the received message to file
        with open(f'.received_messages_{self.name}.txt', 'a') as f:
            f.write(f"{message}\n")

test_agent_2 = MessageLoggerAgent('agenet_2', port=5000, recipients=hardware.recipients, state=hardware.state)
