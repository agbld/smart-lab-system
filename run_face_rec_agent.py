#%%
import agent
import hardware

state = {
    "member": [
        {
            "name": "agbld",
            "status": 0,
            "seat_id": 0,
        },
        {
            "name": "shawn ",
            "status": 0,
            "seat_id": 1,
        }
    ]
}

recipients = [
    {'ip_address': '127.0.0.1', 'port': 5000},
]

face_rec_agent = agent.FaceRecAgent('face_rec_agent', './known_faces', recipients=recipients, port=5001, state=state, seat_id_to_rgb_pin=hardware.seat_id_to_rgb_pin)

face_rec_agent.make_known_faces_embeddings()

face_rec_agent.face_recognition()