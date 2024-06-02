import agent
import hardware

outdoor_face_rec_agent = agent.OudoorFaceRecAgent('./known_faces', recipients=hardware.recipients, port=5001, state=hardware.state)

outdoor_face_rec_agent.make_known_faces_embeddings()

outdoor_face_rec_agent.face_recognition()