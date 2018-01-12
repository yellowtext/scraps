# -*- coding: utf-8 -*-

import _mysql
import re
import chardet

class quotes:
    def __init__(self, quotes_date, quotes_text):
        self.quotes_date = quotes_date
        self.quotes_text = quotes_text

    def __str__(self):
        return self.quotes_date + " " + self.quotes_text

class report:
    def __init__(self, quote_id, report_date, author, task, task_time, additional):
        self.quote_id = quote_id
        self.report_date = report_date
        self.author = author
        self.task = task
        self.task_time = task_time
        self.additional = additional

    def __str__(self):
        return self.report_date + " " + self.author + " " + self.task + " " + self.task_time + " " + self.quote_id + " " + self.additional

class affirmation:
    def __init__(self, affirmation_date, affirmation_text):
        self.affirmation_date = affirmation_date
        self.affirmation_text = affirmation_text

    def __str__(self):
        return self.affirmation_date + " " + self.affirmation_text

class lastts:
    def __init__(self, last_time):
        self.last_time = last_time

    def __str__(self):
        return self.last_time

class DBConnector:
    def __init__(self, DB):
        self.DB = DB

    def readQuote (self, fetchrow):
        quotes_date = fetchrow[1]
        quotes_text = str(fetchrow[2], "utf-8")
        obj_quote = quotes(quotes_date, quotes_text)
        return obj_quote

    def readReport (self,fetchrow):
        quote_id = fetchrow[1]
        report_date = fetchrow[2]
        author = str(fetchrow[3], "utf-8")
        task = str(fetchrow[4], "utf-8")
        task_time = fetchrow[5]
        additional = str(fetchrow[6], "utf-8")
        obj_report = report(quote_id, report_date, author, task, task_time, additional)
        return obj_report

    def readAffirmation (self,fetchrow):
        affirmation_date = fetchrow[1]
        affirmation_text = str(fetchrow[2], "utf-8")
        obj_affirmation = affirmation(affirmation_date, affirmation_text)
        return obj_affirmation

    def readLastts (self, fetchrow):
        last_time = fetchrow[1]
        obj_lastts = lastts(last_time)
        return obj_lastts

    def writeQuote (self, obj_quote):
        self.DB.query("""INSERT INTO quotes (quotes_date, quotes_text) 
                         VALUES ('""" + obj_quote.quotes_date + """', '""" +
                         obj_quote.quotes_text + """')""")

    def writeReport (self, obj_report):
        self.DB.query("""INSERT INTO reports
                         (quote_id, report_date, author, task, task_time, additional) 
                         VALUES ('""" + obj_report.quote_id + """', '""" + obj_report.report_date +
                         """', '""" + obj_report.author + """', '""" + obj_report.task + """', '"""
                         + obj_report.task_time +"""', '""" + obj_report.additional + """')""")

    def writeAffirmation (self, obj_affirmation):
        self.DB.query("""INSERT INTO affirmation (affirmation_date, affirmation_text) 
                         VALUES ('""" + obj_affirmation.affirmation_date + """', '""" +
                         obj_affirmation.affirmation_text + """')""")

    def writeLastts (self, obj_lastts):
        self.DB.query("""INSERT INTO lastts (last_time) 
                         VALUES ('""" + obj_lastts.last_time + """')""")

class rawReport:
    def __init__(self, obj_report, quote):
        self.obj_report = obj_report
        self.quote = quote

class Parser:
    def parsePost(self, line_posts):
        quote_id = 'None'
        quote_id = 'None'
        report_date = author = quotes_date = quotes_text = ''
        task = []
        task_time = []
        additional = []
        obj_report = []

        for i in range(len(line_posts)):
            if re.findall(r'#r.*$', line_posts[i]):
                if "".join(re.findall(r'r.*$', line_posts[i])) == 'r':
                    author = 'skyshine'
                else:
                    author = 'DeathF'

            if re.findall(r'[0-9]+\.[0-9]+\.[0-9]', line_posts[i]):
                quotes_date = report_date = "20" + "".join(
                    re.findall(r'([0-9]+)\]$', line_posts[i]) + re.findall(r'\.[0-9]+\.', line_posts[i]) + re.findall(
                        r'\[([0-9]+)', line_posts[i]))

            if re.findall(r'.*\|.*', line_posts[i]):
                task.append("".join(re.findall(r'(.*) \|', line_posts[i])))
                task_time.append(re.findall(r'\| (.*)', line_posts[i]))

                if re.findall(r'\(', line_posts[i + 1]):
                    additional.append("".join(re.findall(r'\((.*)\)', line_posts[i + 1])))
                else:
                    additional.append("None")

            if re.findall(r'^-.*', line_posts[i]):
                if re.findall(r'[а-яА-Яa-zA-Z0-9_]+', line_posts[i + 1]):
                    quotes_text = line_posts[i + 1]
                else:
                    quotes_text = line_posts[i + 2]

        for i in range(len(task_time)):
            if re.findall(r'.*ч.*м', str(task_time[i])):
                task_time[i] = 60 * int("".join(re.findall(r'([0-9]+)ч', str(task_time[i])))) + int(
                    "".join(re.findall(r'([0-9]+)м', str(task_time[i]))))
            elif re.findall(r'.*ч', str(task_time[i])):
                task_time[i] = 60 * int("".join(re.findall(r'([0-9]+)ч', str(task_time[i]))))
            else:
                task_time[i] = int("".join(re.findall(r'([0-9]+)м', str(task_time[i]))))

        for i in range(len(task)):
            obj_report.append(report(quote_id, report_date, author, task[i], str(task_time[i]), additional[i]))

        obj_rawReport = rawReport(obj_report, quotes_text)

        return obj_rawReport

if __name__ == '__main__':
    db = _mysql.connect(host="localhost", user="root", passwd="Ghjuhfvvbhjdfybt72", db='meetingplace')

    connector = DBConnector(db)

    posts = open('C:\\Users\\DeathF\\Desktop\\project\\posts1.txt', 'r', encoding='utf8')
    line_posts = posts.readlines()

    parse = Parser()
    obj_rawReport = parse.parsePost(line_posts)

    obj_quotes = quotes(obj_rawReport.obj_report[0].report_date, obj_rawReport.quote)
    connector.writeQuote(obj_quotes)

    db.query('SELECT MAX(quotes_id) FROM quotes')
    r = db.store_result()
    quote_id = "".join(str(v) for v in r.fetch_row())
    quote_id = "".join(re.findall(r'[0-9]+', quote_id))

    for i in range(len(obj_rawReport.obj_report)):
        obj_rawReport.obj_report[i].quote_id = quote_id
        connector.writeReport(obj_rawReport.obj_report[i])

    #for i in range(len(task)):
    #    obj_report = report(quote_id, report_date, author, str(task[i]), str(task_time[i]), str(additional[i]))
    #    connector.writeReport(obj_report)

    db.query('SELECT * FROM reports')
    r = db.store_result()

    db.query('SELECT COUNT(reports_id) FROM reports')
    i = db.use_result()
    i = i.fetch_row()
    i = int(i[0][0])

    while i != 0:
        print(connector.readReport(r.fetch_row()[0]))
        i -= 1
