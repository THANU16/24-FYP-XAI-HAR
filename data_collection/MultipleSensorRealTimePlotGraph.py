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
acc_x_data = []
acc_y_data = []
acc_z_data = []
acc_time_data = []

gyro_x_data = []
gyro_y_data = []
gyro_z_data = []
gyro_time_data = []

x_data_color = "#d32f2f"  # red
y_data_color = "#7cb342"  # green
z_data_color = "#0288d1"  # blue
background_color = "#fafafa"  # white (material)


class Sensor:
    def __init__(self, address, sensor_type, x_data, y_data, z_data, time_data):
        self.address = address
        self.sensor_type = sensor_type
        self.x_data = x_data
        self.y_data = y_data
        self.z_data = z_data
        self.time_data = time_data

    def on_message(self, ws, message):
        values = json.loads(message)['values']
        timestamp = json.loads(message)['timestamp']
        print(f"x: {values[0]}, y: {values[1]}, z: {values[2]}")

        self.x_data.append(values[0])
        self.y_data.append(values[1])
        self.z_data.append(values[2])
        current_timestamp = time.time()
        self.time_data.append(current_timestamp)

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
    acc_x_data.clear()
    acc_y_data.clear()
    acc_z_data.clear()
    acc_time_data.clear()

    gyro_x_data.clear()
    gyro_y_data.clear()
    gyro_z_data.clear()
    gyro_time_data.clear()
    
def convert_to_csv():
    global ACTION, SUBJECT_ID
    print("\nStopping data capture...")
    df_acc = pd.DataFrame({'action' : [ACTION]*len(acc_time_data),
                            'subject_id': [SUBJECT_ID]*len(acc_time_data),
                           'time': acc_time_data, 'acc_x': acc_x_data, 'acc_y': acc_y_data, 'acc_z': acc_z_data})
        
    df_gyro = pd.DataFrame({'action' : [ACTION]*len(gyro_time_data),
                            'subject_id': [SUBJECT_ID]*len(gyro_time_data),
                            'time': gyro_time_data, 'gyro_x': gyro_x_data, 'gyro_y': gyro_y_data, 'gyro_z': gyro_z_data})
    
    df_acc.to_csv(ACTION+"_subject_"+str(SUBJECT_ID)+"_accelerometer_data.csv", index=False)
    df_gyro.to_csv(ACTION+"_subject_"+str(SUBJECT_ID)+"_gyroscope_data.csv", index=False)
    print("Data saved to CSV files")
    ACTION = None

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QtWidgets.QVBoxLayout(self.centralWidget)

        self.accelerometerWidget = pg.PlotWidget()
        self.gyroscopeWidget = pg.PlotWidget()

        self.layout.addWidget(QtWidgets.QLabel("Accelerometer Plot"))
        self.layout.addWidget(self.accelerometerWidget)
        self.layout.addWidget(QtWidgets.QLabel("Gyroscope Plot"))
        self.layout.addWidget(self.gyroscopeWidget)

        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.startButton = QtWidgets.QPushButton("Start Action")
        self.stopButton = QtWidgets.QPushButton("Stop Action")
        self.buttonLayout.addWidget(self.startButton)
        self.buttonLayout.addWidget(self.stopButton)
        self.layout.addLayout(self.buttonLayout)

        self.accelerometerWidget.setBackground(background_color)
        self.accelerometerWidget.setTitle("Accelerometer Plot", color="#8d6e63", size="20pt")

        self.gyroscopeWidget.setBackground(background_color)
        self.gyroscopeWidget.setTitle("Gyroscope Plot", color="#8d6e63", size="20pt")

        styles = {"color": "#f00", "font-size": "15px"}
        self.accelerometerWidget.setLabel("left", "m/s^2", **styles)
        self.accelerometerWidget.setLabel("bottom", "Timestamp", **styles)
        self.accelerometerWidget.addLegend()

        self.gyroscopeWidget.setLabel("left", "rad/s", **styles)
        self.gyroscopeWidget.setLabel("bottom", "Timestamp", **styles)
        self.gyroscopeWidget.addLegend()

        self.acc_x_data_line = self.accelerometerWidget.plot([], [], name="acc_x", pen=pg.mkPen(color=x_data_color))
        self.acc_y_data_line = self.accelerometerWidget.plot([], [], name="acc_y", pen=pg.mkPen(color=y_data_color))
        self.acc_z_data_line = self.accelerometerWidget.plot([], [], name="acc_z", pen=pg.mkPen(color=z_data_color))

        self.gyro_x_data_line = self.gyroscopeWidget.plot([], [], name="gyro_x", pen=pg.mkPen(color="#ff5722"))
        self.gyro_y_data_line = self.gyroscopeWidget.plot([], [], name="gyro_y", pen=pg.mkPen(color="#795548"))
        self.gyro_z_data_line = self.gyroscopeWidget.plot([], [], name="gyro_z", pen=pg.mkPen(color="#9e9e9e"))

        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

        self.startButton.clicked.connect(self.start_action)
        self.stopButton.clicked.connect(self.stop_action)

    def update_plot_data(self):
        limit = -1000
        self.acc_x_data_line.setData(acc_time_data[limit:], acc_x_data[limit:])
        self.acc_y_data_line.setData(acc_time_data[limit:], acc_y_data[limit:])
        self.acc_z_data_line.setData(acc_time_data[limit:], acc_z_data[limit:])

        self.gyro_x_data_line.setData(gyro_time_data[limit:], gyro_x_data[limit:])
        self.gyro_y_data_line.setData(gyro_time_data[limit:], gyro_y_data[limit:])
        self.gyro_z_data_line.setData(gyro_time_data[limit:], gyro_z_data[limit:])

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
    accelerometer_sensor = Sensor(
        "10.136.103.158:8080",
        "android.sensor.accelerometer",
        acc_x_data,
        acc_y_data,
        acc_z_data,
        acc_time_data,
    )
    gyroscope_sensor = Sensor(
        "10.136.103.158:8080",
        "android.sensor.gyroscope",
        gyro_x_data,
        gyro_y_data,
        gyro_z_data,
        gyro_time_data,
    )

    accelerometer_sensor.connect()
    gyroscope_sensor.connect()

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
