import enum
import unittest
from dataclasses import dataclass, field
from typing import List, Tuple

import zcommons as zc


@dataclass()
class Chapter:

    name: str
    npages: int
    nwords: int


@dataclass()
class Book:

    name: str
    author: str
    chapters: List[Chapter] = field(default_factory=lambda: [])
    nwords: int = field(init=False)

    def __post_init__(self):
        self.nwords = 0
        for c in self.chapters:
            self.nwords += c.nwords


@dataclass()
class Sample(zc.dataclass.DataMixin):

    first: str
    second: str = field(init=False)
    third: str = field(default="third", init=False)

    def __post_init__(self):
        self.second = "second"


@dataclass()
class ByteDemo:

    id: str
    data: bytes


class Color(enum.Enum):

    RED = "red"
    GREEN = "green"
    BLUE = "blue"


@dataclass()
class ComplexDemo(zc.dataclass.DataMixin):

    color: Color
    data: bytes
    s: str
    i: int

    def to_json_dict(self) -> dict:
        return {
            "color": self.color.value,
            "data": zc.dataclass.bytes_encode(self.data, "hex"),
            "s": self.s,
            "i": self.i
        }

    @classmethod
    def from_json_dict(cls, json_dict: dict) -> "ComplexDemo":
        return ComplexDemo(
            Color(json_dict["color"]),
            zc.dataclass.bytes_decode(json_dict["data"], "hex"),
            json_dict["s"],
            json_dict["i"]
        )


class O2dTest(unittest.TestCase):

    def test_base(self):
        self.assertEqual(zc.dataclass.asdict(123), 123)
        self.assertEqual(zc.dataclass.asdict([1, 2, 3]), [1, 2, 3])
        self.assertEqual(zc.dataclass.asdict({'a': 1, 'b': 2}), {'a': 1, 'b': 2})
        self.assertEqual(zc.dataclass.asobj(int, "123"), 123)
        self.assertEqual(zc.dataclass.asobj(Tuple[int], [1, 2, 3]), (1, 2, 3))

    def test_dataclass(self):
        c1 = Chapter("first", 2, 2000)
        c1d = zc.dataclass.asdict(c1)
        self.assertEqual(c1d, {"name": "first", "npages": 2, "nwords": 2000})
        c1_rec = zc.dataclass.asobj(Chapter, c1d)
        self.assertEqual(c1, c1_rec)

        c2 = Chapter("second", 3, 1000)
        c2d = zc.dataclass.asdict(c2)
        b1 = Book("book1", "author1", [c1, c2])
        b1d = zc.dataclass.asdict(b1)
        self.assertEqual(b1d, {"name": "book1", "author": "author1", "chapters": [c1d, c2d], "nwords": 3000})
        b1_rec = zc.dataclass.asobj(Book, b1d)
        self.assertEqual(b1, b1_rec)

    def test_no_init(self):
        s1 = Sample("first")
        s1d = zc.dataclass.asdict(s1)
        self.assertDictEqual(s1d, {"first": "first", "second": "second", "third": "third"})
        self.assertDictEqual(s1d, s1.to_json_dict())
        s1.first = "first-1"
        s1.second = "second-1"
        s1.third = "third-1"
        s1d = zc.dataclass.asdict(s1)
        self.assertEqual(s1d, {"first": "first-1", "second": "second-1", "third": "third-1"})
        s1_rec = zc.dataclass.asobj(Sample, s1d)
        self.assertEqual(s1, s1_rec)

    def test_bytes(self):
        bd1 = ByteDemo("q", b"wert")
        bd1d = zc.dataclass.asdict(bd1)
        self.assertEqual(bd1d, {"id": "q", "data": b"wert"})
        bd1_rec = zc.dataclass.asobj(ByteDemo, bd1d)
        self.assertEqual(bd1, bd1_rec)

    def test_none(self):
        c = Chapter(name="first", npages=None, nwords=None)
        cd = zc.dataclass.asdict(c)
        self.assertEqual(cd, {"name": "first", "npages": None, "nwords": None})
        c_rec = zc.dataclass.asobj(Chapter, cd)
        self.assertEqual(c, c_rec)

    def test_complex(self):
        c1 = ComplexDemo(Color.RED, b"data", "str", 1)
        self.assertDictEqual(c1.to_json_dict(), {
            "color": "red",
            "data": "64617461",
            "s": "str",
            "i": 1
        })
        c2 = ComplexDemo.from_json_dict(c1.to_json_dict())
        self.assertEqual(c1, c2)
