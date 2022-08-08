import json, os
import pathlib
import pickle, socket, cv2, threading, struct, time
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CN_project.settings")
django.setup()
from django.contrib.auth import authenticate

from app1 import models

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def run(IP, PORT):
    IP = IP
    PORT = PORT
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print(f'listening on port {PORT}')
    listen()


def listen():
    global c
    while True:
        conn, addr = server_socket.accept()
        print(f'new connection : {addr}')
        data = conn.recv(1024).decode("utf-8")
        thread = threading.Thread(target=auth, args=(conn, data))
        thread.start()


def auth(client_socket, data):
    username, password = json.loads(data)
    # print(authenticate(username=username, password=password))
    if authenticate(username=username, password=password):
        client_socket.sendall('ok'.encode('utf-8'))
        video_id = int(client_socket.recv(1024).decode("utf-8"))
        try:
            video_obj = models.Video.objects.get(id=video_id)
            base = str(os.path.dirname(os.path.abspath("__file__")).replace('\\', '/').replace('/app1', ''))
            video_path = base + '/media/' + str(video_obj.video_file)
            client_socket.sendall('ok'.encode('utf-8'))
            stream_video(client_socket, video_path)
            client_socket.close()
            return
        except Exception as e:
            print(e)
            pass
    client_socket.sendall('error'.encode('utf-8'))
    client_socket.close()


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
            client_socket.close()
            return


thread = threading.Thread(target=run, args=('127.0.0.1', 8001))
thread.start()
