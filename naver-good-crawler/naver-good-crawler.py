# Thanks to https://fishneverdies.tistory.com/23 original source provider
# 네이버 검색어/날짜 기반 크롤러, 결과물은 링크/제목/날짜/본문이 나옴. 언론사는 나오지 않음
import urllib
import urllib.request
import urllib.parse
import bs4
import re

def naverCrawler(File, Query, StartDate, EndDate):

    count = 1
    url = ""
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    headers = {'User-Agent': user_agent}

    while(1):
        if count == 1:
            url = "https://m.search.naver.com/search.naver?where=m_news&sm=mtb_pge&query=" + str(urllib.parse.quote(Query)) + "&sort=1&photo=0&field=0&pd=3&ds=" + str(StartDate) + "&de=" + str(EndDate) + "&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:from" + str(StartDate) + "to" + str(EndDate)
        else:
            url = "https://m.search.naver.com/search.naver?where=m_news&sm=mtb_pge&query=" + str(urllib.parse.quote(Query)) + "&sort=1&photo=0&field=0&pd=3&ds=" + str(StartDate) + "&de=" + str(EndDate) + "&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:from" + str(StartDate) + "&de=" + str(EndDate) + "&start=" + str(count)

        count = count + 15

        # 1. 모바일 네이버 뉴스의 검색 목록 주소를 반복해서 들어간다.
        try:
            req = urllib.request.Request(url, None, headers)
            u = urllib.request.urlopen(req)
            c = u.read().decode('utf-8')
            soup = bs4.BeautifulSoup(c, "html.parser")

            links = soup.find("ul", {"class": "list_news"}).find_all("a", attrs = {"href" : re.compile("^https://m.news.naver")}) 

            # 만약 기사가 중복되어 나올 경우 아래 소스를 사용
            #links = soup.find("ul", {"class": "list_news"}).find_all("a", attrs = {"href" : re.compile("^https://m.news.naver"), "class" : "news_tit"})

            

            # A. 목록 주소의 세부 기사 주소를 반복해서 들어간다.
            for link in links:

              url2 = link.get("href")
              try:
                 req2 = urllib.request.Request(url2, None, headers)
                 u2 = urllib.request.urlopen(req2)
                 c2 = u2.read().decode('utf-8')
                 soup2 = bs4.BeautifulSoup(c2, "html.parser")
                 doc2 = []
                 doc2.append(url2)

                 title = soup2.find("h2", {"class" : "media_end_head_headline"}).string
                 doc2.append(title)

                 date = soup2.find("span", {"class" : "media_end_head_info_datestamp_time"}).string
                 doc2.append(date)

                 content = soup2.find("div", {"id" : "dic_area"})
                 content = re.sub("<.*?>", " ", str(content))
                 doc2.append(content.replace("\n","").lstrip())

                 File.write(doc2[0] + "\t" + doc2[1] + "\t" + doc2[2] + '\t' + doc2[3] + "\n")

                # A-1. 만약 세부 기사 주소가 없다면, 다음 기사 주소로 넘어간다.
              except Exception as e:
                    print("url2:: " + url2)


        # 1-1. 만약 목록 주소가 없다면, 종료한다.
        except:
          print("url:: " + url)
        break


if __name__ == "__main__":
   file = open("../navernews.txt", "w", encoding = "utf-8") #이치멘 텍스트 파일 생성
   query = "철도"
   startDate = "20181201"
   endDate = "20181210"
   naverCrawler(file, query, startDate, endDate) #file이라는 인자가 들어간 crawler 함수를 호출
   file.close()
