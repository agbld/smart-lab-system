# Import libraries

# ...

# Pin definitions

SEAT_ID_TO_RGB_PIN = {
    0: (0, 1, 2),
    1: (3, 4, 5),
}

RELAY_PIN = 6

SEAT_ID_TO_BUTTON_PIN = {
    0: 7,
    1: 8,
}


# Hardware access functions

def set_seat_rgb(seat_id, r, g, b):
    # set the RGB LED to the given value
    r_pin = SEAT_ID_TO_RGB_PIN[seat_id][0]
    g_pin = SEAT_ID_TO_RGB_PIN[seat_id][1]
    b_pin = SEAT_ID_TO_RGB_PIN[seat_id][2]
    pass

def set_relay(value):
    # set the relay to the given value
    pass

def set_lcd(text):
    # set the LCD text
    pass

def get_seat_button(seat_id):
    # return True if button is pressed, False otherwise
    btn_pin = SEAT_ID_TO_BUTTON_PIN[seat_id]
    pass

def get_temperature():
    # return the temperature in Celsius
    pass

def get_humidity():
    # return the humidity in %
    pass

def get_photoresistor():
    # return the light intensity in %
    pass