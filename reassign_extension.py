from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import tkinter
from playsound import playsound
import time
import os

#global variables to hold information
password = ""
fname = ""
lname = ""
extension = ""
set_description = ""
global choice

#this function assigns the global variables to the info collected by
#network chan
def input_info():
    playsound('reassign_extension/disgust.wav')

    #retrieving and assigning information
    global password
    password = enter_pass.get()
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

#password
enter_pass = tkinter.Entry(window, show="*")
enter_pass.place(height=20,width=150,x=10,y=125)
tkinter.Label(window, font = "verdana 10", text = "Password", bg = "white").place(x=10,y=100)

#first name
enter_fname = tkinter.Entry(window)
enter_fname.place(height=20,width=150,x=10,y=175)
tkinter.Label(window,font = "verdana 10", text = "First Name", bg = "white").place(x=10,y=150)

#last name
enter_lname = tkinter.Entry(window)
enter_lname.place(height=20,width=150,x=10,y=225)
tkinter.Label(window,font = "verdana 10", text = "Last Name", bg = "white").place(x=10,y=200)

#extension
enter_ext = tkinter.Entry(window)
enter_ext.place(height=20,width=50,x=10,y=275)
tkinter.Label(window,font = "verdana 10", text = "Ext.", bg = "white").place(x=10,y=250)

#custom button
hurts = tkinter.PhotoImage(file = "reassign_extension/hurts.png")
tkinter.Button(window, command = input_info, image = hurts, bg = "white").place(height=45, width = 100, x=75, y = 250)

#add in the pictures for the title and greeting anime girl
icon = tkinter.PhotoImage(file = "reassign_extension/network_chan.png")
tkinter.Label(window, image = icon, bg="white").place(x=175,y=5)

title = tkinter.PhotoImage(file = "reassign_extension/title.png")
tkinter.Label(window, image = title, bg = "white").place(x=5,y=5)

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

#click on the user
driver.find_element_by_xpath("//*[@id='contentautoscroll']/form/table[2]/tbody/tr[2]/td[2]/a").click()

################################################################################
# IMPLEMENT DEVICE ASSOCIATION AND SET PRIMARY Extension
################################################################################

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
    confirm_img = tkinter.PhotoImage(file = "reassign_extension/confirm.png")
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
confirm_img = tkinter.PhotoImage(file = "reassign_extension/confirm.png")
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

driver.close()

# celebration
root = tkinter.Tk()
frames = [tkinter.PhotoImage(file='reassign_extension/dancing.gif',format = 'gif -index %i' %(i)) for i in range(100)]

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
