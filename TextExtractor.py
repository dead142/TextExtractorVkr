import glob
import os

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBox
from pdfminer.layout import LTTextLine


class TextExtractor:
    __file_path = None
    __directory_path = None
    max_count_file = 1

    def __init__(self, directory_path=None, max_count_file=1, file_path=None):
        """
        :param directory_path: Path to directory. ex E:\OneDrive\НИКОР 2019 - 2020\2021\ВКР\pdf
        :param max_count_file: Maximum count of files
        """
        self.__directory_path = directory_path if directory_path else self.__directory_path
        self.__file_path = file_path if file_path else self.__directory_path
        self.max_count_file = max_count_file

    # for multiply files
    # def getFilesFromDirectory(self):
    #     """ Get recursive all pdf files directory """
    #     d = {}
    #     result = []
    #     for x in os.walk(self.directory_path):
    #         print("path is: ", x[1])
    #         print("path is: ", x[0])
    #         for y in glob.glob(os.path.join(x[0], '*.pdf')):
    #             result.append(y)
    #     print(result)
    #     print(d)
    #     return result

    def getFileChapters(self, file_path=None) -> list:
        """
        :param file_path:
        :return: List of lists chapters with first page
        ex. [['8', 'Введение '], ['11', 'Термины, определения и сокращения ']]
        """
        pages_with_chapter = []
        chapters = []
        self.__document_pages_count = 0
        file_path = file_path if file_path else self.__file_path
        pages = extract_pages(file_path)

        for page_layout in pages:
            self.__document_pages_count += 1
            for element in page_layout:  # LTPage
                if isinstance(element, LTTextBox):
                    if 'оглавление' in element.get_text().lower():
                        pages_with_chapter.append(page_layout)
                        for row in page_layout:
                            if isinstance(row, LTTextBox):
                                s = row.get_text()
                                text = s[:s.find("..")]
                                page = ''.join(i for i in s if i.isdigit())[-2:]
                                if (page.strip()) or (text.strip()):  # проверяем не пустые ли значения
                                    chapters.append([page, text])
                                # print(s.rfind("."))
                                print(text)
                                print(page)
        chapters.pop(0)  # удаляем нулевой элемент
        return chapters

    def generatePagesForChapters(self, chapters: list) -> list:
        """
        Generate pages list for each chapter
        :param chapters: List of chapter with pages
        ex. [['8', 'Введение '], ['11', 'Термины, определения и сокращения ']]
        :return: List of chapter with page begin and end
        ex. [['8', 'Введение ', [8, 9, 10]], ['11', 'Термины, определения и сокращения ', [11, 12]]]
        """
        print(chapters)
        for i, value in enumerate(chapters):
            nextP = i + 1
            print(self.__document_pages_count)
            try:
                d = list(range(int(value[0]), int(chapters[nextP][0]), 1))
                chapters[i].append(d)
            except IndexError:
                d = list(range(int(value[0]), int(self.__document_pages_count), 1))
                chapters[i].append(d)
        return chapters

    def getContent(self, chapters):
        '''
        Get content of chapters
        :param chapters:
        :return:
        '''
        chapters_with_content = []
        for i, value in enumerate(chapters):
            value[2] = [x - 1 for x in value[2]]  # Так как массив страниц с 0 начинается
            data = extract_pages(self.__file_path, page_numbers=value[2])
            if value[2]:
                for page_layout in data:
                    print(page_layout)
                    chapter_text = ""
                    for page in page_layout:
                        if isinstance(page, LTTextBox) or isinstance(page, LTTextLine):
                            chapter_text = chapter_text + page.get_text()
                        chapters_with_content.append([value[1], chapter_text])
        return chapters_with_content
