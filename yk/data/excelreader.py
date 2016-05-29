import openpyxl
from openpyxl.worksheet import Worksheet

from yk.data.frame import Frame


def read_from_file(file_name, sheet_name_list):
    # reads the data from an Excel file into the list of Frames
    # sheet_name_list takes a list of names of worksheets from the file to import

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
    # reads a single Frame from an Excel file

    sheet_name_list = [sheet_name]
    frame_list = read_from_file(file_name, sheet_name_list)
    return frame_list[sheet_name]
