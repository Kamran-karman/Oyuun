import csv
import os


def read_file(file: int or str | bytes | os.PathLike[str] | os.PathLike[bytes], data: list, encoding='utf-8'):
    with open(file, encoding=encoding) as file_read:
        for row in file_read:
            data.append(row.replace('\n', ''))


def read_csv_file(file: int or str | bytes | os.PathLike[str] | os.PathLike[bytes], slovar: dict):
    with open(file, encoding='utf-8') as file_csv:
        reader = csv.DictReader(file_csv, delimiter=';')
        for row in reader:
            print(row)
            slovar.update({row['pers']: (float(row['center_x']), float(row['center_y']))})


def write_file(file: int or str | bytes | os.PathLike[str] | os.PathLike[bytes], data: list):
    with open(file, 'w') as file_write:
        s = 0
        for d in data:
            s += 1
            if s == len(data):
                konec = ''
            else:
                konec = '\n'

            if isinstance(d, list):
                d_str = ''
                for i in d:
                    d_str += f'{i} '
                file_write.write(d_str + konec)
            else:
                file_write.write(str(d) + konec)


def write_csv_file(file: int or str | bytes | os.PathLike[str] | os.PathLike[bytes], data: list[list],
                   fieldnames: list[str]):
    with open(file, 'w', newline='') as file_csv:
        writer = csv.DictWriter(file_csv, fieldnames, delimiter=';')
        writer.writeheader()
        for row in data:
            if len(row) != 0:
                slovar = {}
                s = 0
                for name in fieldnames:
                    slovar.update({name: row[s]})
                    s += 1
                writer.writerow(slovar)

