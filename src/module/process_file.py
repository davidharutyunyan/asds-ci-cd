from src.data.preprocessing_helpers import row_to_list, convert_to_int
import pandas as pd
def process_file(read_path, write_path):
    source_file = open(read_path)
    rows = source_file.readlines()
    rows.pop(0)
    areas = []
    values = []
    for row in rows:
        row_l = row_to_list(row)
        if row_l is not None:
            print(row_l[0], row_l[1])
            areas.append(convert_to_int(row_l[0]))
            values.append(convert_to_int(row_l[1]))
    df = pd.DataFrame({
        'area': areas,
        'value': values,
    }, columns=['area', 'value'])
    df.to_csv(write_path, index = False)

