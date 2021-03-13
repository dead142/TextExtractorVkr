from IntroductionParse import *
import pandas as pd
import gc

import time

# from tqdm import tqdm 335
path = [
    'Исследование влияния алгоритма стохастического градиентного спуска на качество обнаружения аномалий телекоммуникационных данных с использованием нейронных сетей.pdf',
    'Разработка VPN-приложения для мобильных устройств на платформе Android.pdf',
    'Анализ методов обеспечения безопасной передачи данных при взаимодействии с устройствами Интернета вещей.pdf',
]
d = []
for i in path:
    print("\n ==========================================================================================", i,
          "\n ==========================================================================================")
    textExtractor = Introduction(file_path=i)
    pageWithChapters = textExtractor.getPagesWithIntroduction()  # {"pageWithChapters": pageWithChapters, "pageKeysWithChapters": pageKeysWithChapters }
    clear_chapters = textExtractor.getChapters(pageWithChapters=pageWithChapters["pageWithChapters"])
    content = textExtractor.get_content(clear_chapters=clear_chapters,
                                        pageKeysWithChapters=pageWithChapters["pageKeysWithChapters"])

    gc.collect()
    d.append([i, content])
    del textExtractor
print(d)
df = pd.DataFrame(d, columns=["FileName", "Text"])
print(df.head)
df.to_csv("ou1t.csv", index=False, mode="a+", encoding="utf-8", sep="|")
