from turtle import st
import requests
from bs4 import BeautifulSoup
from .reFinder import Finder
from .exceptions import ResponseParseException, RequestParseException, AuthenticationException
from .objs import Teacher, Student, LostWriting, WritingAuthor
import httpx

baseURL = "https://student.gs.hs.kr/student"


class wrapper:
    def __init__(self, token: str) -> None:
        self.token = token
        self.httpClient = httpx.AsyncClient(cookies={'JSESSIONID': self.token})

    async def searchFromStudent(self, query: str) -> Student:
        req = await self.httpClient.post(
            f'{baseURL}/searchStudent.do?target=&isGrade=&callback=&terms={"studentId" if query.isnumeric() else "name"}&search={query}&grade=&ban=&pageOnCnt=10')
        rawHTMLctx = req.text
        bs4Finder = BeautifulSoup(rawHTMLctx, 'html.parser')

        try:
            id = bs4Finder.find('td', {'class': "item3"}).text
            name = bs4Finder.find('td', {'class': "item4"}).text
            phone = bs4Finder.find('td', {'class': "item5"}).text
            return Student(id, name, phone)
        except:
            raise RequestParseException("Invalid Query Or Token")

    async def searchFromPhone(self, query: str) -> Teacher or dict:

        reFinder = Finder()
        req = await self.httpClient.post(
            f'{baseURL}/sms/ajax/how.do?mobile={query}')
        
        req = req.text

        if len(reFinder.MatchName(req)) < 1:
            return

        try:
            if reFinder.MatchLargeBracket(req)[0] == "교사":
                return Teacher(reFinder.MatchMidBracket(req)[0], reFinder.MatchName(req)[0], query)
            elif reFinder.MatchLargeBracket(req)[0] == "학생":
                return Student(reFinder.MatchMidBracket(req)[0], reFinder.MatchName(req)[0], query)
        except:
            raise ResponseParseException(
                "The server returned unexpected result")

    async def getMissingItemList(self) -> dict:
        reFinder = Finder()
        req = await self.httpClient.get(
            f'{baseURL}/notice/missingList.do?page=1&pageOnCnt=1000', cookies={'JSESSIONID': self.token})
        rawHTMLctx = req.text
        bs4Finder = BeautifulSoup(rawHTMLctx, 'html.parser')
        domList = bs4Finder.select('tr')
        fullList = []
        for item in domList:
            content = item.contents
            for contentItem in content:
                if contentItem != '\n':
                    global _title, _type, date, id, author
                    if contentItem['class'][0] in ['item3', 'item5']:
                        try:
                            if contentItem['class'][0] == 'item3':
                                if contentItem.a.find('span'):
                                    _title = contentItem.a.span.get_text()
                                    _type = 'lost' if reFinder.MatchLargeBracket(_title)[
                                        0] == "분실" else 'found'
                                elif contentItem.a.get_text().isnumeric():
                                    id = contentItem.a.get_text()
                            else:
                                date = contentItem.a.span['title']
                        except:
                            pass
                    else:
                        try:
                            if contentItem['class'][0] == "item4":
                                name = contentItem.a.br.previous_sibling.get_text(
                                    strip=True)
                                typeStr = reFinder.MatchMidBracket(
                                    contentItem.a.small.get_text(strip=True))[0]
                                author = WritingAuthor(
                                    name, "teacher" if typeStr == "교사" else "student")

                        except:
                            pass
            try:
                fullList.append(LostWriting(
                    id, _title, author, date, _type))
            except:
                pass

        return fullList
