import agent
import hardware

outdoor_face_rec_agent = agent.OudoorFaceRecAgent('./known_faces', recipients=hardware.recipients, port=5000, state=hardware.state, recheck_counts=1)

# outdoor_face_rec_agent.make_known_faces_embeddings()

outdoor_face_rec_agent.face_recognition()