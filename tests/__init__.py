from .test_automate import * # noqa
from .test_validate import * # noqa
from .test_db_helper import * # noqa


def main():
    import unittest
    testsuite = unittest.TestLoader().discover('.')
    unittest.TextTestRunner(verbosity=1).run(testsuite)


if __name__ == '__main__':
    main()
