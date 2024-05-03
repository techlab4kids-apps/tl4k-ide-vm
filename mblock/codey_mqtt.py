from cloud_message.mqtt import MQTTClient
import codey
import rocky
import time
import ubinascii
import json
import random

# Fill in your router's ssid and password here.

rete = 'procioniopossum'
password = 'tombolina'
#rete = 'TL4K-4G-NET'
#password = 'techlab4kids'

MQTTHOST = "192.168.10.119"
MQTTPORT = 1883

DEBUG_MODE = True

# Fill in as you like
CODEY_ID = random.randint(1000, 9999)
clientID = 'TL4K-Codey-{}'.format(CODEY_ID)

# Example Path
myTopic = "tl4k/{}/command/#".format(clientID)
broadcastTopic = "tl4k/broadcast/command/#"

mqttClient = MQTTClient(clientID, MQTTHOST, port=MQTTPORT, user='', password='', keepalive=0, ssl=False)

# Connect to the MQTT server
def mqtt_connect():
    time.sleep(1)
    mqttClient.connect()

def handle_led_show(params):
    r = params.get('r', 0)
    g = params.get('g', 0)
    b = params.get('b', 0)
    codey.led.show(r, g, b)

def handle_led_set_red(params):
    val = params.get('val', 0)
    codey.led.set_red(val)

def handle_led_set_green(params):
    val = params.get('val', 0)
    codey.led.set_green(val)

def handle_led_set_blue(params):
    val = params.get('val', 0)
    codey.led.set_blue(val)

def handle_led_off(params):
    codey.led.off()

def handle_display_show_image(params):
    image = params.get('image', '')
    pos_x = params.get('pos_x', 0)
    pos_y = params.get('pos_y', 0)
    time_s = params.get('time_s', None)
    codey.display.show_image(image, pos_x, pos_y, time_s)

def handle_display_show(params):
    var = params.get('var', '')
    pos_x = params.get('pos_x', 0)
    pos_y = params.get('pos_y', 0)
    wait = params.get('wait', True)
    codey.display.show(var, pos_x, pos_y, wait)

def handle_display_set_pixel(params):
    pos_x = params.get('pos_x', 0)
    pos_y = params.get('pos_y', 0)
    status = params.get('status', True)
    codey.display.set_pixel(pos_x, pos_y, status)

def handle_display_get_pixel(params):
    pos_x = params.get('pos_x', 0)
    pos_y = params.get('pos_y', 0)
    return codey.display.get_pixel(pos_x, pos_y)

def handle_display_toggle_pixel(params):
    pos_x = params.get('pos_x', 0)
    pos_y = params.get('pos_y', 0)
    codey.display.toggle_pixel(pos_x, pos_y)

def handle_display_clear(params):
    codey.display.clear()

def handle_display_show_emotion(params, emotion):
    codey.display.show_image(emotion)

def handle_rocky_stop(params):
    rocky.stop()

def handle_rocky_forward(params):
    print_debug("handle_rocky_forward", params)

    speed = params.get('speed', 50)
    print_debug("handle_rocky_forward", "speed: {}".format(speed))

    time_s = params.get('time_s', 1)
    print_debug("handle_rocky_forward", "time_s: {}".format(time_s))

    straight = params.get('straight', True)
    print_debug("handle_rocky_forward", "straight: {}".format(straight))

    rocky.forward(speed, time_s, straight)

def handle_rocky_backward(params):
    speed = params.get('speed',100)
    time_s = params.get('time_s',0)
    straight = params.get()
    rocky.backward(speed, time_s, straight)

def handle_rocky_turn_left(params):
    speed = params.get('speed',100)
    time_s = params.get('time_s',0)
    rocky.turn_left(speed, time_s)

def handle_rocky_turn_right(params):
    speed = params.get('speed',100)
    time_s = params.get('time_s',0)
    rocky.turn_right(speed, time_s)

def handle_rocky_drive(params):
    left_power = params.get('left_power',100)
    right_power = params.get('right_power',100)
    rocky.drive(left_power, right_power)

def handle_rocky_turn_right_by_degree(params):
    angle = params.get('angle',90)
    speed = params.get('speed',40)
    rocky.turn_right_by_degree(angle, speed)

def handle_rocky_turn_left_by_degree(params):
    angle = params.get('angle',90)
    speed = params.get('speed',40)
    rocky.turn_left_by_degree(angle, speed)

def handle_get_loudness(params):
    codey.sound_sensor.get_loudness()

def handle_light_sensor_get_value(params):
    codey.light_sensor.get_value()

def handle_potentiometer_get_value(params):
    codey.potentiometer.get_value()

# Function to convert a column to hexadecimal
def column_to_hex(col_data):
    #print("column_to_hex '{}'".format(col_data))
    # Join the column data into a single string of binary numbers
    binary_string = ''.join(str(bit) for bit in col_data)
    #print("column_to_hex binary_string '{}'".format(binary_string))
    # Convert the binary string to a hexadecimal number
    # hex_number = format(int(binary_string, 2), '02x')

    # Convert binary string to an integer
    integer_value = int(binary_string, 2)
    #print("column_to_hex integer_value'{}'".format(integer_value))
    # Convert integer to hexadecimal string and remove the '0x' prefix
    #hexadecimal_string = hex(integer_value)[2:]
    hexadecimal_string = "{:02x}".format(integer_value)
    #print("column_to_hex hexadecimal_string'{}'".format(hexadecimal_string))
    # Optionally, ensure the hexadecimal string is formatted to have even length (common in many applications)
    #hexadecimal_string = hexadecimal_string.zfill((len(hexadecimal_string) + 1) // 2 * 2)
    #print("column_to_hex hexadecimal_string 2'{}'".format(hexadecimal_string))

    return hexadecimal_string

    # Constructing the matrix based on the updated image
