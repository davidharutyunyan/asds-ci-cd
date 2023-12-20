def row_to_list(row):
    row_list = row.split('\t')
    if len(row_list) != 2 or row_list[0] == '':
        return None
    row_list[1] = row_list[1].split('\n')[0]
    return row_list

def convert_to_int(integer_string_with_commas):
    return int(integer_string_with_commas.replace(',', ''))