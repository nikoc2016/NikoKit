import re
import traceback

import ldap3

from NikoKit.NikoStd.NKPrint import eprint


class NKAd:
    dn = "distinguishedName"
    cn = "cn"
    CN = "CN"
    sn = "sn"
    ou = "ou"
    OU = "OU"
    givenName = "givenName"
    sAMAccountName = "sAMAccountName"
    lastLogon = "lastLogon"
    accountExpires = "accountExpires"
    objectclass = "objectclass"
    userAccountControl = "userAccountControl"
    memberOf = "memberOf"
    ALL_ATTRIBUTES = "*"
    oc_group = "group"
    oc_person = "person"
    oc_ou = "OrganizationalUnit"

    def __init__(self,
                 host,
                 username,
                 password,
                 search_base="OU=org,DC=domain,DC=controller",  # MUST BE UPPERCASE
                 port=389):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.search_base = search_base
        try:
            self.server = ldap3.Server(host=host, get_info=ldap3.ALL)
            self.conn = ldap3.Connection(server=self.server,
                                         user=self.username,
                                         password=self.password,
                                         auto_bind=True,
                                         fast_decoder=True,
                                         check_names=True,
                                         authentication=ldap3.NTLM)
        except:
            eprint(traceback.format_exc())

    class NKAdUser:
        def __init__(self):
            self.person = None
            self.groups = []
            self.ous = []

        def __repr__(self):
            return "NKAdUser<person=%s, groups=%s, ous=%s>" % (self.person.sAMAccountName, self.groups, self.ous)

    def get_groups(self):
        targets = []
        query_success = self.conn.search(
            search_base=self.search_base,
            attributes=[self.dn],
            search_filter="(%s=%s)" % (self.objectclass, self.oc_group)
        )
        if query_success:
            for entry in self.conn.entries:
                group_name_re_result = re.search("CN=(.*?),", str(entry.distinguishedName))
                if group_name_re_result:
                    targets.append(group_name_re_result.group(1))
        return targets

    def get_ous(self):
        targets = []
        query_success = self.conn.search(
            search_base=self.search_base,
            attributes=[self.dn],
            search_filter="(%s=%s)" % (self.objectclass, self.oc_ou),
            search_scope=ldap3.SUBTREE,
        )
        if query_success:
            for entry in self.conn.entries:
                unique_part = str(entry.distinguishedName).split(self.search_base)[0]
                ou_re_result = re.search("OU=(.*?),", unique_part)
                if ou_re_result:
                    targets.append(ou_re_result.group(1))
        return targets

    def get_users(self,
                  account_list=None,
                  name_list=None,
                  group_list=None,
                  ou_list=None,
                  attribute_list=None,
                  active_user_only=True):
        ad_ous = self.get_ous()
        ad_groups = self.get_groups()

        if not attribute_list:
            attribute_list = self.get_default_attributes()

        attr_set = set(attribute_list)
        attr_set.add(self.sAMAccountName)
        attr_set.add(self.dn)
        attr_set.add(self.cn)
        attr_set.add(self.memberOf)
        attr_set.add(self.userAccountControl)
        attribute_list = list(attr_set)

        if self.sAMAccountName not in attribute_list:
            attribute_list.append(self.sAMAccountName)

        name_filtering_counter = 0
        name_filtering_str = ""
        object_filtering_str = "(%s=%s)" % (self.objectclass, self.oc_person)

        if isinstance(account_list, list):
            for account in account_list:
                name_filtering_counter += 1
                name_filtering_str += "(%s=%s)" % (self.sAMAccountName, account)

        if isinstance(name_list, list):
            for name in name_list:
                name_filtering_counter += 1
                name_filtering_str += "(%s=%s)" % (self.cn, name)

        if name_filtering_counter > 1:
            name_filtering_str = "(|" + name_filtering_str + ")"
        if name_filtering_counter > 0:
            final_filtering_str = "(&%s%s)" % (name_filtering_str, object_filtering_str)
        else:
            final_filtering_str = object_filtering_str

        targets = {}

        query_success = self.conn.search(
            search_base=self.search_base,
            attributes=attribute_list,
            search_filter=final_filtering_str,
        )

        if query_success:
            for entry in self.conn.entries:
                if (not active_user_only) or (entry.userAccountControl != 66050 and entry.userAccountControl != 514):
                    # Building NKAdUser
                    user = NKAd.NKAdUser()
                    user.person = entry
                    for ou in ad_ous:
                        if ou in str(entry.distinguishedName):
                            user.ous.append(ou)
                    for group in ad_groups:
                        if group in str(entry.memberOf):
                            user.groups.append(group)

                    # Filtering Groups and OU
                    valid_entry = False
                    if group_list or ou_list:
                        if group_list:
                            for group in group_list:
                                if group in user.groups:
                                    valid_entry = True
                                    break
                        if not valid_entry and ou_list:
                            for ou in ou_list:
                                if ou in user.ous:
                                    valid_entry = True
                    else:
                        valid_entry = True

                    if valid_entry:
                        targets[str(entry.sAMAccountName)] = user

        return targets

    @classmethod
    def get_default_attributes(cls):
        return [cls.dn, cls.sAMAccountName, cls.cn, cls.sn, cls.givenName, cls.lastLogon, cls.accountExpires,
                cls.memberOf, cls.userAccountControl]
