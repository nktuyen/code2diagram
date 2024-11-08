"""Imports"""
#System imports
import os
import enum
#Project imports
from task.walking_task import WalkingTask
from option.print_option import PrintOption
from model.directory_model import DirectoryModel
from model.io_model import IoModel, IoType
from model.file_model import FileModel
from model.symlink_model import SymLinkModel
from model.directory_model import DirectoryModel

COLUMN_NAME_INDEX: str = "#"
COLUMN_NAME_NAME: str = "Name"
COLUMN_NAME_TYPE: str = "Type"
COLUMN_NAME_SIZE: str = "Size"
COLUMN_NAME_EXTENSION: str = "Extension"
COLUMN_NAME_REMARK: str = "Remark"

S_comma: str = ","
S_semicolon: str = ";"
S_colon: str = ":"
S_newline: str = "\n"
S_tab: str = "\t"
S_dot: str = "."
S_space: str = " "
S_vertical_bar: str = "|"
S_underscrore: str = "_"
S_minus: str = "-"
S_plus: str = "+"

class Alignment(enum.IntEnum):
    """class Alignment"""
    LEFT = 0
    CENTER = 1
    RIGHT = 2

class Column:
    """class Column"""
    def __init__(self, name: str = '', index: int = 0, width: int = 0, align: Alignment = Alignment.LEFT):
        self._name: str = name
        self._index: int = index
        self._width: int = width
        self._align: Alignment = align
        self._visible: bool = False
        self._initial_width: int = width

    def __str__(self):
        return self.name
    
    @property
    def name(self) -> str:
        return self._name
    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def index(self) -> int:
        return self._index

    @property
    def initial_width(self) -> int:
        return self._initial_width

    @property
    def width(self) -> int:
        return self._width
    @width.setter
    def width(self, value: int):
        self._width = value

    @property
    def align(self) -> Alignment:
        return self._align
    @align.setter
    def align(self, value: Alignment):
        self._align = value
    
    @property
    def visible(self) -> bool:
        return self._visible
    @visible.setter
    def visible(self, value: bool) -> None:
        self._visible = value
    

class Cell:
    def __init__(self, value: str = "", row = None, column: Column = None):
        self._value: str = value
        self._row = row
        self._column: Column = column

    def __str__(self):
        return self._value
    
    @property
    def value(self) -> str:
        return self._value
    @value.setter
    def value(self, value: str):
        self._value = value
    
    @property
    def row(self):
        return self._row
    
    @property
    def column(self) -> Column:
        return self._column


class Row:
    def __init__(self, index: int, tag: IoModel = None):
        self._index: int = index
        self._cells: list = []
        self._tag: IoModel = tag

    def __str__(self):
        return f"Row(index={self.index},cells.count={len(self.cells)})"
    
    @property
    def index(self) -> int:
        return self._index
    @index.setter
    def index(self, index: int):
        self._index = index
    
    @property
    def cells(self) -> list:
        return self._cells
    
    @property
    def tag(self) -> IoModel:
        return self._tag
    @tag.setter
    def tag(self, value: IoModel):
        self._tag = value


