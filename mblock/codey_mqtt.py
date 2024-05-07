from cloud_message.mqtt import MQTTClient
import codey
import rocky

import time
import ubinascii
import json
import random
import utime
import event
import _thread

rete = 'procioniopossum'
password = 'tombolina'
#rete = 'TL4K-4G-NET'
#password = 'techlab4kids'

MQTTHOST = "192.168.10.116"
MQTTPORT = 1883

DEBUG_MODE = True

MQTT_TIME_INTERVAL_MS = 900

CODEY_ID = random.randint(1000, 9999)
clientIdCommands = 'TL4K-Codey-{}-commands'.format(CODEY_ID)
clientIdEvents = 'TL4K-Codey-{}-events'.format(CODEY_ID)

# Example Path
myDataTopic = "tl4k/devices/{}/data/".format(clientIdCommands)
myEventTopic = "tl4k/devices/{}/event/".format(clientIdCommands)
myTopic = "tl4k/devices/{}/command/#".format(clientIdCommands)
broadcastTopic = "tl4k/devices/broadcast/command/#"

mqttClientCommands = MQTTClient(clientIdCommands, MQTTHOST, port=MQTTPORT, user='', password='', keepalive=0, ssl=False)
mqttClientEvents = MQTTClient(clientIdEvents, MQTTHOST, port=MQTTPORT, user='', password='', keepalive=0, ssl=False)

def notify_event(event):
    #print("notify_event")
    #print_debug("event", event)
    #global sendData
    #if (sendData):
    msg = event
    print_debug("event", "msg {} to topic {}".format(msg, myEventTopic))

    mqttClientEvents.publish(myEventTopic, json.dumps(msg), retain=False, qos=0)

#@event.start
def start_callback():
    notify_event("start")

@event.button_a_pressed
def button_a_pressed_callback():
    notify_event("button_a_pressed")

@event.button_b_pressed
def button_b_pressed_callback():
    notify_event("button_b_pressed")

@event.button_c_pressed
def button_c_pressed_callback():
    notify_event("button_c_pressed")

#event.start(start_callback)

def mqtt_connect():
    time.sleep(1)
    mqttClientCommands.connect()
    mqttClientEvents.connect()

def logError(msg, codeyAction):
    print(msg)
    codeyAction()

def print_debug(function, params = {}):
    global DEBUG_MODE
    if (DEBUG_MODE):
        print("'{}': data: '{}'".format(function, params))

codey.wifi.start(rete, password)
codey.led.show(255,0,0)

args = []

#def mqtt_thread():
sendData = False
dataToSend = []
start = None

# subscribe message
def mqtt_subscribe():
    print_debug("Setting the callback")
    mqttClientCommands.set_callback(on_new_mqtt_message)

    print_debug("Subscribing to myTopic '{}'".format(myTopic))
    mqttClientCommands.subscribe(myTopic, qos = 0)
    print_debug("Subscribed to myTopic '{}'".format(myTopic))

    print_debug("Subscribing to broadcastTopic '{}'".format(broadcastTopic))
    mqttClientCommands.subscribe(broadcastTopic, qos = 0)
    print_debug("Subscribed to broadcastTopic '{}'".format(broadcastTopic))

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
                    try:
                        handler(params)
                    except:
                        logError("Error executing command {}:".format(command), codey.emotion.uh_oh)
                else:
                    logError("No handler available for command {}:".format(command), codey.emotion.uh_oh)
            except:
                logError("Error getting handler for command '{}'", command)
                codey.emotion.uh_oh()

    except json.JSONDecodeError:
        print("Error decoding JSON")
        codey.emotion.uh_oh()
    except Exception as e:
        print("Error handling message:", e)
        codey.emotion.uh_oh()

