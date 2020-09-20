# Title: SCPBot     Author: TDXPQ (Aditya Jindal)
# Description:  Custom functions for the discord SCPBot.

# Import needed python libraries.
import random
import math
import urllib.request

# Import needed exteranl libraries.
import bs4 as bs

class Scp:  #The Scp class is to keep all the scp information grouped together for ease of access
    def __init__(self, num):
        self.num = int(num)
        self.series =  math.floor((num/1000)+1) #Compute SCP sereis from the number.
        self.valid = True   #Varaible used to see if the inputted SCP number is a valid number. 
        self.name = 'Could not obtain name'
        self.desc = ['No written description available']


    def string_number(self):    #Function will be used to when getting the scp url
        if self.num <= 9:
            self.str_num = '00' +str(self.num)
        elif self.num <= 99:
            self.str_num = '0' +str(self.num)
        else:
            self.str_num = str(self.num)

def scp_info(num):
    scp = Scp(num)
    scp.string_number()
    
    if scp.series == 1:     #Open the series website to get scp's name.
        scp.sause_series = urllib.request.urlopen('http://www.scp-wiki.net/scp-series').read()  #Series 1 has a different url than the other series.
    else:
        try:    #The try block sees if the the series page for the number exists the purpose is to remove hardcoding a MAX_SCP number.
            scp.sause_series = urllib.request.urlopen('http://www.scp-wiki.net/scp-series-' +str(scp.series)).read()
        except:
            scp.valid = False
            return scp 

    scp.soup_series = bs.BeautifulSoup(scp.sause_series, 'lxml')
    for creature in scp.soup_series.find_all('li'):     #Put all the SCPs in a list and sort throught them to get the one the user wanted.
        if scp.str_num in str(creature.a):  #The conditional searches for the SCP number as a string in the links for the SCPs incase the SCP has a weird naming convention.
            scp.name = creature.text

            if ('SCP-' +scp.str_num) in scp.name:   #This conditional checks to see if the naming convention is normal
                del_segment = (len(scp.str_num)+7)  #del_segment used to calculate how much of the beginning needds to be remove to leave only the name
                scp.name = (scp.name[-(len(scp.name)-del_segment):])    #Line used to make the SCP name only the name without any other information.
    
    if scp.name != '[ACCESS DENIED]':
        scp_description(scp)
    return scp


def scp_description(scp):
    scp.sause_scp = urllib.request.urlopen('http://www.scp-wiki.net/scp-' +scp.str_num).read()
    scp.soup_scp = bs.BeautifulSoup(scp.sause_scp, 'lxml')

    iteration = False   #Boolean used to only scrape the decription from the scp page.
    for paragraph in scp.soup_scp.find_all('p'):     #Sort through all paragraph tags to get to the description.
        if iteration and (paragraph.find_all('strong') or '«' in paragraph.text):  #Used to stop adding to the description by indicating that a new header had been reached
            iteration = False
        elif 'Description' in paragraph.text and paragraph.find_all('strong'):  #Conditional used to indicate the start of the description.
            scp.desc = []
            scp.desc.append(paragraph.text)
            iteration = True
        elif iteration and not paragraph.find_all('strong'):    #Conditional used to gather information between the description header and next header (the total description).
            scp.desc.append(paragraph.text) 
    return scp

def scp_max():  #The Function is to get the largest scp number without hardcoding the value.
    series = 2
    while True: #The while loop will keep trying values untill a series page is not found then break essentailly finding the largest series page which we can then use to find a Max SCP for our random funtion.
        try:
            sause_series = urllib.request.urlopen('http://www.scp-wiki.net/scp-series-' +str(series)).read()
            series += 1
        except:
            break
    max_scp = ((series - 1) * 1000) - 1
    return max_scp


def scp_rand():
    max_scp = scp_max()
    while True:
        user_input = random.randrange(1,max_scp)
        scp_entry = scp_info(user_input)
        if (scp_entry.name != ('Could not obtain name' or '[ACCESS DENIED]')) and scp_entry.desc[0] != 'No written description available':  #The conditional ensures that the user does not get a bad SCP entry.
            break
    return scp_entry

def scp_name(name): #Functions purpose is to get SCP's number based off their name or part of their name
    scp_num = 0
    max_scp = scp_max()
    max_series = math.floor((max_scp + 1)/1000) + 1 #Obtain the number of series fro the number max number of scp entries.
    for i in range (1,max_series):
        if i == 1:
            sause_series = urllib.request.urlopen('http://www.scp-wiki.net/scp-series').read()
        else:
            sause_series = urllib.request.urlopen('http://www.scp-wiki.net/scp-series-' +str(i)).read()
        soup_series = bs.BeautifulSoup(sause_series, 'lxml')

        for scp in soup_series.find_all('li'):     #Put all the SCPs in a list and sort throught them to get the one the user wanted.
            if name in str(scp):  #The conditional searches for the SCP number as a string in the links for the SCPs incase the SCP has a weird naming convention.
                if i == 1:
                    scp_num = int(str(scp.a)[14:17])
                else:
                    num_limit = math.ceil(i/10)+17  #Equation to determine how large of a slice to take of the link text
                    scp_num = int(str(scp.a)[14:num_limit])
    return scp_num


# Following code usefull for testing and debugging.
def main():
    user_input = random.randrange(-100,6999)
    # user_input = 5919

    scp_entry = scp_info(user_input)

    if scp_entry.valid:
        print(f"SCP:{scp_entry.str_num}\nSeries:{scp_entry.series}")
        print(f"Name:{scp_entry.name}")
        for paragraph in range(0, len(scp_entry.desc)):
            print(scp_entry.desc[paragraph]) 
    else:
        print(f"{scp_entry.num} is an invalid SCP Number")
    return

if __name__ == "__main__":
    num = scp_name('Taboo')
    scp = scp_info(num)
    print(scp.str_num)
    # main()