import pickle, socket, cv2, threading, struct, time


class Server:
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.IP, self.PORT))
        self.server_socket.listen()
        thread = threading.Thread(target=self.listen)
        thread.start()

    def listen(self):
        print(f'listening on port {self.PORT}')
        while True:
            conn, addr = self.server_socket.accept()
            data = conn.recv(1024)
            video_path = data.decode("utf-8")
            thread = threading.Thread(target=stream_video, args=(conn, video_path))
            thread.start()


def stream_video(client_socket, video_path):
    video = cv2.VideoCapture(video_path)
    video_FPS = video.get(cv2.CAP_PROP_FPS)
    frames_num = struct.pack('L', int(video.get(cv2.CAP_PROP_FRAME_COUNT)))
    client_socket.sendall(frames_num)
    # print(f' video_FPS={video_FPS}')
    ideal_time = 1 / video_FPS
    wait_time = 1 / video_FPS
    t = time.time()
    while True:
        try:
            status, frame = video.read()
            height, width = frame.shape[:2]
            frame = cv2.resize(frame, (500, round(height * 500 / width)), interpolation=cv2.INTER_NEAREST)

            frame = pickle.dumps(frame)
            frame_size = struct.pack('L', len(frame))
            data = frame_size + frame
            client_socket.sendall(data)

            delta = time.time() - t
            wait_time += (ideal_time - delta)
            t = time.time()
            # print(f' fps={int(1 / delta)}')
            cv2.waitKey(int(1000 * wait_time))
        except Exception as e:
            # print("[Error] " + str(e))
            return


server = Server('127.0.0.1', 8001)
