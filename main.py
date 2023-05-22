import RPi.GPIO as GPIO
import time
from configparser import ConfigParser
from helpers import init_all_loggers, get_main_bot_logger


logger = get_main_bot_logger()


def toggle_relay(relay_pin, duration):
    GPIO.output(relay_pin, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(relay_pin, GPIO.LOW)
    logger.info(f"Relay {relay_pin} activated")

def main(config):
    config_settings = config['SETTINGS']
    config_gpio = config['GPIO']
    init_all_loggers(log_level=config_settings.get("LOG_LEVEL"))

    TRIG = int(config_gpio.get("ULTRASONIC_TRIG"))
    ECHO = int(config_gpio.get("ULTRASONIC_ECHO"))
    RELAY = int(config_gpio.get("RELAY"))
    DURATION = int(config_settings.get("RELAY_DURATION"))

    logger.info(f"Starting up main....")
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        max_time = 0.04
        while True:
            GPIO.setup(TRIG,GPIO.OUT)
            GPIO.setup(ECHO,GPIO.IN)
            GPIO.setup(RELAY, GPIO.OUT)

            GPIO.output(TRIG,False)
            time.sleep(0.01)
            GPIO.output(TRIG,True)
            time.sleep(0.00001)
            GPIO.output(TRIG,False)

            pulse_start = time.time()
            timeout = pulse_start + max_time
            while GPIO.input(ECHO) == 0 and pulse_start < timeout:
                pulse_start = time.time()

            pulse_end = time.time()
            timeout = pulse_end + max_time
            while GPIO.input(ECHO) == 1 and pulse_end < timeout:
                pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17000
            distance = round(distance, 2)

            if distance < 20:
                toggle_relay(relay_pin=RELAY, duration=DURATION)

    except Exception as e:
        logger.info(f"__Exception:Main__: {e}")
        GPIO.cleanup()


if __name__ == "__main__":
    config = ConfigParser()
    config.read("config.ini")

    main(config)