from flask import Flask, request
import threading
import time
from datetime import datetime

app = Flask(__name__)

# Global variables
timer_thread = None
new_log_event = threading.Event()
max_wait_time = 0
max_wait_message = ""
max_wait_received_time = ""
last_log_message = ""

# Variables for tracking iterations
last_iteration_time = None
iteration_times = []

def timer_function():
    global max_wait_time, max_wait_message, max_wait_received_time
    seconds = 0
    while not new_log_event.is_set():
        time.sleep(10)
        seconds += 10
        print(f"{seconds} seconds have passed... (Max so far: {max_wait_time} seconds for message: '{max_wait_message}', received at: {max_wait_received_time})")
        if seconds > max_wait_time:
            max_wait_time = seconds
            max_wait_message = last_log_message
            max_wait_received_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@app.route('/log', methods=['POST'])
def log():
    global timer_thread, last_log_message, last_iteration_time, iteration_times
    message = request.json['log']
    current_time = datetime.now()
    print(message)

    if message == "Starting new iteration":
        if last_iteration_time is not None:
            iteration_duration = (current_time - last_iteration_time).total_seconds()
            iteration_times.append(iteration_duration)
            max_iteration = max(iteration_times)
            avg_iteration = sum(iteration_times) / len(iteration_times)
            print(f"Previous iteration took {iteration_duration:.2f} seconds, max: {max_iteration:.2f} seconds, average: {avg_iteration:.2f} seconds")
        last_iteration_time = current_time

    # Stop the previous timer if it's running
    if timer_thread and timer_thread.is_alive():
        new_log_event.set()
        timer_thread.join()

    # Update last_log_message
    last_log_message = message

    # Reset the event and start a new timer
    new_log_event.clear()
    timer_thread = threading.Thread(target=timer_function)
    timer_thread.start()

    return "Log received", 200

@app.route('/test', methods=['GET'])
def test():
    return "Test successful", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
