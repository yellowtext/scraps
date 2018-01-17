from meetingplace import *

class VK:
    def writeBD(self, login, password, db):
        connector = DBConnector(db)
        parse = Parser()

        db.query('SELECT MAX(last_time) FROM lastts')
        r = db.store_result()
        last_time = "".join(str(v) for v in r.fetch_row())

        # с этой конструкции я канеш ваще выпадываю. либа для mysql с которой мы работает это просто какой-то кал
        if last_time != '(None,)':
            last_time = int("".join(re.findall(r'[0-9]+', last_time)))

        # но главное шо работает
        if type(last_time) != int:
            last_time = 0

        vk_session = vk_api.VkApi(login, password)

        try:
            vk_session.auth()
        except vk_api.AuthError as error_msg:
            print(error_msg)
            return

        tools = vk_api.VkTools(vk_session)

        wall = tools.get_all('wall.get', 100, {'owner_id': -158045488})

        max_time = 0

        for i in range(len(wall['items'])):
            if int(wall['items'][i]['date']) > max_time:
                max_time = int(wall['items'][i]['date'])

            if int(wall['items'][i]['date']) > int(last_time):
                obj = parse.parsePost(wall['items'][i]['date'], wall['items'][i]['text'])

                if type(obj) == rawReport:
                    obj_quotes = Quote(obj.obj_report[0].report_date, obj.quote)
                    connector.writeQuote(obj_quotes)

                    db.query('SELECT MAX(quotes_id) FROM quotes')
                    r = db.store_result()
                    quote_id = "".join(str(v) for v in r.fetch_row())
                    quote_id = "".join(re.findall(r'[0-9]+', quote_id))

                    for i in range(len(obj.obj_report)):
                        obj.obj_report[i].quote_id = quote_id
                        connector.writeReport(obj.obj_report[i])

                elif type(obj) == Affirmation:
                    connector.writeAffirmation(obj)

            if i == (len(wall['items']) - 1):
                obj_lastts = Lastts(str(max_time))
                connector.writeLastts(obj_lastts)
