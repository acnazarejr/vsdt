"""Video Control class file"""

import math
import cv2

class Video(object):
    """Video class"""

    def __init__(self, video_file):
        """Init method"""

        self._video_file = video_file
        self._frames = None
        self._fps = None

        self._process_video_file()

        # self._video_sensor.start()
        #
        # file_dir = os.path.dirname(os.path.realpath(__file__))
        # #pylint: disable=E1101
        # self._face_detector = cv2.CascadeClassifier(
        #     os.path.join(file_dir, 'data', 'haarcascade_frontalface_default.xml'))
        # #pylint: enable=E1101
        #
        # self._buffer_size = buffer_size
        # self._buffer = deque(maxlen=self._buffer_size)
        # self._running = False
        # self._capture_thread = None
        # self._face_recognition = FaceRecognition('gallery')

    def _process_video_file(self):
        """process video file"""
        #pylint: disable=E1101
        capture = cv2.VideoCapture(self._video_file)
        self._fps = capture.get(cv2.CAP_PROP_FPS)
        #pylint: enable=E1101
        self._frames = {}
        time = 0
        success, image = capture.read()
        while success:
            self._frames[time] = image
            time += math.floor(1000/self._fps)
            success, image = capture.read()
            print(time)

    # def next_processed_frame(self):
    #     """Next processed frame method"""
    #
    #     #pylint: disable=E1101
    #     if self._buffer:
    #         return True, self._buffer.pop()
    #     #return self._video_sensor.next_data()
    #     return False, None
    #     #pylint: enable=E1101
    #
    # def start(self):
    #     """Start capture method"""
    #     self._running = True
    #     self._capture_thread = threading.Thread(target=self.__process_frame)
    #     self._capture_thread.start()
    #
    # def pause(self):
    #     """Pause method"""
    #     self._running = False
    #
    # def stop(self):
    #     """Stop capture method"""
    #     self._running = False
    #     self._video_sensor.stop()
    #
    # def is_started(self):
    #     """Check if control was started"""
    #     return self._running
    #
    # def __del__(self):
    #     """Del method"""
    #     self.stop()
    #
    # def __process_frame(self):
    #     """Grab method"""
    #
    #     while self._running:
    #         retval, frame = self._video_sensor.next_data()
    #         if retval:
    #             #pylint: disable=E1101
    #             gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    #             faces = self._face_detector.detectMultiScale(gray, 1.3, 5)
    #             for (x,y,w,h) in faces:
    #                 self._face_recognition.train_test(frame, x, y, w, h)
    #                 #cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
    #             #pylint: enable=E1101
    #             self._buffer.append((frame, faces))
    #         else:
    #             raise Exception('Camera failed')
