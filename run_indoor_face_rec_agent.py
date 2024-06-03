import agent
import hardware

indoor_face_rec_agent = agent.IndoorFaceRecAgent('./known_faces', recipients=hardware.recipients, port=5001, state=hardware.state, photoresistor_threshold = 100, humidity_threshold = 50, temperature_threshold = 25)

indoor_face_rec_agent.make_known_faces_embeddings()

indoor_face_rec_agent.face_recognition()