from urllib.request import urlopen
from bs4 import BeautifulSoup

PHONE_SITE = 'http://gsd-auth-callinfo.s3-website.us-east-2.amazonaws.com/'


class PhoneNumberEntry:
    def __init__(self, phone_number, report_count, comment):
        self.area_code = phone_number[:3]
        self.phone_number = phone_number
        self.report_count = report_count
        self.comment = comment.replace('"', '\\"')

    def __unicode__(self):
        skeleton = u'{{ "area_code": "{}", "phone_number": "{}", "report_count": "{}", "comment": "{}" }}'
        return skeleton.format(self.area_code, self.phone_number, self.report_count, self.comment)

    def __str__(self):
        return self.__unicode__()

    def __repr__(self):
        return self.__unicode__()


class Parser:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    @classmethod
    def get_parsed_entries(cls):
        with urlopen(PHONE_SITE) as response:
            parser = cls(response.read())
        return [entry for entry in parser.parse()]

    @staticmethod
    def entry_parse(html):
        num_of_reports = html.find(class_='oos_previewSide').getText()
        # remove special characters like (,) from phone number
        number = html.find(class_='oos_previewHeader').getText().replace("(", "").replace(")", "")
        comment = html.find('div', class_='oos_previewBody').getText()
        return PhoneNumberEntry(number, num_of_reports, comment)

    def parse(self):
        latest_entries = self.soup.find('ul', id='previews').find_all('li', class_='oos_listItem')
        return map(self.entry_parse, latest_entries)


if __name__ == "__main__":
    for phone_entry in Parser.get_parsed_entries():
        print(phone_entry)
