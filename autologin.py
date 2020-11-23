from selenium import webdriver
#import datetime, re
import urllib.request, ssl, time

'''
This script is created by Rohit Anand
'''

driver = None
'''now = datetime.datetime.now()
t1 = now.replace(hour=16, minute=59, second=59)
t2 = now.replace(hour=8, minute=00, second=00)'''

with open('auth.txt') as f:
    lines = f.readlines()


def update(driver):
    time.sleep(0.5)
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(0.5)
    driver.switch_to.frame("loginStatus")
    Rtime = int(driver.find_element_by_xpath("/html/body/form[1]/div/div[2]/div[4]/table/tbody/tr/td[2]/input").get_attribute('value'))
    flag = False
    while 10<Rtime:
            
        
        if flag:
            time.sleep(300)
            driver.switch_to.frame("loginStatus")
            driver.execute_script("""
            var frame = window.frameElement;
            if (!frame) {
                return 'root of window named ' + document.title;
            }
            var ret   = '<' + frame.tagName;
            if (frame.name) {
                ret += ' name=' + frame.name;
            }
            if (frame.id) {
                ret += ' id=' + frame.id;
            }
            return ret + '>';
            """)
            Rtime = int(driver.find_element_by_xpath("/html/body/form[1]/div/div[2]/div[4]/table/tbody/tr/td[2]/input").get_attribute('value'))
            driver.find_element_by_xpath("/html/body/form[1]/div/div[2]/div[2]/table/tbody/tr/td[3]/input").click()
        time.sleep(0.5)
        driver.switch_to.default_content()
        print('Remaining Minutes: '+ str(Rtime))
        flag= True
        
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/form[1]/div/div[2]/div[6]/input[2]").click()
    driver.quit()


def login(driver, lines):

    driver.get('http://122.0.0.254/dynPolLoginRedirect.html')

    if 'Policy Login Redirect' in driver.title:
        driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[3]/a').click()
        if driver.current_url == 'https://122.0.0.254/dynLoginLockout.html':
            raise ValueError('You are locked out for sometime...')

        assert 'SonicWALL - Authentication' in driver.title

        driver.switch_to.frame("authFrm")
        username = driver.find_element_by_xpath("//*[@id='userName']")
        password = driver.find_element_by_xpath("/html/body/form/div/div[6]/div[2]/input")
        username.send_keys(lines[0])
        password.send_keys(lines[1])

        driver.find_element_by_xpath("/html/body/form/div/div[10]/div[2]/input").click()
        cur = driver.current_window_handle
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(0.5)
        driver.switch_to.frame("frm2")
        driver.find_element_by_xpath("/html/body/form/center/table/tbody/tr/td[1]/input").click()
        time.sleep(1)
        driver.switch_to.window(cur)
        driver.close()
        print('You are successfully connected to SonicWALL')
        update(driver)
        start()

    elif driver.current_url == 'https://122.0.0.254/dynLoggedOut.html?didLogout=yes':
        login(driver, lines)

    elif driver.current_url == 'https://122.0.0.254/dynLoginLockout.html':
        print('You are locked out for sometime...')
        exit()


def start():

    global driver
    while True:
        try:
            urllib.request.urlopen('https://www.google.com')
            if driver is not None and len(driver.window_handles)!=0:
                update(driver)
            print('You are connected to INTERNET!!!')
        except:
            try:
                urllib.request.urlopen(url='http://122.0.0.254/dynPolLoginRedirect.html', context=ssl.SSLContext())
                driver=webdriver.Firefox(executable_path='geckodriver')
                login(driver=driver, lines=lines)
            except:
                print('Connect to sonicWALL')
        time.sleep(1.5)
                
                
'''
if (not t2<now<t1) or bool(re.search('^[Ss]', str(now.strftime('%A')))):
    start()
else:
    print('Internet is allowed after 5 PM')'''
    
start()