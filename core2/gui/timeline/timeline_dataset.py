from .timeline_interfaces import ITimelineItem

import numpy as np
from scipy.signal import savgol_filter, resample

class TimelineDataset(ITimelineItem):
    """
    A Dataset which can be displayed in the timeline.
    The get_data_range function has to be overwritten accordingly.

    """
    VIS_TYPE_AREA = 0
    VIS_TYPE_LINE = 1

    def __init__(self, name, data, ms_to_idx = 1.0, vis_type = VIS_TYPE_LINE):
        self.data = data
        self.strip_height = 45
        self.name = name
        self.ms_to_idx = ms_to_idx
        self.vis_type = vis_type

    def get_data_range(self, t_start, t_end, norm=True, subsample=True):
        idx_a = int(np.floor(t_start / self.ms_to_idx))
        idx_b = int(np.ceil(t_end / self.ms_to_idx))

        offset = (t_start / self.ms_to_idx) - int(np.floor(t_start / self.ms_to_idx))

        ms = np.array(list(range(idx_a, idx_b)))
        ms = np.multiply(ms, self.ms_to_idx)
        ms = np.subtract(ms, offset)

        data = np.array(self.data[idx_a:idx_b].copy())
        if data.shape[0] == 0:
            return  np.array([]), np.array([])
        if data.shape[0] > 1000:
            k = int(data.shape[0] / 1000)

            if k % 2 == 0:
                f = k + 1
            else:
                f = k

            data = resample(data, data[0::k].shape[0])
            ms = ms[0::k]
        if norm:
            data /= np.amax(self.data)
        try:
            return data, ms
        except Exception as e:
            raise e
        return np.array([]), np.array([])

    def get_name(self):
        return self.name

    def get_notes(self):
        return ""