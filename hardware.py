#%%
# Import libraries

import time
import board
import adafruit_dht
import RPi.GPIO as GPIO
import digitalio
import busio
from adafruit_character_lcd.character_lcd_i2c import Character_LCD_I2C
from adafruit_mcp230xx.mcp23008 import MCP23008
from rpi_lcd import LCD

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

# Published messages repipients definitions

recipients = [
    {'ip_address': '127.0.0.1', 'port': 5000},
]

#%%
# Pin definitions

SEAT_ID_TO_LED_PIN = {
    0: 17,
    1: 16
}
GPIO.setup(SEAT_ID_TO_LED_PIN[0], GPIO.OUT)
GPIO.setup(SEAT_ID_TO_LED_PIN[1], GPIO.OUT)

SEAT_ID_TO_BUTTON_PIN = {
    0: 27,
    1: 22
}
GPIO.setup(SEAT_ID_TO_BUTTON_PIN[0], GPIO.OUT)
GPIO.setup(SEAT_ID_TO_BUTTON_PIN[1], GPIO.OUT)

BUZZER_PIN = 23
GPIO.setup(BUZZER_PIN, GPIO.OUT)

RELAY_PIN = 24
GPIO.setup(RELAY_PIN, GPIO.OUT)

FAN_PIN = 25
GPIO.setup(FAN_PIN, GPIO.OUT)
fan_pwm = GPIO.PWM(FAN_PIN, 25000)
fan_pwm.start(0)

LDR_PIN = 4
GPIO.setup(LDR_PIN, GPIO.IN)

BUTTON_PIN = 5
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

dhtDevice = adafruit_dht.DHT11(board.D12)

# Set the GPIO pin numbering scheme
GPIO.setmode(GPIO.BCM)

# Define lamp pin and set it as output
LAMP_PIN = 13
GPIO.setup(LAMP_PIN, GPIO.OUT)
lamp_pwm = GPIO.PWM(LAMP_PIN, 1000)  # The frequency in Hz
lamp_pwm.start(0)  # Initial duty cycle of 0 percent

lcd = LCD(address=0x26)

#%%
# Hardware access functions

def set_LED(state,seat_id):
    LED_PIN = SEAT_ID_TO_LED_PIN[seat_id]
    if state == 0:  
        GPIO.output(LED_PIN, GPIO.LOW)
    elif state == 1:  
        GPIO.output(LED_PIN, GPIO.HIGH)


def set_lamp(value):
    """
    設定燈的亮度。
    
    :param value: 數值範圍從0到100，代表亮度百分比。
    """
    if 0 <= value <= 100:
        lamp_pwm.ChangeDutyCycle(value)
    else:
        print("Error: Value should be between 0 and 100.")

def set_relay(value):
    """
    设置继电器的状态。

    :param value: 布尔值，True 为打开，False 为关闭。
    """
    if value:
        GPIO.output(RELAY_PIN, GPIO.HIGH)  # 打开继电器
    else:
        GPIO.output(RELAY_PIN, GPIO.LOW)   # 关闭继电器


def set_lcd(text):
    """
    设置LCD的文本。

    :param text: 要显示的文本字符串
    """
    lcd.text(text, 1)

def set_AC(value):
    """
    设置风扇的速度。

    :param value: 范围从0到100，代表风扇速度的百分比。
    """
    if 0 <= value <= 100:
        fan_pwm.ChangeDutyCycle(value)
    else:
        print("Error: Value should be between 0 and 100.")

def ring_alarm():
    """
    控制蜂鸣器响三声。
    """
    for _ in range(3):
        for _ in range(100):
            GPIO.output(BUZZER_PIN, GPIO.HIGH)  # 打开蜂鸣器
            time.sleep(0.001)  # 蜂鸣器响0.5秒
            GPIO.output(BUZZER_PIN, GPIO.LOW)   # 关闭蜂鸣器
            time.sleep(0.001)  # 停止0.5秒
        time.sleep(0.05)  # 停止0.5秒

def get_seat_doorbell(seat_id):
    # return True if button is pressed, False otherwise
    btn_pin = SEAT_ID_TO_BUTTON_PIN[seat_id]
    return GPIO.input(btn_pin)

def get_register_button():
   return GPIO.input(BUTTON_PIN)

def get_temperature():
    try:
        temperature_c = dhtDevice.temperature
        return temperature_c
    except RuntimeError as error:
            print(error.args[0])
            time.sleep(2.0)
    except Exception as error:
            dhtDevice.exit()
            raise error

def get_humidity():
    # 返回湿度百分比
    try:
        humidity = dhtDevice.humidity
        return humidity
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
    except Exception as error:
        dhtDevice.exit()
        raise error
# %%
