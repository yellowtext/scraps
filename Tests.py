import _mysql
import re
from meetingplace import Parser
from meetingplace import quotes

def parseFile(file):
    posts = open(file, 'r', encoding='utf8')
    line_posts = posts.readlines()

    parse = Parser()
    obj_rawReport = parse.parsePost(line_posts)

    print(obj_rawReport.quote)

    for i in range(len(obj_rawReport.obj_report)):
        print(obj_rawReport.obj_report[i])

parseFile('posts1.txt')
parseFile('posts2.txt')