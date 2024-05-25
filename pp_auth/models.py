from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id):
        self.id = id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True


class Guest:
    # all inputs are string split, so do all type conversions here
    def __init__(self, id, name, front_image, back_image, day, is_group, group_code, orientation):
        self._id = id
        self._name = name
        self._front_image = front_image
        self._back_image = back_image
        self._day = int(day)
        self._is_group = (is_group == "1")
        if group_code == "":
            self._group_code = None
        else:
            self._group_code = int(group_code)
        self._orientation = orientation
        self._invite_slug = None            # not assigned until admin generates an invite via ui event
        self._auth_id = None                # tracks the same UUID given out to the client's cookie

    # id: is a number unique among the set of Guests
    # added so that there is something easy to put into unique URLs
    # because "names" have whitespace and other formatting factors
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def front_image(self):
        return self._front_image

    @front_image.setter
    def front_image(self, front_image):
        self._front_image = front_image

    @property
    def back_image(self):
        return self._back_image

    @back_image.setter
    def back_image(self, back_image):
        self._back_image = back_image

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, day):
        self._day = day

    @property
    def is_group(self):
        return self._is_group

    @is_group.setter
    def is_group(self, is_group):
        self._is_group = is_group

    @property
    def group_code(self):
        return self._group_code

    @group_code.setter
    def group_code(self, group_code):
        self._group_code = group_code

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, orientation):
        self._orientation = orientation

    @property
    def invite_slug(self):
        return self._invite_slug

    @invite_slug.setter
    def invite_slug(self, invite_slug):
        self._invite_slug = invite_slug

    @property
    def auth_id(self):
        return self._auth_id

    @auth_id.setter
    def auth_id(self, auth_id):
        self._auth_id = auth_id

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)
