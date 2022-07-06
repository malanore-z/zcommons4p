from typing import Union, Sequence


KeyType = Union[str, Sequence[str]]


class ConfigDict(dict):

    """
    A dict subclass for config.
    For example:
        config_dict = ConfigDict()
        config_dict["a.b.c1"] = "v1"
        config_dict["a.b.c2"] = "v2"
        config_dict["a.b.c.d1"] = 1
        assert(config_dict["a"]["b"]["c1"] == "v1")
    """

    def __init__(self, d: dict = None):
        super(ConfigDict, self).__init__()
        self.__d = {}
        if d is None:
            d = {}
        for k, v in d.items():
            if isinstance(v, dict):
                self.__d[k] = ConfigDict(v)
            else:
                self.__d[k] = v

    def exists(self, __key, include_dict=False):
        """
        whether __key exists.

        :param __key:
        :param include_dict: whether include config dict, e.g. "a.b.c" and "a.b.d" exists, the value of "a.b" is config
            dict, if include_dict is False, exists("a.b") returns False.
        :return:
        """
        return self.__exists(__key, include_dict=include_dict)

    def get(self, __key, __default=None):
        """
        get the value of key

        :param __key:
        :param __default:
        :return:
        """
        return self.__get(__key, default=__default)

    def put_if_absent(self, __key, __value):
        """
        put (__key, __value) if __key not exists.

        :param __key:
        :param __value:
        :return:
        """
        self.__put(__key, __value, overwrite=False)

    def remove(self, __key, include_dict=False, strict=True):
        """
        remove __key

        :param __key:
        :param include_dict: whether remove batch values if the value of __key is config dict
        :param strict: if raise exceptions when __key not found
        :return:
        """
        self.__del(__key, include_dict, strict)

    def __contains__(self, __key):
        return self.__exists(__key, include_dict=False)

    def __setitem__(self, __key, value):
        self.__put(__key, value, overwrite=True)

    def __getitem__(self, __key):
        return self.__get(__key)

    def __delitem__(self, __key):
        self.__del(__key, include_dict=False, strict=True)

    def keys(self):
        all_keys = []

        def __cat_keys(__config_dict, __key_seq):
            for k, v in __config_dict.__d.items():
                __key_seq.append(k)
                if isinstance(v, ConfigDict):
                    __cat_keys(v, __key_seq)
                else:
                    all_keys.append(".".join(__key_seq))
                del __key_seq[len(__key_seq) - 1]

        __cat_keys(self, [])
        all_keys.sort()
        return all_keys

    def items(self):
        __keys = self.keys()
        __items = []
        for k in __keys:
            __items.append((k, self.get(k)))
        return __items

    def __get(self, key, **kwargs):
        key_seq = self.__split_key(key)
        try:
            return self.__get_impl(key_seq)
        except KeyError:
            if "default" in kwargs:
                return kwargs["default"]
            else:
                raise KeyError(key)

    def __put(self, key, value, overwrite=True):
        key_seq = self.__split_key(key)
        try:
            self.__put_impl(key_seq, value, overwrite)
        except KeyError:
            raise KeyError(f"already exists a prefix key of {key}")

    def __exists(self, key, include_dict):
        try:
            v = self[key]
            if include_dict or not isinstance(v, ConfigDict):
                return True
            else:
                return False
        except KeyError:
            return False

    def __del(self, key, include_dict=False, strict=True):
        key_seq = self.__split_key(key)
        try:
            self.__del_impl(key_seq, include_dict)
        except KeyError:
            if strict:
                raise KeyError(key)

    def __get_impl(self, key_seq):
        if len(key_seq) == 1:
            return self.__d[key_seq[0]]
        v = self.__d[key_seq[0]]
        if not isinstance(v, ConfigDict):
            raise KeyError()
        return v.__get_impl(key_seq[1:])

    def __put_impl(self, key_seq, value, overwrite):
        if len(key_seq) == 1:
            if overwrite or key_seq[0] not in self.__d:
                self.__d[key_seq[0]] = value
            return
        if key_seq[0] not in self.__d:
            self.__d[key_seq[0]] = ConfigDict()
        v = self.__d[key_seq[0]]
        if not isinstance(v, ConfigDict):
            raise KeyError()
        v.__put_impl(key_seq[1:], value, overwrite)

    def __del_impl(self, key_seq, include_dict):
        if len(key_seq) == 1:
            if key_seq[0] in self.__d:
                if not include_dict and isinstance(self.__d[key_seq[0]], ConfigDict):
                    raise KeyError()
            return
        v = self.__d[key_seq[0]]
        if not isinstance(v, ConfigDict):
            raise KeyError()
        v.__del_impl(key_seq[1:], include_dict)

    @classmethod
    def __split_key(cls, key: str):
        if key is None or not isinstance(key, str) or key == "":
            raise KeyError(f"key must be str and not empty")
        return key.split(".")


if __name__ == '__main__':
    cd = ConfigDict({})
    q = cd["qwe"]
    cd["asd"] = "sad"
