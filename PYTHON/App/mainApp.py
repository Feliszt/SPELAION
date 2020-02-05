# --------------------------------------------------------
#   MAINAPP of Collectif TOAST's ALFRED installation
#   This app runs app01 and app02 and kills them
#
#   Félix Côte, Benjamin Muzart / 2020
# --------------------------------------------------------

# GUI
from  tkinter import *
# misc
import time
import sys
import subprocess
import time
import json
# OSC Server
from pythonosc import dispatcher
from pythonosc import osc_server
import threading

class App:
    def __init__(self, _window, _config):
        # window stuff
        self.window = _window
        self.window.title("Main App")

        # set window size
        winW = 400
        winH = 400
        winX = int(1920 * 0.5 - winW * 0.5)
        winY = int(1080 * 0.5 - winH * 0.5)
        winGeometry = "{}x{}+{}+{}".format(winW, winH, winX, winY)
        self.window.geometry(winGeometry)

        # Set dispatcher
        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.map("/runApps", self.runAppsOSC)
        self.dispatcher.map("/runApp01", self.runApp01OSC)
        self.dispatcher.map("/runApp02", self.runApp02OSC)
        self.dispatcher.map("/runApp03", self.runApp03OSC)
        self.dispatcher.map("/killApps", self.killAppsOSC)
        self.dispatcher.map("/killApp01", self.killApp01OSC)
        self.dispatcher.map("/killApp02", self.killApp02OSC)
        self.dispatcher.map("/killApp03", self.killApp03OSC)

        # Launch OSC Server
        self.server = osc_server.ThreadingOSCUDPServer((_config["MainApp_OSC_addr"], _config["MainApp_OSC_port"]), self.dispatcher)
        self.serverThread = threading.Thread(target = self.server.serve_forever)
        self.serverThread.start()

        # set App 01
        # app that runs VideoCapture and Image Classification
        # part 1 and 2 of ALFRED's tryptic
        self.runApp01Cmd = "python.exe App01.py &"

        # set App 02
        # app that displays result images
        # part 2 of ALFRED's tryptic
        self.runApp02Cmd = "python.exe App02.py &"

        # set App 03
        # app that runs GAN
        # part 3 of ALFRED's tryptic
        self.runApp03Cmd = "python.exe App03.py &"

        # run all apps
        self.first = True
        self.runApps()
        self.first = False

        # frames
        runButton = Button(self.window, text="RUN", command=self.runApps)
        killButton = Button(self.window, text="STOP", command=self.killApps)
        runApp01Button = Button(self.window, text="RUN APP01", command=self.runApp01)
        runApp02Button = Button(self.window, text="RUN APP02", command=self.runApp02)
        runApp03Button = Button(self.window, text="RUN APP03", command=self.runApp03)
        killApp01Button = Button(self.window, text="KILL APP01", command=self.killApp01)
        killApp02Button = Button(self.window, text="KILL APP02", command=self.killApp02)
        killApp03Button = Button(self.window, text="KILL APP03", command=self.killApp03)
        runButton.pack()
        killButton.pack()
        runApp01Button.pack()
        killApp01Button.pack()
        runApp02Button.pack()
        killApp02Button.pack()
        runApp03Button.pack()
        killApp03Button.pack()

        # run main loop
        self.window.protocol("WM_DELETE_WINDOW", self.killMainApp)
        self.window.mainloop()

    def runApps(self):
        if(self.first) :
            self.app01 = subprocess.Popen(self.runApp01Cmd)
            self.app02 = subprocess.Popen(self.runApp02Cmd)
            self.app03 = subprocess.Popen(self.runApp03Cmd)
            return

        self.runApp01()
        self.runApp02()
        self.runApp03()

    def runAppsOSC(self, unused_addr):
        self.runApps()

    def runApp01(self):
        # kill app if already running
        if self.app01.poll() == None:
            print("App01 already running.")
            self.killApp01()
        # run app
        self.app01 = subprocess.Popen(self.runApp01Cmd)

    def runApp01OSC(self, unused_addr):
        self.runApp01()

    def runApp02(self):
        # kill app if already running
        if self.app02.poll() == None:
            print("App02 already running.")
            self.killApp02()
        # run app
        self.app02 = subprocess.Popen(self.runApp02Cmd)

    def runApp02OSC(self, unused_addr):
        self.runApp02()

    def runApp03(self):
        # kill app if already running
        if self.app03.poll() == None:
            print("App03 already running.")
            self.killApp03()
        # run app
        self.app03 = subprocess.Popen(self.runApp03Cmd)

    def runApp03OSC(self, unused_addr):
        self.runApp03()

    def killApp01(self):
        print("Killing App01.")
        self.app01.kill()

    def killApp01OSC(self, unused_addr):
        self.killApp01()

    def killApp02(self):
        print("Killing App02.")
        self.app02.kill()

    def killApp02OSC(self, unused_addr):
        self.killApp02()

    def killApp03(self):
        print("Killing App03.")
        self.app03.kill()

    def killApp03OSC(self, unused_addr):
        self.killApp03()

    def killApps(self):
        print("Killing apps.\n")
        self.app01.kill()
        self.app02.kill()
        self.app03.kill()

    def killAppsOSC(self, unused_addr):
        self.killApps()

    def killMainApp(self):
        self.killApps()
        self.window.destroy()

    def killMainAppOSC(self, unused_addr):
        self.killMainApp()

def main():
    # show info
    print("Running Main App.")

    # parse arguments
    #Read JSON data into the datastore variable
    with open('data/config.json', 'r') as f:
        config = json.load(f)

    # run App
    App(Tk(), config)


if __name__ == "__main__":
    main()
