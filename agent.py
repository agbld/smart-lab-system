import threading
import time
import requests
import abc
import os
import face_recognition
import cv2
import numpy as np
import pickle

from flask import Flask, request, jsonify

import hardware

class Agent(metaclass=abc.ABCMeta):
    def __init__(self, name: str, port: int = 5000, recipients: list = [], state: dict = {}, seat_id_to_rgb_pin: dict = {}):
        self._state = state
        self.__name = name
        self._seat_id_to_rgb_pin = seat_id_to_rgb_pin
        self.__recipients = recipients
        self._incoming_messages = []
        self._outgoing_messages = []
        self.__start_message_listener(port=port)
        self.__start_message_handler()
        self.__start_message_sender()
        self.__start_LED_seat_indicators()

    @property
    def state(self):
        return self._state

    @property
    def name(self):
        return self.__name
        
    def __start_message_listener(self, port: int = 5000):
        def message_listener():
            app = Flask(__name__)

            @app.route('/message', methods=['POST'])
            def message():
                message = request.json
                self._incoming_messages.append(message)
                return jsonify({'status': 'success'})
            
            app.run(host='0.0.0.0', port=port)  # Listen on all interfaces

        self._message_listener = threading.Thread(target=message_listener)
        self._message_listener.start()

    @abc.abstractmethod
    def handle_message(self, message: dict):
        """
        An abstract method to handle a message.

        Parameters
        ----------
        message : dict
            A dictionary to specify the message to be handled.
        """
        pass
    
    def __start_message_handler(self):
        def message_handler():
            while True:
                if self._incoming_messages:
                    message = self._incoming_messages.pop(0)
                    if 'state' in message:
                        self._state = message['state']
                    else:
                        self.handle_message(message)
                # time.sleep(0.1)

        self._message_handler = threading.Thread(target=message_handler)
        self._message_handler.start()

    def __start_message_sender(self):
        def message_sender():
            while True:
                for message in self._outgoing_messages:
                    try: 
                        requests.post(f'http://{message["ip_address"]}:{message["port"]}/message', json=message['message'])
                        self._outgoing_messages.remove(message)
                    except requests.exceptions.ConnectionError:
                        if not message['resend_if_failed']:
                            self._outgoing_messages.remove(message)
                    time.sleep(0.1)

        self._message_sender = threading.Thread(target=message_sender)
        self._message_sender.start()

    def send_message(self, ip_address: str, port: int, resend_if_failed: bool, message: dict):
        """
        A method to send a message to another agent.
        
        Parameters
        ----------
        ip_address : str
            A string to specify the IP address of the agent to send the message to.
        port : int
            An integer to specify the port of the agent to send the message to.
        resend_if_failed : bool
            A boolean to specify whether the message should be resent if the sending fails.
        message : dict
            A dictionary to specify the message to be sent.
        """
        self._outgoing_messages.append({'ip_address': ip_address, 'port': port, 'resend_if_failed': resend_if_failed, 'message': message})
    
    def publish_message(self, resend_if_failed: bool, message: dict):
        """
        A method to publish a message to all recipients.
        
        Parameters
        ----------
        message : dict
            A dictionary to specify the message to be published.
        """
        for recipient in self.__recipients:
            self.send_message(recipient['ip_address'], recipient['port'], resend_if_failed, message)

    def __start_LED_seat_indicators(self):
        def update_LED_seat_indicators():
            while True:
                for member in self.state['member']:
                    if member['status'] == 0:
                        hardware.set_seat_rgb(member['seat_id'], 0, 0, 0) # Turn off the LED
                    elif member['status'] == 1:
                        hardware.set_seat_rgb(member['seat_id'], 255, 255, 0) # Yellow
                    elif member['status'] == 2:
                        hardware.set_seat_rgb(member['seat_id'], 0, 255, 0) # Green
                time.sleep(0.5)

        self._LED_seat_indicators = threading.Thread(target=update_LED_seat_indicators)
        self._LED_seat_indicators.start()

