import agent
import hardware

indoor_face_rec_agent = agent.IndoorFaceRecAgent('./known_faces', recipients=hardware.recipients, port=5000, state=hardware.state, brightness_threshold = 50, humidity_threshold = 50, temperature_threshold = 25)

# indoor_face_rec_agent.make_known_faces_embeddings()

indoor_face_rec_agent.face_recognition()