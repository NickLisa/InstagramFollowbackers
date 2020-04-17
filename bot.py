from selenium import webdriver
from time import sleep
from secrets import pw 																			# Save password in seperate file named secrets.py with variable pw = 'password'

class InstaBot:
    def __init__(self, username, pw):
        self.driver = webdriver.Chrome()                                                        # Loads Chrome webdriver
        self.username = username
        print('Opening Instagram...')
        self.driver.get("https://instagram.com")                                                # Navigates to Instagram
        sleep(2)
        print('Entering username...')
        self.driver.find_element_by_xpath("//input[@name='username']").send_keys(username)      # Types username
        print('Entering password...')
        self.driver.find_element_by_xpath("//input[@name='password']").send_keys(pw)            # Types password
        self.driver.find_element_by_xpath("//button[@type='submit']").click()                   # Click login
        sleep(4)
        print('Dealing with popup...')
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()      # Click on notifications popup
        sleep(2)

    def get_unfollowers(self):
        print('Navigating to profile page...')
        self.driver.get("https://instagram.com/{}/".format(self.username))                      # Navigate to profile page
        sleep(2)
        print('Opening following...')
        self.driver.find_element_by_xpath("//a[contains(@href, '/following')]").click()         # Open following box
        following = self._get_names()                                                           # Put all usernames in following
        self.driver.find_element_by_xpath("//a[contains(@href, '/followers')]").click()         # Open followers box
        followers = self._get_names()                                                           # Put all usernames in followers
        print('Generating users not following back...')
        not_following_back = [user for user in following if user not in followers]              # Make new list // loop through both lists adding only if user from following is not in followers
        print('The following users do not follow back: ', not_following_back)

    def _get_names(self):
        sleep(2)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")          # Find box using levels of divs
        last_ht, ht = 0, 1                                                                      # Initialize height attributes
        print('Scrolling through list...')
        while last_ht != ht:                                                                    # While the heights arent the same
            last_ht = ht
            sleep(2)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
                """, scroll_box)                                                                # Script to scroll down to bottom to allow loading of more names
        print('DONE SCROLLING!')
        links = scroll_box.find_elements_by_tag_name('a')                                       # Gets element containing username
        print('Creating list...')
        names = [name.text for name in links if name.text != '']                                # Loops through names adding to variable names
        # Close button
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button").click()
        return names

my_bot = InstaBot('[ENTER USERNAME]', pw)
my_bot.get_unfollowers()
