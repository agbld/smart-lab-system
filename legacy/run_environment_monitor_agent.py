import agent
import hardware

boss_agent = agent.BossAgent('Boss', port=5000, recipients=hardware.recipients, state=hardware.state, photoresistor_threshold = 100, humidity_threshold = 50, temperature_threshold = 25)