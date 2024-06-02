import agent
import hardware

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
    {'ip_address': '127.0.0.1', 'port': 5000},
]

outdoor_face_rec_agent = agent.OudoorFaceRecAgent('outdoor_face_rec_agent', './known_faces', recipients=recipients, port=5001, state=state, seat_id_to_rgb_pin=hardware.SEAT_ID_TO_RGB_PIN)

outdoor_face_rec_agent.make_known_faces_embeddings()

outdoor_face_rec_agent.face_recognition()