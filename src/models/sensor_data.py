"""SensorData class file."""

#pylint: disable=E0611
#pylint: disable=E0401
from models.temporal_data import TemporalData
#pylint: enable=E0401
#pylint: enable=E0611

SENSORTYPES = (
    'accelerometer',
    'magnetometer',
    'gyroscope',
    'barometer',
    'gps'
    )

SENSORTYPES_VALUES_SIZES = {
    'accelerometer':3,
    'magnetometer':3,
    'gyroscope':3,
    'barometer':1,
    'gps':2
    }

class SensorData(TemporalData):
    """Sensor Data class"""

    def __init__(self, sensor_type, readings, data_id=None):
        """Init method."""
        TemporalData.__init__(self)

        if not sensor_type in SENSORTYPES:
            raise AttributeError('Invalid sensor type: {}'.format(sensor_type))
        self._sensor_type = sensor_type
        self._readings = readings
        self._data_id = data_id if data_id is not None else self._sensor_type
        self._start_time = self._readings[0][0]
        self._end_time = self._readings[-1][0]
        self._interval = float(self.length / len(self._readings))

    def to_dict(self):
        """Export data to dict."""
        ret_dict = {}
        ret_dict['data_id'] = self._data_id
        ret_dict['start_time'] = self._start_time
        ret_dict['end_time'] = self._end_time
        ret_dict['interval'] = self._interval
        ret_dict['sensor_type'] = self._sensor_type
        ret_dict['readings'] = self._readings
        return ret_dict

    @property
    def sensor_type(self):
        """str: Sensor type."""
        return self._sensor_type

    @property
    def readings(self):
        """int: Readings from sensor."""
        return self._readings
