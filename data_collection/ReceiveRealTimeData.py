import websocket
import json
import pandas as pd
import sys
import argparse

ACTION = None

x_data = []
y_data = []
z_data = []


def on_message(ws, message):
    global df
    values = json.loads(message)['values']
    x = values[0]
    y = values[1]
    z = values[2]
    
    print(f"x: {x}, y: {y}, z: {z}")
    
    x_data.append(x)
    y_data.append(y)
    z_data.append(z)

def on_error(ws, error):
    print("error occurred ", error)
    
def on_close(ws, close_code, reason):
    print("connection closed: ", reason)
    convert_to_csv()
    
    
def on_open(ws):
    print("connected")

def connect(url):
    ws = websocket.WebSocketApp(url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()


def connect_to_accelerometer():
    connect("ws://10.10.16.27:8080/sensor/connect?type=android.sensor.accelerometer")


def convert_to_csv():
    # When the user stops the program (e.g., by pressing Ctrl+C), save the data
    print("\nStopping data capture...")
    if ACTION:
        df = pd.DataFrame({'action': [ACTION]*len(x_data), 'x': x_data, 'y': y_data, 'z': z_data})
        csv_name = ACTION + "_data.csv"
        df.to_csv(csv_name, index=False)
        print(f"Data saved to {csv_name}")
        x_data.clear()
        y_data.clear()
        z_data.clear()
    else:
        print("Invalid action. Please provide a valid action.")
    sys.exit(0)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", help="Action name")
    args = parser.parse_args()
    print("Capturing data for action: ", args.action)
    action = args.action
    ACTION = action

    if not action:
        print("Please provide a valid action using -a or --action.")
        sys.exit(1)

    # Connect to the accelerometer data stream
    connect_to_accelerometer()
