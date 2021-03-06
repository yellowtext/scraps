# -*- coding: utf-8 -*-

import _mysql
import re
import chardet
import datetime
import vk_api
from VK import *

class Quote:
    def __init__(self, quote_date, quote_text):
        self.quote_date = quote_date
        self.quote_text = quote_text

    def __str__(self):
        return self.quote_date + " " + self.quote_text

class Report:
    def __init__(self, quote_id, report_date, author, task, task_time, additional):
        self.quote_id = quote_id
        self.report_date = report_date
        self.author = author
        self.task = task
        self.task_time = task_time
        self.additional = additional

    def __str__(self):
        return self.report_date + " " + self.author + " " + self.task + " " + self.task_time + " " + self.quote_id + " " + self.additional

class Affirmation:
    def __init__(self, affirmation_date, affirmation_text):
        self.affirmation_date = affirmation_date
        self.affirmation_text = affirmation_text

    def __str__(self):
        return self.affirmation_date + " " + self.affirmation_text

class Lastts:
    def __init__(self, last_time):
        self.last_time = last_time

    def __str__(self):
        return self.last_time


#"DB" connector because DataBase. Not BD - it's wrong.
class DBConnector:
    def __init__(self, DB):
        self.DB = DB

    def readQuote (self, fetchrow):
        quote_date = fetchrow[1]
        quote_text = str(fetchrow[2], "utf-8")
        obj_quote = Quote(quote_date, quote_text)
        return obj_quote

    def readReport (self,fetchrow):
        quote_id = fetchrow[1]
        report_date = fetchrow[2]
        author = str(fetchrow[3], "utf-8")
        task = str(fetchrow[4], "utf-8")
        task_time = fetchrow[5]
        additional = str(fetchrow[6], "utf-8")
        obj_report = Report(quote_id, report_date, author, task, task_time, additional)
        return obj_report

    def readAffirmation (self,fetchrow):
        affirmation_date = fetchrow[1]
        affirmation_text = str(fetchrow[2], "utf-8")
        obj_affirmation = Affirmation(affirmation_date, affirmation_text)
        return obj_affirmation

    def readLastts (self, fetchrow):
        last_time = fetchrow[1]
        obj_lastts = Lastts(last_time)
        return obj_lastts

    def writeQuote (self, obj_quote):
        self.DB.query("""INSERT INTO quotes (quotes_date, quotes_text) 
                         VALUES ('""" + obj_quote.quote_date + """', '""" +
                         obj_quote.quote_text + """')""")

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
                         VALUES ('""" + str(obj_lastts.last_time) + """')""")

class rawReport:
    def __init__(self, obj_report, quote):
        self.obj_report = obj_report
        self.quote = quote

class Parser:
    def parseAffirmation(self, date_post, line_posts):
        affirmation_date = affirmation_text = ''

        affirmation_date = str(datetime.datetime.fromtimestamp(date_post))
        affirmation_date = "".join(re.findall(r'\d{4}-\d{2}-\d{2}', affirmation_date))

        for i in range(len(line_posts)):
            if re.findall(r'^[A-za-zА-Яа-я]+', line_posts[i]):
                affirmation_text = "".join(re.findall(r'^[A-za-zА-Яа-я]+', line_posts[i]))

        obj_affirmation = Affirmation(affirmation_date, affirmation_text)

        return obj_affirmation

    def parseReport(self, line_posts):
        quote_id = 'None'
        report_date = author = quotes_date = quotes_text = ''
        task = []
        task_time = []
        additional = []
        obj_report = []

        for i in range(len(line_posts)):
            if "".join(re.findall(r'#r.*$', line_posts[0])) == '#report':
                author = 'DeathF'
            else:
                author = 'skyshine'

            if re.findall(r'[0-9]+\.[0-9]+\.[0-9]+', line_posts[i]):
                if len("".join(re.findall(r'[0-9]+\.[0-9]+\.[0-9]+', line_posts[i]))) == 8:
                    quotes_date = report_date = "20" + "".join(
                        re.findall(r'(\d{2})\] ?$', line_posts[i]) + re.findall(r'\.\d{2}\.', line_posts[i]) + re.findall(
                            r'\[(\d{2})', line_posts[i]))

                else:
                    quotes_date = report_date = "20" + "".join(
                        re.findall(r'(\d{2})\] ?$', line_posts[i]) + re.findall(r'\.\d{2}\.', line_posts[i])) + "0" + "".join(re.findall(
                            r'\[(\d{1})', line_posts[i]))

            if re.findall(r'.*\|.*', line_posts[i]):
                task.append("".join(re.findall(r'(.*) \|', line_posts[i])))
                task_time.append(re.findall(r'\| (.*)', line_posts[i]))

                task[len(task) - 1] = task[len(task) - 1].replace("'", "\\'")

                if re.findall(r'\(', line_posts[i + 1]):
                    additional.append("".join(re.findall(r'\((.*)\)', line_posts[i + 1])))
                    additional[len(additional) - 1] = additional[len(additional) - 1].replace("'", "\\'")
                else:
                    additional.append("None")

            if re.findall(r'^-.*', line_posts[i]):
                if re.findall(r'.+', line_posts[i + 1]):
                    quotes_text = line_posts[i + 1]
                    quotes_text = quotes_text.replace("'", "\\'")
                else:
                    quotes_text = line_posts[i + 2]
                    quotes_text = quotes_text.replace("'", "\\'")

        for i in range(len(task_time)):
            if re.findall(r'.*ч.*м', str(task_time[i])):
                task_time[i] = 60 * int("".join(re.findall(r'([0-9]+)ч', str(task_time[i])))) + int(
                    "".join(re.findall(r'([0-9]+)м', str(task_time[i]))))
            elif re.findall(r'.*ч', str(task_time[i])):
                task_time[i] = 60 * int("".join(re.findall(r'([0-9]+)ч', str(task_time[i]))))
            else:
                task_time[i] = int("".join(re.findall(r'([0-9]+)м', str(task_time[i]))))

        for i in range(len(task)):
            obj_report.append(Report(quote_id, report_date, author, task[i], str(task_time[i]), additional[i]))

        obj_rawReport = rawReport(obj_report, quotes_text)

        return obj_rawReport

    def parsePost(self, date_posts, line_posts):
        parse = Parser

        line_posts = line_posts.split('\n')

        if re.findall(r'] #r.*$', line_posts[0]):
            return parse.parseReport(parse, line_posts)
        elif re.findall(r'^#af.*$', line_posts[0]):
            return parse.parseAffirmation(parse, date_posts, line_posts)


if __name__ == '__main__':
    db = _mysql.connect(host="localhost", user="root", passwd="Ghjuhfvvbhjdfybt72", db='meetingplace')

    connector = DBConnector(db)

    obj_vk = VK
    obj_vk.writeBD(obj_vk, '89831283291', 'Ghjuhfvvbhjdfybt', db)

    db.query('SELECT * FROM reports')
    r = db.store_result()

    db.query('SELECT COUNT(reports_id) FROM reports')
    i = db.use_result()
    i = i.fetch_row()
    i = int(i[0][0])

    while i != 0:
        print(connector.readReport(r.fetch_row()[0]))
        i -= 1
