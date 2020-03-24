import cv2
import tornado
import asyncio
import traceback

from tornado.websocket import WebSocketHandler
from tornado.ioloop import IOLoop


ALLOWED_CONNECTIONS_NUMBER = 1


class WSHandler(WebSocketHandler):

    _connections = 0

    def initialize(self, camera):
        self._camera = camera
        self.streaming = True

    def check_origin(self, origin):

        WSHandler._connections += 1
        if WSHandler._connections == ALLOWED_CONNECTIONS_NUMBER:
            return True
        print(" >>> Streaming in progress, camera is locked!")
        return

    async def send_frames(self):

        if not self._camera.is_open:
            self._camera.start()
            while self.streaming:
                img = await IOLoop.current().run_in_executor(
                    None, self._camera.get_frame)
                if img is not None:
                    try:
                        await self.write_message(img, binary=True)
                    except:
                        print(traceback.format_exc())
        else:
            print(" >>> already streaming")

    def stop_streaming(self):
        self.streaming = False

    def open(self):
        print(" >>> connection opened")
        IOLoop.current().spawn_callback(self.send_frames)

    def on_close(self):
        print(" >>> connection closed")
        IOLoop.current().spawn_callback(self.stop_streaming)
        WSHandler._connections = 0
        self._camera.close()


class Camera:

    def __init__(self):
        self.capture = None
        self.is_open = False

    def start(self):
        self.is_open = True
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

    def get_frame(self):
        ret, img = self.capture.read()
        if ret:
            img = cv2.imencode('.jpg', img)[1].tostring()
            return img
    
    def close(self):
        self.is_open = False
        self.capture.release()


def main():
    camera = Camera()
    app = tornado.web.Application([
        (r"/camera", WSHandler, dict(camera=camera)),
    ])
    app.listen(8080)
    IOLoop.instance().start()


if __name__ == "__main__":
    main()