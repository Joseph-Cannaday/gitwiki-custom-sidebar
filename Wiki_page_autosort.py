"""
As of 10-7-21, this has only been tested on github enterprise. 
One may need to verify the html class and formatting of the page list to
ensure this implementation matches other versions of github
"""
from bs4 import BeautifulSoup
import lxml
filename = 'foo.html' #name of the html file of the homepage wiki
#this can be retrieved automatically for public repos using the requests lib

#make sure to save the home page of the wiki to the same directory as this script
with open(filename,'r') as f:# replace name in quotes with whatever the filename is
    tree = f.read()

soup = BeautifulSoup(tree, 'lxml')

#locate the pagelist directory in the page
pagelist = soup.find('div', attrs={'class': 'd-none js-wiki-sidebar-toggle-display'})

#find all the pagelinks
links = pagelist.find_all('a')

#create output file
f = open('output.txt', 'w')
curfold = '' #list is already alphabetical but keep track of when folder changes
for link in links:
    slink = link.string
    if ':' in slink:
        fname =  slink[slink.find('>')+1 : slink.find(':')] #finds foldername
        if fname != curfold:
            if curfold != '': #exception case for first value in list
                print ('</details>', file = f)
            curfold = fname
            print ('<details>', '<summary><b>', fname, '</b></summary>', file = f) #titles dropdown menu as foldername
        
        link.string.replace_with(slink[slink.find(':')+1 :])
        print('<b>',link,'</b><br>', file = f)
if links: #exception case for last value in list
    print ('</details>', file = f)
f.close()
