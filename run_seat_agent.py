import agent
import hardware

seat_agent = agent.SeatAgent('agbld', './known_faces', recipients=hardware.recipients, port=5000, state=hardware.state, check_interval=5, important_person='shawn')

seat_agent.make_known_faces_embeddings()

seat_agent.face_recognition()