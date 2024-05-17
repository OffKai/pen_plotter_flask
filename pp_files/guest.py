
class Guest:

    def __init__(self, name, filename, day):
        self._name = name
        self._filename = filename
        self._day = day

    # name: is the full name of the talent(s)
    # capitalization is included, and should follow the talents' preferences (e.g. purposely lowercase), but accents are removed
    # time slots with multiple talents have the combined list of names, comma separated, and whitespace included
    # name is used as a key for the whole object instance, because they should be unique
    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, filename):
        self._filename = filename

    # day: is encoded as an integer 0, 1, or 2, representing friday saturday sunday, respectively
    # 3 is used in other code for "all"
    # storing day in the guest data is useful for separating them by day in the UI
    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, day):
        self._day = day