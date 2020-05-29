from bs4 import BeautifulSoup
import requests
import re
import numpy as np


# Most of this exercise is looking at a candidate website and figuring out its HTML data-structure to parse out the
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
# scrape = requests.get('https://grid.websudoku.com/?') # Child frame for websudoku.com


# soup = BeautifulSoup(scrape.text, 'html.parser')


# print(soup.prettify())
# sudoku_raw = soup.find_all("td", {"class": ''}, recursive=True)
# print(sudoku_raw)


def new_sudoku():

    # Scrape and soup need to be generated each time the function is called if I want new puzzles:
    scrape = requests.get('https://grid.websudoku.com/?')
    soup = BeautifulSoup(scrape.text, 'html.parser')

    sudoku = []
    for tr in soup.findAll("tr", recursive=True):
        for td in tr.findAll("td", {'class': re.compile(r'[a-z][0-9]')}):
            for input in td.findAll('input'): # Don't think I need a nested list for this since there's only one element?
                # TODO: possible clean up this for loop since it's not really relevant. That said, it's constant time so
                # not a huge concern here unless the code for the website is changed
                # sudoku.append(input['id'])

                # Working but returns 3x:
                # Debugged but it seems it may be just due to the html file structure nature that repeats 'class' multiple
                # times. 'id' is also repeated and there's nothing else that seems like a good unique identifier. Will just
                # have to truncate 2.

                if 'value' in input.attrs:
                    sudoku.append(int(input.attrs['value']))
                else:
                    sudoku.append(0)

    sudoku = np.array(sudoku[0:81]).reshape(9, 9).tolist()

    # N.B. instead of installing NumPy, could redefine one ourselves but I'm taking the alternative solution to contrast
    # options compared to transposing to solve column constraint in the main program. With NumPy installed, it may be
    # worth checking there now.

    return sudoku

if __name__ == '__main__':
    sudoku = new_sudoku()
    #
    # for i in range(len(sudoku)):
    #     if i%9 == 0:
    #         print()
    #     print(sudoku[i], end='')
    print(sudoku)



# TODO: explore same method with regex.

