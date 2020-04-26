import requests
from bs4 import BeautifulSoup
import sys
from colorama import Fore, Back, Style, init

init()

URL = 'https://www.texnopolis.net/movie/'

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
print(f'\n {Fore.GREEN}You might think this is slow but gud shit takes time mkay... {Style.RESET_ALL}')

asciiPic1 = "                    __\r\n`       `          .^o ~\\  `        `   `                `\r\n         ``  `    Y /'~) }      _____          `        `` `\r\n          `       l/  / /    ,-~     ~~--.,_    `         `    ``\r\n     `           `   ( (    /  ~-._         ^.\r\n     ``      `        \\ \"--'--.    \"-._       \\       `    `\r\n       `           `   \"-.________     ~--.,__ ^.             `\r\n               `    `            \\\"~r-.,___.-'-. ^.\r\n      `    `                 `    YI    \\\\      ~-.\\     `      `\r\n            `             `       ||     \\\\        `\\\r\n        `                  `      ||     //\r\n  `           `                   ||    //\r\n   `           `          `       ()   //\r\n                `          `      ||  //     `   `\r\n           `                      || ( c      `\r\n            `        ___._ __  ___I|__`--__._ __  _\r\n                   \"~     ~  \"~  \"\"   ~~\"    ~  ~~"

asciiPic2 = "        ,----,\r\n   ___.`      `,\r\n   `===  D     :\r\n     `'.      .'\r\n        )    (                   ,\r\n       /      \\_________________/|\r\n      /                          |\r\n     |                           ;\r\n     |               _____       /\r\n     |      \\       ______7    ,'\r\n     |       \\    ______7     /\r\n      \\       `-,____7      ,'   bye\r\n^~^~^~^`\\                  /~^~^~^~^\r\n  ~^~^~^ `----------------' ~^~^~^\r\n ~^~^~^~^~^^~^~^~^~^~^~^~^~^~^~^~"
print(f' {Fore.MAGENTA} ' + asciiPic1 + f'{Style.RESET_ALL}')

page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.content, "html.parser")

titles = soup.findAll("h2", {"class":"movieTitle"})
summaries = soup.findAll("p", {"class":"movieSummary"})
infos = soup.findAll("table", {"class":"infoDetailsTable"})
dates = soup.findAll("div", {"class":"timeslots"})

# timeslot_set is dates xd
def getListOfMoviesCenter(titles, summaries, infos, timeslot_set):
	# vitsentzos_table = None
	vitsentzosCasts = list()
	# timeslots are the schedules for vitzentzos + texnopolis for ONE movie
	for index, timeslots in enumerate(timeslot_set):
		# individual_tables are all the seperate schedules for vitzentzos + texnopolis + different rooms
		individual_tables = timeslots.findAll("table", {"class":"table table-striped timeslotsTable"})

		# table is one of all the individual schedule tables
		for table in individual_tables:
			possible_vitsentzos_table = table.findAll("span", {"class":"telephone"})

			# for every table we check the phone to see if that schedule is a vitsentzos schedule
			for tel in possible_vitsentzos_table:
				if tel.get_text().strip() == "2815 103 102":
					data = { "title": titles[index].get_text().strip(), "summary": summaries[index].get_text().strip(), "info":infos[index].get_text().strip(), "schedule": table.get_text().replace("\n\n", "\n") }
					vitsentzosCasts.append(data)
					break

	return vitsentzosCasts
		
MoviesList = getListOfMoviesCenter(titles, summaries, infos, dates)

if len(sys.argv) > 1 and sys.argv[1] == "-center":

	for movie in MoviesList:
		print(movie["title"] + '\n' + movie["schedule"])

elif len(sys.argv) > 1 and sys.argv[1] == "-all":

	for index, title in enumerate(titles):
		print(title.get_text().strip() + '\n')
		print(summaries[index].get_text().strip())
		print(infos[index].get_text().strip())
		print(dates[index].get_text().replace("\n\n", "\n"))
else:
	print("Invalid params fam")

print("For help type --help")
while True:
	user_input = input("Enter another command: ")

	if user_input == "exit":
		print(f'{Fore.YELLOW}' + asciiPic2)
		break
	elif user_input == "--help":
		print(f'{Fore.CYAN}')
		print(f"\n##################################################\n# This bootiful program helps                    #\n# in checking for new movies                     #\n# in Heraklion.(center mostly)                   #\n#                                                #\n#                                                #\n#------------------- Commands -------------------#\n#                                                #\n# - all: shows all the movies available in       #\n#        texnopolis and vitsentzos.              #\n#                                                #\n# - center: shows only titles and vitsentzos     #\n#           schedule ;)                          #\n#                                                #\n# - exit: exits the program :(                   #\n#                                                #\n#                                                #\n##################################################\n\n\n")
		print(f'{Style.RESET_ALL}')
	elif user_input == "all":
		for index, title in enumerate(titles):
			print(f'{Back.YELLOW}' + title.get_text().strip() + f'{Style.RESET_ALL}\n')
			print(summaries[index].get_text().strip())
			print(infos[index].get_text().strip())
			print(dates[index].get_text().replace("\n\n", "\n"))
	elif user_input == "center":
		for movie in MoviesList:
			print(f'\n{Back.YELLOW}' + movie["title"] + f'{Style.RESET_ALL}' + f'{Style.DIM}' + movie["schedule"] + f'{Style.RESET_ALL}')
	else:
		print(f"\n{Fore.RED} Not a command I know, sr fam {Style.RESET_ALL}")