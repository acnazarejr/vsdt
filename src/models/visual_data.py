#pylint: disable=E0401
"""Video Control class file"""

import os
import json
import datetime
import dateutil.parser

import cv2
from control import utils
from models.temporal_data import TemporalData

class VisualData(TemporalData):
    """Visual Data class"""

    def __init__(self, json_file=None):
        """Init method"""
        TemporalData.__init__(self)

        self._json_file = json_file
        self._data_id = None
        self._fps = None
        self._frames_count = None
        self._interval = None
        self._start_time = None
        self._end_time = None
        self._video_file = None
        self._video_capture = None
        self._timestamps = None

        if self._json_file is not None:
            with open(self._json_file) as json_file_reader:
                json_dict = json.load(json_file_reader)
                self._data_id = json_dict['data_id']
                self._fps = json_dict['fps']
                self._frames_count = json_dict['frames_count']
                self._interval = json_dict['interval']
                self._start_time = dateutil.parser.parse(json_dict['start_time'])
                self._end_time = dateutil.parser.parse(json_dict['end_time'])
                self._video_file = json_dict['video_file']
                if not os.path.isfile(self._video_file):
                    raise FileNotFoundError('Invalid video file')
                #pylint: disable=E1101
                capture = cv2.VideoCapture(self._video_file)
                #pylint: enable=E1101
                if not capture.isOpened():
                    raise FileNotFoundError('Invalid video file')
                self._video_capture = capture
                self._timestamps = [dateutil.parser.parse(timestamp)
                                    for timestamp in json_dict['timestamps']]

    def set_video_file(self, video_file):
        """Set the video file to visual data"""
        #pylint: disable=E1101
        if not os.path.isfile(video_file):
            raise FileNotFoundError('Invalid video file')
        capture = cv2.VideoCapture(video_file)
        if not capture.isOpened():
            raise FileNotFoundError('Invalid video file')

        self._video_file = video_file
        self._video_capture = capture

        self._fps = self._video_capture.get(cv2.CAP_PROP_FPS)
        self._frames_count = int(self._video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        self._interval = (1000/self._fps)
        self._timestamps = [None] * self._frames_count
        self.synchonize_timestamps(utils.milliseconds_to_timestamp(0), 0)
        #pylint: enable=E1101

    def has_video(self):
        """check if visual data has video"""
        return self._video_capture is not None

    def get_frame(self, time):
        "get frame at time"
        time_milliseconds = utils.time_delta_in_milliseconds(time, self._start_time)
        required_frame = int(time_milliseconds // self._interval)
        #pylint: disable=E1101
        next_frame = self._video_capture.get(cv2.CAP_PROP_POS_FRAMES)
        #pylint: enable=E1101

        frame = None
        if required_frame != next_frame:
            #pylint: disable=E1101
            self._video_capture.set(cv2.CAP_PROP_POS_FRAMES, required_frame)
            #pylint: enable=E1101

        ret, frame = self._video_capture.read()
        if not ret:
            raise MemoryError('Invalid frame at {}'.format(time))
        return frame, self._timestamps[required_frame]

    def synchonize_timestamps(self, ref_timestamp, ref_frame=None):
        """generate frame timestamps from a reference frame and a reference timestamp"""

        ref_frame = ref_frame if ref_frame is not None else self.current_frame
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

        self._start_time = self._timestamps[0]
        self._end_time = self._timestamps[self._frames_count - 1]

    def save(self, json_file=None):
        """save method"""
        if json_file is not None:
            self._json_file = json_file
        if self._json_file is None:
            raise FileNotFoundError('This visual data is new and does not have a json file')

        json_dict = self.to_dict()
        with open(self._json_file, 'w') as json_file:
            json.dump(json_dict, json_file, default=utils.handler)

    def to_dict(self):
        """generate json timestamps"""
        ret_dict = {}
        ret_dict['timestamps'] = self._timestamps
        ret_dict['data_id'] = self._data_id
        ret_dict['fps'] = self._fps
        ret_dict['frames_count'] = self._frames_count
        ret_dict['interval'] = self._interval
        ret_dict['start_time'] = self._start_time
        ret_dict['end_time'] = self._end_time
        ret_dict['video_file'] = self._video_file
        return ret_dict

    @staticmethod
    def create_from_video(video_file):
        """Create a new visual data from a video file"""
        visual_data = VisualData()
        visual_data.set_video_file(video_file)
        #pylint: disable=W0201
        visual_data.data_id = os.path.splitext(os.path.basename(video_file))[0]
        #pylint: enable=W0201
        return visual_data

    @property
    def current_frame(self):
        """fps property"""
        #pylint: disable=E1101
        return int(self._video_capture.get(cv2.CAP_PROP_POS_FRAMES) - 1)
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
    def json_file(self):
        """json file property"""
        return self._json_file

    @property
    def video_file(self):
        """video file property"""
        return self._video_file
