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

class affirmation:
    def __init__(self, affirmation_date, affirmation_text):
        self.affirmation_date = affirmation_date
        self.affirmation_text = affirmation_text

class lastts:
    def __init__(self, last_time):
        self.last_time = last_time

class DBConnector:
    def readQuote (fetchrow):
        quotes_date = str(fetchrow[1], "utf-8")
        quotes_text = str(fetchrow[2], "utf-8")
        obj_quote = quotes(quotes_date, quotes_text)
        return obj_quote

    def readReport (fetchrow):
        quote_id = str(fetchrow[1], "utf-8")
        report_date = str(fetchrow[2], "utf-8")
        author = str(fetchrow[3], "utf-8")
        task = str(fetchrow[4], "utf-8")
        task_time = str(fetchrow[5], "utf-8")
        additional = str(fetchrow[6], "utf-8")
        obj_report = report(quote_id, report_date, author, task, task_time, additional)
        return obj_report

    def readAffirmation (fetchrow):
        affirmation_date = str(fetchrow[1], "utf-8")
        affirmation_text = str(fetchrow[2], "utf-8")
        obj_affirmation = affirmation(affirmation_date, affirmation_text)
        return obj_affirmation

    def readLastts (fetchrow):
        last_time = str(fetchrow[1], "utf-8")
        obj_lastts = lastts(last_time)
        return obj_lastts

if __name__ == '__main__':
    db = _mysql.connect(host="localhost", user="root", passwd="Ghjuhfvvbhjdfybt72", db="meetingplace")
    db.query('SELECT * FROM reports')
    r = db.use_result()

    readR = DBConnector()
    print(readR.readReport(r.fetch_row()))