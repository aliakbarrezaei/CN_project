from django.db import models
from django.contrib.auth.models import User
import pickle, socket, cv2, struct, threading


class Video(models.Model):
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='videos/')
    pub_date = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField('Users', related_name='likes')
    dislikes = models.ManyToManyField('Users', related_name='dislike')
    video_status = (('A', 'accessible'), ('I', 'inaccessible'))
    label_status = (('L', 'limited'), ('U', 'unlimited'))
    label = models.CharField(max_length=1, choices=label_status, default='U', help_text='label status')
    status = models.CharField(max_length=1, choices=video_status, default='A', help_text='Video status')

    def __str__(self):
        return '%s , %s,  like_count: %s, dislike_count: %s' % (
            self.title, self.video_file, self.likes.all().count(), self.dislikes.all().count())


class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    comment = models.CharField(max_length=300)

    def __str__(self):
        return ('%s, %s ,%s') % (self.user.user, self.video, self.comment)


class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    strike_status = (('S', 'striked'), ('N', 'non-striked'))
    status = models.CharField(max_length=1, choices=strike_status, default='N', help_text='Strike status')
    unavailable_videos_count = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'User management'
        verbose_name_plural = 'User management'


class Admin(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    register_status = (('N', 'not confirmed'), ('C', 'confirmed'))
    status = models.CharField(max_length=1, choices=register_status, default='N', help_text='Register status')

    def __str__(self):
        return self.admin.username

    class Meta:
        verbose_name = 'Admin management'
        verbose_name_plural = 'Admin management'


class Client:
    def __init__(self, IP, PORT, video_path):
        self.IP = IP
        self.PORT = PORT
        self.video_path = video_path
        thread = threading.Thread(target=self.stream_video)
        thread.start()

    def stream_video(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.IP, self.PORT))

        client_socket.sendall(self.video_path.encode('utf-8'))

        payload_size = struct.calcsize("L")
        data = client_socket.recv(payload_size)
        frames_num = struct.unpack("L", data)[0]

        for frame_num in range(frames_num):
            data = b''
            packed_msg_size = client_socket.recv(payload_size)
            msg_size = struct.unpack("L", packed_msg_size)[0]
            remaining_msg_size = msg_size

            while remaining_msg_size != 0:
                data += client_socket.recv(remaining_msg_size)
                remaining_msg_size = msg_size - len(data)

            frame_data = data
            frame = pickle.loads(frame_data)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) in [ord('q'), 27]:
                break

        client_socket.close()
