from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
import sys


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TK Window")
        self.resize(1200, 800)

        v_box = QtWidgets.QVBoxLayout(self)
        # v_box.addStretch()
        self.grid_add = QtWidgets.QGridLayout()
        v_box.addLayout(self.grid_add)
        self.v_box = v_box

        generator_unpacking = self.el_grid_setting(1, 0, 1, 1, mt=1, start_row=0)
        generator_unpacking = list(generator_unpacking)[0]
        self.bt = self.add_el(QPushButton(), *generator_unpacking)

        for e, el_grid in enumerate(self.el_grid_setting(10, 10, mt=2, start_row=0, start_col=1)):

            sh_ui_name = str(e)
            sh_ui_nowbt = QPushButton(sh_ui_name)
            # new == sh_ui_nowbt
            new = self.add_el(sh_ui_nowbt, *el_grid)
            new.clicked.connect(lambda: print('teste'))


    def el_grid_setting(self, row: int, col: int, rp=1, cp=1, mt=0, start_row=0, start_col=0):
        """
        :param row: till row
        :param col: till col
        :param rp: row_span
        :param cp: col_span
        :param start_row: where (row) would you like to start?
        :param start_col: ...

        :param mt: 0 -> line increment, 1 -> col increment, 2 -> both increment

        :return: generator with all equal sized for grid
        """
        if mt > 2:
            mt = 0

        range_row = row + start_row
        range_col = col + start_col

        from itertools import zip_longest
        if mt == 0:
            # line increment
            for r, c, rs, cs in zip_longest(range(start_row, range_row), f'{col}' * row,
                                            range(rp, rp + 1), range(cp, cp + 1), fillvalue=1):
                tup = int(r), int(c), int(rs), int(cs)
                # print(tup)
                yield tup
        elif mt == 1:
            # col increment
            for r, c, rs, cs in zip_longest(f'{row}' * col, range(start_col, range_col),
                                            range(rp, rp + 1), range(cp, cp + 1), fillvalue=1):
                tup = int(r), int(c), int(rs), int(cs)
                # print(tup)
                yield tup
        elif mt == 2:
            # both increment
            for r in range(0, row):
                for c in range(0, col):
                    # print('col')
                    for rs, cs in zip(range(rp, rp + 1), range(cp, cp + 1)):
                        tup = int(r), int(c), int(rs), int(cs)
                        yield tup

    def add_el(self, el, row: int, col: int, rowspan: int, colspan: int, style=None, obj_name=None, **kwargs):
        """
        :param el: any PyQt5 element like button etc
        :param row: grid
        :param col: grid
        :param rowspan: grid
        :param colspan: grid
        :param style: style
        :param obj_name:
        :param kwargs: set new property [idk if is working yet]
        :return:
        """
        self.grid_add.addWidget(el, row, col, rowspan, colspan)
        # only clickable functions
        # no clicked anymore
        # el.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        if style:
            el.setStyleSheet(style)
        if kwargs:
            for k, v in kwargs.items():

                el.setProperty(str(k), str(v))
                # print(str(k), str(v))
        if obj_name is not None:
            el.setObjectName(obj_name)

        return el


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet(style_sheet)
    exe = App()
    exe.show()
    app.exec_()
