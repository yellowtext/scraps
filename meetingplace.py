import _mysql

class quotes:
    def __init__(self, quotes_date, quotes_text):
        self.quotes_date = quotes_date
        self.quotes_text = quotes_text

class report:
    def __init__(self, quote_id, report_date, author, task, task_time, additional):
        self.quote_id = quote_id
        self.report_date = report_date
        self.author = author
        self.task = task
        self.task_time = task_time
        self.additional = additional

    def __str__(self):
        return self.report_date + " " + self.author + " " + self.task + " " + self.task_time + " " + self.quote_id + " "+ self.additional

class affirmation:
    def __init__(self, affirmation_date, affirmation_text):
        self.affirmation_date = affirmation_date
        self.affirmation_text = affirmation_text

class lastts:
    def __init__(self, last_time):
        self.last_time = last_time

class DBConnector:
    def readQuote (self, fetchrow):
        quotes_date = str(fetchrow[1], "cp866")
        quotes_text = str(fetchrow[2], "cp866")
        obj_quote = quotes(quotes_date, quotes_text)
        return obj_quote

    def readReport (self,fetchrow):
        quote_id = fetchrow[1]
        report_date = fetchrow[2]
        author = str(fetchrow[3], "cp866")
        task = str(fetchrow[4], "cp866")
        task_time = fetchrow[5]
        additional = str(fetchrow[6], "cp866")
        obj_report = report(quote_id, report_date, author, task, task_time, additional)
        return obj_report

    def readAffirmation (self,fetchrow):
        affirmation_date = str(fetchrow[1], "cp866")
        affirmation_text = str(fetchrow[2], "cp866")
        obj_affirmation = affirmation(affirmation_date, affirmation_text)
        return obj_affirmation

    def readLastts (self, fetchrow):
        last_time = str(fetchrow[1], "cp866")
        obj_lastts = lastts(last_time)
        return obj_lastts

if __name__ == '__main__':
    db = _mysql.connect(host="localhost", user="root", passwd="Ghjuhfvvbhjdfybt72", db="meetingplace")
    db.query('SELECT * FROM reports')
    r = db.store_result()

    db.query('SELECT COUNT(author) FROM reports')
    i = db.use_result()
    i = i.fetch_row()
    i = int(i[0][0])

    read = DBConnector()

    while i != 0:
        print(read.readReport(r.fetch_row()[0]))
        i -= 1
