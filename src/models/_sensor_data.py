#pylint: disable=E0401
"""Sensor Data class file"""

import json
import dateutil.parser
from enum import Enum
from control import utils
from models.temporal_data import TemporalData

class SensorType(Enum):
    """Sensor Type enum"""
    ACCELEROMETER = 'accelerometer'
    MAGNETOMETER = 'magnetometer'
    GYROSCOPE = 'gyroscope'
    BAROMETER = 'barometer'
    GPS = 'gps'

class SensorData(TemporalData):
    """Sensor Data class"""

    def __init__(self, json_file=None):
        """Init method"""
        TemporalData.__init__(self)

        self._json_file = json_file
        self._data_id = None
        self._start_time = None
        self._end_time = None
        self._device_name = 'unknown'
        self._device_type = 'smartphone'
        self._device_location = 'unknown'
        self._sensors = {}

        if self._json_file is not None:
            with open(self._json_file) as json_file_reader:
                json_dict = json.load(json_file_reader)
                self._data_id = json_dict['data_id']
                self._start_time = json_dict['start_time']
                if self._start_time is not None:
                    self._start_time = dateutil.parser.parse(self._start_time)
                self._end_time = json_dict['end_time']
                if self._end_time is not None:
                    self._end_time = dateutil.parser.parse(self._end_time)
                self._device_name = json_dict['device_name']
                self._device_type = json_dict['device_type']
                self._device_location = json_dict['device_location']
                self._sensors = json_dict['sensors']
                for sensor in self._sensors:
                    for item in self._sensors[sensor]:
                        item['timestamp'] = dateutil.parser.parse(item['timestamp'])


    def save(self, json_file=None):
        """save method"""
        if json_file is not None:
            self._json_file = json_file
        if self._json_file is None:
            raise FileNotFoundError('This sensor data is new and does not have a json file')

        json_dict = self.to_dict()
        with open(self._json_file, 'w') as json_file:
            json.dump(json_dict, json_file, default=utils.handler)

    def to_dict(self):
        """generate json timestamps"""
        ret_dict = {}
        ret_dict['sensors'] = self._sensors
        ret_dict['data_id'] = self._data_id
        ret_dict['start_time'] = self._start_time
        ret_dict['end_time'] = self._end_time
        ret_dict['sensors'] = self._sensors
        ret_dict['device_name'] = self._device_name
        ret_dict['device_type'] = self._device_type
        ret_dict['device_location'] = self._device_location
        return ret_dict

    def add_sensor(self, sensor_type, data):
        """add data"""
        self._sensors[sensor_type] = data
        self._limits_calculation()

    def remove_sensor(self, sensor_type):
        """remove data"""
        del self._sensors[sensor_type]
        self._limits_calculation()

    def _limits_calculation(self):
        """limits calculation"""
        starts = []
        ends = []
        for data in self._sensors.values():
            starts.append(data[0]['timestamp'])
            ends.append(data[-1]['timestamp'])
        self._start_time = min(starts) if starts else None
        self._end_time = max(ends) if ends else None

    def sensor_to_list(self, sensor_type):
        """convert sensor to a list of tuples"""
        ret_list = []
        for data in self._sensors[sensor_type]:
            timestamp = data['timestamp']
            values = tuple(data['values'].values())
            ret_list.append((timestamp, ) + values)
        return ret_list

    def has_sensor(self, sensor_type):
        """check if sensor data has sensor_type"""
        return sensor_type in self._sensors

    @property
    def device_name(self):
        """device name property"""
        return self._device_name

    @device_name.setter
    def device_name(self, value):
        """device name property"""
        if value == '':
            value = 'unknown'
        self._device_name = value

    @property
    def device_type(self):
        """device type property"""
        return self._device_type

    @device_type.setter
    def device_type(self, value):
        """device type property"""
        self._device_type = value

    @property
    def device_location(self):
        """device local property"""
        return self._device_location

    @device_location.setter
    def device_location(self, value):
        """device location property"""
        if value == '':
            value = 'unknown'
        self._device_location = value

    @property
    def sensors(self):
        """sensors count property"""
        return self._sensors

    @property
    def sensors_count(self):
        """sensors count property"""
        return len(self._sensors)

    @property
    def json_file(self):
        """json file property"""
        return self._json_file
