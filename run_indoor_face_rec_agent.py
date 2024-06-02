import agent
import hardware

indoor_face_rec_agent = agent.IndoorFaceRecAgent('./known_faces', recipients=hardware.recipients, port=5001, state=hardware.state)

indoor_face_rec_agent.make_known_faces_embeddings()

indoor_face_rec_agent.face_recognition()