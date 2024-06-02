import agent
import hardware

boss_agent = agent.BossAgent('Boss', port=5000, recipients=hardware.recipients, state=hardware.state)
