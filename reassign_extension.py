from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tkinter
from playsound import playsound
import time
import os

#global variables to hold information
password = ""
upassword = ""
fname = ""
lname = ""
extension = ""
set_description = ""
global choice

#this function assigns the global variables to the info collected by
#network chan
def input_info():
    playsound('C:\\Users\\nettechs\\Desktop\\Code\\reassign_extension\\disgust.wav')

    #retrieving and assigning information
    global password
    password = enter_pass.get()
    global upassword
    upassword = enter_unity.get()
    global fname
    fname = enter_fname.get()
    global lname
    lname = enter_lname.get()
    global extension
    extension = enter_ext.get()

    #closing the window
    window.destroy()

def input_choice():
    global choice
    choice = v.get()
    window.destroy()

def input_description():
    global set_description
    set_description = enter_des.get()

    window.destroy()

################################################################################
#creating window, setting size, setting background
window = tkinter.Tk()
window.title("Extension Reassignment")
window.geometry('400x300')
window.configure(bg = "white")
window.resizable(False,False)


#creation and placement of text inputs

#call manager password
enter_pass = tkinter.Entry(window, show="*")
enter_pass.place(height=20,width=150,x=10,y=100)
tkinter.Label(window, font = "verdana 10", text = "Call Manager Password", bg = "white").place(x=10,y=75)

#unity password
enter_unity = tkinter.Entry(window, show="*")
enter_unity.place(height=20,width=150,x=10,y=140)
tkinter.Label(window, font = "verdana 10", text = "Unity Password", bg = "white").place(x=10,y=115)

#first name
enter_fname = tkinter.Entry(window)
enter_fname.place(height=20,width=150,x=10,y=180)
tkinter.Label(window,font = "verdana 10", text = "First Name", bg = "white").place(x=10,y=155)

#last name
enter_lname = tkinter.Entry(window)
enter_lname.place(height=20,width=150,x=10,y=220)
tkinter.Label(window,font = "verdana 10", text = "Last Name", bg = "white").place(x=10,y=195)

#extension
enter_ext = tkinter.Entry(window)
enter_ext.place(height=20,width=50,x=10,y=260)
tkinter.Label(window,font = "verdana 10", text = "Ext.", bg = "white").place(x=10,y=235)

#custom button
hurts = tkinter.PhotoImage(file = "C:\\Users\\nettechs\\Desktop\\Code\\reassign_extension\\hurts.png")
tkinter.Button(window, command = input_info, image = hurts, bg = "white").place(height=45, width = 100, x=75, y = 250)

#add in the pictures for the title and greeting anime girl
icon = tkinter.PhotoImage(file = "C:\\Users\\nettechs\\Desktop\\Code\\reassign_extension\\network_chan.png")
tkinter.Label(window, image = icon, bg="white").place(x=175,y=5)

title = tkinter.PhotoImage(file = "C:\\Users\\nettechs\\Desktop\\Code\\reassign_extension\\title.png")
tkinter.Label(window, image = title, bg = "white").place(x=5,y=0)

window.mainloop()
################################################################################


#create web driver and navigate to call manager
driver = webdriver.Chrome()
driver.get("https://10.98.48.2/ccmadmin/showHome.do")

#search for username and enter nettechs
web_username = driver.find_element_by_name("j_username")
web_username.clear()
web_username.send_keys("nettechs")

#seach for password and enter supplied password
web_password = driver.find_element_by_name("j_password")
web_password.clear()
web_password.send_keys(password)
web_password.send_keys(Keys.RETURN)

#navigate to end user tab
driver.get("https://10.98.48.2/ccmadmin/userFindList.do")
#select criteria as last name and set to exact
driver.find_element_by_xpath("//select[@name='searchField0']/option[text()='Last name']").click()
driver.find_element_by_xpath("//select[@name='searchLimit0']/option[text()='is exactly']").click()

