import argparse
import sys

import tests


def parse_args():
    parser = argparse.ArgumentParser(description="zcommons test")

    parser.add_argument("--force-site", action="store_true", help="force test sources in site-packages")
    parser.add_argument("--force-src", action="store_true", help="force test sources in the same project directory")
    parser.add_argument("--exclude-counter", action="store_true", help="exclude counter tests for less time consumption")

    return parser.parse_args()


args = parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.force_site:
        tests.force_site_package()
    if args.force_src:
        tests.force_src_package()


import unittest


if not args.exclude_counter:
    from .test_counter import *
from .test_o2d import *
from .test_threadgroup import *


unittest.main(argv=sys.argv[0:1], verbosity=2)
