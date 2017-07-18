from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType
import json
import requests
import re


def print_to_file(filename, string):
	with open(filename, 'a') as f:
		f.write(string + '\n')


def wait_to_load(driver, locator):
	try:
		WebDriverWait(driver, 20).until(
			EC.presence_of_element_located(locator)
		)
		return 1
	except:
		print(locator)
		print('Fail to load!')
		return 0

def match_aff(aff, aff_found):
	similar_ratio = 0.3
	aff_filter = ['University', 'College', 'of', 'at', 'The', '']
	aff_words = re.split('[ ;.,&-]', aff)
	aff_words = [x for x in aff_words if x not in aff_filter]
	aff_words_found = re.split('[ ;.,&()-]', aff_found)
	# print(aff_words)
	# print(aff_words_found)
	if len(set(aff_words) & set(aff_words_found)) / len(set(aff_words)) > similar_ratio:
		return True
	else:
		return False

def main():
	# Test func match_aff
	# aff = ['University of Michigan', 'University of Illinois at Urbana-Champaign', \ 
	# 'University of Maryland; College Park']
	# aff_found = ['Univ. of Michigan', 'Intel Corporation, 1906 Fox Drive, Champaign, \
	# IL 61820, U.S.A.', '* Ph.D in 1997 from University of Maryland|University of Michigan']
	# for i in range(len(aff)):
	#     print(match_aff(aff[i], aff_found[i]))

	# Choose webdriver
	# dcap = dict(DesiredCapabilities.Firefox)
	dcap = dict(DesiredCapabilities.PHANTOMJS)
	# headers = {'Referer':'https://aminer.org/', 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
	# for key, value in headers.items():
	# 	dcap['phantomjs.page.customHeaders.{}'.format(key)] = value
	# dcap['phantomjs.page.settings.userAgent'] = \
	# 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4'
	dcap['phantomjs.page.settings.loadImages'] = False
	
	# Proxy Setting
	PROXY_ADD = "45.56.86.93:3128"
	# dcap['proxy'] = {
	#     "httpProxy":PROXY_ADD,
	#     "ftpProxy":PROXY_ADD,
	#     "sslProxy":PROXY_ADD,
	#     "noProxy":None,
	#     "proxyType":"MANUAL",
	#     "class":"org.openqa.selenium.Proxy",
	#     "autodetect":False
	# }
	# proxy = webdriver.Proxy()  
	# proxy.proxy_type = ProxyType.MANUAL  
	# proxy.http_proxy = PROXY_ADD  
	# proxy.add_to_capabilities(dcap)
	# service_args = ['--proxy=205.189.37.79:53281', '--proxy-type=none']
	# driver = webdriver.Firefox()
	driver = webdriver.PhantomJS(desired_capabilities=dcap)
	# driver.start_session(dcap)

	# When using phantomjs, need to maximize the window
	driver.maximize_window()

	driver.get("http://www.whatismyip.org")
	locator = (By.XPATH, "/html/body/div[2]/span")
	wait_to_load(driver, locator)
	IP = driver.find_element(By.XPATH, "/html/body/div[2]/span")
	print(IP.text)

	# Read in names and affiliations
	names = []
	affiliations = []
	input_file = 'test.txt'
	output_file = 'result.txt'
	try:
		with open(output_file) as f:
			result = json.load(f)
	except:
		result = []
	with open(input_file) as f:
		lines = f.readlines()
	lines = [line.rstrip('\n') for line in lines]
	for line in lines:
		line = re.split("[',]", line)
		line = list(filter(None, line))
		names.append(line[0])
		affiliations.append(line[1])

	start_url = "https://aminer.org"
	similar_ratio = 0.6
	count = 0
	#clear previous result
	# open('person_failed.txt', 'w').close()
	# open('person_not_found.txt', 'w').close()
	# open('page_source.txt', 'w').close()
	# open('affiliations.txt', 'w').close()
	
	for i in range(len(names)):

		# Store result every 10 steps
		if i % 10 == 0:
			open(output_file, 'w').close()
			print_to_file(output_file, json.dumps(result))

		# Print progress
		if i % 10 == 0:
			print("Progress: " + str(i) + " / " + str(len(names)))


		name = names[i]
		aff = affiliations[i]
		name_words = re.split('[ ().,-]', name)
		name_words = list(filter(None, name_words))
		
		driver.get(start_url)
		action_chains = ActionChains(driver)
		
		# Wait
		locator = (By.XPATH, "//ui-view//searchbox[@id='search-project']")
		if not wait_to_load(driver, locator):
			print_to_file('person_failed.txt', name)
			continue

		# Do the search
		search_box = driver.find_element(By.XPATH, "//ui-view//searchbox[@id='search-project']//input")
		search_box.clear()
		search_box.send_keys(name)
		search_box.send_keys(Keys.ENTER)
		
		locator = (By.ID, "searchTabWrapper")
		if not wait_to_load(driver, locator):
			print_to_file('person_failed.txt', name)
			continue

		locator = (By.CLASS_NAME, "person-detail")
		if not wait_to_load(driver, locator):
			print_to_file('person_not_found.txt', name)
			continue
		person_pages = driver.find_elements(By.CLASS_NAME, "person-detail")

		if len(person_pages) == 1:
			# When single result found
			# Check the name, match if correct (not check affiliation)
			name_found = person_pages[0].find_element(By.CLASS_NAME, "people-result-name").text
			name_words_found = re.split('[ ().,-]', name_found)
			name_words_found = list(filter(None, name_words_found))
			if len(set(name_words) & set(name_words_found)) / len(name_words) >= similar_ratio:
				person_page_url = person_pages[0].find_element(By.CLASS_NAME, "un-styled")\
				.get_attribute("href")
			else:
				print_to_file('person_not_found.txt', name)
				continue
		else:
			# When multiple result found
			# Try to use the "USA" location filter
			locator = (By.XPATH, "//a[@class='text-xs ng-binding']")
			if wait_to_load(driver, locator):
				filters = driver.find_elements(By.XPATH, "//a[@class='text-xs ng-binding']")
				for filt in filters:
					if "USA" in filt.text:
						filt_USA = filt
						action_chains.click(filt_USA).perform()
						print("Success using filter!")
						break
			else:
				print_to_file('person_not_found.txt', name)
				continue

			# Relocate person
			locator = (By.CLASS_NAME, "person-detail")
			if not wait_to_load(driver, locator):
				print_to_file('person_not_found.txt', name)
				continue
			person_pages = driver.find_elements(By.CLASS_NAME, "person-detail")

			for page in person_pages:
				found = False

				# Check the name, if not match, stop matching
				name_found = page.find_element(By.CLASS_NAME, "people-result-name").text
				name_words_found = re.split('[ ().,-]', name_found)
				name_words_found = list(filter(None, name_words_found))
				similar = len(set(name_words) & set(name_words_found)) / len(name_words)
				if not similar >= similar_ratio:
					print_to_file('person_not_found.txt', name)
					break

				# Check the affiliation
				try:
					aff_found = page.find_element(By.XPATH, ".//div[contains(@ng-if, 'affiliation')]").text
					if match_aff(aff, aff_found):
						found = True
						person_page_url = page.find_element(By.CLASS_NAME, "un-styled")\
						.get_attribute("href")    
						break
				except:
					continue
			

			if not found:
				print_to_file('person_not_found.txt', name)
				continue

		# simple try: choose the first one
		# person_page_url = driver.find_elements(By.CLASS_NAME, "un-styled")[0].get_attribute("href")
		
		driver.get(person_page_url)
		# print_to_file('page_source.txt', driver.page_source)


		###################################################
		## No longer need this                              ##
		## (request for json instead of browser monitor) ## 
		###################################################

		# Get radar detail
		# Wait
		# locator = (By.ID, "popover_radar")
		# if not wait_to_load(driver, locator):
		#     print_to_file('person_failed.txt', name)
		#     continue
		# radar = driver.find_element(By.ID, "popover_radar")
		# # print(radar.get_attribute("rel"))    #check

		# Move the mouse to radar
		# action_chains.reset_actions()
		# action_chains.move_to_element(radar).perform()
		
		# # Wait
		# locator = (By.CLASS_NAME, "popover-content")
		# # TODO: Try to improve
		# while not wait_to_load(driver,locator):
		#     driver.refresh()
		#     locator = (By.ID, "popover_radar")
		#     if not wait_to_load(driver, locator):
		#         print_to_file('person_failed.txt', name)
		#         continue
		#     radar = driver.find_element(By.ID, "popover_radar")
		#     action_chains.move_to_element(radar).perform()
		#     locator = (By.CLASS_NAME, "popover-content")

		# # Mouse hover extremely not persistent, need to log failed person
		# if not wait_to_load(driver, locator):
		#     print_to_file('person_failed.txt', name)
		#     continue
		# radar_detail = driver.find_element(By.CLASS_NAME, "popover-content").text.split('\n')
		# print_to_file('result.txt', radar_detail[0])
		# print_to_file('result.txt', radar_detail[1])
		# print_to_file('result.txt', radar_detail[2])
		# print_to_file('result.txt', radar_detail[3])

		count += 1
		person_result = {}
		person_result['name'] = name
		# print_to_file('result.txt', str(count) + '. ' + name)
		person_id = person_page_url.rsplit('/', 1)[-1]
		
		# Get radar detail
		radar_url = "https://api.aminer.org/api/person/indices/" + person_id
		radar_detail = requests.get(radar_url).json()["statics"][0]
		person_result['#Papers'] = str(radar_detail[0])
		person_result['#Citations'] = str(radar_detail[1])
		person_result['h-index'] = str(radar_detail[2])
		person_result['G-index'] = str(radar_detail[3])
		# print_to_file('result.txt', "#Papers: " + str(radar_detail[0]))
		# print_to_file('result.txt', "#Citations: " + str(radar_detail[1]))
		# print_to_file('result.txt', "h-index: " + str(radar_detail[2]))
		# print_to_file('result.txt', "G-index: " + str(radar_detail[3]))

		# Get paper status
		paper_status_url = "https://api.aminer.org/api/person/pubs/" + person_id + "/stats"
		paper_over_year = requests.get(paper_status_url).json()
		paper_over_year = paper_over_year["years"]
		person_result['Publication over years'] = str(paper_over_year)
		# print_to_file('result.txt', "Publications over years : " + str(paper_over_year))
		person_result['Paper'] = []

		# Get paper details
		paper_detail_url = "https://api.aminer.org/api/person/pubs/" + person_id + "/all/year/0/20"
		paper_detail = requests.get(paper_detail_url, \
			headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) \
			Gecko/20100101 Firefox/51.0'}).json()
		for paper in paper_detail:
			paper_result = {}
			try:
				paper_result['Title'] = paper["title"]
			except:
				paper_result['Title'] = ''
			paper_result['Citations'] = paper["num_citation"]
			paper_result['Publication date'] = paper["year"]
			paper_result['Author'] = []
			# print_to_file('result.txt', "[Paper #" + str(i) + "]")
			# print_to_file('result.txt', "Title: " + paper["title"])
			# print_to_file('result.txt', "Citations: " + str(paper["num_citation"]))
			# print_to_file('result.txt', "Publication date: " + str(paper["year"]))
			for author in paper["authors"]:
				author_result = {}
				try:
					author_result['Name'] = author["name"]
				except:
					author_result['Name'] = ''
				# print_to_file('result.txt', "Author: " + author["name"])

				try:
					aff = author["aff"]["desc"]

					#Format the affiliations
					aff = aff.replace('university', 'University')
					aff = aff.replace('Univ.', 'University')
					author_result['Affiliation'] = aff
					aff = re.split('[,|]', aff)
					for aff_split in aff:
						if 'University' in aff_split:
							author_result['Affiliation'] = aff_split
							break
					# print_to_file('affiliations.txt', author_result['Affiliation'])
					# print_to_file('result.txt', "Affiliation: " + author["aff"]["desc"])

				except:
					author_result['Affiliation'] = ''
					# print_to_file('result.txt', "Affiliation: ")
				paper_result['Author'].append(author_result)

			try:
				paper_result['Venue Name'] = paper["venue"]["name"]
				# print_to_file('result.txt', "Venue Name: " + paper["venue"]["name"])
			except:
				paper_result['Venue Name'] = ''
				# print_to_file('result.txt', "Venue Name: ")
			person_result['Paper'].append(paper_result)

		result.append(person_result)
		print("Success collect " + name)

	driver.quit()
	open(output_file, 'w').close()
	print_to_file(output_file, json.dumps(result))


if __name__ == '__main__':
	main()