#enter last name into search field
web_search_name = driver.find_element_by_name("searchString0")
web_search_name.click()
web_search_name.clear()
web_search_name.send_keys(lname)

#select second criteria as first name and set to exact
driver.find_element_by_xpath("//*[@id='filterRow0']/td[9]/button").click()
driver.find_element_by_xpath("//select[@name='searchField1']/option[text()='First name']").click()
driver.find_element_by_xpath("//select[@name='searchLimit1']/option[text()='is exactly']").click()

#enter first name into search field
web_search_name = driver.find_element_by_name("searchString1")
web_search_name.click()
web_search_name.clear()
web_search_name.send_keys(fname)

#LETS GOO click find
driver.find_element_by_name("findButton").click()

#if no results come back, user is not in the system
try:
    result_count = (int)(driver.find_element_by_xpath("//*[@id='t12']/tbody/tr/td[1]/span[2]").text[10:11])
except:
    raise Exception("User is not in the system!")

#if more than one result returns, then there are multiple people with same Name
#this requires the user to do it manually
if result_count > 1:
    raise Exception("There are two staff members with the same name!")

user_id = driver.find_element_by_xpath("//*[@id='contentautoscroll']/form/table[2]/tbody/tr[2]/td[2]/a").text
#click on the user
driver.find_element_by_xpath("//*[@id='contentautoscroll']/form/table[2]/tbody/tr[2]/td[2]/a").click()

################################################################################
# IMPLEMENT DEVICE ASSOCIATION AND SET PRIMARY Extension
################################################################################
time.sleep(1)
#navigate to user device association
driver.find_element_by_xpath("//*[@id='contentautoscroll']/form/fieldset[5]/table/tbody/tr[1]/td[3]/input[1]").click()

#set search criteria
driver.find_element_by_xpath("//select[@name='searchField0']/option[text()='Directory Number']").click()
driver.find_element_by_xpath("//select[@name='searchLimit0']/option[text()='is exactly']").click()

#enter last name into search field
web_search_association = driver.find_element_by_name("searchString0")
web_search_association.click()
web_search_association.clear()
web_search_association.send_keys(extension)

#LETS GOO click find
driver.find_element_by_name("findButton").click()

#if no results come back, user is not in the system
try:
    result_count = (int)(driver.find_element_by_xpath("//*[@id='t12']/tbody/tr/td[1]/span[2]").text[10:11])
except:
    raise Exception("No device found!")

#if more than one result returns, then a popup window appears for confirmation
if result_count > 1:
    #creating window to check description, setting size, setting background
    window = tkinter.Tk()
    window.title("Phone Confirmation")
    window.geometry('270x250')
    window.configure(bg = "white")
    window.resizable(False,False)

    v = tkinter.IntVar()
    v.set(0)  # initializing the choice, i.e. Python

    tkinter.Label(window,
             text="""Choose your favourite programming language:""",
             justify = tkinter.LEFT,
             bg = "white",
             padx = 20).pack()

    for index in range(2, result_count+2):
        xpath = "//*[@id='contentautoscroll']/form/table[2]/tbody/tr[" + str(index) + "]/td[3]"
        tkinter.Radiobutton(window,
                      text = driver.find_element_by_xpath(xpath).text,
                      bg = "white",
                      padx = 20,
                      variable = v,
                      value = index).pack(anchor=tkinter.W)

    #custom button
    confirm_img = tkinter.PhotoImage(file = "C:\\Users\\nettechs\\Desktop\\Code\\reassign_extension\\confirm.png")
    confirm_button = tkinter.Button(window, bg = "white", image = confirm_img, command = input_choice)
    confirm_button.place(width = 150, height = 70, x = 50, y = 175)

    window.mainloop()

else:
    #choice is first option
    global choice
    choice = 2

#check the box
xpath = "//*[@id='contentautoscroll']/form/table[2]/tbody/tr[" + str(choice) + "]/td[1]/input[1]"
if driver.find_element_by_xpath(xpath).is_selected():
    pass
