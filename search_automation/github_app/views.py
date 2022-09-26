
from types import NoneType
from django.shortcuts import render,redirect
#from django.http import HttpResponse
from .models import user
import requests
from bs4 import BeautifulSoup as bs

from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

#messages.info(request,"message")

#result_page below
def result(request):
    return render(request,"result.html")

#Github related information search and web scraping part below
def search_internet(request):
    if request.method == "POST":
        user_db_record = user()
        username = request.POST["username"]
        #Sending request to the target website to get a response and parse it
        response = requests.get(f"https://github.com/{username}")
        #Web scraping part
        soup = bs(response.content,"lxml")
        #With the help of Python one-liners, we can easily handle unwanted scenarios
        user_db_record.username = soup.find("span", {"class":"p-name vcard-fullname d-block overflow-hidden"}).text if soup.find("span", {"class":"p-name vcard-fullname d-block overflow-hidden"}) !=None else "No username information"
        user_db_record.nickname= soup.find("span", {"class":"p-nickname vcard-username d-block"}).text if soup.find("span", {"class":"p-nickname vcard-username d-block"}) != None else "No nickname"
        user_db_record.biography= soup.find("div", {"class":"p-note user-profile-bio mb-3 js-user-profile-bio f4"})["data-bio-text"] if soup.find("div", {"class":"p-note user-profile-bio mb-3 js-user-profile-bio f4"}) != None else f"{username} has no biography"
        #if soup.find("span", {"class":"p-org"}) == None:
        #    user_db_record.organization= f"{username} has no organization information"
        #else:
        #    user_db_record.organization = soup.find("span", {"class":"p-org"}).find("div").text
        
        user_db_record.organization = soup.find("span", {"class":"p-org"}).find("div").text if soup.find("span", {"class":"p-org"}) != None else f"{username} has no organization information"
        user_db_record.location= soup.find("span",{"class":"p-label"}).text if soup.find("span",{"class":"p-label"}) != None else f"{username} has no location information"
        user_db_record.profile_website= soup.find("li",{"data-test-selector":"profile-website-url"}).text if soup.find("li",{"data-test-selector":"profile-website-url"}) != None else f"{username} has no profile website!"
        user_db_record.twitter_account_link= soup.find("a", {"class":"Link--primary","rel":"nofollow me"})["href"] if soup.find("a", {"class":"Link--primary","rel":"nofollow me"}) != None else f"{username} has no twitter account"
        user_db_record.popular_repositories= [repo_master.find("p",{"class":"pinned-item-desc color-fg-muted text-small d-block mt-2 mb-3"}).text for repo_master in soup.find("ol",{"class":"d-flex flex-wrap list-style-none gutter-condensed mb-4"}).findChildren("li",recursive=False)] if soup.find("ol",{"class":"d-flex flex-wrap list-style-none gutter-condensed mb-4"}) != None else f"{username} has no projects yet!"
        user_db_record.all_repositories=f"https://github.com/{username}?tab=repositories"
        #Save records to the database
        user_db_record.save()
        return render(request,"result.html",{"related_information":user_db_record})

    else:
        return render(request,"search.html")
