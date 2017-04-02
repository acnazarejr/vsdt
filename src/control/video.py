"""Video Control class file"""

from collections import OrderedDict
import math
import cv2


class LimitedSizeDict(OrderedDict):
    def __init__(self, *args, **kwds):
        self.size_limit = kwds.pop("size_limit", None)
        OrderedDict.__init__(self, *args, **kwds)
        self._check_size_limit()

    def __setitem__(self, key, value):
        OrderedDict.__setitem__(self, key, value)
        self._check_size_limit()

    def _check_size_limit(self):
        if self.size_limit is not None:
            while len(self) > self.size_limit:
                self.popitem(last=False)


class Video(object):
    """Video class"""

    def __init__(self, video_file):
        """Init method"""

        self._video_file = video_file
        self._fps = None
        self._frames_count = None
        self._length = None
        self._capture = None

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
        self._capture = cv2.VideoCapture(self._video_file)
        self._fps = self._capture.get(cv2.CAP_PROP_FPS)
        print(self._fps)
        self._frames_count = self._capture.get(cv2.CAP_PROP_FRAME_COUNT)
        print(self._frames_count)
        self._length = (self.frames_count/self._fps)*1000
        print(self._length)
        #pylint: enable=E1101

    def get_frame(self, time):
        "get frame at time"
        frame_idx = time // (1000/self._fps)

        _, frame = self._capture.read()
        print(1000/self._fps, frame_idx, self._capture.get(cv2.CAP_PROP_POS_FRAMES), self._capture.get(cv2.CAP_PROP_POS_MSEC), time)
        return frame

    @property
    def fps(self):
        """fps property"""
        return self._fps

    @fps.setter
    def fps(self, value):
        self._fps = value

    @property
    def frames_count(self):
        """frames count property"""
        return self._frames_count

    @frames_count.setter
    def frames_count(self, value):
        self._frames_count = value

    @property
    def length(self):
        """length property"""
        return self._length

    @length.setter
    def length(self, value):
        self._length = value

        # #pylint: disable=E1101
        # capture = cv2.VideoCapture(self._video_file)
        # self._fps = capture.get(cv2.CAP_PROP_FPS)
        # #pylint: enable=E1101
        # self._frames = {}
        # time = 0
        # count = 0
        # while capture.isOpened():
        #     success, image = capture.read()
        #     # self._frames[time] = image
        #     time += math.floor(1000/self._fps)
        #     count += 1
        #     if(count % 50 == 0):
        #         print(count, time)
        #     if not success:
        #         print('error', count, time)
        # capture.release()

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
