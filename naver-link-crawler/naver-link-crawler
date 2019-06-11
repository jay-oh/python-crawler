# Thanks to https://yoonpunk.tistory.com for original source
# 네이버 URL 기반 네이버 뉴스 크롤러
from bs4 import BeautifulSoup
import urllib.request

# 출력 파일 명
OUTPUT_FILE_NAME = 'output.txt'
# 긁어 올 네이버뉴스 URL
URL = 'http://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=103&oid=055'\
      '&aid=0000445667'
 
 
# 크롤링 함수
def text_crawl(URL):
    source_code_from_URL = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
    text = ''
    for item in soup.find_all('div', id='articleBodyContents'):
        text = text + str(item.find_all(text=True))
    return text
 
 
# 메인 함수
def main():
    # 영문 윈도우 Enconding 추가(encoding='utf-8')
    open_output_file = open(OUTPUT_FILE_NAME, 'w', encoding='utf-8')
    result_text = text_crawl(URL)
    open_output_file.write(result_text)
    open_output_file.close()
    
 
if __name__ == '__main__':
    main()

# Thanks to https://yoonpunk.tistory.com for original source