else:
    driver.find_element_by_xpath(xpath).click()
mac = driver.find_element_by_xpath("//*[@id='contentautoscroll']/form/table[2]/tbody/tr[" + str(choice) + "]/td[3]").text


#save selected/changes
driver.find_element_by_xpath("//*[@id='5tbl']").click()
driver.find_element_by_xpath("//*[@id='topnavbar']/table[2]/tbody/tr/td[2]/div/input").click()

#set primary extension
select_element = Select(driver.find_element_by_xpath("//*[@id='PRIMARYEXTENSION']"))
select_element.select_by_visible_text(extension + " in OnClusterPT")

#save changes
driver.find_element_by_xpath("//*[@id='1tbl']").click()

#navigate to phone search
driver.get("https://10.98.48.2/ccmadmin/phoneFindList.do")
#select criteria as directory number and set to exact
driver.find_element_by_xpath("//select[@name='searchField0']/option[text()='Directory Number']").click()
driver.find_element_by_xpath("//select[@name='searchLimit0']/option[text()='is exactly']").click()

#enter extension into search field
web_search_ext = driver.find_element_by_name("searchString0")
web_search_ext.click()
web_search_ext.clear()
web_search_ext.send_keys(extension)

#LETS GOO click find
driver.find_element_by_name("findButton").click()


#if no results come back, phone is not in the system
try:
    result_count = (int)(driver.find_element_by_xpath("//*[@id='t12']/tbody/tr/td[1]/span[2]").text[10:11])
except:
    raise Exception("No phone with that extension could be found.")

global mac_choice
if result_count > 1:
    #we need to find the index of the matching mac address
    for index in range(2, result_count+2):
        xpath = "//*[@id='contentautoscroll']/form[1]/table[2]/tbody/tr[" + str(index) + "]/td[3]/a"
        #substring of the mac itself
        compare_mac = driver.find_element_by_xpath(xpath).text[:-3]
        #if the mac address matches, save index and break loop
        if mac == compare_mac:
            mac_choice = index
            break

else:
    #default is first choice
    mac_choice = 2

#clicking the correct phone
xpath = "//*[@id='contentautoscroll']/form[1]/table[2]/tbody/tr[" + str(mac_choice) + "]/td[3]/a"
driver.find_element_by_xpath(xpath).click()

################################################################################
# IMPLEMENT DESCRIPTION and OWNER UPDATES AND SET NAME ON phone
################################################################################

#extracting phone description
phone_description = driver.find_element_by_xpath("//*[@id='DESCRIPTION']").get_attribute("value")
des_array = phone_description.split(",")

#removing last two elements
des_array.remove(des_array[len(des_array)-1])
des_array.remove(des_array[len(des_array)-1])

new_description = ""
for s in range(0,len(des_array)):
    new_description += des_array[s]
    new_description += ","

new_description = new_description + fname + ","
new_description = new_description + lname

#creating window to check description, setting size, setting background
window = tkinter.Tk()
window.title("Description Confirmation")
window.geometry('270x150')
window.configure(bg = "white")
window.resizable(False,False)

#description
enter_des = tkinter.Entry(window)
enter_des.insert(0,new_description)
enter_des.place(height=25,width=250,x=10,y=30)
tkinter.Label(window,font = "verdana 8", text = "New description:", bg = "white").place(x=10,y=5)

#custom button
confirm_img = tkinter.PhotoImage(file = "C:\\Users\\nettechs\\Desktop\\Code\\reassign_extension\\confirm.png")
confirm_button = tkinter.Button(window, bg = "white", image = confirm_img, command = input_description)
confirm_button.place(width = 150, height = 70, x = 60, y = 75)

window.mainloop()

#entering description into the input box
phone_des_input = driver.find_element_by_xpath("//*[@id='DESCRIPTION']")
phone_des_input.click()
phone_des_input.clear()
phone_des_input.send_keys(set_description)

