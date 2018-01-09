import _mysql

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

if __name__ == '__main__':
    db = _mysql.connect(host="localhost", user="root", passwd="Ghjuhfvvbhjdfybt72", db='meetingplace')

    connector = DBConnector(db)
    obj_lastts = lastts('2017-01-01 00:00:00')
    connector.writeLastts(obj_lastts)

    db.query('SELECT * FROM lastts')
    r = db.store_result()

    db.query('SELECT COUNT(last_time) FROM lastts')
    i = db.use_result()
    i = i.fetch_row()
    i = int(i[0][0])

    while i != 0:
        print(connector.readLastts(r.fetch_row()[0]))
        i -= 1