def sendMqttData():
    global sendData
    #print_debug("sendMqttData sendData", sendData)

    msg = {}
    now = utime.ticks_ms()

    global start

    if start == None:
        start = utime.ticks_ms()
        print_debug("initializing start time", start)
    else:
        elapsedTime = utime.ticks_diff(now, start)
        #print_debug("elapsedTime", elapsedTime)
        if (sendData and elapsedTime > MQTT_TIME_INTERVAL_MS):
            codey.led.show(255,255,0)
            start = now

            global dataToSend
            #print_debug("sendMqttData dataToSend", dataToSend)
            if "light" in dataToSend:
                msg["light"] = codey.light_sensor.get_value()
            if "light strength" in dataToSend:
                msg["light strength"] = rocky.color_ir_sensor.get_light_strength()
            if "sound" in dataToSend:
                msg["sound"] = codey.sound_sensor.get_loudness()
            if "color component":
                msg["color component"] = {
                    "red": rocky.color_ir_sensor.get_red(),
                    "green": rocky.color_ir_sensor.get_green(),
                    "blue": rocky.color_ir_sensor.get_blue()
                }
            if "color matched":
                msg["color matched"] = {
                    "is_red": rocky.color_ir_sensor.is_color("red"),
                    "is_green": rocky.color_ir_sensor.is_color("green"),
                    "is_blue": rocky.color_ir_sensor.is_color("blue"),
                    "is_yellow": rocky.color_ir_sensor.is_color("yellow"),
                    "is_cyan": rocky.color_ir_sensor.is_color("cyan"),
                    "is_purple": rocky.color_ir_sensor.is_color("purple"),
                    "is_white": rocky.color_ir_sensor.is_color("white"),
                    "is_black": rocky.color_ir_sensor.is_color("black"),
                }
            if "obstacle ahead":
                msg["obstacle ahead"] = rocky.color_ir_sensor.is_obstacle_ahead()

            print_debug("sendMqttData", "msg {} to topic {}".format(msg, myDataTopic))
            if len(msg) > 0:
                mqttClientCommands.publish(myDataTopic, json.dumps(msg), retain=False, qos=0)
        else:
            codey.led.show(0,0,255)

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
    function = "handle_rocky_forward"
    #print_debug(function, params)

    speed = params.get('speed', 50)
    #print_debug(function, "speed: {}".format(speed))

    time_s = params.get('time_s', 1)
    print_debug(function, "time_s: {}".format(time_s))
    if time_s == 0:
        time_s = None
    print_debug(function, "time_s: {}".format(time_s))

    straight = params.get('straight', True)
    #print_debug(function, "straight: {}".format(straight))

    rocky.forward(speed, time_s, straight)

def handle_rocky_backward(params):
    function = "handle_rocky_backward"
    #print_debug(function, params)

    speed = params.get('speed', 50)
    #print_debug(function, "speed: {}".format(speed))

    time_s = params.get('time_s', 1)
    if time_s == 0:
        time_s = None
    #print_debug(function, "time_s: {}".format(time_s))

    straight = params.get('straight', True)
    #print_debug(function, "straight: {}".format(straight))
    rocky.backward(speed, time_s, straight)

def handle_rocky_turn_by_degree(params):
    function = "handle_rocky_turn_right_by_degree"
    #print_debug(function, params)

    speed = params.get('speed', 40)
    #print_debug(function, "speed: {}".format(speed))

    angle = params.get('angle', 90)
    #print_debug(function, "time_s: {}".format(time_s))

    rocky.turn_right_by_degree(angle, speed)

def handle_rocky_turn_right_by_degree(params):
    function = "handle_rocky_turn_right_by_degree"
    #print_debug(function, params)

    angle = params.get('angle', 90)
    #print_debug(function, "time_s: {}".format(time_s))
    speed = params.get('speed', 40)
    #print_debug(function, "speed: {}".format(speed))

    rocky.turn_right_by_degree(angle, speed)

def handle_rocky_turn_left_by_degree(params):
    angle = params.get('angle',90)
    speed = params.get('speed',40)
    rocky.turn_left_by_degree(angle, speed)

def handle_rocky_turn_left(params):
    function = "handle_rocky_turn_left"
    #print_debug(function, params)

    speed = params.get('speed', 40)
    #print_debug(function, "speed: {}".format(speed))

    time_s = params.get('time_s', 1)
    #print_debug(function, "time_s: {}".format(time_s))

    straight = params.get('straight', True)
    #print_debug(function, "straight: {}".format(straight))
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

    # Convert binary string to an integer
    integer_value = int(binary_string, 2)
    #print("column_to_hex integer_value'{}'".format(integer_value))
    # Convert integer to hexadecimal string and remove the '0x' prefix

    hexadecimal_string = "{:02x}".format(integer_value)
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