#setting phone owner HERE
driver.find_element_by_xpath("//*[@id='userPhoner']").click()
driver.find_element_by_xpath("//*[@id='find_fkenduser']").click()

driver.switch_to.window(driver.window_handles[1])
# POP UP #
#####################################################################################################

#select criteria as last name and set to exact
driver.find_element_by_xpath("//select[@name='searchField0']/option[text()='Last name']").click()
driver.find_element_by_xpath("//select[@name='searchLimit0']/option[text()='is exactly']").click()

#enter last name into search field
web_search_name = driver.find_element_by_name("searchString0")
web_search_name.click()
web_search_name.clear()
web_search_name.send_keys(lname)

#select second criteria as first name and set to exact
#driver.find_element_by_xpath("//*[@id='filterRow0']/td[9]/button").click()
driver.find_element_by_xpath("//select[@name='searchField1']/option[text()='First name']").click()
driver.find_element_by_xpath("//select[@name='searchLimit1']/option[text()='is exactly']").click()

#enter first name into search field
web_search_name = driver.find_element_by_name("searchString1")
web_search_name.click()
web_search_name.clear()
web_search_name.send_keys(fname)

#LETS GOO click find
driver.find_element_by_name("findButton").click()

#if no results come back, user is not in the system
try:
    result_count = (int)(driver.find_element_by_xpath("//*[@id='t12']/tbody/tr/td[1]/span[2]").text[10:11])
except:
    raise Exception("User is not in the system!")

driver.find_element_by_xpath("//*[@id='contentautoscroll']/form/table[2]/tbody/tr[2]/td[1]/input[1]").click()
driver.find_element_by_xpath("//*[@id='7tbl']").click()

#switching back to main window
driver.switch_to.window(driver.window_handles[0])

###################################################################################################################

#saving description and owner
driver.find_element_by_xpath("//*[@id='2tbl']").click()

#Switch the control to the Alert window
obj = driver.switch_to_alert()
#use the accept() method to accept the alert
obj.accept()

#switch back to main window
time.sleep(2)
driver.switch_to.window(driver.window_handles[0])
#navigate to extension
driver.find_element_by_xpath("//*[@id='contentautoscroll']/form/table/tbody/tr/td[1]/fieldset/table/tbody/tr[2]/td[2]/u/a").click()

full_name = fname + " " + lname

#update description, alerting name, and ASCII Alerting name
ext_description = driver.find_element_by_xpath("//*[@id='DESCRIPTION']")
ext_alerting = driver.find_element_by_xpath("//*[@id='ALERTINGNAME']")
ext_ascii = driver.find_element_by_xpath("//*[@id='ALERTINGNAMEASCII']")

ext_description.click()
ext_description.clear()
ext_description.send_keys(set_description)

ext_alerting.click()
ext_alerting.clear()
ext_alerting.send_keys(full_name)

ext_ascii.click()
ext_ascii.clear()
ext_ascii.send_keys(full_name)

#update display asciidisplay, and linetext
ext_display = driver.find_element_by_xpath("//*[@id='DISPLAY']")
ext_ascii_display = driver.find_element_by_xpath("//*[@id='DISPLAYASCII']")
ext_line_text = driver.find_element_by_xpath("//*[@id='LABEL']")

ext_display.click()
ext_display.clear()
ext_display.send_keys(full_name)

ext_ascii_display.click()
ext_ascii_display.clear()
ext_ascii_display.send_keys(full_name)

ext_line_text.click()
ext_line_text.clear()
ext_line_text.send_keys(full_name)

#saving name UPDATES
driver.find_element_by_xpath("//*[@id='1tbl']").click()


driver.get("https://10.98.48.4/cuadmin/home.do")

unity_user = driver.find_element_by_xpath("/html/body/form/div[2]/table[1]/tbody/tr[1]/td[2]/table/tbody/tr[2]/td/input")
unity_pass = driver.find_element_by_xpath("/html/body/form/div[2]/table[1]/tbody/tr[1]/td[2]/table/tbody/tr[4]/td/input")

