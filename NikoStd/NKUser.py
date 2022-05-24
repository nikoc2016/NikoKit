from NikoKit.NikoStd.NKDataStructure import NKDataStructure


class NKUser(NKDataStructure):
    def __init__(self,
                 user_id=None,
                 user_account=None,
                 user_print_name=None,
                 user_permission=None,
                 user_account_link_dict=None,
                 *args,
                 **kwargs
                 ):
        self.user_id = user_id
        self.user_account = user_account
        self.user_print_name = user_print_name
        self.user_permission = user_permission
        self.user_account_link_dict = user_account_link_dict

        super(NKUser, self).__init__(*args, **kwargs)

    def p_key(self):
        return self.user_id
