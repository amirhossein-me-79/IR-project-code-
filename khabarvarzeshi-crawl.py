import requests
from bs4 import BeautifulSoup
from newspaper import Article
from tqdm import tqdm
import pandas as pd

def repeatitive(links,urls):
    for link in links :
        if link.a["href"] in urls:
            return True;
    return False;

def scrap_year(year):
    start_page = int(input("ENTER THE START PAGE :"));
    end_page = int(input("ENTER THE END PAGE :"));
    while end_page < start_page:
        print("END PAGE MUST BE BIGGER THAN START PAGE");
        end_page = int(input("ENTER ANOTHER END PAGE :"));
    scrapped_data = [];
    url_list = [];
    page = start_page-1;
    while True :
        page += 1;
        page_url = f"https://www.khabarvarzeshi.com/archive?pi={page}&pl=14&ms=0&dy=4&mn=10&yr={year}";         #url of each page
        html = requests.get(page_url).text;                         #download html of each page
        soup = BeautifulSoup(html,features='html.parser');          #extracting the html of the page
        links = soup.find_all("h3");                                #find the h3 in the html of page
        if repeatitive(links,url_list):
            break;
        number = 0;
        for link in tqdm(links) :
            news_url = "https://khabarvarzeshi.com/"+ link.a["href"];        #url of each news in each page 
            url_list.append(link.a["href"]);
            try:
                article = Article(news_url);
                article.download();
                article.parse();
                scrapped_data.append({"url" : news_url ,"title" : article.title , "text": article.text});
            except:
                print(f"Faild to process page {page_url} news {news_url}");
            else :
                number += 1;

            if (number==30):
                break;
        if (page == end_page):
            break;
        
    
    df = pd.DataFrame(scrapped_data);
    df.to_csv(f"khabarvarzeshi-{year}.csv");
    print(len(scrapped_data));

if __name__ == '__main__':
    year = int(input("ENTER A YEAR :"));
    scrap_year(year);