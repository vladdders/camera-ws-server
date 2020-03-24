<h1>Webcam server</h1>

A simple tornado server that collects frames from the webcam and displays them in the browser.
Its purpose is to have a js process communicate with the python process.

<h2>Installation</h2>

`pip install -r requirements.txt` (use python3.7)

<h2>Usage</h2>

Start the server: `python server.py`

Open `index.html` in your browser.

<h2>Further info</h2>

Keep in mind that the camera is controlled upon opening/closing the websocket connection from `client.js`. This can be applied to any type of camera as long as there's an interface between the camera and the python process.

It allows only one client/connection (the localhost) because the whole point is to have an application that controls the camera.