import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

header = ({'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'})


def get_all_movies(base_url):
    all_movies = {
        "name" : [],
        "link" : []
    }
    page_num = 1
    while True:
        # print(page_num)
        html = requests.get(headers=header,url=base_url)
        soup = BeautifulSoup(html.content,'lxml')
        movies = soup.find_all("div",attrs={
            "class" : "post-content"
        })
        for movie in movies:
            details = movie.find("h2").find("a")
            link_m = details.get("href")
            name_m = details.text
            all_movies["link"].append(f'=HYPERLINK("{link_m}", "{link_m}")')
            all_movies["name"].append(name_m)
        
        next_button = soup.find("div",attrs={
            "class" : "navigation"
        }).find("a",attrs={
            "class" : "next page-numbers"
        })

        if next_button:
            base_url = next_button.get("href")
        else:
            break
        page_num += 1
    return all_movies,page_num


def create_excel(data_dict, excel_file_name):
    
    df = pd.DataFrame.from_dict(data_dict, orient='index')
    df = df.transpose()
    df.to_excel(excel_file_name, index=False)


def end(time_start,pages,movies):
    time_taken = round(time.time() - time_start,2)
    print(f"Total time taken : {time_taken} sec")
    print(f"Total movies : {movies}")
    print(f"Total pages scrapped : {pages}")
    print(f"Time taken per page : {round(time_taken/pages,2)} sec")


if __name__ == "__main__":
    time_start = time.time()
    url = "https://katmoviehd.day/category/hollywood-eng/"
    all_movies,pages = get_all_movies(url)
    end(time_start,pages,len(all_movies["name"]))
    create_excel(all_movies,excel_file_name = "movies.xlsx")