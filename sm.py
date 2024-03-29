import time
from threading import Thread
from flask import Flask, jsonify, request
from flask_ask import Ask, statement

app=Flask(__name__)
ask=Ask(app, '/')

@ask.intent('LedIntent')
def led(color, status):
   print('OKE')
   return statement("Turning the {} light {}".format(color, status))

# @app.errorhandler(Exception)
# def error_handler(e):
#     return "Unknown Error", 500


# @app.route('/test', methods=['GET'])
# def test():
#     """
#     Test endpoint to show breakage
#     """
#     AAAAAA
#     return jsonify(True)


class FlaskThread(Thread):
    def run(self):
        app.run(
            host='127.0.0.1', port=5000, debug=True, use_debugger=True,
            use_reloader=False)


def main():
    server = FlaskThread()
    server.daemon = True
    server.start()

    # simulate doing something else while flask runs in background
    time.sleep(100000)


if __name__ == '__main__':
    main()


# import eventlet
# import json
# from flask import Flask, render_template
# from flask_mqtt import Mqtt
# from flask_socketio import SocketIO
# from flask_bootstrap import Bootstrap

# eventlet.monkey_patch()

# app = Flask(__name__)
# app.config['SECRET'] = 'my secret key'
# app.config['TEMPLATES_AUTO_RELOAD'] = True
# app.config['MQTT_BROKER_URL'] = '192.168.0.5'
# app.config['MQTT_BROKER_PORT'] = 1883
# app.config['MQTT_USERNAME'] = ''
# app.config['MQTT_PASSWORD'] = ''
# app.config['MQTT_KEEPALIVE'] = 5
# app.config['MQTT_TLS_ENABLED'] = False

# # Parameters for SSL enabled
# # app.config['MQTT_BROKER_PORT'] = 8883
# # app.config['MQTT_TLS_ENABLED'] = True
# # app.config['MQTT_TLS_INSECURE'] = True
# # app.config['MQTT_TLS_CA_CERTS'] = 'ca.crt'

# mqtt = Mqtt(app)
# socketio = SocketIO(app)
# bootstrap = Bootstrap(app)


# @app.route('/')
# def index():
#     return render_template('index.html')


# @socketio.on('publish')
# def handle_publish(json_str):
#     data = json.loads(json_str)
#     mqtt.publish(data['topic'], data['message'])


# @socketio.on('subscribe')
# def handle_subscribe(json_str):
#     data = json.loads(json_str)
#     mqtt.subscribe('aaa')


# @socketio.on('unsubscribe_all')
# def handle_unsubscribe_all():
#     mqtt.unsubscribe_all()


# @mqtt.on_message()
# def handle_mqtt_message(client, userdata, message):
#     data = dict(
#         topic=message.topic,
#         payload=message.payload.decode()
#     )
#     print(message.topic)
#     socketio.emit('mqtt_message', data=data)


# @mqtt.on_log()
# def handle_logging(client, userdata, level, buf):
#     #print(level, buf)
#     pass


# if __name__ == '__main__':
#     socketio.run(app, host='192.168.0.5', port=5000, use_reloader=False, debug=True)