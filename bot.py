# Here I am going to jump into web scrapping
import urllib.request 
from bs4 import BeautifulSoup 
import html5lib
import requests 
import smtplib 
import time


#url = requests.get("https://www.flipkart.com/urbanic-women-bodycon-blue-dress/p/itm09eb5f9170f6d") 
#soup = BeautifulSoup(url.content, "html.parser")

#print(soup.prettify())


#res = soup.title
#print(res.string)

#res = soup.find_all("p") 
#print(res.string)

#res = soup.find_all("p")[0] 
#print(res.find_all("b")) 

#count = 0
#for link in soup.find_all("a"):  
#    print(str(count)+ " -> " + link.get("href")) 
#    count =+ 1                     #get the link of the page
# 
# OR 

listflip = {} 
listama = {} 

# Check the site to which product belongs
def checkSite(): 
    ques = input("Which site product you want to track: ") 
    return str(ques) 
 
def check_price():  
    ans = checkSite() 
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'}
    # Check the price for flipkart product
    if(ans == "Flipkart"):
        url = input("Enter the url: ") 
        flipkartResponse = requests.get(url,headers = headers) 
        flipSoup = BeautifulSoup(flipkartResponse.content, 'html5lib') 

        price = float(flipSoup.find('div', attrs="_30jeq3 _16Jk6d").text.replace(',','').replace('₹','')[1:])
        #print(price) 
        #everytime the prices change it get saved in the list
        listflip.append(price) 
        return price 
    # Check the price for Amazon product
    elif(ans == "Amazon"): 
        url = input("Enter the product url: ") 
        amazonResponse = requests.get(url, headers=headers) 
        amazonSoup = BeautifulSoup(amazonResponse.content, 'html5lib') 
        price = float(amazonSoup.find('span', attrs= 'a-offscreen').text.replace(',','').replace('₹','')[1:]) 
        listama.append(price) 
        return price
    
#send email if price got down
def send_mail(message,mailID): 
    send = smtplib.SMTP('smtp.gmail.com',587) 
    send.starttls() 
    send.login("ndpt8822@gmail.com","PASSWORD") 
    send.sendmail("ndpt8822@gmail.com",mailID,message) # a sending email id and a receiving email.id and a message
    send.quit()

#check the price decreased or not
def check_decrease_price(list): 
    if list[-1] < list[-2]: 
        return True 
    else: 
        return False

if __name__ == "__main__":  
    currPrice = check_price()  
    mailID = input("Enter your mail id: ")
    count = 1
    while(True): 
        if count > 1:  
            site = checkSite()
            if(site == "Flipkart"):
                flag = check_decrease_price(listflip) 
                if flag: 
                    decrease = listflip[-1] - listflip[-2] 
                    message = "Price has decreased by {decrease} rupees." 
                    send_mail(message) 
            elif(site == "Amazon"):
                flag = check_decrease_price(listama) 
                if flag: 
                    decrease = listama[-1] - listama[-2] 
                    message = "Price has decreased by {decrease} rupees." 
                    send_mail(message, mailID)
        time.sleep(43000)   #check the price has decreased or not after every 12 hours 
        count =+ 1  
