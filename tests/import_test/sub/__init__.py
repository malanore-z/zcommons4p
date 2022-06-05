
class Outer(object):

    class Inner(object):

        def __init__(self):
            super(Outer.Inner, self).__init__()

        def check(self):
            return True

    def __init__(self):
        super(Outer, self).__init__()
