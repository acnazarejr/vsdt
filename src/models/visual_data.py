"""VisualData class file."""

import os
import json
import datetime
from shutil import copyfile
import dateutil.parser

import cv2
#pylint: disable=E0611
#pylint: disable=E0401
from utils.time import time_delta_in_milliseconds, milliseconds_to_datetime
from utils.files import is_path_creatable
from utils.json import json_handler
from models.temporal_data import TemporalData
#pylint: enable=E0401
#pylint: enable=E0611

class VisualData(TemporalData):
    """VisualData class."""

    ###############################################################################################
    # Init
    ###############################################################################################

    def __init__(self, json_file=None):
        """Init method."""
        TemporalData.__init__(self)

        self._data_id = None
        self._fps = None
        self._frames_count = None
        self._interval = None
        self._start_time = None
        self._end_time = None
        self._video_file_basename = None
        self._video_file_path = None
        self._video_capture = None
        self._timestamps = None

        if json_file is not None:
            with open(json_file) as json_file_reader:
                json_dict = json.load(json_file_reader)
                self._data_id = json_dict['data_id']
                self._interval = json_dict['interval']
                self._start_time = dateutil.parser.parse(json_dict['start_time'])
                self._end_time = dateutil.parser.parse(json_dict['end_time'])
                self._fps = json_dict['fps']
                self._frames_count = json_dict['frames_count']
                self._video_file_name = json_dict['video_file_name']
                self._video_file_path = os.path.join(os.path.dirname(json_file),
                                                     self._video_file_name)
                if not os.path.isfile(self._video_file_path):
                    raise FileNotFoundError('Invalid video file path: {}'.format(
                        self._video_file_path))
                #pylint: disable=E1101
                capture = cv2.VideoCapture(self._video_file_path)
                #pylint: enable=E1101
                if not capture.isOpened():
                    raise AssertionError('Invalid video format: {}'.format(self._video_file_path))
                self._video_capture = capture
                self._timestamps = [dateutil.parser.parse(timestamp)
                                    for timestamp in json_dict['timestamps']]

    ###############################################################################################
    # Public Methods
    ###############################################################################################
    def has_video(self):
        """bool: returns if visual data has a valid video or not"""
        return (self._video_capture is not None) and (self._video_capture.isOpened())


    def set_video(self, video_file_path):
        """Set the video file to visual data."""
        #pylint: disable=E1101
        if not os.path.isfile(video_file_path):
            raise FileNotFoundError('Invalid video file path: {}'.format(video_file_path))
        capture = cv2.VideoCapture(video_file_path)
        if not capture.isOpened():
            raise AssertionError('Invalid video format: {}'.format(video_file_path))

        self._video_file_name = os.path.basename(video_file_path)
        self._video_file_path = video_file_path
        self._video_capture = capture

        self._fps = self._video_capture.get(cv2.CAP_PROP_FPS)
        self._frames_count = int(self._video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        self._timestamps = [None] * self._frames_count
        self._interval = (1000/self._fps)
        self.synchonize_timestamps(milliseconds_to_datetime(0), 0)
        #pylint: enable=E1101


    def synchonize_timestamps(self, ref_timestamp, ref_frame=None):
        """Generate frame timestamps from a reference frame and a reference timestamp."""
        if not self.has_video():
            raise RuntimeError('This visual data has no video')

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


    def frame_at_time(self, time):
        """Get frame at time."""
        if not self.has_video():
            raise RuntimeError('This visual data has no video')

        if (time < self._start_time) or (time > self._end_time):
            return None, None

        time_milliseconds = time_delta_in_milliseconds(time, self._start_time)
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


    def save(self, json_file):
        """Save visual data in the specified json file."""
        if not self.has_video():
            raise RuntimeError('This visual data has no video')
        if not is_path_creatable(json_file):
            raise FileNotFoundError('Invalide json_file: {}'.format(json_file))

        video_file_path = os.path.join(os.path.dirname(json_file), self._video_file_name)
        if not os.path.exists(video_file_path):
            copyfile(self._video_file_path, video_file_path)
            self._video_file_path = video_file_path

        json_dict = self.to_dict()
        with open(json_file, 'w') as json_file_writer:
            json.dump(json_dict, json_file_writer, default=json_handler)


    def to_dict(self):
        """generate json timestamps"""
        if not self.has_video():
            raise RuntimeError('This visual data has no video')

        ret_dict = {}
        ret_dict['timestamps'] = self._timestamps
        ret_dict['data_id'] = self._data_id
        ret_dict['fps'] = self._fps
        ret_dict['frames_count'] = self._frames_count
        ret_dict['interval'] = self._interval
        ret_dict['start_time'] = self._start_time
        ret_dict['end_time'] = self._end_time
        ret_dict['video_file_name'] = self._video_file_name
        return ret_dict

    ###############################################################################################
    # Static methods
    ###############################################################################################
    @staticmethod
    def create_from_video(video_file_path):
        """Create a new visual data from a video file"""
        visual_data = VisualData()
        visual_data.set_video(video_file_path)
        #pylint: disable=W0201
        visual_data.data_id = os.path.splitext(os.path.basename(video_file_path))[0]
        #pylint: enable=W0201
        return visual_data


    ###############################################################################################
    # Properties
    ###############################################################################################
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
    def video_file_name(self):
        """video file property"""
        return self._video_file_name

    @property
    def video_file_path(self):
        """video file property"""
        return self._video_file_path
