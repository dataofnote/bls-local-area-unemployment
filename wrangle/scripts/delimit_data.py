# from pathlib import Path
# from csv import DictReader, DictWriter
# import re
# from sys import argv

# FIELD_DESCRIPTIONS_PATH = Path('wrangle', 'scripts', 'field_descriptions.psv')

# def load_field_descriptions():
#     fieldrows = []
#     for row in DictReader(FIELD_DESCRIPTIONS_PATH):
#         row[length] = int(row[length])
#         fieldrows.append(row)
#     return fieldrows

# def parse_header(txt):
#     headers = re.split(r'\s+', txt.strip())
#     return headers


# if __name__ == '__main__':
#     src_path = Path(argv[1])
#     if not src_path.is_file():
#         raise IOError("First argument must be a valid file name.")

#     with src_path.open('r') as rf:
#         headers = parse_header(rf.readline())
#         print(headers)
