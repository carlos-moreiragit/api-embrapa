from bs4 import BeautifulSoup

class Parser:
    page = None
    def __init__(self, page):
       self.page = page
       
    def parse(self):
        soup = BeautifulSoup(self.page.content, "html.parser")
        
        data = []

        table = soup.find('table', attrs={'class':'tb_dados'})
        table_header = table.find('thead')
        rows = table_header.find_all('tr')
        for row in rows:
            cols = row.find_all('th')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])

        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])

        table_footer = table.find('tfoot')
        rows = table_footer.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])

        return data