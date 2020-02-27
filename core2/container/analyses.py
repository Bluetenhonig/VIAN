from core2.container.annotation import Annotation

class Analysis(Annotation):
    def __init__(self, analysis_type_name = None):
        super(Analysis, self).__init__()
        self.analysis_type_name = analysis_type_name

class HDF5Analysis(Analysis):
    def __init__(self, hdf5_dataset, hdf5_index):
        super(HDF5Analysis, self).__init__()
        self.hdf5_dataset = hdf5_dataset
        self.hdf5_index = hdf5_index

