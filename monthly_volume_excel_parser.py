#!/usr/bin/env python

import xlrd
import re

REPORT_TYPE_HEADER = 'Monthly Hourly Volume'
SITE_NAME = 'Site Names:'
SITE_LOCATION = 'Location:'


def find_column_number_and_contents_matching_search_term(row, target_string):
    for i, cell in enumerate(row):
        if does_cell_contain_string(cell.value, target_string):
            return {'column_number': i, 'contents': cell.value}


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


def get_cell_contents_right_of_target_label(row, target_string=SITE_NAME):
    # type: (List(object), str) -> object
    result = None

    for i, cell in enumerate(row):
        # we want to return the first non-blank cell after the cell containing the target label string is found
        if does_cell_contain_string(cell.value, target_string):
            # target label
            pass
        elif cell.value is None or cell.value == '':
            # blank cell
            pass
        else:
            # desired value cell!
            result = {'column_number': i, 'contents': cell.value}
            break

    return result


def find_direction_headers_with_coordinates(rows):
    # type: (List(object)) -> List[object]
    result = []

    for i, row in enumerate(rows):
        sub_result = find_column_number_and_contents_matching_search_term(row, REPORT_TYPE_HEADER)

        if sub_result is not None:
            sub_result['row_number'] = i
            result.append(sub_result)

    return result


def find_contents_right_of_labels_with_coordinates(rows, target_label_string):
    # type: (List(object)) -> List[object]
    result = []

    for i, row in enumerate(rows):
        # find the cell w/ the Site Name:
        label_cell = find_column_number_and_contents_matching_search_term(row, target_label_string)

        if label_cell is not None:
            sub_result = get_cell_contents_right_of_target_label(row, target_label_string)
            sub_result['row_number'] = i
            result.append(sub_result)

    return result


def find_date_cells(rows):
    matches = []

    for row_i, row in enumerate(rows):
        for col_i, cell in enumerate(row):
            match = re.search(r'(Sun|Mon|Tue|Wed|Thu|Fri|Sat), [0-9][0-9]', str(cell.value))
            if match:
                matches.append({'row_number': row_i, 'column_number': col_i, 'contents': cell.value})

    return matches


def find_rows_containing_dates(rows):
    matches = []

    for row_i, row in enumerate(rows):
        i = 0
        cell = row[i]
        match = re.search(r'(Sun|Mon|Tue|Wed|Thu|Fri|Sat), [0-9][0-9]', str(cell.value))
        if match:
            matches.append({'row_number': row_i, 'row': row})
    return matches


def nice_list_print(list):
    for i, item in enumerate(list):
        print '{0}: {1}'.format(i, item)


def find_and_print_interesting_things(sheet):
    header_cells = find_direction_headers_with_coordinates(sheet.get_rows())
    print '----------------- Found {0} header cells -----------------'.format(len(header_cells))
    nice_list_print(header_cells)
    print

    site_names = find_contents_right_of_labels_with_coordinates(sheet.get_rows(), SITE_NAME)
    print '----------------- Found {0} site name cells -----------------'.format(len(site_names))
    nice_list_print(site_names)
    print

    locations = find_contents_right_of_labels_with_coordinates(sheet.get_rows(), SITE_LOCATION)
    print '----------------- Found {0} site location cells -----------------'.format(len(locations))
    nice_list_print(locations)
    print

    date_cells = find_date_cells(sheet.get_rows())
    print '----------------- Found {0} date cells -----------------'.format(len(date_cells))
    nice_list_print(date_cells)
    print


def main():
    target_file = 'data/MV03 - Site -0301 on 01-01-2008.xls'

    print 'Opening file {0}\n'.format(target_file)
    book = xlrd.open_workbook(target_file)
    sheet = book.sheet_by_index(0)

    # find_and_print_interesting_things(sheet)

    date_rows = find_rows_containing_dates(sheet.get_rows())
    print '----------------- Found {0} date rows -----------------'.format(len(date_rows))
    nice_list_print(date_rows)
    print


if __name__ == '__main__':
    main()
