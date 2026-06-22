import sys
import re
from collections import Counter

def process_text(text):
    words = re.findall(r"\b[a-zA-Zа-яА-ЯёЁ]+\b", text.lower())
    word_counts = Counter(words)
    return sorted(word_counts.items(), key=lambda x: (-x[1], x[0]))

def main():
    output_to_console = "-c" in sys.argv

    with open("resourse_1.txt", "r", encoding="utf-8") as f:
        text = f.read()

    result = process_text(text)

    if output_to_console:
        for word, count in result:
            print(f"{word} {count}")
    else:
        with open("result_1.txt", "w", encoding="utf-8") as f:
            for word, count in result:
                f.write(f"{word} {count}\n")

if __name__ == "__main__":
    main()