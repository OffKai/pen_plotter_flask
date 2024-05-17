class Guest:

    def __init__(self, name, filename, day, id):
        self._name = name
        self._filename = filename
        self._day = day
        self._id = id
        self._invite_slug = "" # not assigned until admin generates an invite via ui event

    # name: is the full name of the talent(s)
    # capitalization is included, and should follow the talents' preferences (e.g. purposely lowercase), but accents are removed
    # time slots with multiple talents have the combined list of names, comma separated, and whitespace included
    @property
    def name(self):
        return self._name

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

    # id: is an integer unique among the set of Guests
    # added so that there is something easy to put into unique URLs
    # because "names" have whitespace and can be ordered differently when it's a group
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def invite_slug(self):
        return self._invite_slug

    @invite_slug.setter
    def invite_slug(self, invite_slug):
        self._invite_slug = invite_slug
