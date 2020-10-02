from datetime import datetime as dt


class Now:

    @staticmethod
    def time():
        pass

    @staticmethod
    def hj():
        return dt.now().day

    @staticmethod
    def m():
        return dt.now().month

    @staticmethod
    def y():
        return dt.now().year