emotion_matrix_default = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # Row 0
    [0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0], # Row 1
    [0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0], # Row 2
    [0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0], # Row 3
    [0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0], # Row 4
    [0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0], # Row 5
    [0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0], # Row 6
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]  # Row 7
]

def handle_display_show_emotion_by_matrix(params, emotion_matrix):
    hex_columns = []
    for col_idx in range(16):
        column_data = [emotion_matrix[row_idx][col_idx] for row_idx in range(8)]

        column = column_to_hex(column_data)
        hex_columns.append(column_to_hex(column_data))


    final_hex_string = ''.join(hex_columns)
    print("final_hex_string '{}'".format(final_hex_string))
    codey.display.show_image(final_hex_string)

# Map each command to its handler function
command_handlers = {
    "led.show": handle_led_show,
    "led.set_red": handle_led_set_red,
    "led.set_green": handle_led_set_green,
    "led.set_blue": handle_led_set_blue,
    "led.off": handle_led_off,

    "display.show_image": handle_display_show_image,
    "display.show": handle_display_show,
    "display.set_pixel": handle_display_set_pixel,
    "display.get_pixel": handle_display_get_pixel,
    "display.toggle_pixel": handle_display_toggle_pixel,
    "display.clear": handle_display_clear,

    #"display.show_default_face": lambda params: handle_display_show_emotion_by_matrix(params, emotion_matrix_default),

    "display.show_default_face": lambda params: handle_display_show_emotion(params, "00003c7e7e3c000000003c7e7e3c0000"),
    "display.show_happy_face": lambda params: handle_display_show_emotion(params, "000c18181c0c000000000c18181c0c00"),  # Example pattern
    "display.show_sad_face": lambda params: handle_display_show_emotion(params, "003c0f003f0c00000000f00f3c3c0300"),  # Example pattern
    "display.show_angry_face": lambda params: handle_display_show_emotion(params, "0f003f0c3c030000000000f00f3c0f00"),  # Example pattern
    "display.show_surprised_face": lambda params: handle_display_show_emotion(params, "03c03f0f3f030000000000f0f3c3f030"),  # Example pattern

    "rocky.stop": handle_rocky_stop,
    "rocky.forward": handle_rocky_forward,
    "rocky.backward": handle_rocky_backward,
    "rocky.turn_left": handle_rocky_turn_left,
    "rocky.turn_right": handle_rocky_turn_right,
    "rocky.drive": handle_rocky_drive,
    "rocky.turn_right_by_degree": handle_rocky_turn_right_by_degree,
    "rocky.turn_left_by_degree": handle_rocky_turn_left_by_degree,

    "sound_sensor.get_loudness": handle_get_loudness,
    "light_sensor.get_value": handle_light_sensor_get_value,
    "potentiometer.get_value": handle_potentiometer_get_value,
}

def on_new_mqtt_message(myTopic, msg):
    print("Received message '{}' on myTopic '{}'".format(msg, myTopic))
    try:
        if myTopic.endswith('/command/'):
            #print("Received command '{}' on myTopic '{}'".format(msg, myTopic))
            data = json.loads(msg)
            command = data.get("comando")
            params = data.get("parametri", {})
            print("Command '{}' with parameters '{}'".format(command, params))

            # Retrieve the handler function based on the command and call it
            try:
                handler = command_handlers.get(command)
                #print("Command handler '{}' on myTopic '{}'".format(handler))
                if handler:
                    handler(params)
                else:
                    print("No handler available for command:", command)
            except:
                print("Error getting handler for command '{}'", command)
        else:
            # Handle other myTopics, e.g., data requests or settings
            if myTopic.endswith('/data_request/'):
                print("Received data request '{}' on myTopic '{}'".format(msg, myTopic))
                process_data_requests(command, params)

            # Implement additional myTopic handlers as necessary

    except json.JSONDecodeError:
        print("Error decoding JSON")
    except Exception as e:
        print("Error handling message:", e)

def print_debug(function, params):
    if (DEBUG_MODE):
        print("'{}': data: '{}'".format(function, params))

# subscribe message
def mqtt_subscribe():
    print("Setting the callback")
    mqttClient.set_callback(on_new_mqtt_message)

    print("Subscribing to myTopic '{}'".format(myTopic))
    mqttClient.subscribe(myTopic, qos = 1)
    print("Subscribed to myTopic '{}'".format(myTopic))

    print("Subscribing to broadcastTopic '{}'".format(broadcastTopic))
    mqttClient.subscribe(broadcastTopic, qos = 1)
    print("Subscribed to broadcastTopic '{}'".format(broadcastTopic))

codey.wifi.start(rete, password)
codey.led.show(255,0,0)

while True:
    if codey.wifi.is_connected():
        print("WIFI connected")
        codey.led.show(0,255,255)

        mqtt_connect()
        codey.led.show(0,255,0)
        codey.emotion.hello()
        time.sleep(1)

        mqtt_subscribe()
        codey.led.show(0,0,255)

        codey.display.show(CODEY_ID)

        while True:
            mqttClient.wait_msg()
            time.sleep(1)

    else:
        codey.led.show(255,0,0)
        codey.emotion.look_around()

