
class A:
    def __init__(self):

        self.test()

    def test(self):
        return 'test'


class B(A):
    def me(self):
        self.test()

