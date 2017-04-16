"""SensorSetData class file"""

import json
import dateutil.parser
# import dateutil.parser
#pylint: disable=E0611
#pylint: disable=E0401
# from control import utils
from models.temporal_data import TemporalData
from models.sensor_data import SensorData
from utils.files import is_path_creatable
from utils.json import json_handler
#pylint: enable=E0401
#pylint: enable=E0611

class SensorSetData(TemporalData):
    """SensorSetData class"""

    ###############################################################################################
    # Init
    ###############################################################################################
    def __init__(self, json_file=None):
        """Init method."""
        TemporalData.__init__(self)

        self._data_id = None
        self._start_time = None
        self._end_time = None
        self._interval = None
        self._device_name = 'unknown'
        self._device_type = 'unknown'
        self._device_location = 'unknown'
        self._sensors_data = []

        if json_file is not None:
            with open(json_file) as json_file_reader:
                json_dict = json.load(json_file_reader)
                self.from_dict(json_dict)

    ###############################################################################################
    # Public Methods
    ###############################################################################################
    def save(self, json_file):
        """save method"""
        if not is_path_creatable(json_file):
            raise FileNotFoundError('Invalide json_file: {}'.format(json_file))

        json_dict = self.to_dict()
        with open(json_file, 'w') as json_file_writer:
            json.dump(json_dict, json_file_writer, default=json_handler)

    def to_dict(self):
        """export data from dict"""
        ret_dict = {}
        ret_dict['data_id'] = self._data_id
        ret_dict['start_time'] = self._start_time
        ret_dict['end_time'] = self._end_time
        ret_dict['interval'] = self._interval
        ret_dict['device_name'] = self._device_name
        ret_dict['device_type'] = self._device_type
        ret_dict['device_location'] = self._device_location
        ret_dict['sensors_data'] = [sensor_data.to_dict() for sensor_data in self._sensors_data]
        return ret_dict

    def from_dict(self, import_dict):
        """import data from dict"""
        self._data_id = import_dict['data_id']
        self._start_time = import_dict['start_time']
        if self._start_time is not None:
            self._start_time = dateutil.parser.parse(self._start_time)
        self._end_time = import_dict['end_time']
        if self._end_time is not None:
            self._end_time = dateutil.parser.parse(self._end_time)
        self._device_name = import_dict['device_name']
        self._device_type = import_dict['device_type']
        self._device_location = import_dict['device_location']
        self._sensors_data.clear()
        for item in import_dict['sensors_data']:
            for reading in item['readings']:
                reading[0] = dateutil.parser.parse(reading[0])
            sensor_data = SensorData(item['sensor_type'], item['readings'])
            self._sensors_data.append(sensor_data)

    def add_sensor_data(self, sensor_type, readings):
        """Add sensor data."""
        sensor_data = SensorData(sensor_type, readings)
        self._sensors_data.append(sensor_data)
        self._limits_calculation()

    def remove_sensor_data(self, sensor_type):
        """Remove sensor data."""
        del_idx = None
        for idx, sensor_data in enumerate(self._sensors_data):
            if sensor_type == sensor_data.sensor_type:
                del_idx = idx
                break
        if del_idx is not None:
            del self._sensors_data[del_idx]
            self._limits_calculation()
            return True
        else:
            return False

    def get_sensor_data(self, sensor_type):
        """Get sensor data."""
        for sensor_data in self._sensors_data:
            if sensor_type == sensor_data.sensor_type:
                return sensor_data
        return None

    # def sensor_to_list(self, sensor_type):
    #     """convert sensor to a list of tuples"""
    #     ret_list = []
    #     for data in self._sensors[sensor_type]:
    #         timestamp = data['timestamp']
    #         values = tuple(data['values'].values())
    #         ret_list.append((timestamp, ) + values)
    #     return ret_list
    #
    def has_sensor(self, sensor_type):
        """Check if has sensor_type."""
        for sensor_data in self._sensors_data:
            if sensor_type == sensor_data.sensor_type:
                return True
        return False

    ###############################################################################################
    # Private methods
    ###############################################################################################
    def _limits_calculation(self):
        """limits calculation"""
        starts = []
        ends = []
        intervals = []
        for sensor_data in self._sensors_data:
            starts.append(sensor_data.start_time)
            ends.append(sensor_data.end_time)
            intervals.append(sensor_data.interval)
        self._start_time = min(starts) if starts else None
        self._end_time = max(ends) if ends else None
        self._interval = min(intervals) if intervals else None

    ###############################################################################################
    # Properties
    ###############################################################################################
    @property
    def sensors_data(self):
        "list: SensorData list."
        return self._sensors_data

    @property
    def device_name(self):
        """str: Device name property."""
        return self._device_name

    @device_name.setter
    def device_name(self, value):
        if (value == '') or (value is None):
            value = 'unknown'
        self._device_name = value

    @property
    def device_type(self):
        """str: Device type property."""
        return self._device_type

    @device_type.setter
    def device_type(self, value):
        if (value == '') or (value is None):
            value = 'unknown'
        self._device_type = value

    @property
    def device_location(self):
        """str: Device local property"""
        return self._device_location

    @device_location.setter
    def device_location(self, value):
        if value == '':
            value = 'unknown'
        self._device_location = value
