import openpyxl
from openpyxl.worksheet import Worksheet

from yk.data.frame import Frame


def read_from_file(file_name, sheet_name_list):

    wb = openpyxl.load_workbook(file_name)

    frames = {}

    for sheet_name in sheet_name_list:
        sheet = wb.get_sheet_by_name(sheet_name) # type: Worksheet
        if sheet is not None:
            names = []

            if len(sheet.rows) > 0:
                for cell in sheet.rows[0]:
                    names.append(cell.value)

            items = []

            for row in sheet.rows[1:]:
                row_values = {}

                for i in range(len(names)):
                    cell = row[i];
                    if cell.value is not None:
                        row_values[names[i]] = cell.value
                    else:
                        row_values[names[i]] = ""

                items.append(row_values)

            frames[sheet_name] = Frame(names, items)

    return frames


def read_signle_frame_from_file(file_name, sheet_name):
    sheet_name_list = [sheet_name]
    frame_list = read_from_file(file_name, sheet_name_list)
    return frame_list[sheet_name]


# test

# file_name = r"c:\personal\projects\tes-p\test.xlsx"
# frame = read_signle_frame_from_file(file_name, "data") # type: Frame
# frame.print_to_console()
