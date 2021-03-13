from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBox
from pdfminer.layout import LTTextLine


class Introduction:
    __document_pages_count = 0

    __file_path = ""

    __document = {}  # {1: {'text': "Текст страницы"}, 2: {.....}}

    __list_pages_without_introduction = [] # list [index, text]

    def __init__(self, file_path=None):
        self.__file_path = file_path
        self.__document = self.pdf_to_dict()
        self.__list_pages_without_introduction = self.del_pages_before_introduction()

    def __cleartext(self, string):
        string = string.strip()
        return string

    def pdf_to_dict(self):
        """

        :return: dict, ex {1: {'text': "Текст страницы"}, 2: {.....}}
        """
        __pages = extract_pages(self.__file_path)
        document = {}
        for i, page_layout in enumerate(__pages):
            self.__document_pages_count += 1
            textPage = ""
            for i, element in enumerate(page_layout):  # LTPage
                if isinstance(element, LTTextBox):
                    textPage += element.get_text()
            document[self.__document_pages_count] = {"text": textPage}
        return document

    def del_pages_before_introduction(self):
        """

        :param document:
        :return:
        """
        flag = False

        for key in self.__document:
            if (self.__document[key]["text"].lower()).find("оглавление") != -1:
                flag = True
            if flag:
                self.__list_pages_without_introduction.append([key, self.__document[key]["text"]])
        print("\n =========> delPagesBeforeIntroduction result is: \n", self.__list_pages_without_introduction)
        return self.__list_pages_without_introduction

    def getPagesWithIntroduction(self):
        """
        :return: dict {"pageWithChapters": list, "pageKeysWithChapters" : [0,1,3]}
        """
        print("\n =========> getPagesWithIntroduction  BEGIN: \n")
        pageKeysWithChapters = []
        pageWithChapters = []
        for key, value in enumerate(self.__list_pages_without_introduction):
            if (value[1].lower().find("введение") != -1 or value[1].lower().find("заключение") != -1) and value[
                1].lower().find("..") != -1:
                pageKeysWithChapters.append(key)
        print("!!!!!!!!!!!!")
        print(pageKeysWithChapters)
        print(len(pageKeysWithChapters))
        if len(pageKeysWithChapters) == 1:
            pass
        else:
            pageKeysWithChapters = list(range(pageKeysWithChapters[0], pageKeysWithChapters[-1] + 1))
        print("\n Numbers pages with introduction : \n")
        print(pageKeysWithChapters)
        for i in pageKeysWithChapters:
            pageWithChapters.append(self.__list_pages_without_introduction[i][1])
        print("\n Pages with introduction : \n")
        for i in pageWithChapters:
            print(i.split("/n"))
        print("\n =========> getPagesWithIntroduction  END \n")
        """
        Удвление стрниц с оглавлением из документа
        """
        # for i in pageKeysWithChapters:
        #     print("Page was delete: ", doc.pop(0))
        # print(doc)
        return {"pageWithChapters": pageWithChapters, "pageKeysWithChapters": pageKeysWithChapters}

    def getChapters(self, pageWithChapters):
        """

        :param pageWithChapters: list
        :return: list
        """
        chapters = []
        clear_chapters = []
        tmp_text = ""
        for pages in pageWithChapters:
            for page in pages.split("\n"):
                for chapter in page.split("\n"):
                    chapters.append(chapter)
        for i in chapters:
            if i.find("..") == -1 and i.lower().find("оглавление") == -1:
                tmp_text = self.__cleartext(i[:i.find("..")]) + " "
                continue
                # Если название главы начинается с цифр
            num = ""
            for k in i[-5:]:
                if k.isdigit():
                    num += k
            text = tmp_text + self.__cleartext(i[:i.find("..")])
            tmp_text = ""
            clear_chapters.append(text)
        return clear_chapters

    def get_content(self, clear_chapters, pageKeysWithChapters, name="введение"):
        print("\n =========> getContent BEGIN  \n")
        print(clear_chapters)
        titles = []
        text = ""
        for key, value in enumerate(clear_chapters):
            if name in value.lower():
                titles = [value, ''.join([i for i in clear_chapters[key + 1] if not i.isdigit()])]
        print(titles)
        for i in pageKeysWithChapters:
            print("Page was delete: ", self.__list_pages_without_introduction.pop(0))
        for i in self.__list_pages_without_introduction:
            # print(i)
            text = text + i[1]
            # text = text.rstrip()
            # text = text.strip('\n')
            #   text = text.strip('\t')
            text = text.replace('\n', "")
        print(text.find(titles[0]))
        print(text.find(titles[1]))
        s = text[text.find(titles[0]): text.find(titles[1])]
        print(s)
