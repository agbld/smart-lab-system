import threading
import time
import requests
import abc
from flask import Flask, request, jsonify

class Agent(metaclass=abc.ABCMeta):
    """
    A parent class for all Raspberry Pi agents.
    
    ...

    Attributes
    ----------
    state : dict
        a dictionary to store the state of the agent
    _incoming_messages : list
        a list to store the incoming messages
    _outgoing_messages : list
        a list to store the outgoing messages
    __name : str
        a string to store the name of the agent

    Methods
    -------
    handle_message(message: dict)
        an abstract method to handle a message
    send_message(ip_address: str, port: int, resend_if_failed: bool, message: dict)
        a method to send a message to another agent
    """
    def __init__(self, name: str, port: int = 5000):
        self.state = {}
        self._incoming_messages = []
        self._outgoing_messages = []
        self.__name = name
        self.__start_message_listener(port=port)
        self.__start_message_handler()
        self.__start_message_sender()

    @property
    def name(self):
        return self.__name
        
    def __start_message_listener(self, port: int = 5000):
        def _message_listener():
            app = Flask(__name__)

            @app.route('/message', methods=['POST'])
            def message():
                message = request.json
                self._incoming_messages.append(message)
                return jsonify({'status': 'success'})
            
            app.run(host='0.0.0.0', port=port)  # Listen on all interfaces

        self._message_listener = threading.Thread(target=_message_listener)
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
        def _message_handler():
            while True:
                if self._incoming_messages:
                    message = self._incoming_messages.pop(0)
                    self.handle_message(message)
                time.sleep(0.1)

        self._message_handler = threading.Thread(target=_message_handler)
        self._message_handler.start()

    def __start_message_sender(self):
        def _message_sender():
            while True:
                for message in self._outgoing_messages:
                    try: 
                        requests.post(f'http://{message["ip_address"]}:{message["port"]}/message', json=message['message'])
                        self._outgoing_messages.remove(message)
                    except requests.exceptions.ConnectionError:
                        if not message['resend_if_failed']:
                            self._outgoing_messages.remove(message)
                    time.sleep(0.1)

        self._message_sender = threading.Thread(target=_message_sender)
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


