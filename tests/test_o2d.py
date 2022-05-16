import unittest
from dataclasses import dataclass, field
from typing import List, Tuple


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
class Sample:

    first: str
    second: str = field(init=False)
    third: str = field(default="third", init=False)

    def __post_init__(self):
        self.second = "second"


class O2dTest(unittest.TestCase):

    def test_base(self):
        self.assertEqual(zcommons.o2d.asdict(123), 123)
        self.assertEqual(zcommons.o2d.asdict([1, 2, 3]), [1, 2, 3])
        self.assertEqual(zcommons.o2d.asdict({'a': 1, 'b': 2}), {'a': 1, 'b': 2})
        self.assertEqual(zcommons.o2d.asobj(int, "123"), 123)
        self.assertEqual(zcommons.o2d.asobj(Tuple[int], [1, 2, 3]), (1, 2, 3))

    def test_dataclass(self):
        c1 = Chapter("first", 2, 2000)
        c1d = zcommons.o2d.asdict(c1)
        self.assertEqual(c1d, {"name": "first", "npages": 2, "nwords": 2000})
        c1_rec = zcommons.o2d.asobj(Chapter, c1d)
        self.assertEqual(c1, c1_rec)

        c2 = Chapter("second", 3, 1000)
        c2d = zcommons.o2d.asdict(c2)
        b1 = Book("book1", "author1", [c1, c2])
        b1d = zcommons.o2d.asdict(b1)
        self.assertEqual(b1d, {"name": "book1", "author": "author1", "chapters": [c1d, c2d], "nwords": 3000})
        b1_rec = zcommons.o2d.asobj(Book, b1d)
        self.assertEqual(b1, b1_rec)

    def test_no_init(self):
        s1 = Sample("first")
        s1d = zcommons.o2d.asdict(s1)
        self.assertEqual(s1d, {"first": "first", "second": "second", "third": "third"})
        s1.first = "first-1"
        s1.second = "second-1"
        s1.third = "third-1"
        s1d = zcommons.o2d.asdict(s1)
        self.assertEqual(s1d, {"first": "first-1", "second": "second-1", "third": "third-1"})
        s1_rec = zcommons.o2d.asobj(Sample, s1d)
        self.assertEqual(s1, s1_rec)
