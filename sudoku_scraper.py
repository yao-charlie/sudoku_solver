from bs4 import BeautifulSoup
import requests
import re

# Most of this excercise is looking at a candidate website and figuring out its HTML data-structure to parse out the
# correct tags and their relevant information.

#First attempt:

# scrape = requests.get('https://www.sudoku-solutions.com/')
# soup = BeautifulSoup(scrape.text)
#
# sudoku_raw = soup.find_all("div", {"class": 'gridCell'})
# # parsed = re.findall("gridCell border tabindex", str(sudoku_raw))
# parsed = re.findall("data-posted tabindex", str(sudoku_raw))
#
# print(sudoku_raw)
# print(parsed)

# Reviewing the nature of this website, I would need to review inputting requests. Will return.


# Second attempt:

# scrape = requests.get('https://www.websudoku.com/') # Parent frame
scrape = requests.get('https://grid.websudoku.com/?') # Child frame for websudoku.com


soup = BeautifulSoup(scrape.text, 'html.parser')


# print(soup.prettify())
# sudoku_raw = soup.find_all("td", {"class": ''}, recursive=True)
# print(sudoku_raw)

for tr in soup.findAll("tr", recursive=True):
    for td in tr.findAll("td", {'class': re.compile(r'[a-z][0-9]')}):
        for input in td.findAll('input'): # Don't think I need a nested list for this since there's only one element?
            # TODO: Look into syntax for .children/.contents in BS4 documentation
            print(input)


print((type(input)))

# TODO: review documentation further on BS to try and parse in more detail related to id & value. After, explore same
#  method with regex.

