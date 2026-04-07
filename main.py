import json

class Movie:
    def __init__(self, title:str, year:int, month:int, characters:list[str], heroes:list[str], villains:list[str], yearSet:int, monthSet:int):
        self.title = title
        self.year = year
        self.month = month
        self.characters = characters
        self.heroes = heroes
        self.villains = villains
        self. yearSet = yearSet
        self.monthSet = monthSet


    def printStats(self):
        print(self.title)
        print("-----")
        print("Release Date: ", self.month, "/", self.year)
        print("Set in: ", self.monthSet, "/", self.yearSet)
        print("-----------------------\n")
        print("Heroes: ", self.heroes)
        print("Villains: ", self.villains)
        print("Characters: ", self.characters)
        print("-----------------------\n")

    def printStatsAbbr(self): #a shorter version of stats
        print(self.title)
        print("-----")
        print("Release Date: ", self.month, "/", self.year)
        print("Set in: ", self.yearSet)
        print("-----------------------\n")


#load in the json file
with open("movies.json", "r") as file:
    data = json.load(file)
#sort them into a list of objects
movies = [] #list of movies
for item in data["movies"]:
    movies.append(Movie(item["title"],  item["releaseYear"],  item["releaseMonth"], item["characters"], item["heroes"], item["villains"], item["yearSet"], item["monthSet"]))
#sort all movie lists alphabetically
for item in movies:
    item.characters.sort()
    item.heroes.sort()
    item.villains.sort()




def realSort(): #sort by release date
    end = len(movies)
    for current in range(end):
        swapped = False 

        for i in range(0, end-current-1):
            if movies[i].year > movies[i+1].year:
               temp = movies[i]
               movies[i] = movies[i+1]
               movies[i+1] = temp
               swapped = True
            if movies[i].year == movies[i+1].year: #handle month ties
                if movies[i].month > movies[i+1].month:
                    temp = movies[i]
                    movies[i] = movies[i+1]
                    movies[i+1] = temp
                    swapped = True
        if not swapped:
            break

realSort()

#sort them chronologically
chronoMovies = [item for item in movies]

def chronoSort():
    end = len(chronoMovies)
    for current in range(end):
        swapped = False 

        for i in range(0, end-current-1):
            if chronoMovies[i].yearSet > chronoMovies[i+1].yearSet:
               temp = chronoMovies[i]
               chronoMovies[i] = chronoMovies[i+1]
               chronoMovies[i+1] = temp
               swapped = True
            if chronoMovies[i].yearSet == chronoMovies[i+1].yearSet: #handle month ties
                if chronoMovies[i].monthSet > chronoMovies[i+1].monthSet:
                    temp = chronoMovies[i]
                    chronoMovies[i] = chronoMovies[i+1]
                    chronoMovies[i+1] = temp
                    swapped = True
        if not swapped:
            break

chronoSort() #sort them



#Console Display
def start():

    userInput = consoleOut()
    #print(userInput)
    if userInput not in ["1", "2", "3", "4", "5"]:
        print("You have not entered a valid option.")
        start()
    if userInput == "1": #print movies in release order
        i = 1
        for item in movies:
            print(i, ". ", end = "")
            print(item.title, "--", item.month, "/", item.year,"\n")
            i = i+1
        #return to title
        userInput = input("Enter '-' to return to options, or enter a movie's title to learn more.")
        searchReturn(userInput)


    if userInput == "2": #print chronological order
        print("\nHere is every movie in the MCU in chronological order: \n----")
        i = 1
        for item in chronoMovies:
            print(i, ". ", end = "")
            print(item.title, "--", item.monthSet, "/", item.yearSet, "\n")
            i = i+1
        #return to title
        userInput = input("Enter '-' to return to options, or enter a movie's title to learn more.")
        searchReturn(userInput)

    if userInput == "3": #search Character
        name = input("Enter a character's name to see their story: ")
        charStory = []
        searchChar(name, charStory)
        i = 1
        for item in charStory:
            print(i, ". ", end = "")
            print(item.title, "--", "set in", item.monthSet, "/", item.yearSet, "\n")
            i = i+1
        #return to title
        userInput = input("Enter '-' to return to options, or enter a movie's title to learn more.")
        searchReturn(userInput)

    if userInput == "4": #search title
        name = input("Enter a hero/villain's title to see its story (ex: Iron Man): ")
        titleStory = []
        searchTitle(name, titleStory)
        i = 1
        for item in titleStory:
            print(i, ". ", end = "")
            print(item.title, "--", "set in",  item.monthSet, "/", item.yearSet, "\n")
            i = i+1
        #return to title
        userInput = input("Enter '-' to return to options, or enter a movie's title to learn more.")
        searchReturn(userInput)

    if userInput == "5": #search item
        userInput = input("Enter the title of a movie you'd like to know more about, or use '-' to return home: ")
        searchReturn(userInput)    



