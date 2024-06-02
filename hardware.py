# Import libraries

# ...

# Pin definitions

seat_id_to_rgb_pin = {
    0: (0, 1, 2),
    1: (3, 4, 5),
}

# Hardware access functions

def set_rgb(r_pin, g_pin, b_pin, r, g, b):
    # set the RGB LED to the given value
    pass

def set_relay(pin, value):
    # set the relay to the given value
    pass

def set_lcd(text):
    # set the LCD text
    pass

def get_button(pin):
    # return True if button is pressed, False otherwise
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