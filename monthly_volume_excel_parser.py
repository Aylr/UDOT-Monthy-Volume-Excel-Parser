#!/usr/bin/env python

import xlrd

REPORT_TYPE_HEADER = 'Monthly Hourly Volume'
SITE_NAME = 'Site Names:'
SITE_LOCATION = 'Location:'


def does_row_contain_string(row, target_string):
    # type: (object, str) -> bool
    """
    Checks if a row contains the header string indicating what the report type is
    :return: True or False
    :param target_string: the string that is being looked for
    :type row: xlrd.Row
    :rtype: bool
    """
    result = False

    for cell in row:
        if does_cell_contain_string(cell.value, target_string):
            return True

    return result


def does_cell_contain_string(value, target_string):
    # type: (object, str) -> bool
    """
    Checks if a cell contains a given string
    :param target_string: the string that is being looked for
    :param value: unknown data type
    :return: True or False
    :rtype: bool
    """
    if is_cell_value_string_or_unicode(value) is False:
        return False

    if target_string in value:
        return True
    else:
        return False


def is_cell_value_string_or_unicode(value):
    # type: (object) -> bool
    """
    Checks if a cell is either a string or unicode
    :param value:
    :return: True or False
    :rtype: bool
    """
    if type(value) == unicode or type(value) == str:
        return True
    else:
        return False


def get_data_adjacent_to_target_label(row, target_string=SITE_NAME):
    # type: (object, str) -> object
    result = None

    for cell in row:
        # we want to return the first non-blank cell after the cell containing the target label string is found
        if does_cell_contain_string(cell.value, target_string):
            # target label
            # print cell.value
            pass
        elif cell.value is None or cell.value == '':
            # blank cell
            # print 'blank'
            pass
        else:
            # desired value cell!
            result = cell.value
            break

    return result


def find_header_rows(sheet):
    # type: (object) -> List[object]
    header_rows = []

    for row in sheet.get_rows():
        if does_row_contain_string(row, REPORT_TYPE_HEADER):
            header_rows.append(row)

    return header_rows


def find_site_names(sheet):
    # type: (object) -> List[object]
    site_names = []

    for row in sheet.get_rows():
        if does_row_contain_string(row, SITE_NAME):
            site_names.append(get_data_adjacent_to_target_label(row, SITE_NAME))

    return site_names


def find_locations(sheet):
    # type: (object) -> List[object]
    site_locations = []

    for row in sheet.get_rows():
        if does_row_contain_string(row, SITE_LOCATION):
            site_locations.append(get_data_adjacent_to_target_label(row, SITE_LOCATION))

    return site_locations


def nice_list_print(list):
    for i, item in enumerate(list):
        print '{0}: {1}'.format(i, item)


def main():
    target_file = 'data/MV03 - Site -0301 on 01-01-2008.xls'

    print 'Opening file {0}\n'.format(target_file)
    book = xlrd.open_workbook(target_file)
    sheet = book.sheet_by_index(0)

    header_rows = find_header_rows(sheet)
    print '----------------- Found {0} header rows -----------------'.format(len(header_rows))
    nice_list_print(header_rows)
    print

    site_names = find_site_names(sheet)
    print '----------------- Found {0} site names -----------------'.format(len(site_names))
    nice_list_print(site_names)
    print

    site_locations = find_locations(sheet)
    print '----------------- Found {0} site locations -----------------'.format(len(site_locations))
    nice_list_print(site_locations)
    print


if __name__ == '__main__':
    main()