def handle_data_request(params):
    function = "handle_data_request"
    #print_debug(function, params)

    shouldSend = params.get('invia', False)
    print_debug(function, "invia: {}".format(shouldSend))
    data = params.get('dati', [])
    print_debug(function, "dati: {}".format(data))

    if shouldSend:
        global sendData
        sendData = True

        global dataToSend
        dataToSend = data

        print_debug("handle_data_request", dataToSend)
    else:
        sendData = False

# Map each command to its handler function
command_handlers = {
    "send.data": handle_data_request,
    "led.show": handle_led_show,
    "led.set_red": handle_led_set_red,
    "led.set_green": handle_led_set_green,
    "led.set_blue": handle_led_set_blue,
    "led.off": handle_led_off,

    "display.show_image": handle_display_show_image,
    "display.show": handle_display_show,
    "display.set_pixel": handle_display_set_pixel,
    #"display.get_pixel": handle_display_get_pixel,
    "display.toggle_pixel": handle_display_toggle_pixel,
    "display.clear": handle_display_clear,

    #"display.show_default_face": lambda params: handle_display_show_emotion_by_matrix(params, emotion_matrix_default),

    "display.show_default_face": lambda params: handle_display_show_emotion(params, "00003c7e7e3c000000003c7e7e3c0000"),
    "display.show_happy_face": lambda params: handle_display_show_emotion(params, "000c18181c0c000000000c18181c0c00"),  # Example pattern
    #"display.show_sad_face": lambda params: handle_display_show_emotion(params, "003c0f003f0c00000000f00f3c3c0300"),  # Example pattern
    #"display.show_angry_face": lambda params: handle_display_show_emotion(params, "0f003f0c3c030000000000f00f3c0f00"),  # Example pattern
    #"display.show_surprised_face": lambda params: handle_display_show_emotion(params, "03c03f0f3f030000000000f0f3c3f030"),  # Example pattern

    "rocky.stop": handle_rocky_stop,
    "rocky.forward": handle_rocky_forward,
    "rocky.backward": handle_rocky_backward,
    "rocky.turn_by_degree": handle_rocky_turn_by_degree,
    #"rocky.turn_left": handle_rocky_turn_left,
    #"rocky.turn_right": handle_rocky_turn_right,
    #"rocky.drive": handle_rocky_drive,
    "rocky.turn_right_by_degree": handle_rocky_turn_right_by_degree,
    "rocky.turn_left_by_degree": handle_rocky_turn_left_by_degree,

    #    "sound_sensor.get_loudness": handle_get_loudness,
    #    "light_sensor.get_value": handle_light_sensor_get_value,
    #    "potentiometer.get_value": handle_potentiometer_get_value,
}

#_thread.start_new_thread(notification_thread, (event, mqttClientEvents))

mqttThreadStarted = False
isWifiConnected = False
isMqttConnected = False
isMqttSubscribed = False



while not isWifiConnected:
    if codey.wifi.is_connected():
        if not isWifiConnected:
            isWifiConnected = True
            print("WIFI connected")
            codey.led.show(0,255,255)

            if not isMqttConnected:
                mqtt_connect()
                isMqttConnected = True

                codey.led.show(0,255,0)
                codey.emotion.hello()
                #time.sleep(1)

                if not isMqttSubscribed:
                    mqtt_subscribe()
                    isMqttSubscribed = True
                    codey.led.show(0,0,255)

                    codey.display.show(CODEY_ID)
                    '''
                    while True:
                        mqttClientCommands.check_msg()
                        sendMqttData()

                        time.sleep(.01)
                    '''
    else:
        codey.led.show(255,0,0)
        codey.emotion.look_around()

    time.sleep(1)

event.button_a_pressed(button_a_pressed_callback)
event.button_b_pressed(button_b_pressed_callback)
event.button_c_pressed(button_c_pressed_callback)
print("Event handersRegistered")

print("Main loop")
while True:
    mqttClientCommands.check_msg()
    sendMqttData()

    time.sleep(.01)

print("terminating program")

#_thread.start_new_thread(mqtt_thread, [])
