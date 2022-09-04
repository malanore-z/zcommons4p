__all__ = [
    "asdict",
    "asobj",
    "DataMixin",
    "BytesEncoderMgr",
    "BytesEncoder",
    "bytes_encode",
    "bytes_decode"
]

import abc
import base64
import dataclasses
import json
import sys
import typing


_BUILTIN_BASE_TYPES = [type(None), bool, int, float, str, bytes]
_BUILTIN_CONTAIN_TYPES = [tuple, list, set, dict]


def asdict(obj, *, dict_factory=dict):
    """
    Convert object to dict.
    If the type of ``object`` is built-in types, the type of return value is same with the type of ``object``.

    :param obj: the object of built-in types or custom class with ``dataclass`` decorator.
    :param dict_factory:  the real type of return dict.
    :return:
    """
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj, dict_factory=dict_factory)
    # return itself directly if obj is base type
    if type(obj) in _BUILTIN_BASE_TYPES:
        return obj
    # traverse container and check the sameness of elements in container
    if type(obj) in _BUILTIN_CONTAIN_TYPES:
        key_type, val_type = None, None
        if type(obj) is dict:
            ret = dict_factory()
            for k, v in obj.items():
                if key_type is None:
                    key_type, val_type = type(k), type(v)
                else:
                    if key_type != type(k) or val_type != type(v):
                        raise TypeError(f"asdict() should be called on container with the same element type")

                ret[asdict(k)] = asdict(v)
            return ret
        else:
            ret = []
            for k in obj:
                if key_type is None:
                    key_type = type(k)
                else:
                    if key_type != type(k):
                        raise TypeError(f"asdict() should be called on container with the same element type")

                ret.append(asdict(k))
            return type(obj)(ret)


def asobj(_cls, d):
    """
    Construct object from dict.

    :param _cls: the type of return value.
    :param d: the data dict.
    :return: a object of ``_cls``
    """
    if d is None:
        return None
    if not isinstance(_cls, type) and not _is_typing(_cls):
        raise TypeError(f"asobj() should be called on type")
    if dataclasses.is_dataclass(_cls):
        init_params = {}
        set_attrs = {}

        for f in getattr(_cls, dataclasses._FIELDS).values():
            # Only consider normal fields
            if f._field_type in [dataclasses._FIELD_CLASSVAR, dataclasses._FIELD_INITVAR]:
                continue

            v = None
            if f.name in d:
                v = asobj(f.type, d[f.name])
            else:
                if f.default is dataclasses._MISSING_TYPE and f.default_factory is dataclasses._MISSING_TYPE:
                    raise ValueError(f"Field {f.name} is required, but its value is missing")

            if f.init:
                init_params[f.name] = v
            else:
                set_attrs[f.name] = v

        ret = _cls(**init_params)
        for k, v in set_attrs.items():
            setattr(ret, k, v)
        return ret

    if _is_typing(_cls):
        if _cls is typing.Any:
            return d
        if _cls.__dict__["__args__"] is None:
            raise TypeError(f"asobj() should be called on container which specified element type")
        orig_base = _origin(_cls)
        if orig_base is dict:
            key_type, val_type = _cls.__dict__["__args__"]
            if type(d) is not dict:
                raise TypeError(f"the type of d is not {_cls}")
            ret = dict()
            for k, v in d.items():
                ret[asobj(key_type, k)] = asobj(val_type, v)
            return ret
        if orig_base in [tuple, list, set]:
            key_type, = _cls.__dict__["__args__"]
            ret = []
            # let it raises
            for k in d:
                ret.append(asobj(key_type, k))
            return orig_base(ret)

    if _cls in _BUILTIN_BASE_TYPES:
        return _cls(d)

    if _cls in _BUILTIN_CONTAIN_TYPES:
        raise TypeError(f"asobj() should be called on container which specified element type")
    raise TypeError(f"unsupport type {_cls}")


def __py36_is_typing(_cls):
    from typing import GenericMeta
    return isinstance(_cls, GenericMeta)


def __py37_is_typing(_cls):
    from typing import _Final
    return isinstance(_cls, _Final)


def __py36_origin(_cls):
    return _cls.__dict__["__extra__"]


def __py37_origin(_cls):
    return _cls.__dict__["__origin__"]


if sys.version_info.minor > 6:
    _is_typing = __py37_is_typing
    _origin = __py37_origin
else:
    _is_typing = __py36_is_typing
    _origin = __py36_origin


def _is_typing_container(_cls):
    return _is_typing(_cls) and _origin(_cls) in _BUILTIN_CONTAIN_TYPES


class DataMixin:

    def to_json_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent=4) -> str:
        return json.dumps(self.to_json_dict(), indent=indent)

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> "DataMixin":
        return asobj(cls, json_dict)

    @classmethod
    def from_json(cls, json_str: str) -> "DataMixin":
        json_dict = json.loads(json_str)
        return asobj(cls, json_dict)


class BytesEncoder:

    @abc.abstractmethod
    def encode(self, b: bytes):
        pass

    @abc.abstractmethod
    def decode(self, s) -> bytes:
        pass


class BytesEncoderMgr:

    __bytes_encoders = {}

    @classmethod
    def add_encoder(cls, encoding, encoder):
        if encoding in cls.__bytes_encoders:
            raise ValueError(f"{encoding} already exists.")
        if not isinstance(encoder, BytesEncoder):
            raise ValueError(f"encoder must be an instance of BytesEncoder's subclass")
        cls.__bytes_encoders[encoding] = encoder

    @classmethod
    def del_encoder(cls, encoding):
        if encoding in cls.__bytes_encoders:
            del cls.__bytes_encoders[encoding]

    @classmethod
    def get_encoder(cls, encoding):
        if encoding not in cls.__bytes_encoders:
            raise ValueError(f"{encoding} not be registered")
        return cls.__bytes_encoders[encoding]

    @classmethod
    def exists_encoder(cls, encoding):
        return encoding in cls.__bytes_encoders

    @classmethod
    def encodings(cls):
        return list(cls.__bytes_encoders.keys())


class _HexEncoder(BytesEncoder):

    def encode(self, b: bytes):
        return b.hex()

    def decode(self, s) -> bytes:
        return bytes.fromhex(s)


class _Base64Encoder(BytesEncoder):

    def encode(self, b: bytes):
        return base64.b64encode(b).decode("ascii")

    def decode(self, s) -> bytes:
        return base64.b64decode(s)


BytesEncoderMgr.add_encoder("hex", _HexEncoder())
BytesEncoderMgr.add_encoder("base64", _Base64Encoder())


def bytes_encode(b: bytes, encoding: str = "base64"):
    encoder = BytesEncoderMgr.get_encoder(encoding)
    return encoder.encode(b)


def bytes_decode(s, encoding: str = "base64"):
    encoder = BytesEncoderMgr.get_encoder(encoding)
    return encoder.decode(s)