class PrintTask(WalkingTask):
    def __init__(self, name: str = '', desc: str = '') -> None:
        super().__init__(name, desc, PrintOption())
        self._directory: DirectoryModel = None
        self._depth_separator: str = ' '
        self._column_separator: str = "|"
        self._columns: dict = {
            COLUMN_NAME_INDEX: Column(COLUMN_NAME_INDEX, 0, 0, Alignment.RIGHT),
            COLUMN_NAME_NAME : Column(COLUMN_NAME_NAME, 1),
            COLUMN_NAME_TYPE : Column(COLUMN_NAME_TYPE, 2),
            COLUMN_NAME_SIZE : Column(COLUMN_NAME_SIZE, 3),
            COLUMN_NAME_EXTENSION : Column(COLUMN_NAME_EXTENSION, 4),
            COLUMN_NAME_REMARK : Column(COLUMN_NAME_REMARK, 5)
        }
        self._rows: list = []
        self._header_row: Row = Row(-1)
        self._header_row.cells.append(Cell(self.index_column.name, self._header_row, self.index_column))
        self._header_row.cells.append(Cell(self.name_column.name, self._header_row, self.name_column))
        self._header_row.cells.append(Cell(self.type_column.name, self._header_row, self.type_column))
        self._header_row.cells.append(Cell(self.size_column.name, self._header_row, self.size_column))
        self._header_row.cells.append(Cell(self.extension_column.name, self._header_row, self.extension_column))
        self._header_row.cells.append(Cell(self.remark_column.name, self._header_row, self.remark_column))

    @property
    def option(self) -> PrintOption:
        return self._option

    @property
    def directory(self) -> DirectoryModel:
        return self._directory
    
    @property
    def columns(self) -> dict:
        return self._columns
    
    @property
    def rows(self) -> list:
        return self._rows
    
    @property
    def header_row(self) -> Row:
        return self._header_row

    @property
    def index_column(self) -> Column:
        """Property index_column"""
        return self.columns[COLUMN_NAME_INDEX]

    @property
    def name_column(self) -> Column:
        """Property name_column"""
        return self.columns[COLUMN_NAME_NAME]
    
    @property
    def type_column(self) -> Column:
        """Property type_column"""
        return self.columns[COLUMN_NAME_TYPE]
    
    @property
    def size_column(self) -> Column:
        """Property size_column"""
        return self.columns[COLUMN_NAME_SIZE]
    
    @property
    def extension_column(self) -> Column:
        """Property extension_column"""
        return self.columns[COLUMN_NAME_EXTENSION]
    
    @property
    def remark_column(self) -> Column:
        """Property remark_column"""
        return self.columns[COLUMN_NAME_REMARK]

    def column(self, index_or_name) -> Column:
        """Method column"""
        if isinstance(index_or_name, int):
            for col in self._columns.values():
                if col.index == int(index_or_name):
                    return col
        elif isinstance(index_or_name, str):
            return self._columns[index_or_name]
        return None

    def row(self, index: int) -> Row:
        """Method row"""
        if index >= len(self._rows):
            return None
        return self._rows[index]

    def cell(self, column, row: int) -> Cell:
        col_index: int = 0
        if isinstance(column, int):
            col_index = column
        else:
            col_name: str = column
            col_index = self.column(col_name).index
        row_obj: Row = self._rows[row]
        return row_obj.cells[col_index]
    
    def _pre_parse_args(self, parser):
        super()._pre_parse_args(parser)

        parser.add_option("-o", "--output-file", default=None, help="Support excel(.xls,.xlsx), csv(.csv) and text format")
        parser.add_option("", "--indent", default=1, help="Number of spaces use to indent children. 0 means no indent")
        parser.add_option("", "--no-header", action="store_false", help="Do not print header row")
    
    def _post_parse_args(self, opts, args) -> bool:
        if not super()._post_parse_args(opts, args):
            return False
        
        if opts is not None:
            if opts.output_file is not None:
                self.option.output_file = opts.output_file
                if self.option.output_file.lower().endswith(".xlsx") or self.option.output_file.lower().endswith(".xls"):
                    try:
                        import xlsxwriter as writer
                    except Exception as ex:
                        if isinstance(ex, ModuleNotFoundError):
                            print("[E]Cannot print to excel file because xlsxwriter module is not installed")
                            return False
            if opts.indent is not None:
                try:
                    self.option.indent = int(opts.indent)
                except:
                    self.option.indent = 0
            if opts.no_header is not None:
                self.option.header = False
            else:
                self.option.header = True
        return True

    def _pre_run(self, args = None) -> bool:
        if not super()._pre_run(args):
            return False
        col: Column = None
        for col in self.columns.values():
            if col.initial_width <= 0:
                col.width = len(self._column_separator + col.name)
        
        if isinstance(self.option.indent, int) and (self.option.indent >= 0):
            self._depth_separator = S_space * self.option.indent
        else:
            self._depth_separator = ""

        return True

    def _on_file(self, file_model: FileModel) -> FileModel:
        new_file: FileModel = super()._on_file(file_model)
        new_row: Row = Row(len(self.rows), new_file)
        for col in self.columns.values():
            new_row.cells.append(Cell("", new_row, col))
        self.rows.append(new_row)
        #Caculate column width
        string: str = ""
        #  Index column
        if self.index_column.initial_width <= 0:
            string = f"{self._column_separator}{str(new_row.index)}"
            if self.index_column.width < len(string):
                self.index_column.width = len(string)
        #  Name column
        if self.name_column.initial_width <= 0:
            string = f"{self._column_separator}{self._depth_separator * new_file.depth}{new_file.base_name}"
            if self.name_column.width < len(string):
                self.name_column.width = len(string)
        #  Type column
        if self.type_column.initial_width <= 0:
            string = f"{self._column_separator}{new_file.kind.name}"
            if self.type_column.width < len(string):
                self.type_column.width = len(string)
        #  Size column
        if self.size_column.initial_width <= 0:
            string = f"{self._column_separator}{str(new_file.size)}"
            if self.size_column.width < len(string):
                self.size_column.width = len(string)
        #  Extension column
        if self.extension_column.initial_width <= 0:
            string = f"{self._column_separator}{new_file.extension}"
            if self.extension_column.width < len(string):
                self.extension_column.width = len(string)
        #  Remark column
        if self.remark_column.initial_width <= 0:
            string = f"{self._column_separator}"
            if self.remark_column.width < len(string):
                self.remark_column.width = len(string)
        
        return new_file

    def _on_directory(self, dir_model: DirectoryModel) -> DirectoryModel:
        new_dir: DirectoryModel = super()._on_directory(dir_model)
        new_row: Row = Row(len(self.rows), new_dir)
        for col in self.columns.values():
            new_row.cells.append(Cell("", new_row, col))
        self.rows.append(new_row)
        #Caculate column width
        string: str = ""
        #  Index column
        if self.index_column.initial_width <= 0:
            string = f"{self._column_separator}{str(new_row.index)}"
            if self.index_column.width < len(string):
                self.index_column.width = len(string)
        #  Name column
        if self.name_column.initial_width <= 0:
            string = f"{self._column_separator}{self._depth_separator * new_dir.depth}{new_dir.base_name}"
            if self.name_column.width < len(string):
                self.name_column.width = len(string)
        #  Type column
        if self.type_column.initial_width <= 0:
            string = f"{self._column_separator}{new_dir.kind.name}"
            if self.type_column.width < len(string):
                self.type_column.width = len(string)
        #  Size column
        if self.size_column.initial_width <= 0:
            string = f"{self._column_separator}{str(new_dir.size)}"
            if self.size_column.width < len(string):
                self.size_column.width = len(string)
        #  Extension column
        if self.extension_column.initial_width <= 0:
            string = f"{self._column_separator}{new_dir.extension}"
            if self.extension_column.width < len(string):
                self.extension_column.width = len(string)
        #  Remark column
        if self.remark_column.initial_width <= 0:
            string = f"{self._column_separator}"
            if self.remark_column.width < len(string):
                self.remark_column.width = len(string)
        return new_dir

    def _on_symlink(self, link_model):
        new_link = super()._on_symlink(link_model)
        new_row: Row = Row(len(self.rows), new_link)
        for col in self.columns.values():
            new_row.cells.append(Cell("", new_row, col))
        self.rows.append(new_row)
        #Caculate column width
        string: str = ""
        #  Index column
        if self.index_column.initial_width <= 0:
            string = f"{self._column_separator}{str(new_row.index)}"
            if self.index_column.width < len(string):
                self.index_column.width = len(string)
        #  Name column
        if self.name_column.initial_width <= 0:
            string = f"{self._column_separator}{self._depth_separator * new_link.depth}{new_link.base_name}"
            if self.name_column.width < len(string):
                self.name_column.width = len(string)
        #  Type column
        if self.type_column.initial_width <= 0:
            string = f"{self._column_separator}{new_link.kind.name}"
            if self.type_column.width < len(string):
                self.type_column.width = len(string)
        #  Size column
        if self.size_column.initial_width <= 0:
            string = f"{self._column_separator}{str(new_link.size)}"
            if self.size_column.width < len(string):
                self.size_column.width = len(string)
        #  Extension column
        if self.extension_column.initial_width <= 0:
            string = f"{self._column_separator}{new_link.extension}"
            if self.extension_column.width < len(string):
                self.extension_column.width = len(string)
        #  Remark column
        if self.remark_column.initial_width <= 0:
            string = f"{self._column_separator}"
            if self.remark_column.width < len(string):
                self.remark_column.width = len(string)
        return new_link
    
    def __console_print(self) -> bool:
        row: Row = None
        cell: Cell = None
        item: IoModel = None
        padding: int = 0
        string: str = ""
        row_string: str = ""
        row_bottom: str = ""
        try:
            for row in self.rows:
                row_string = ""
                row_bottom = ""
                item = row.tag
                for cell in row.cells:
                    #Update cell's value
                    if row.index > self.header_row.index:
                        if cell.column.name == COLUMN_NAME_INDEX:
                            cell.value = str(row.index)
                        elif cell.column.name == COLUMN_NAME_NAME:
                            cell.value = (self._depth_separator) * item.depth + item.base_name
                        elif cell.column.name == COLUMN_NAME_TYPE:
                            cell.value = item.kind.name
                        elif cell.column.name == COLUMN_NAME_SIZE:
                            cell.value = str(item.size)
                        elif cell.column.name == COLUMN_NAME_EXTENSION:
                            cell.value = item.extension
                        elif cell.column.name == COLUMN_NAME_REMARK:
                            cell.value = ""
                    padding = cell.column.width
                    #Print left border
                    row_string += (self._column_separator)
                    row_bottom += S_plus
                    padding -= len(self._column_separator)
                    #Print cell's value
                    if cell.column.align == Alignment.CENTER:
                        string = ((padding / 2 - len(cell.value) / 2) * S_space)
                        row_string += (string)
                        row_bottom += S_minus * len(string)
                        padding -= len(string)
                        row_string += (cell.value)
                        row_bottom += S_minus * len(cell.value)
                        padding += len(cell.value)
                        row_string += (padding * S_space)
                        row_bottom += (padding * S_minus)
                    elif cell.column.align == Alignment.RIGHT:
                        string = (padding - len(cell.value)) * S_space
                        row_string += (string)
                        row_bottom += S_minus * len(string)
                        row_string += (cell.value)
                        row_bottom += S_minus * len(cell.value)
                    else: #cell.column.align == Alignment.LEFT:
                        row_string += (cell.value)
                        row_bottom += S_minus * len(cell.value)
                        padding -= len(cell.value)
                        row_string += (padding * S_space)
                        row_bottom += (padding * S_minus)
                    if cell.column.index == len(self.columns)-1: #Last cell
                        row_string += self._column_separator
                        row_bottom += S_plus
                if row.index == self.header_row.index:
                    print(row_bottom)
                print(row_string)
                if row.index == self.header_row.index:
                    print(row_bottom)
        except Exception as ex:
            print(f"[E]{ex}")
            return False
        return True

    def __csv_print(self) -> bool:
        return True
    
    def __excel_print(self) -> bool:
        return True
    
    def __text_print(self) -> bool:
        return True

    def _on_run(self, args = None) -> bool:
        self.rows.clear()
        if self.option.header:
            self.rows.append(self.header_row)
            self.header_row.index = 0
        else:
            self.header_row.index = -1
        if not super()._on_run(args):
            return False
        if self.option.output_file is not None:
            if self.option.output_file.lower().endswith(".csv"):
                return self.__csv_print()
            elif self.option.output_file.lower().endswith(".xlsx") or self.option.output_file.lower().endswith(".xlsx"):
                return self.__excel_print()
            else:
                return self.__text_print()
        else:
            return self.__console_print()