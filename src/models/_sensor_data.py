# """Video Control class file"""
#
# import random
# import numpy as np
#
# class SensorData(object):
#     """Sensor Data class"""
#
#     def __init__(self, sensor_file):
#         """Init method"""
#
#         #pylint: disable=E1101
#         self._video_file = sensor_file
#
#         self._data_count = 1000
#         self._start_time = 0
#         self._end_time = 60000
#         self._timestamps = np.arange(self._start_time, self._end_time, 0.2)
#         self._x_values = [random.randint(0, 10) for i in range(len(self._timestamps))]
#         self._y_values = [random.randint(0, 10) for i in range(len(self._timestamps))]
#         self._z_values = [random.randint(0, 10) for i in range(len(self._timestamps))]
#         #pylint: enable=E1101
