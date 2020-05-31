'''
    This program will read in 17 thousand rows of data, clean it, perform text
    analysis, numerical summary analysis and output two data files. The first
    data file shows the amount of profit earned for the top app in each star
    rating category and the second shows the top 10 apps ordered by star rating
    followed by number of reviews
'''

#Importing necessary packages
import csv
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import sklearn 
from sklearn.feature_extraction.text import CountVectorizer


#Loading the list
infile = 'appstore_games.csv'

# create new empty list
GamesList = []

with open(infile, 'r') as csvfile:
    # the csv file reader returns a list of the csv items on each line
    ALReader = csv.reader(csvfile,  dialect='excel', delimiter=',')

    for line in ALReader:
      # skip lines without data
      if line[0] == '' or line[0].startswith('Name'):
          continue
      else:
          # create a list for each game
          game = [line[0], line[1], line[2], line[3], line[4], line[5]]
          # add this game to the list
          GamesList.append(game)
      
      
csvfile.close()


#Converting games list to a pandas dataframe for better access to analysis tools
GamesDF = pd.DataFrame(GamesList, columns = ['Name', 'AVG Score', 'Review Count', 'Price', 'Description', 'size' ])
#Converting Numerical fields into correct formats for math to be done
GamesDF['AVG Score'] = pd.to_numeric(GamesDF['AVG Score'], errors='coerce')
GamesDF['Review Count'] = pd.to_numeric(GamesDF['Review Count'], errors='coerce')
GamesDF['Price'] = pd.to_numeric(GamesDF['Price'], errors='coerce')
GamesDF['size'] = pd.to_numeric(GamesDF['size'], errors='coerce')
GamesSorted = GamesDF.sort_values(['AVG Score', 'Review Count'], ascending = False)

#partitioning two arrays in order to perform text analysis on both the game description
#and the game title
Descriptions = GamesDF['Description']
Names = GamesDF['Name']


#Converting each array into a string so they can be tokenized
descriptionstr = ""

for ele in Descriptions:
    descriptionstr += ele
    
Namestr = ""

for ele in Names:
        Namestr += ele

#Tokenizing each string
tokenized_word=word_tokenize(descriptionstr)
tokenized_Name=word_tokenize(Namestr)

#Creating a frequency distribution chart for each set of tokenized words
#sorting by the most common words
fdist = FreqDist(tokenized_word)

print(fdist.most_common(1))

fdistName = FreqDist(tokenized_Name)

print(fdistName.most_common(1))

print(VectorizedDF_Text)

#further refining the tokens by removing stopwords

stop_words=set(stopwords.words("english"))


filtered_text=[]
for w in tokenized_word:
 #   print(w)
    if w not in stop_words:
        filtered_text.append(w)

filtered_Name=[]
for w in tokenized_Name:
 #   print(w)
    if w not in stop_words:
        filtered_Name.append(w)

fdist = FreqDist(filtered_text)

print(fdist.most_common(1))

fdistName = FreqDist(filtered_Name)

#finalizing each plot
fdist.N()

fdist.plot(30,cumulative=False)
plt.show()

fdistName.N()

fdistName.plot(30,cumulative=False)
plt.show()

#prepping lists to generate hishest sales games
Gamestop10 = GamesSorted.head(10)


highestsales0 = []
salesmax0 = 0

highestsales1 = []
salesmax1 = 0

highestsale2s = []
salesmax2 = 0

highestsales3 = []
salesmax3 = 0

highestsales4 = []
salesmax4 = 0

#Calculating the amount of sales in dollars based on the review counts.
#Grouping games based on number of stars the game has, minimum of 1, games can have partial stars
for i in range(len(GamesDF)):
    x = GamesDF.iloc[i]
    sales = x[2] * x[3]
    if x[1] >= 4:
        if sales > salesmax4:
            salesmax4 = sales
            highestsales4 = x
    elif x[1] >= 3:
        if sales > salesmax3:
            salesmax3 = sales
            highestsales3 = x
    elif x[1] >= 2:
        if sales > salesmax2:
            salesmax2 = sales
            highestsales2 = x
    elif x[1] >= 1:
        if sales > salesmax1:
            salesmax1 = sales
            highestsales1 = x
        
# Write a report text file with a title and the average of the salaries
# First create an output file name
outfile1 = 'SalesbyRating.txt'
# open the file for writing
fout1 = open(outfile1, 'w')

# write title at top of file
fout1.write("Top game sales by Rating\n\n")

fout1.write('In the 4 to 5 star range:\n')
fout1.write(highestsales4[0])
fout1.write('\n')
fout1.write('Total dollars earned from sale of app: ${:,.2f}'.format(salesmax4))

fout1.write('\n')

fout1.write('In the 3 to 4 star range:\n')
fout1.write(highestsales3[0])
fout1.write('\n')
fout1.write('Total dollars earned from sale of app: ${:,.2f}'.format(salesmax3))

fout1.write('\n')

fout1.write('In the 2 to 3 star range:\n')
fout1.write(highestsales2[0])
fout1.write('\n')
fout1.write('Total dollars earned from sale of app: ${:,.2f}'.format(salesmax2))
fout1.write('\n')

fout1.write('In the 1 to 2 star range:\n')
fout1.write(highestsales1[0])
fout1.write('\n')
fout1.write('Total dollars earned from sale of app: ${:,.2f}'.format(salesmax1))


fout1.close()

# Write a file for the top 10 games of all time.
# We write a comma separated file, using the csv writer to quote the player names with commas
# first create an output file name
outfile2 = 'Top10Apps.csv'

# open the file
with open(outfile2, 'w', newline='') as csvfileout:
    # create a csv writer for a comman sep file, with quoting as needed
    ALwriter = csv.writer(csvfileout, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    # write the header row as a list of column labels
    ALwriter.writerow(['Name', 'Rating', 'Sales'])
    for i in range(len(Gamestop10)):
        x = Gamestop10.iloc[i]
        ALwriter.writerow([x[0], x[1], x[2], x[5]])

csvfileout.close()

#Finding the mean game size for comparison against top 10 list
GamesDF['size'].mean()
