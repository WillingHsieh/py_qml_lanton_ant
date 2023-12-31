# This Python file uses the following encoding: utf-8
import sys
from pathlib import Path
from PySide6.QtCore import QObject, Slot, Signal, Property
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType
import random

from ant import *
from db import *

class Cells(QObject):
    def __init__(self):
        super().__init__()

        # ==== 設定參數 ====

        self.__rows = 11
        self.__cols = 11
        self.__len = 59

        self.__rows = 51
        self.__cols = 51
        self.__len = 20

        # self.__rows = 111
        # self.__cols = 111
        # self.__len = 9

        # 格子總數
        self.__count = self.__rows * self.__cols

        # 初始化 data/data_next
        self.__data = [ False for i in range( self.__count)]
        self.__data_next = [ False for i in range( self.__count)]

        # 初始化 鄰居查表
        self.__data_nbs = []
        for i in range(self.__count):
            self.__data_nbs.append( self.get_around_nbs(i))

        # 資料庫以及地圖名稱列表
        self.__db = DB()
        self.__maps_name = self.__db.get_name_list()
        self._maps_name_changed.emit( self.__maps_name)

        # 螞蟻
        self.ant = Ant( self)
        print( "init...end")

    # ==== 計算結果的緩存 ====

    __data_next = []
    def data_next_clear(self):
        for idx in range( self.__count):
            self.__data_next[ idx] = False

    # data_next 回存到 data
    def restore_data(self):
        for idx in range( self.__count):
            val = self.__data_next[ idx]
            self.set_data( idx, val)

    # ==== 座標換算/查表 ====

    def get_row_col(self, idx):
        row = idx // self.__cols
        col = idx % self.__cols
        return row, col

    def get_idx(self, row, col):
        return row * self.__cols + col

    # 上 右 下 左 為 0, 1, 2 ,3
    def get_around_nbs(self, idx):
        nbs = []
        row, col = self.get_row_col(idx)
        left  = ( col - 1 + self.__cols ) % self.__cols
        right = ( col + 1               ) % self.__cols
        up   = ( row - 1 + self.__rows ) % self.__rows
        down  = ( row + 1               ) % self.__rows
        nbs_row_cols = (
            ( up,  col),    # 上
            ( row,  right), # 右
            ( down, col),   # 下
            ( row,  left),  # 左
            ( up,  left),
            ( up,  right),
            ( down, left),
            ( down, right)
        )
        for ( r, c) in nbs_row_cols:
            nbs.append( self.get_idx( r, c))
        return nbs

    # 高度
    def get_rows(self):
        return self.__rows
    _rows_changed = Signal(int)
    rows = Property(int, get_rows, notify=_rows_changed)

    # 寬度
    def get_cols(self):
        return self.__cols
    _cols_changed = Signal(int)
    cols = Property(int, get_cols, notify=_cols_changed)

    # 格子大小
    def get_len(self):
        return self.__len
    _len_changed = Signal( int)
    len = Property( int, get_len, notify=_len_changed)

    # ==== 地圖 ====

    def get_maps_name(self):
        return self.__maps_name
    _maps_name_changed = Signal(list)
    maps_name = Property(list, get_maps_name, notify=_maps_name_changed)

    # 將地圖存回 data
    def restore_map(self, list_map):
        self.data_clear()
        for ( r, c) in list_map:
            self.set_data( self.get_idx( r, c), True)

    @Slot( str)
    def load_map(self, str_name):
        print( "str_name:", str_name)
        list_map = self.__db.get_map( str_name)
        # print( "list_map:", list_map)
        self.restore_map( list_map)

    @Slot( str)
    def save_map(self, str_name):
        # print( str_name)

        # 存入資料庫
        map_data = []
        for i in range( self.__count):
            if self.__data[ i]:
                map_data.append( self.get_row_col( i))
        str_map = str( map_data)
        # print( str_map)
        self.__db.insert_data(str_name, str_map)

        self.__maps_name = self.__db.get_name_list()
        self._maps_name_changed.emit(self.__maps_name)

    @Slot( str)
    def del_map(self, str_name):
        # print( str_name)
        self.__db.del_data( str_name)

        self.__maps_name = self.__db.get_name_list()
        self._maps_name_changed.emit(self.__maps_name)

    # ==== 對應到 UI 的陣列 ====

    def get_data(self):
        return self.__data
    _data_changed = Signal( list)
    data = Property(list, get_data, notify=_data_changed)

    def is_data_true(self, idx):
        return self.__data[ idx]

    # 設定單一格子，會響應到 UI
    @Slot( int, bool)
    def set_data(self, idx, val):
        if self.__data[ idx] != val:
            self.__data[idx] = val
            self._cell_changed.emit( idx, val)
    _cell_changed = Signal( int, bool)

    # ==== 按鈕對應功能 ====

    @Slot( int)
    def load_random(self, percent):
        list_len = int(self.__count * percent / 100)
        print( "list_len:", list_len)

        list_pos = set()
        while len(list_pos) < list_len:
            list_pos.add( random.randint(0, self.__count-1))
        print( len(list_pos), list_pos)

        for ii in list_pos:
            self.set_data( ii, True)

    @Slot()
    def data_clear(self):
        for idx in range( self.__count):
            self.set_data( idx, False)

    # 螞蟻的計時器
    def get_ant_ti(self):
        return self.ant.get_ti_ms()
    ant_ti_changed = Signal( int)
    ant_ti = Property( int, get_ant_ti, notify=ant_ti_changed)

    # 螞蟻的位置
    def get_ant_pos(self):
        return self.ant.get_idx( )
    ant_pos_changed = Signal( int)
    ant_pos = Property( int, get_ant_pos, notify=ant_pos_changed)

    # 螞蟻的方向
    def get_ant_way(self):
        return self.ant.get_way( )
    ant_way_changed = Signal( int)
    ant_way = Property( int, get_ant_way, notify=ant_way_changed)

    # 跌代
    @Slot()
    def step(self):
        self.ant.step()

    @Slot()
    def stop(self):
        self.ant.stop()

    @Slot()
    def begin(self):
        # print( "begin()...")
        self.ant.begin()

    @Slot()
    def speed_up(self):
        self.ant.speed_up()

    @Slot()
    def speed_down(self):
        self.ant.speed_down()

    # ==== 平移 ====

    def shift_way(self, way):

        # 計算結果存放到 __data_next
        self.data_next_clear()
        for i in range( self.__count):
            if self.__data[ i]:
                idx_next = self.__data_nbs[ i][ way]
                self.__data_next[ idx_next] = True
        self.restore_data()

    @Slot()
    def shift_up(self):
        self.shift_way(Ways.up)
        self.ant.move_up()

    @Slot()
    def shift_down(self):
        self.shift_way( Ways.down)
        self.ant.move_down()

    @Slot()
    def shift_left(self):
        self.shift_way(Ways.left)
        self.ant.move_left()

    @Slot()
    def shift_right(self):
        self.shift_way( Ways.right)
        self.ant.move_right()

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    qmlRegisterType( Cells, 'Cells', 1, 0, 'Cells')

    qml_file = Path(__file__).resolve().parent / "main.qml"
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
