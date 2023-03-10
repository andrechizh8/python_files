import os
from os.path import basename
from PyPDF2 import PdfReader
import xlrd
import zipfile
from zipfile import ZipFile
import csv

path_from = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'file_source')
path_to = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')


path_to_zip = os.path.join(path_to, 'zip_archive.zip')



def test_create_zip_archive():
    file_directory = os.listdir(path_from)
    with ZipFile(path_to_zip, 'w') as my_zip:
        for file in file_directory:
            add_file = os.path.join(path_from, file)
            my_zip.write(add_file, basename(add_file))
    file_list = my_zip.namelist()
    assert len(file_list) == 5, 'Количество добавленных в архив файлов не соответсвует количеству файлов в директории'



def test_read_pdf():
    with zipfile.ZipFile(path_to_zip) as my_zip:
        file = my_zip.extract('doc.pdf')
        pdfReader = PdfReader(file)
        page = pdfReader.getPage(0)
        text = page.extractText()
        assert 'pytest Documentation' in text, 'Первая страница PDF файла не содержит текст "pytest Documentation"'

    os.remove(file)



def test_read_csv():
    with zipfile.ZipFile(path_to_zip) as my_zip:
        file = my_zip.extract('names.csv')
    with open(file) as csv_file:
        csv_file = csv.reader(csv_file)
        csv_list = []
        for i in csv_file:
            text = " ".join(i).replace(";", " ")
            csv_list.append(text)

        assert csv_list[0] == 'Anna Pavel Peter', f'Ожидаемый результат : "Anna Pavel Peter"\n' \
                                                  f'Фактический результат: {csv_list[0]}'

    os.remove(file)




def test_read_xls():
    with zipfile.ZipFile(path_to_zip) as my_zip:
        file = my_zip.extract('table.xls')
        book = xlrd.open_workbook(file)
        sheet = book.sheet_by_index(0)
        last_name = sheet.cell_value(rowx=2, colx=2)
        assert last_name == 'Hashimoto', f'Ожидаемый результат: Hashimoto\n' \
                                         f'Фактический результат: {last_name}'

    os.remove(file)




def test_read_txt():
    with zipfile.ZipFile(path_to_zip) as my_zip:
        file = my_zip.extract('example.txt')
    with open(file) as txt_file:
        lines = txt_file.readlines()
        assert 'abc' in lines

    os.remove(file)




def test_check_png_size():
    with zipfile.ZipFile(path_to_zip, 'r') as my_zip:
        file = my_zip.extract('selenium_image.png')
    file_size = os.path.getsize(file)
    assert file_size == 23783, 'Размер png файла в архиве не соответствует размеру файла в директории'

    os.remove(file)