class FaceRecAgent(Agent):
    def __init__(self, name: str, known_faces_dir: str, port: int = 5000, recipients: list = [], state: dict = {}, seat_id_to_rgb_pin: dict = {}):
        super().__init__(name, port, recipients, state, seat_id_to_rgb_pin)

        self.__known_faces_dir = known_faces_dir

    @property
    def known_faces_dir(self):
        return self.__known_faces_dir
    
    def make_known_faces_embeddings(self):
        known_faces_dir = self.known_faces_dir

        known_faces = {'names': [], 'encodings': []}

        for person in os.listdir(known_faces_dir):
            person_dir = os.path.join(known_faces_dir, person)
            if not os.path.isdir(person_dir):
                continue

            print(f"Processing {person}")
            person_images = os.listdir(person_dir)

            person_face_encodings = []
            for image in person_images:
                image_path = os.path.join(person_dir, image)
                image = self.load_image(image_path)
                faces = self.get_faces_from_frame(image)
                face_encodings = self.get_face_encodings_from_faces(faces)
                person_face_encodings.extend(face_encodings[0])
            person_face_encodings = np.array(person_face_encodings)

            person_average_face_encoding = np.mean(person_face_encodings, axis=0)
            
            known_faces['names'].append(person)
            known_faces['encodings'].append(person_average_face_encoding)

        # Save the known_faces dict to a file
        file_path = os.path.join(known_faces_dir, "known_faces.pickle")
        with open(file_path, 'wb') as f:
            pickle.dump(known_faces, f)
        print("Saved known_faces to a file")
    
    def face_recognition(self):
        # Load the known_faces from the pickle file
        file_path = os.path.join(self.known_faces_dir, "known_faces.pickle")
        with open(file_path, 'rb') as f:
            known_faces = pickle.load(f)

        # Print known persons
        print("Known persons:")
        for person in known_faces['names']:
            print(person)
        print()

        # Continiously recognize the faces from the video capture

        # Open the video capture
        video_capture = cv2.VideoCapture(0)

        # Setup tolerance for face recognition. Lower is more strict.
        tolerance = 0.6

        same_face_count = 0
        last_person = "Unknown"

        while True:
            # Start the timer for calculating the frames per second
            start = time.time()

            # Get the frame from the video capture
            frame = self.get_frame_rgb(video_capture, continious=True, resize_ratio=0.5)

            # Recognize the faces from the frame
            name = "Unknown"
            try:
                faces = self.get_faces_from_frame(frame)
                face_encoding = self.get_face_encodings_from_faces(faces)[0] # Only handle the first face in current implementation
                face_distances = face_recognition.face_distance(known_faces['encodings'], face_encoding)
                best_match_index = np.argmin(face_distances) # Get the index of the best match

                # If the best match is within the tolerance, set the name
                if face_distances[best_match_index] < tolerance:
                    name = known_faces['names'][best_match_index]
            except:
                pass

            if name != "Unknown":
                if name == last_person:
                    same_face_count += 1
                else:
                    same_face_count = 0
                    last_person = name
                
                if same_face_count > 5: # TODO: Change this to a proper value on target device
                    self.found_person(name)
            
            # Calculate the recognized frames per second
            interval = time.time() - start
            fps = 1 / interval

            print(f"FPS: {fps:.2f} - Found {name}        ", end="\r")

    def found_person(self, name: str):
        # Find the person in the state
        for member in self.state['member']:
            if member['name'] == name:
                member['status'] = 1
                break

        # Update the LCD
        hardware.set_lcd(f"Hello {name}!")
        
        # Send the updated state to the recipients
        self.publish_message(resend_if_failed=False, message={'state': self.state})
        self.publish_message(resend_if_failed=False, message={'found': f"{name}", 'from': f"{self.name}"})

        # Turn on the relay for 1 second
        hardware.set_relay(True)
        time.sleep(1)
        hardware.set_relay(False)

    def load_image(self, image_path: str, resize_ratio: float = 1) -> np.ndarray:
        """
        Load an image from a file path.
        """

        image = cv2.imread(image_path)

        if resize_ratio != 1:
            image = cv2.resize(image, (0, 0), fx=resize_ratio, fy=resize_ratio)

        assert image is not None, f"Failed to load image from path: {image_path}"

        return image

    def get_frame_rgb(self, video_capture: cv2.VideoCapture, continious: bool = False, resize_ratio: float = 1) -> np.ndarray:
        """
        Get a single frame from the video capture and return the frame in RGB format.
        """

        ret, frame = video_capture.read()

        if resize_ratio != 1:
            frame = cv2.resize(frame, (0, 0), fx=resize_ratio, fy=resize_ratio)

        if not continious:
            video_capture.release()

        assert ret, "Failed to read frame from video capture."

        return frame[:, :, ::-1]

    def get_faces_from_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Get all faces from a frame.
        """

        face_locations = face_recognition.face_locations(frame)
        faces = []
        for (top, right, bottom, left) in face_locations:
            face_frame = frame[top:bottom, left:right]
            faces.append(face_frame)

        return np.array(faces)

    def get_face_encodings_from_faces(self, faces: np.ndarray) -> np.ndarray:
        """
        Get the face encodings from a list of faces.
        """
        face_encodings = []
        for face in faces:
            face_encoding = face_recognition.face_encodings(face)
            face_encodings.append(face_encoding) 

        return np.array(face_encodings)

    def handle_message(self, message: dict):
        pass