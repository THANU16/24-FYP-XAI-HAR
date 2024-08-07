"""
Python code to show real-time plot from live accelerometer's
data received via SensorServer app over websocket
"""

from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import websocket
import json
import threading
import pandas as pd
import time

ACTION = None
SUBJECT_ID = None
# Initialize lists to store the accelerometer and gyroscope data
device1 = {"acc_x": [], "acc_y": [], "acc_z": [], "acc_time": [], "gyro_x": [], "gyro_y": [], "gyro_z": [], "gyro_time": []}
device2 = {"acc_x": [], "acc_y": [], "acc_z": [], "acc_time": [], "gyro_x": [], "gyro_y": [], "gyro_z": [], "gyro_time": []}
device3 = {"acc_x": [], "acc_y": [], "acc_z": [], "acc_time": [], "gyro_x": [], "gyro_y": [], "gyro_z": [], "gyro_time": []}

x_data_color = "#d32f2f"  # red
y_data_color = "#7cb342"  # green
z_data_color = "#0288d1"  # blue
background_color = "#fafafa"  # white (material)

device1_acc_df = pd.DataFrame({'time': [], 'x': [], 'y': [], 'z': []})
device1_gyro_df = pd.DataFrame({'time': [], 'x': [], 'y': [], 'z': []})

device2_acc_df = pd.DataFrame({'time': [], 'x': [], 'y': [], 'z': []})
device2_gyro_df = pd.DataFrame({'time': [], 'x': [], 'y': [], 'z': []})

device3_acc_df = pd.DataFrame({'time': [], 'x': [], 'y': [], 'z': []})
device3_gyro_df = pd.DataFrame({'time': [], 'x': [], 'y': [], 'z': []})

