# TextExtractor для пояcнительных записок к ВКР ИТМО

## Набор завимостей 

```commandline
    pip install -r requirements.txt
```

## Базовое использование

```python
import TextExtractor 

textExtractor = TextExtractor(
    file_path='full_path_to_VKR\vkr.pdf')
chapters = textExtractor.getFileChapters()
chapter_pages = textExtractor.generatePagesForChapters(chapters)
chapters_with_content = textExtractor.getContent(chapter_pages)

df = pd.DataFrame(chapters_with_content)
df.to_csv("out.csv", index=False)

 

```