

src_used = False
src_path = None


def add_src_path():
    global src_used, src_path
    if src_used:
        return

    import os
    import sys
    src_used = True
    src_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
    sys.path.insert(0, src_path)


def del_src_path():
    global src_used, src_path
    if not src_used:
        return

    import sys
    src_used = False
    for i in range(len(sys.path)):
        if src_path == sys.path[i]:
            del sys.path[i]
            break


def force_src_package():
    add_src_path()

    import importlib
    import zcommons

    importlib.reload(zcommons)


def force_site_package():
    del_src_path()

    import importlib
    import zcommons

    importlib.reload(zcommons)


try:
    import zcommons
except:
    force_src_package()