#functions
def consoleOut():
    print("Please select an option from the list by entering its number below:")
    print("1. Print release order\n2. Print chronological order\n3. Search for a character\n4. Search for a title\n5. Search for a movie")
    userInput = input("Please enter an option: ")
    return userInput


def searchReturn(term:str): #find a movie by title and print its details
    #incomplete titles are not searching properly. caps are handled though.
    if term == "-": #if - was entered, return home
        start()
    for item in movies:
        if term.title() == item.title.title():
            print()
            item.printStats()
            print() 
            userInput = input("Enter another title, or use '-' to return home.")
            searchReturn(userInput)
    #if no perfect matches were found, we want to look for partial matches
    partialList = [] #a list of partial matches
    for item in movies:
        found = item.title.title()
        if found.find(term.title()) != -1:
            partialList.append(item)

    if not partialList:#if absolutely nothing was found, indicate such
        userInput = input("No result found. Try again, or use '-' to return home.")
        searchReturn(userInput)

    #print all partial matches
    for item in partialList:
        print()
        item.printStats()
        print()
    userInput = input("Enter another title, or use '-' to return home.")
    searchReturn(userInput)
    

def searchChar(name:str, charList:list[str]): #search for movies with a certain Character
    for item in chronoMovies:
        for term in item.characters:
            if name.title() == term.title(): #title caps the whole word to account for caps errors
                charList.append(item)

    if not charList: #if a character could not be found, search for partial matches
        for item in chronoMovies:
            for term in item.characters:
                found = term.title() #found is the caps locked name of a character from a movie
                if found.find(name.title()) != -1: #if the character's name contains a caps locked version of the string, it was a match
                    charList.append(item)

def searchTitle(name:str, titleList:list[str]): #search for movies with a certain Title
    #TO implement: delete all colons and swap dashes for spaces in both the list and search term (just temporarily) to allow for missing colons or spider mans

    for item in chronoMovies:
        for term in item.heroes: #find heroes
            if name.title() == term.title(): #title caps the whole word to account for caps errors
                titleList.append(item)
        for term in item.villains: #find villains
            if name.title() == term.title(): #title caps the whole word to account for caps errors
                titleList.append(item)

    if not titleList: #if a title could not be found, search for partial matche
        name = name + " " #stop partial matches. I.E. man matching mantiss
        for item in chronoMovies:
            for term in item.heroes:
                found = term.title() #found is the caps locked name of a character from a movie
                found = found + " "
                if found.find(name.title()) != -1: #if the character's name contains a caps locked version of the string, it was a match
                    #handle duplicates
                    foundMatch = False
                    for dupCheck in titleList:
                        if dupCheck.title == item.title:
                           foundMatch = True #if there already exists an instance of this movie in our list, note that

                    if not foundMatch: #if there is no dupe instance in our list
                        titleList.append(item)

            for term in item.villains:
                found = term.title() #found is the caps locked name of a character from a movie
                found = found + " "
                if found.find(name.title()) != -1: #if the character's name contains a caps locked version of the string, it was a match
                    #handle duplicates 
                    foundMatch = False
                    for dupCheck in titleList:
                        if dupCheck.title == item.title:
                           foundMatch = True #if there already exists an instance of this movie in our list, note that

                    if not foundMatch: #if there is no dupe instance in our list
                        titleList.append(item)

#run
print("Welcome to Marvel Movies!")

start()