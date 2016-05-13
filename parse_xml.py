import sys
import os
from bs4 import BeautifulSoup
from zipfile import ZipFile

def main(argv):
    root, ext = os.path.splitext(argv[1])
    with ZipFile(argv[1]) as myzip:
        with myzip.open("content.xml") as f:
            soup = BeautifulSoup(f.read(), "lxml")

    # print(soup)
    notes = soup.findAll("draw:frame", {"presentation:class": "notes"})
    with open("{}.script.txt".format(root), "w") as f:
        for index, note in enumerate(notes):
            bits = note.findAll("text:s")
            for bit in bits:
                note.find("text:s").replace_with(" ")
            print("_Slide {}".format(index))
            f.write("_Slide {}\n".format(index))
            print(note.text)
            f.write("{}\n".format(note.text))

if __name__ == "__main__":
    main(sys.argv)
