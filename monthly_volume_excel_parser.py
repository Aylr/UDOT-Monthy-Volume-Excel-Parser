#!/usr/bin/env python

import xlrd

REPORT_TYPE_HEADER = 'Monthly Hourly Volume'
SITE_NAME = 'Site Names:'


def does_row_contain_string(row, target_string):
    """
    Checks if a row contains the header string indicating what the report type is
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

def get_site_name_from_row(row):
    result = None

    for cell in row:
        if does_cell_contain_string(cell.value, SITE_NAME):
            print cell.value
        elif cell.value is None or cell.value == '':
            print 'blank'
        else:
            result = cell.value
            break

    return result

def main():
    target_file = 'data/MV03 - Site -0301 on 01-01-2008.xls'

    print 'Opening file {0}'.format(target_file)
    book = xlrd.open_workbook(target_file)
    sheet = book.sheet_by_index(0)

    header_rows = []
    for row in sheet.get_rows():
        if does_row_contain_string(row, REPORT_TYPE_HEADER):
            header_rows.append(row)

    print '----------------- Found {0} header rows -----------------'.format(len(header_rows))
    print header_rows

    site_name_rows = []
    site_names = []

    for row in sheet.get_rows():
        if does_row_contain_string(row, SITE_NAME):
            site_name_rows.append(row)
            site_names.append(get_site_name_from_row(row))

    print '----------------- Found {0} site rows -----------------'.format(len(site_name_rows))
    print site_name_rows

    print '----------------- Found {0} site names -----------------'.format(len(site_names))
    print site_names


if __name__ == '__main__':
    main()
