def log_warning(*args):
    print(args)

class ITimelineItem:

    def get_type(self):
        return 0

    def get_name(self):
        return "No Name"

    def get_notes(self):
        return ""

    def set_timeline_visibility(self, visibility):
        log_warning("ITimelineItem: Not Implemented", self)

    def get_timeline_visibility(self):
        log_warning("ITimelineItem: Not Implemented", self)
