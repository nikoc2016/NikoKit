import os
import os.path as p


class NKRoute:
    def __init__(self,
                 route,
                 sep=os.sep,
                 *args,
                 **kwargs):
        super(NKRoute, self).__init__(*args, **kwargs)
        self.sep = sep
        self.segments = route.split(sep)

    def exists(self):
        return self.is_path() or self.is_dir()

    def is_path(self):
        return p.isfile(repr(self))

    def is_dir(self):
        return p.isdir(repr(self))

    def __repr__(self):
        return self.sep.join(self.segments)
