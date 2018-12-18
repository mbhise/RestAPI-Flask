import sqlite3 as lite

from scraper import PhoneNumberEntry, Parser


class PhoneDataLayer:
    def __init__(self, db='numbers.db'):
        self.db = db

        con = None
        try:
            con = lite.connect(self.db)
            with con:
                cur = con.cursor()
                cur.execute(
                    "CREATE TABLE IF NOT EXISTS Numbers(number TEXT primary key not null, "
                    "count INT, comment TEXT, date TEXT)")

                self.insert_entries(Parser.get_parsed_entries())
        except lite.Error as e:
            raise e
        finally:
            if con:
                con.close()

    def insert_entries(self, entries):
        con = lite.connect(self.db)
        with con:
            cur = con.cursor()
            for entry in entries:
                cur.execute(
                    "INSERT OR REPLACE INTO Numbers(number, count, comment, date) VALUES "
                    "(?, ?, ?, CURRENT_TIMESTAMP);", [entry.phone_number, entry.report_count, entry.comment])
        con.close()

    def get_db_entries(self, limit):
        con = lite.connect(self.db)
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Numbers ORDER BY date LIMIT {}".format(limit))
            rows = cur.fetchall()

        entries = []
        for row in rows:
            entries.append(PhoneNumberEntry(row[0], row[1], row[2]))

        con.close()
        return entries

    def get_all_entries(self):
        con = lite.connect(self.db)
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Numbers ORDER BY date;")
            rows = cur.fetchall()

        entries = []
        for row in rows:
            entries.append(PhoneNumberEntry(row[0], row[1], row[2]))

        con.close()
        return entries

    def get_entries(self, entry_limit=None):
        if entry_limit is not None:
            return self.get_db_entries(entry_limit)
        else:
            return self.get_all_entries()
