class NKVersion:
    ALPHA = "Alpha"
    BETA = "Beta"
    PREVIEW = "Preview"
    RELEASE = "Release"
    STABLE = "Stable"

    def __init__(self, version_string):
        versions = version_string.split(".")
        self.main_version = int(versions[0])
        self.sub_version = int(versions[1])
        self.mini_version = int(versions[2])

    def __eq__(self, other):
        return self.main_version == other.main_versionand \
               and self.sub_version == other.sub_version \
               and self.mini_version == other.mini_version

    def __ge__(self, other):
        if self.main_version > other.main_version:
            return True
        elif self.main_version == other.main_version:
            if self.sub_version > other.sub_version:
                return True
            elif self.sub_version == other.sub_version:
                if self.mini_version >= other.mini_version:
                    return True

        return False

    def __gt__(self, other):
        if self.main_version > other.main_version:
            return True
        elif self.main_version == other.main_version:
            if self.sub_version > other.sub_version:
                return True
            elif self.sub_version == other.sub_version:
                if self.mini_version > other.mini_version:
                    return True

        return False

    def __le__(self, other):
        if self.main_version < other.main_version:
            return True
        elif self.main_version == other.main_version:
            if self.sub_version < other.sub_version:
                return True
            elif self.sub_version == other.sub_version:
                if self.mini_version <= other.mini_version:
                    return True

        return False

    def __lt__(self, other):
        if self.main_version < other.main_version:
            return True
        elif self.main_version == other.main_version:
            if self.sub_version < other.sub_version:
                return True
            elif self.sub_version == other.sub_version:
                if self.mini_version < other.mini_version:
                    return True

        return False

    def __ne__(self, other):
        if self.main_version != other.main_version \
                or self.sub_version != other.sub_version \
                or self.mini_version != other.mini_version:
            return True

        return False

    def __str__(self):
        return ("%i.%i.%i" % (self.main_version,
                              self.sub_version,
                              self.mini_version))