unity_user.click()
unity_user.clear()
unity_user.send_keys("nettechs")

unity_pass.click()
unity_pass.clear()
unity_pass.send_keys(upassword)
unity_pass.send_keys(Keys.RETURN)

sideframe = driver.find_element_by_xpath("//*[@id='tree']")
driver.switch_to.frame(sideframe)
driver.find_element_by_xpath("//*[@id='cutree_1']/a").click()

#switching back to main window
driver.switch_to.window(driver.window_handles[0])
mainframe = driver.find_element_by_xpath("//*[@id='bottomPane']/frame[2]")
driver.switch_to.frame(mainframe)

#select criteria as extension and set to exact
driver.find_element_by_xpath("//select[@name='searchField0']/option[text()='Extension']").click()
driver.find_element_by_xpath("//select[@name='searchLimit0']/option[text()='is exactly']").click()

#enter extension into search field
web_search_name = driver.find_element_by_name("searchString0")
web_search_name.click()
web_search_name.clear()
web_search_name.send_keys(extension)

#LETS GOO click find
driver.find_element_by_name("findButton").click()

#if no results come back, there is no previous voice mail box
old_fname = ""
old_lname = ""
try:
    result_count = (int)(driver.find_element_by_xpath("//*[@id='t12']/tbody/tr/td[1]/span[2]").text[10:11])
    old_fname = driver.find_element_by_xpath("//*[@id='searchGlobalUser']/table[3]/tbody/tr[2]/td[5]").text
    old_lname = driver.find_element_by_xpath("//*[@id='searchGlobalUser']/table[3]/tbody/tr[2]/td[6]").text
except:
    result_count = 0


if result_count > 0 and old_fname != fname and old_lname != lname:
    driver.find_element_by_xpath("//*[@id='objectId']").click()
    #deleting old voice mail box
    driver.find_element_by_xpath("//*[@id='DeleteSelectedButton']").click()
    #Switch the control to the Alert window
    obj = driver.switch_to_alert()
    #use the accept() method to accept the alert
    obj.accept()
    #switch back to main window
    time.sleep(3)
    driver.switch_to.window(driver.window_handles[0])

driver.switch_to.window(driver.window_handles[0])
driver.switch_to.frame(sideframe)

#importing user
driver.find_element_by_xpath("//*[@id='cutree_2']/a").click()

driver.switch_to.window(driver.window_handles[0])
driver.switch_to.frame(mainframe)

driver.find_element_by_xpath("//select[@name='mediaSwitchObjectId']/option[text()='UoPS Call Manager']").click()
driver.find_element_by_xpath("//select[@name='searchField']/option[text()='Extension']").click()
driver.find_element_by_xpath("//select[@name='searchCriteria']/option[text()='Is Exactly']").click()

#enter extension into search field
web_search_name = driver.find_element_by_name("searchString")
web_search_name.click()
web_search_name.clear()
web_search_name.send_keys(extension)

driver.find_element_by_xpath("//*[@id='search']").click()

import_index = 2
user_check = ""
while user_check != user_id:
    import_index = import_index + 1
    import_xpath = "/html/body/div/form/table/tbody/tr[" + str(import_index) + "]/td[2]"
    user_check = driver.find_element_by_xpath(import_xpath).text

id_path = import_index - 3
select_xpath = "//*[@id='" + str(id_path) + "']"

driver.find_element_by_xpath(select_xpath).click()
#import new user
driver.find_element_by_xpath("//*[@id='importUsersButton']").click()
time.sleep(2)

driver.switch_to.window(driver.window_handles[0])
driver.switch_to.frame(sideframe)

driver.find_element_by_xpath("//*[@id='cutree_1']/a").click()

driver.switch_to.window(driver.window_handles[0])
driver.switch_to.frame(mainframe)

