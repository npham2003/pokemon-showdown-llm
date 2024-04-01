from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.support.ui import Select
import time
import sys
 
# instantiate options 
options = webdriver.ChromeOptions() 
 
# run browser in headless mode 
options.headless = True 
 
# instantiate driver 
driver = webdriver.Chrome(service=ChromeService( 
	ChromeDriverManager().install()), options=options) 
 
# load website 
url = 'https://play.pokemonshowdown.com/' 

# get the entire website content 
driver.get(url) 

formatName = "[Gen 1] OU"

teamText = """Starmie  
Ability: Illuminate  
- Blizzard  
- Psychic  
- Thunder Wave  
- Recover  

Exeggutor  
Ability: Chlorophyll  
- Sleep Powder  
- Psychic  
- Double-Edge  
- Explosion  

Alakazam  
Ability: Synchronize  
- Psychic  
- Seismic Toss  
- Thunder Wave  
- Recover  

Chansey  
Ability: Natural Cure  
- Ice Beam  
- Thunderbolt  
- Thunder Wave  
- Soft-Boiled  

Snorlax  
Ability: Immunity  
- Body Slam  
- Reflect  
- Hyper Beam  
- Rest  

Tauros  
Ability: Intimidate  
- Body Slam  
- Hyper Beam  
- Blizzard  
- Earthquake"""


time.sleep(3);

html = driver.page_source
 
# select elements by class name 

elements = driver.find_elements(By.NAME, 'joinRoom') 


for title in elements: 
	# select H2s, within element, by tag name 
	if title.text == "Teambuilder":
		teambuilderButton = title
		
teambuilderButton.click()

time.sleep(1)


elements = driver.find_elements(By.NAME, 'newTop') 
for title in elements: 
	# select H2s, within element, by tag name 
	if title.text == "New Team":
		newTeamButton = title
		
newTeamButton.click()

time.sleep(1)


elements = driver.find_elements(By.TAG_NAME, 'button') 
for title in elements: 
	# select H2s, within element, by tag name 
	if title.text == "Import from text or URL":
		importButton = title
		
importButton.click()

time.sleep(1)

i=1
elements = driver.find_elements(By.CLASS_NAME, 'textbox') 
elements[1].click()
elements[1].send_keys(teamText)
time.sleep(1)

driver.find_element(By.NAME, "saveImport").click()

time.sleep(1)

formatSelect = driver.find_element(By.CLASS_NAME, "select.formatselect.teambuilderformatselect")

formatSelect.click()

formats = driver.find_elements(By.TAG_NAME, 'details')

for title in formats: 
	# select H2s, within element, by tag name 
	

	if title.text == "Past Gens OU":
		title.click()
		
time.sleep(1)
formats = driver.find_elements(By.CLASS_NAME, 'option')
print("hi")
for title in formats: 
	# select H2s, within element, by tag name 
	if title.text == formatName:
		title.click()
		break
	

time.sleep(1)

driver.find_element(By.NAME, "validate").click()

time.sleep(1)


if driver.find_element(By.CLASS_NAME, "ps-popup").text == "Your team is valid for " + formatName +".\nOK":
	print("valid team")
else:
	sys.exit("Invalid Team")

time.sleep(1)

driver.find_element(By.CLASS_NAME, "button.autofocus").click()

time.sleep(1)

tabButtons = driver.find_elements(By.CLASS_NAME, 'roomtab.button')

for title in tabButtons: 
	# select H2s, within element, by tag name 
	print(title.text)
	if title.text=="Home":
		title.click()
		break


time.sleep(10)
