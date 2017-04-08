"""Video Control class file"""

from collections import OrderedDict
import cv2


class FrameCache(OrderedDict):
    """FrameCache class"""

    def __init__(self, *args, **kwds):
        """Init method"""
        self.size_limit = kwds.pop("size_limit", None)
        OrderedDict.__init__(self, *args, **kwds)
        self._check_size_limit()

    #pylint: disable=W0221
    def __setitem__(self, key, value):
        """Set Item method"""
        OrderedDict.__setitem__(self, key, value)
        self._check_size_limit()
    #pylint: enable=W0221

    def _check_size_limit(self):
        if self.size_limit is not None:
            while len(self) > self.size_limit:
                self.popitem(last=False)


class VisualData(object):
    """Visual Data class"""

    def __init__(self, video_file):
        """Init method"""

        #pylint: disable=E1101
        self._video_file = video_file
        self._capture = cv2.VideoCapture(self._video_file)

        self._fps = self._capture.get(cv2.CAP_PROP_FPS)
        self._frames_count = self._capture.get(cv2.CAP_PROP_FRAME_COUNT)

        self._length = (self.frames_count/self._fps)*1000
        self._start_time = 0
        self._end_time = self._length
        self._interval = (1000/self._fps)
        #pylint: enable=E1101

    def get_frame(self, time):
        "get frame at time"
        required_frame = time // (1000/self._fps)
        #pylint: disable=E1101
        next_frame = self._capture.get(cv2.CAP_PROP_POS_FRAMES)
        #pylint: enable=E1101

        frame = None
        if required_frame != next_frame:
            #pylint: disable=E1101
            self._capture.set(cv2.CAP_PROP_POS_FRAMES, required_frame)
            #pylint: enable=E1101

        _, frame = self._capture.read()
        return frame

    def _convert_time_to_frame_id(self, time):
        """given a timestamp, convert it to frame id sequence"""
        return time//self._interval


    @property
    def fps(self):
        """fps property"""
        return self._fps

    @property
    def start_time(self):
        """start time property"""
        return self._start_time

    @property
    def end_time(self):
        """end time property"""
        return self._end_time

    @property
    def interval(self):
        """start time property"""
        return self._interval

    @property
    def frames_count(self):
        """frames count property"""
        return self._frames_count

    @property
    def length(self):
        """length property"""
        return self._length
