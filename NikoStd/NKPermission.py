from enum import auto, Flag


# WARNING, Method returns new permission instead of modifying
class NKPermission(Flag):
    def grant(self, new_permission):
        return self | new_permission

    def revoke(self, new_permission):
        return self ^ new_permission

    def has(self, new_permission):
        return self & new_permission

    @classmethod
    def get_super(cls):
        super_perm = cls(0)
        for perm in cls:
            super_perm = super_perm.grant(perm)
        return super_perm
