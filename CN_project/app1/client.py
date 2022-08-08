from datetime import datetime
import json, pickle, struct, threading, socket, cv2


class Client:
    def __init__(self, IP, PORT, video, username, password):
        self.IP = IP
        self.PORT = PORT
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username= username
        self.password = password
        self.video_id = video
        self.title = f'{self.video_id} - {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}'
        thread = threading.Thread(target=self.run)
        thread.start()

    def run(self):
        try:
            self.client_socket.connect((self.IP, self.PORT))
        except ConnectionRefusedError:
            print('could not connect to the server.')
            return
        auth = self.send_request(self.username, self.password)
        if auth:
            self.stream_video()

    def send_request(self, username, password):
        self.client_socket.sendall(json.dumps([username, password]).encode('utf-8'))
        resp = self.client_socket.recv(1024).decode('utf-8')
        return True if resp == 'ok' else False

    def stream_video(self):
        self.client_socket.sendall(str(self.video_id).encode('utf-8'))
        resp = self.client_socket.recv(2).decode('utf-8')
        if resp == 'er':
            return
        payload_size = struct.calcsize("L")
        data = self.client_socket.recv(payload_size)
        frames_num = struct.unpack("L", data)[0]

        for frame_num in range(frames_num):
            data = b''
            packed_msg_size = self.client_socket.recv(payload_size)
            msg_size = struct.unpack("L", packed_msg_size)[0]
            remaining_msg_size = msg_size

            while remaining_msg_size != 0:
                data += self.client_socket.recv(remaining_msg_size)
                remaining_msg_size = msg_size - len(data)

            frame_data = data
            frame = pickle.loads(frame_data)
            cv2.imshow(self.title, frame)
            if cv2.waitKey(1) in [ord('q'), 27]:
                break

        self.client_socket.close()

