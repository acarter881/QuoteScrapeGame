import random
import requests
from bs4 import BeautifulSoup

url = 'http://quotes.toscrape.com'

# http://quotes.toscrape.com/page/1/               # This is the format of the URL
html_list = []

for i in range(1,11):                              # Scraping the first ten pages
    r = requests.get(url + '/page/' + str(i) + '/')
    html_list.append(r.text)

soup = BeautifulSoup(str(html_list), 'html.parser')

chunks = soup.find_all(class_ = 'quote')

big_list = []
for chunk in chunks:
    quote = chunk.find(class_ = 'text').text        # This is a quote
    author = chunk.find(class_ = 'author').text     # This is the name of an author
    biography = chunk.find('a')['href']             # This is a link to an author's biography
    big_list.append([quote, author, biography])
    
random_selection = random.choice(big_list)          # Get a random list that includes the quote, author, and biography link
random_quote = random_selection[0]                  # Variable for the random quote
random_author = random_selection[1]                 # Variable for the random author
random_biography = random_selection[2]              # Variable for the random biography link

print(random_quote)   

number_of_guesses = 4
guess = ""

while 1:     
    guess = input()
    bio_page = requests.get(url + random_biography)
    html_bio = bio_page.text
    soup = BeautifulSoup(html_bio, 'html.parser')
    
    if guess == random_author:
        print('Correct')
        continue_playing = input('\nDo you want to continue playing? ')  
        if continue_playing.lower() == 'yes':
            number_of_guesses = 4
            random_selection = random.choice(big_list)
            random_quote = random_selection[0] 
            random_author = random_selection[1]
            random_biography = random_selection[2] 
            print(random_quote)
        else:
            break
    # On the first wrong attempt, provide user with author's birth date and location
    elif guess != random_author and number_of_guesses == 4: 
        dob = soup.find(class_ = 'author-born-date').text  
        pob = soup.find(class_ = 'author-born-location').text        
        number_of_guesses -= 1 
        print('Hint: The author was born on ' + dob + ' ' + pob + '.')
    # On the second wrong attempt, provide user with first letter of author's first name
    elif guess != random_author and number_of_guesses == 3: 
        first_of_first = soup.find(class_ = 'author-title').text[0]
        number_of_guesses -= 1 
        print('Hint: The first letter of the author\'s first name is: ' + first_of_first)
    elif guess != random_author and number_of_guesses == 2: 
        first_of_last = soup.find(class_ = 'author-title').text.split()[1][0]
        number_of_guesses -= 1
        print('Hint: The first letter of the author\'s last name is: ' + first_of_last)
    elif guess != random_author and number_of_guesses == 1:
        number_of_guesses -= 1

    if number_of_guesses == 0:
        print('No, that\'s incorrect, the name of the author is: ' + random_author)
        continue_playing = input('\nDo you want to continue playing? ')  
        if continue_playing.lower() == 'yes':
            number_of_guesses = 4
            random_selection = random.choice(big_list)
            random_quote = random_selection[0] 
            random_author = random_selection[1]
            random_biography = random_selection[2] 
            print(random_quote)
        else:
            break
            
print('\nThank you for playing')  
