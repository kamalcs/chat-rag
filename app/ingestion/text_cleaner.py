import re


class TextCleaner:

    def clean(self, text: str) -> str:

        if not text:
            return ""

        text = text.replace("\r\n", "\n")

        text = text.replace("\r", "\n")

        text = "\n".join(line.strip() for line in text.split("\n"))

        text = re.sub(r"\n{3,}", "\n\n", text)

        text = re.sub(r"[ \t]+", " ", text)

        return text.strip()
