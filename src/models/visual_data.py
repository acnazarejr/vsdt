#pylint: disable=E0401
"""Video Control class file"""

import json
import datetime
import dateutil

import cv2
from control import utils
from models.data import Data

class VisualData(Data):
    """Visual Data class"""

    def __init__(self, video_file, json_file_name=None):
        """Init method"""

        super(VisualData, self).__init__()

        #pylint: disable=E1101
        self._video_file = video_file
        self._capture = cv2.VideoCapture(self._video_file)

        if not self._capture.isOpened():
            return

        self._fps = self._capture.get(cv2.CAP_PROP_FPS)
        self._frames_count = int(self._capture.get(cv2.CAP_PROP_FRAME_COUNT))
        self._interval = (1000/self._fps)

        if json_file_name is None:
            self._timestamps = [None] * self._frames_count
            self.synchonize_timestamps(utils.milliseconds_to_timestamp(0), 0)
        else:
            self.load_json(json_file_name)

        #pylint: enable=E1101

    def get_frame(self, time):
        "get frame at time"
        time_milliseconds = utils.time_delta_in_milliseconds(time, self._start_time)
        required_frame = int(time_milliseconds // self._interval)
        #pylint: disable=E1101
        next_frame = self._capture.get(cv2.CAP_PROP_POS_FRAMES)
        #pylint: enable=E1101

        frame = None
        if required_frame != next_frame:
            #pylint: disable=E1101
            self._capture.set(cv2.CAP_PROP_POS_FRAMES, required_frame)
            #pylint: enable=E1101

        _, frame = self._capture.read()
        return frame, self._timestamps[required_frame]

    def synchonize_timestamps(self, ref_timestamp, ref_frame=None):
        """generate frame timestamps from a reference frame and a reference timestamp"""

        ref_frame = ref_frame if ref_frame is not None else self.current_frame

        print(ref_timestamp, ref_frame)

        for current_frame in range(ref_frame, -1, -1):
            steps = ref_frame - current_frame
            diff_time = self._interval * steps
            current_timestamp = ref_timestamp - datetime.timedelta(milliseconds=diff_time)
            self._timestamps[current_frame] = current_timestamp

        for current_frame in range(ref_frame, self._frames_count):
            steps = current_frame - ref_frame
            diff_time = self._interval * steps
            current_timestamp = ref_timestamp + datetime.timedelta(milliseconds=diff_time)
            self._timestamps[current_frame] = current_timestamp

        self._refresh_limit_values()

    def load_json(self, json_file_name):
        """generate json timestamps"""
        with open(json_file_name) as json_file:
            json_dict = json.load(json_file)
        self._timestamps = [dateutil.parser.parse(str_timestamp)
                            for str_timestamp in json_dict['timestamps']]
        self._refresh_limit_values()

    def save_json(self, json_file_name):
        """generate json timestamps"""
        json_dict = self.generate_json_dict()
        with open(json_file_name, 'w') as json_file:
            json.dump(json_dict, json_file, default=utils.datetime_handler)

    def generate_json_dict(self):
        """generate json timestamps"""
        json_dict = {}
        json_dict['timestamps'] = self._timestamps
        return json_dict

    def _refresh_limit_values(self):
        """refresh limit values"""
        self._length = int((self.frames_count/self._fps)*1000)
        self._start_time = self._timestamps[0]
        self._end_time = self._start_time + datetime.timedelta(milliseconds=self._length)


    def _convert_time_to_frame_id(self, time):
        """given a timestamp, convert it to frame id sequence"""
        return time//self._interval

    def is_opened(self):
        """returns if video data is opened"""
        return self._capture.isOpened()

    @property
    def current_frame(self):
        """fps property"""
        #pylint: disable=E1101
        return int(self._capture.get(cv2.CAP_PROP_POS_FRAMES) - 1)
        #pylint: enable=E1101

    @property
    def fps(self):
        """fps property"""
        return self._fps

    @property
    def frames_count(self):
        """frames count property"""
        return self._frames_count

    @property
    def video_file(self):
        """length property"""
        return self._video_file
