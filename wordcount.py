import os
import argparse
import re


def init_argparser():
    parser = argparse.ArgumentParser(description="word count")
    parser.add_argument("filename", type=str)

    parser.add_argument("-o", "--output", type=str, default="result.txt")

    parser.add_argument("-c", "--chars", action="store_true")
    parser.add_argument("-w", "--words", action="store_true")
    parser.add_argument("-l", "--lines", action="store_true")

    parser.add_argument("-s", "--search", action="store_true")
    parser.add_argument("-a", "--advance", action="store_true")
    parser.add_argument("-e", "--stoplist", type=str)

    return parser


def basic_count(content):
    count = {
        "chars": len(content),
        "words": len(re.split(r"[\s,]+", content))-1,
        "lines": len(content.split('\n'))-1,
    }
    return count


def count_output(args, result):
    output = open(args.output, "w+")
    for r in result:
        if args.stoplist:
            stoplist = open(args.stoplist)
            stopchars = stoplist.read().split()
            for c in stopchars:
                r["words"] -= len(re.findall(c, content))
            stoplist.close()
        if args.chars:
            output.write("{}, 字符数: {}\n".format(r["filename"], r["chars"]))
        if args.lines:
            output.write("{}, 行数: {}\n".format(r["filename"], r["lines"]))
        if args.words:
            output.write("{}, 单词数: {}\n".format(r["filename"], r["words"]))
    output.close()


def file_word_count(args, path):
    fd = open(path)
    wc = basic_count(fd.read())
    fd.close()
    name = os.path.basename(path)
    wc["filename"] = name
    return wc


def word_count(args, rootpath):
    count = []
    fileregex = args.filename.replace("*", "\\w*")
    for name in os.listdir(rootpath):
        path = os.path.join(rootpath, name)
        if args.search and os.path.isdir(path):
            count += word_count(args, path)
        elif re.findall(fileregex, name):
            count.append(file_word_count(args, path))
    return count


if __name__ == "__main__":
    parser = init_argparser()
    args = parser.parse_args()
    count = word_count(args, os.getcwd())
    count_output(args, count)