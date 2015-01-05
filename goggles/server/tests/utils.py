# https://gist.github.com/NotSqrt/5f3c76cd15e40ef62d09


# Disable migrations for when runnings tests, shaves 10s off of each test.
class DisableMigrations(object):

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return "notmigrations"