driver.find_element_by_xpath("//*[@id='searchGlobalUser']/table[3]/tbody/tr[2]/td[3]/a").click()
driver.find_element_by_xpath("//select[@name='cosObjectId']/option[text()='Voice Mail plus Single Inbox COS']").click()

#saving
driver.find_element_by_xpath("//*[@id='control-buttons-save']").click()
time.sleep(2)

user_menu = driver.find_element_by_xpath("//*[@id='udm']/li[2]/a")
action = ActionChains(driver)
action.move_to_element(user_menu).perform()
time.sleep(1)
driver.find_element_by_xpath("//*[@id='menu-item-search-external-service-accounts']").click()

driver.find_element_by_xpath("/html/body/div/form/table/tbody/tr[1]/td/button[2]").click()
driver.find_element_by_xpath("//*[@id='externalServiceObjectId']/option[text()='webmail.pugetsound.edu']").click()
driver.find_element_by_xpath("//*[@id='actionRadioCorpEmail']").click()

driver.find_element_by_xpath("//*[@id='enableTtsOfEmailCapability']").click()
driver.find_element_by_xpath("//*[@id='enableCalendarCapability']").click()

driver.find_element_by_xpath("//*[@id='control-buttons-save']").click()
time.sleep(2)

driver.get("https://webmail.pugetsound.edu")

email_user = driver.find_element_by_xpath("//*[@id='username']")
email_user.click()
email_user.clear()
email_user.send_keys("nettechs")

email_pass = driver.find_element_by_xpath("//*[@id='password']")
email_pass.click()
email_pass.clear()
email_pass.send_keys(password)
email_pass.send_keys(Keys.RETURN)
driver.implicitly_wait(10)

time.sleep(2)
driver.find_element_by_xpath("/html/body/div[2]/div/div[3]/div[3]/div/div[1]/div[2]/div[1]/div[2]/div/div[1]/button[1]").click()

user_email = user_id + "@pugetsound.edu"
time.sleep(8)
email_to = driver.find_element_by_xpath("/html/body/div[2]/div/div[3]/div[3]/div/div[1]/div[2]/div[7]/div/div/div[3]/div[2]/div[1]/div[3]/div[1]/div[2]/div/div/span/div[1]/form/input")
email_to.click()
email_to.send_keys(user_email)

email_subject = driver.find_element_by_xpath("/html/body/div[2]/div/div[3]/div[3]/div/div[1]/div[2]/div[7]/div/div/div[3]/div[2]/div[1]/div[7]/div/div/input")
email_subject.click()
email_subject.send_keys("TICK:")

writeframe = driver.find_element_by_xpath("//*[@id='EditorBody']")
driver.switch_to.frame(writeframe)

editor = driver.find_element_by_xpath("//*[@id='MicrosoftOWAEditorRegion']")
editor.send_keys("Hi " + fname + ",\n\n")
editor.send_keys('''I am contacting you regarding the ticket that was submitted for an extension reassignment. As you requested, extension x''' + extension + ''' has been reassigned to ''' + full_name + '''. We have enabled voicemail-to-email for your account and your voicemail PIN has been set to 1234. You will be prompted to change this when logging in for your first time. If there's anything else you need assistance with, please feel free to contact us!\n\nNettechs\nNetwork Technicians\nTechnology Services, University of Puget Sound\n1500 N. Warner St., Tacoma, WA 98416-1068 \nnettechs@pugetsound.edu\nOffice: Library #027\n(253) 879-2605 - Office''')


#driver.close()

# celebration
root = tkinter.Tk()
frames = [tkinter.PhotoImage(file='C:\\Users\\nettechs\\Desktop\\Code\\reassign_extension\\dancing.gif',format = 'gif -index %i' %(i)) for i in range(100)]

def update(ind):
    frame = frames[ind]
    ind += 1
    label.configure(image=frame)
    if ind == 99:
        ind = 1
    root.after(50, update, ind)
label = tkinter.Label(root)
label.pack()
root.after(0, update, 0)
root.mainloop()
