import csv
from time import sleep
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

writer = csv.writer(open('results.csv', 'w')) # preparing csv file to store parsing result later
writer.writerow(['Name', 'Job Title', 'University', 'Location', 'URL'])

driver = webdriver.Chrome(ChromeDriverManager().install())

# navigate to sign in page
driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin/')

# customize email
username_input = driver.find_element_by_name('session_key')
username_input.send_keys('email@email.com')
sleep(0.5)

# customize password
password_input = driver.find_element_by_name('session_password')
password_input.send_keys('password')
sleep(0.5)

# auto login
driver.find_element_by_class_name('login__form_action_container').click()
sleep(0.5)

driver.get('https://www.google.com/')
sleep(0.5)

# customize search query to fit needs
search_input = driver.find_element_by_name('q')
search_input.send_keys('site:linkedin.com/in/ AND "marketing management"')
search_input.send_keys(Keys.RETURN)

# grab all linkedin profiles from first page at Google
profiles = driver.find_elements_by_xpath('//*[@class="r"]/a[1]') 
profiles = [profile.get_attribute('href') for profile in profiles]

# crawl each profile and retrieve data
for profile in profiles:
    driver.get(profile)

    try:
        sel = Selector(text=driver.page_source)
        name = sel.xpath('//title/text()').extract_first().split(' | ')[0]
        job_title = sel.xpath('//*[@class="mt1 t-18 t-black t-normal break-words"]/text()').extract_first().strip()
        schools = ', '.join(sel.xpath('//*[contains(@class, "pv-entity__school-name")]/text()').extract())
        location = sel.xpath('//*[@class="t-16 t-black t-normal inline-block"]/text()').extract_first().strip()
        ln_url = driver.current_url
        
    except:
        print('failed')

    # print to console for testing purpose
    print('\n')
    print(name)
    print(job_title)
    print(schools)
    print(location)
    print(ln_url)
    print('\n')

    writer.writerow([name, job_title, schools, location, ln_url])

driver.quit()