class Sensor:
    def __init__(self, address, sensor_type, x_data, y_data, z_data, time_data, df):
        self.address = address
        self.sensor_type = sensor_type
        self.x_data = x_data
        self.y_data = y_data
        self.z_data = z_data
        self.time_data = time_data
        self.df = df

    def on_message(self, ws, message):
        values = json.loads(message)['values']
        timestamp = json.loads(message)['timestamp']

        self.x_data.append(values[0])
        self.y_data.append(values[1])
        self.z_data.append(values[2])
        current_timestamp = time.time()
        self.time_data.append(current_timestamp)
        
        new_row = pd.DataFrame({'time': [current_timestamp], 'x': [values[0]], 'y': [values[1]], 'z': [values[2]]})
        self.df = pd.concat([self.df, new_row], ignore_index=True)

    def on_error(self, ws, error):
        print("error occurred")
        print(error)

    def on_close(self, ws, close_code, reason):
        print("connection close")
        print("close code: ", close_code)
        print("reason: ", reason)

    def on_open(self, ws):
        print(f"connected to: {self.address}")

    def make_websocket_connection(self):
        print(f"ws://{self.address}/sensor/connect?type={self.sensor_type}")
        ws = websocket.WebSocketApp(
            f"ws://{self.address}/sensor/connect?type={self.sensor_type}",
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        ws.run_forever()

    def connect(self):
        thread = threading.Thread(target=self.make_websocket_connection)
        thread.start()

def clear_data():
    device1_acc_df.drop(device1_acc_df.index, inplace=True)
    device1_gyro_df.drop(device1_gyro_df.index, inplace=True)
    device2_acc_df.drop(device2_acc_df.index, inplace=True)
    device2_gyro_df.drop(device2_gyro_df.index, inplace=True)
    device3_acc_df.drop(device3_acc_df.index, inplace=True)
    device3_gyro_df.drop(device3_gyro_df.index, inplace=True)
    
    
def convert_to_csv():
    global ACTION, SUBJECT_ID
    print("\nStopping data capture...")
    device1_acc_df.assign(action= [ACTION]*len(device1_acc_df))
    device1_acc_df.assign(subject_id= [SUBJECT_ID]*len(device1_acc_df))
    device1_gyro_df.assign(action= [ACTION]*len(device1_gyro_df))
    device1_gyro_df.assign(subject_id= [SUBJECT_ID]*len(device1_gyro_df))
    device1_acc_df.to_csv(ACTION+"_subject_"+str(SUBJECT_ID)+"_device1_accelerometer_data.csv", index=False)
    device1_gyro_df.to_csv(ACTION+"_subject_"+str(SUBJECT_ID)+"_device1_gyroscope_data.csv", index=False)
    
    device2_acc_df.assign(action= [ACTION]*len(device2_acc_df))
    device2_acc_df.assign(subject_id= [SUBJECT_ID]*len(device2_acc_df))
    device2_gyro_df.assign(action= [ACTION]*len(device2_gyro_df))
    device2_gyro_df.assign(subject_id= [SUBJECT_ID]*len(device2_gyro_df))
    device2_acc_df.to_csv(ACTION+"_subject_"+str(SUBJECT_ID)+"_device2_accelerometer_data.csv", index=False)
    device2_gyro_df.to_csv(ACTION+"_subject_"+str(SUBJECT_ID)+"_device2_gyroscope_data.csv", index=False)
    
    device3_acc_df.assign(action= [ACTION]*len(device3_acc_df))
    device3_acc_df.assign(subject_id= [SUBJECT_ID]*len(device3_acc_df))
    device3_gyro_df.assign(action= [ACTION]*len(device3_gyro_df))
    device3_gyro_df.assign(subject_id= [SUBJECT_ID]*len(device3_gyro_df))
    device3_acc_df.to_csv(ACTION+"_subject_"+str(SUBJECT_ID)+"_device3_accelerometer_data.csv", index=False)
    device3_gyro_df.to_csv(ACTION+"_subject_"+str(SUBJECT_ID)+"_device3_gyroscope_data.csv", index=False)
    
    print("Data saved to CSV files")
    ACTION = None

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QtWidgets.QGridLayout(self.centralWidget)

        # Row 1 - Device 1
        self.accelerometerWidget1 = pg.PlotWidget()
        self.gyroscopeWidget1 = pg.PlotWidget()
        self.layout.addWidget(QtWidgets.QLabel("Accelerometer Plot (Device 1)"), 0, 0)
        self.layout.addWidget(self.accelerometerWidget1, 1, 0)
        self.layout.addWidget(QtWidgets.QLabel("Gyroscope Plot (Device 1)"), 0, 1)
        self.layout.addWidget(self.gyroscopeWidget1, 1, 1)

        # Row 2 - Device 2
        self.accelerometerWidget2 = pg.PlotWidget()
        self.gyroscopeWidget2 = pg.PlotWidget()
        self.layout.addWidget(QtWidgets.QLabel("Accelerometer Plot (Device 2)"), 2, 0)
        self.layout.addWidget(self.accelerometerWidget2, 3, 0)
        self.layout.addWidget(QtWidgets.QLabel("Gyroscope Plot (Device 2)"), 2, 1)
        self.layout.addWidget(self.gyroscopeWidget2, 3, 1)

        # Row 3 - Device 3
        self.accelerometerWidget3 = pg.PlotWidget()
        self.gyroscopeWidget3 = pg.PlotWidget()
        self.layout.addWidget(QtWidgets.QLabel("Accelerometer Plot (Device 3)"), 4, 0)
        self.layout.addWidget(self.accelerometerWidget3, 5, 0)
        self.layout.addWidget(QtWidgets.QLabel("Gyroscope Plot (Device 3)"), 4, 1)
        self.layout.addWidget(self.gyroscopeWidget3, 5, 1)

        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.startButton = QtWidgets.QPushButton("Start Action")
        self.stopButton = QtWidgets.QPushButton("Stop Action")
        self.buttonLayout.addWidget(self.startButton)
        self.buttonLayout.addWidget(self.stopButton)
        self.layout.addLayout(self.buttonLayout, 6, 0, 1, 2)

        for widget in [self.accelerometerWidget1, self.accelerometerWidget2, self.accelerometerWidget3]:
            widget.setBackground(background_color)
            widget.setTitle("Accelerometer Plot", color="#8d6e63", size="20pt")
            widget.setLabel("left", "m/s^2", **{"color": "#f00", "font-size": "15px"})
            widget.setLabel("bottom", "Timestamp", **{"color": "#f00", "font-size": "15px"})
            widget.addLegend()

        for widget in [self.gyroscopeWidget1, self.gyroscopeWidget2, self.gyroscopeWidget3]:
            widget.setBackground(background_color)
            widget.setTitle("Gyroscope Plot", color="#8d6e63", size="20pt")
            widget.setLabel("left", "rad/s", **{"color": "#f00", "font-size": "15px"})
            widget.setLabel("bottom", "Timestamp", **{"color": "#f00", "font-size": "15px"})
            widget.addLegend()

        self.accelerometerWidget1_x_dat = self.accelerometerWidget1.plot([], [], name="acc_x", pen=pg.mkPen(color=x_data_color))
        self.accelerometerWidget1_y_dat = self.accelerometerWidget1.plot([], [], name="acc_y", pen=pg.mkPen(color=y_data_color))
        self.accelerometerWidget1_z_dat = self.accelerometerWidget1.plot([], [], name="acc_z", pen=pg.mkPen(color=z_data_color))
        self.accelerometerWidget2_x_dat = self.accelerometerWidget2.plot([], [], name="acc_x", pen=pg.mkPen(color=x_data_color))
        self.accelerometerWidget2_y_dat = self.accelerometerWidget2.plot([], [], name="acc_y", pen=pg.mkPen(color=y_data_color))
        self.accelerometerWidget2_z_dat = self.accelerometerWidget2.plot([], [], name="acc_z", pen=pg.mkPen(color=z_data_color))
        self.accelerometerWidget3_x_dat = self.accelerometerWidget3.plot([], [], name="acc_x", pen=pg.mkPen(color=x_data_color))
        self.accelerometerWidget3_y_dat = self.accelerometerWidget3.plot([], [], name="acc_y", pen=pg.mkPen(color=y_data_color))
        self.accelerometerWidget3_z_dat = self.accelerometerWidget3.plot([], [], name="acc_z", pen=pg.mkPen(color=z_data_color))
        
        self.gyroscopeWidget1_x_dat = self.gyroscopeWidget1.plot([], [], name="gyro_x", pen=pg.mkPen(color="#ff5722"))
        self.gyroscopeWidget1_y_dat = self.gyroscopeWidget1.plot([], [], name="gyro_y", pen=pg.mkPen(color="#795548"))
        self.gyroscopeWidget1_z_dat = self.gyroscopeWidget1.plot([], [], name="gyro_z", pen=pg.mkPen(color="#9e9e9e"))
        self.gyroscopeWidget2_x_dat = self.gyroscopeWidget2.plot([], [], name="gyro_x", pen=pg.mkPen(color="#ff5722"))
        self.gyroscopeWidget2_y_dat = self.gyroscopeWidget2.plot([], [], name="gyro_y", pen=pg.mkPen(color="#795548"))
        self.gyroscopeWidget2_z_dat = self.gyroscopeWidget2.plot([], [], name="gyro_z", pen=pg.mkPen(color="#9e9e9e"))
        self.gyroscopeWidget3_x_dat = self.gyroscopeWidget3.plot([], [], name="gyro_x", pen=pg.mkPen(color="#ff5722"))
        self.gyroscopeWidget3_y_dat = self.gyroscopeWidget3.plot([], [], name="gyro_y", pen=pg.mkPen(color="#795548"))
        self.gyroscopeWidget3_z_dat = self.gyroscopeWidget3.plot([], [], name="gyro_z", pen=pg.mkPen(color="#9e9e9e"))

        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

        self.startButton.clicked.connect(self.start_action)
        self.stopButton.clicked.connect(self.stop_action)

    def update_plot_data(self):
        limit = -1000
        
        self.accelerometerWidget1_x_dat.setData(device1["acc_time"][limit:], device1["acc_x"][limit:])
        self.accelerometerWidget1_y_dat.setData(device1["acc_time"][limit:], device1["acc_y"][limit:])
        self.accelerometerWidget1_z_dat.setData(device1["acc_time"][limit:], device1["acc_z"][limit:])
        
        self.gyroscopeWidget1_x_dat.setData(device1["gyro_time"][limit:], device1["gyro_x"][limit:])
        self.gyroscopeWidget1_y_dat.setData(device1["gyro_time"][limit:], device1["gyro_y"][limit:])
        self.gyroscopeWidget1_z_dat.setData(device1["gyro_time"][limit:], device1["gyro_z"][limit:])
        
        self.accelerometerWidget2_x_dat.setData(device2["acc_time"][limit:], device2["acc_x"][limit:])
        self.accelerometerWidget2_y_dat.setData(device2["acc_time"][limit:], device2["acc_y"][limit:])
        self.accelerometerWidget2_z_dat.setData(device2["acc_time"][limit:], device2["acc_z"][limit:])
        
        self.gyroscopeWidget2_x_dat.setData(device2["gyro_time"][limit:], device2["gyro_x"][limit:])
        self.gyroscopeWidget2_y_dat.setData(device2["gyro_time"][limit:], device2["gyro_y"][limit:])
        self.gyroscopeWidget2_z_dat.setData(device2["gyro_time"][limit:], device2["gyro_z"][limit:])
        
        self.accelerometerWidget3_x_dat.setData(device3["acc_time"][limit:], device3["acc_x"][limit:])
        self.accelerometerWidget3_y_dat.setData(device3["acc_time"][limit:], device3["acc_y"][limit:])
        self.accelerometerWidget3_z_dat.setData(device3["acc_time"][limit:], device3["acc_z"][limit:])
        
        self.gyroscopeWidget3_x_dat.setData(device3["gyro_time"][limit:], device3["gyro_x"][limit:])
        self.gyroscopeWidget3_y_dat.setData(device3["gyro_time"][limit:], device3["gyro_y"][limit:])
        self.gyroscopeWidget3_z_dat.setData(device3["gyro_time"][limit:], device3["gyro_z"][limit:])

    def start_action(self):
        global ACTION, SUBJECT_ID

        # Get the action name
        action_name, ok_action = QtWidgets.QInputDialog.getText(self, "Start Action", "Enter action name:")
        
        # If action name is provided, get the subject ID
        if ok_action and action_name:
            subject_id, ok_subject = QtWidgets.QInputDialog.getInt(self, "Subject ID", "Enter subject ID:")
            
            if ok_subject:
                print(f"Action '{action_name}' started with Subject ID '{subject_id}'")
                ACTION = action_name
                SUBJECT_ID = subject_id
                clear_data()
            else:
                print("Subject ID input was cancelled")
        else:
            print("Action name input was cancelled")

    def stop_action(self, stopping_length=1000):
        global ACTION, SUBJECT_ID
        print(f"Action '{ACTION}' stopped with Subject ID '{SUBJECT_ID}'")
        convert_to_csv()


if __name__ == "__main__":
    device1_accelerometer_sensor = Sensor(
        "10.10.23.88:8080",
        "android.sensor.accelerometer",
        device1["acc_x"],
        device1["acc_y"],
        device1["acc_z"],
        device1["acc_time"],
        device1_acc_df,
    )
    device1_gyroscope_sensor = Sensor(
        "10.10.23.88:8080",
        "android.sensor.gyroscope",
        device1["gyro_x"],
        device1["gyro_y"],
        device1["gyro_z"],
        device1["gyro_time"],
        device1_gyro_df,
    )
    
    device2_accelerometer_sensor = Sensor(
        "10.10.23.88:8080",
        "android.sensor.accelerometer",
        device2["acc_x"],
        device2["acc_y"],
        device2["acc_z"],
        device2["acc_time"],
        device2_acc_df,
    )
    device2_gyroscope_sensor = Sensor(
        "10.10.23.88:8080",
        "android.sensor.gyroscope",
        device2["gyro_x"],
        device2["gyro_y"],
        device2["gyro_z"],
        device2["gyro_time"],
        device2_gyro_df,
    )
    
    device3_accelerometer_sensor = Sensor(
        "10.10.23.88:8080",
        "android.sensor.accelerometer",
        device3["acc_x"],
        device3["acc_y"],
        device3["acc_z"],
        device3["acc_time"],
        device3_acc_df,
    )
    device3_gyroscope_sensor = Sensor(
        "10.10.23.88:8080",
        "android.sensor.gyroscope",
        device3["gyro_x"],
        device3["gyro_y"],
        device3["gyro_z"],
        device3["gyro_time"],
        device3_gyro_df,
    )

    device1_accelerometer_sensor.connect()
    device1_gyroscope_sensor.connect()
    device2_accelerometer_sensor.connect()
    device2_gyroscope_sensor.connect()
    device3_accelerometer_sensor.connect()
    device3_gyroscope_sensor.connect()

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
