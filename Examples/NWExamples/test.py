class A:

    @classmethod
    def standard_ghost(cls):
        return {
            "xid": "1",
            "xclass": "1",
        }

    @classmethod
    def from_ghost(cls, ghost):
        full_ghost = cls.standard_ghost()
        print(full_ghost)
        full_ghost.update(ghost)
        return cls(**ghost)

    def __init__(self, xid="dei", xclass="dec"):
        print(xid, xclass)
        self.xid = xid
        self.xclass = xclass


class B(A):
    @classmethod
    def standard_ghost(cls):
        print(super(B, B).standard_ghost())
        return {
            "xid": "dei",
            "xclass":"dec",
            "xextra": "dexb"
        }

    def __init__(self, xextra="dexb", **kwargs):
        super(B, self).__init__(**kwargs)


a = B.from_ghost({
            "xid": "oc",
            "xclass":"oc",
            "xextra": "oc"
        })

print(a.__dict__)
