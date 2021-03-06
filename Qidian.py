import json
from urllib.request import Request, urlopen

#from main_Classes import BaseWebSite
#from main_Classes import Logic

from WebSiteParentsClass import BaseWebSite
from Tools import Tools

class Qidian(BaseWebSite):

	#used
	def running(self):
		self.get_chapter(self.link)

	#used
	def get_chapter(self, number):

		adres = "https://www.webnovel.com/apiajax/chapter/GetChapterList?_csrfToken=vu0HnBRS6ValeqUdXH2MJaH9TgldX4UM1lkCG6Qp&bookId=%s&_=1501845622524" % number
		req = Request(adres, headers={'User-Agent': 'Mozilla/5.0'})
		webpage = urlopen(req).read()
		webpage = json.loads(webpage)
		chapterItems = webpage["data"]["chapterItems"]
		bookName = webpage["data"]["bookInfo"]["bookName"]
		self.title = bookName
		bookId = webpage["data"]["bookInfo"]["bookId"]
		for i in chapterItems:
			text = self.download_www_to_text(i["chapterId"], bookId)
			name = "%s-%s-%s" % (bookName, str(i["chapterIndex"]).rjust(4).replace(" ", "0"), i["chapterName"])
			name = self.clean_to_name_file(name.replace(" ", "_"))
			self.toTextFile(text, name)
			self.add_text_to_listWidget_from_Gui(name)
			if not self.work:
				break


	#used
	def download_www_to_text(self, chapterId, bookId):
		www = "https://www.webnovel.com/book/%s/%s" % (bookId, chapterId)

		soup = self.make_soup(www)
		text = soup.find("div", class_="cha-words")
		text=str(text.text)
		text = text.replace(chr(32)+chr(32), "")
		text = text.replace(chr(10), "\n")
		text = text.replace(chr(13), "\n")
		while "\n\n" in text:
			text = text.replace("\n\n", "\n")

		return text.replace("\n", "\r\n")


	#used
	def all_title_and_link_from_translating(self, number_web=1):

		dict_with_all_title_and_links={}
		id = "bookId"
		name = "bookName"
		while True:
			adres_all_title_ajax = "https://www.webnovel.com/apiajax/listing/popularAjax?_csrfToken=vu0HnBRS6ValeqUdXH2MJaH9TgldX4UM1lkCG6Qp&category=&pageIndex=" + str(
				number_web)
			req = Request(adres_all_title_ajax, headers={'User-Agent': 'Mozilla/5.0'})
			webpage = urlopen(req).read()
			webpage = json.loads(webpage)
			items = webpage["data"]["items"]
			if not len(items): break
			number_web+=1

			for dic in items:

				dict_with_all_title_and_links[dic["bookName"]]=dic["bookId"]
		return dict_with_all_title_and_links
