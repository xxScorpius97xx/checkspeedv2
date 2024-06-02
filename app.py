from flask import Flask, jsonify, render_template
import subprocess

app = Flask(__name__)

def run_speedtest_script():
    script = """
import requests
import speedtest

def check_internet_connection():
    url = "http://www.google.com"
    timeout = 5
    try:
        requests.get(url, timeout=timeout)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False

def test_speed():
    st = speedtest.Speedtest()
    st.download()
    st.upload()
    res = st.results.dict()
    return res

def categorize_ping(ping):
    if ping <= 50:
        return "Excellent"
    elif 50 < ping <= 100:
        return "Good"
    elif 100 < ping <= 150:
        return "Fair"
    elif 150 < ping <= 200:
        return "Poor"
    else:
        return "Very Poor"

def categorize_speed(speed):
    if speed < 1:
        return "Very Slow"
    elif 1 <= speed < 5:
        return "Slow"
    elif 5 <= speed < 25:
        return "Medium"
    elif 25 <= speed < 100:
        return "Fast"
    else:
        return "Very Fast"

if __name__ == "__main__":
    if check_internet_connection():
        print("You are connected to the internet.")
        speed_results = test_speed()
        ping_category = categorize_ping(speed_results['ping'])
        download_category = categorize_speed(speed_results['download'] / 1_000_000)
        upload_category = categorize_speed(speed_results['upload'] / 1_000_000)

        print(f"Ping: {speed_results['ping']} ms - Category: {ping_category}")
        print(f"Download Speed: {speed_results['download'] / 1_000_000:.2f} Mbps - Category: {download_category}")
        print(f"Upload Speed: {speed_results['upload'] / 1_000_000:.2f} Mbps - Category: {upload_category}")
    else:
        print("You are not connected to the internet.")
"""
    process = subprocess.Popen(
        ['python3', '-c', script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    return stdout.decode('utf-8'), stderr.decode('utf-8')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-speedtest', methods=['POST'])
def run_speedtest():
    stdout, stderr = run_speedtest_script()
    result = {
        "stdout": stdout,
        "stderr": stderr
    }
    return jsonify(result)
