# OSC Server
from pythonosc import dispatcher
from pythonosc import osc_server
import threading

# OSC classification reception
def test(unused_addr, _value):
    print("[MainApp] - {}".format(_value))

#
addr = "192.168.43.106"
port = 8000

# Set dispatcher
dispatcher = dispatcher.Dispatcher()
dispatcher.map("/test", test)

# Launch OSC Server
server = osc_server.ThreadingOSCUDPServer((addr, port), dispatcher)
serverThread = threading.Thread(target = server.serve_forever)
serverThread.start()
