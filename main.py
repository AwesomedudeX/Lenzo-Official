import streamlit as st

import time
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn

from PIL import Image

st.set_page_config("Lenzo Official Website", layout="wide", initial_sidebar_state="expanded", page_icon="logo.png")
pd.set_option("display.max_rows", None, "display.max_columns", None)

sidebar = st.sidebar
expander = st.expander
refresh = sidebar.button(':red[**Refresh Page**]')

pages = {
    "Homepage": 0,
    "About Us": 1,
    "Picture Editing": 2
}

def loaddata():
    import userdata as src
    return src.accountdata

def savedata(data):
    write = f"accountdata = {data}"
    open("userdata.py", "w").write(write)

if ['accountid', 'loginstatus', 'email', 'phonenumber', 'password', 'accounts', 'promptconfirm'] not in st.session_state:

    st.session_state.promptconfirm = False

    st.session_state.accountid = 0
    st.session_state.email = ""
    st.session_state.phonenumber = ""
    st.session_state.password = ""
    st.session_state.name = ""

    try:
        
        import userdata as src
        st.session_state.accounts = src.accountdata

    except:

        st.session_state.accounts = {
            'ids': [1],
            'emails': ['admin@lenzo.com'],
            'phonenumbers': ['(825) 762-6822'],
            'passwords': ['1162008'],
            'names': ['Admin'],
            'images': [['Aged Gold.png', 'Chrome Silver.png', 'Carbon Black.png', 'Cold Steel.png']]
        }

        savedata(st.session_state.accountdata)

loginstatuscol = sidebar.columns(1)[0]
loginexpander = sidebar.expander(":blue[**Sign In**]")

loginchoice = loginexpander.radio("**Would you like to sign into an account, or sign up for an account?**", ["Sign In", "Sign Up"])

if loginchoice == "Sign In":
    
    loginexpander.title(":green[Sign In:]")
    st.session_state.email = loginexpander.text_input("**Email:**")
    st.session_state.password = loginexpander.text_input("**Password:**", type="password")

else:
    
    loginexpander.title(":blue[Sign Up:]")
    
    st.session_state.email = loginexpander.text_input("**Email:**")
    st.session_state.phonenumber = loginexpander.text_input("**Phone Number (Optional):**")
    st.session_state.password = loginexpander.text_input("**Password:**", type="password")
    st.session_state.name = loginexpander.text_input("**Name:**")

if loginchoice == "Sign Up":

    if "@" not in st.session_state.email and "." not in st.session_state.email[-4:]:
        loginexpander.write("Please enter a valid email.")

    elif loginexpander.button(":green[**Sign Up**]", use_container_width=True):

        if st.session_state.email in st.session_state.accounts["emails"]:
            loginexpander.write("**An account with this email :red[already exists]. Please :blue[sign in] with this email, or create a :green[new] account.**")

        else:

            st.session_state.accounts["ids"].append(len(st.session_state.accounts["ids"])+1)              
            st.session_state.accounts["emails"].append(st.session_state.email)                
            st.session_state.accounts["phonenumbers"].append(st.session_state.phonenumber)
            st.session_state.accounts["passwords"].append(st.session_state.password)                
            st.session_state.accounts["names"].append(st.session_state.name)                
            st.session_state.accounts["images"].append([])                

            try:
                loginexpander.write("**Account created :green[successfully]! Please :blue[sign in] with your new **:blue[Lenzo]** account.**")                
                time.sleep(5)
                savedata(st.session_state.accounts)
                
            except:

                try:
                    savedata(st.session_state.accounts)
                except:
                    loginexpander.write("**There was an :red[error] in creating your account. Please click the :green[Sign Up] button again.**")                
                    

            st.session_state.accounts = loaddata()

else:
            
    if st.session_state.email != "" and st.session_state.password != "":

            if st.session_state.email not in st.session_state.accounts["emails"]:
                loginexpander.write("**Sorry, but we could :red[not] find your account. Please :blue[try again] with another email, or create a :green[new] account.**")

            else:

                for i in range(len(st.session_state.accounts["ids"])):
                
                    if st.session_state.email == st.session_state.accounts["emails"][i]:
                        
                        if st.session_state.password == st.session_state.accounts['passwords'][i]:
                            
                            st.session_state.accountid = st.session_state.accounts['ids'][i]
                            st.session_state.name = st.session_state.accounts["names"][i]
                            st.session_state.phonenumber = st.session_state.accounts["phonenumbers"][i]
                            
                            loginexpander.subheader(f":blue[Hello] {st.session_state.accounts['names'][st.session_state.accountid-1]}!")

                        else:
                            loginexpander.write("**:red[Incorrect] email/password. Please :blue[try again].**")

                        break

if st.session_state.accountid == 0:
    loginstatuscol.subheader("Signed in as :green[Guest]")
    loginstatuscol.write("**You'll need to :green[log in] to upload/view photos or :blue[order] products.**")

else:

    loginstatuscol.subheader(f"Signed in as :blue[{st.session_state.accounts['names'][st.session_state.accountid-1]}]")
    pages["Order Online"] = 3
    pages["My Photos"] = 4
    pages["My Account"] = 5

    if st.session_state.name == "Admin":
        pages["User Information"] = 6

page = sidebar.selectbox(f"**:red[Navigation:]**", pages)
pageindex = pages[page]
camcolors = ["Carbon Black", "Cold Steel", "Aged Gold", "Chrome Silver"]

if pageindex == 0:
    st.title(":blue[Lenzo Cameras Inc.]")

else:

    st.title(f":blue[{page}]")

    if pageindex == 3:
        
        cols = st.columns(2)
        c1 = cols[0].columns(2)

        color = c1[0].selectbox("**Select your :blue[color]:**", camcolors)
        edition = c1[1].selectbox("**Select your camera :blue[version]:**", ["Lite", "Pro"])
        cols[0].expander("**:blue[Camera Preview]**").image(f"{color}.png")

        if edition == "Lite":
            camprice = 249.99
        else:
            camprice = 299.99

        st.header(":blue[Order] Information")
        
        address = st.text_input(":red[**City:**]")
        province = st.selectbox(":red[**Province/Territory:**]", ["Alberta", "British Columbia", "Manitoba", "New Brunswick", "Newfoundland and Labrador", "Nova Scotia", "Ontario", "Prince Edward Island", "Quebec", "Saskatchewan", "Northwest Territories", "Nunavut Territories", "Yukon Territories"])
        address = st.text_input(":red[**Address:**]")
        postalcode = st.text_input(":red[**Postal Code:**]")

        st.write("---")

        paymethod = st.selectbox("**:blue[Payment Method]**", ["Credit", "Debit"])
        provider = st.selectbox("**:blue[Card Provider]**", ["MasterCard", "Visa", "TD", "RBC", "American Express", "BMO"])
        cardnum = "".join(st.text_input(":blue[**Card Number (#### #### ####)**]").split(" "))
        pin = st.text_input(":blue[**PIN (####):**]")
        priority = st.checkbox("**:green[Express Delivery] (+$10 per order)**")

        if cardnum != "" and pin != "":

            if len(cardnum) == 12 and len(pin) in [3, 4]:

                try:
                    cardnum = int(cardnum)
                    pin = int(pin)
                    invalidpaymentinfo = False

                except:
                    invalidpaymentinfo = True
                    st.write("**Please enter a :red[valid] PIN number/card number.**")

            else:
                invalidpaymentinfo = True
                st.write("**Please enter a :red[valid] PIN number/card number.**")

        else:
            invalidpaymentinfo = True

        st.write("---")
        st.write(f"**:blue[LenzoCam]: ${camprice}**")
        
        st.write(f"**Subtotal: ${camprice}**")
        st.write("**Tax: 15%**")

        if priority:
            prioritycost = 10
            delivertime = "1-3 business days."
            st.write(f"**:green[Express Delivery]: ${prioritycost}.00**")
        else:
            prioritycost = 0
            delivertime = "5-7 business days."

        st.write(f"**:red[Grand Total]: ${round((camprice)*1.15+prioritycost, 2)}**")
        st.write(f"**:green[Delivery Time]: {delivertime}**")

        if not invalidpaymentinfo and st.button(":blue[**Order Now!**]"):

            st.write(f"**Order placed :green[successfully]! Your order will :blue[arrive] in around {delivertime} We'll :blue[notify] you when it gets there.**")

    if pageindex == 4:

        mode = sidebar.radio("**What do you want to do?**", ["**:blue[My Photos]**", "**:red[Delete] Photos**", "**:green[Upload] Photos**"])

        if mode == "**:green[Upload] Photos**":

            file = st.file_uploader("**Upload photos :green[here]:**")

            if file and st.button("Upload"):

                if file.name[-4:] in [".png", ".jpg"]:
                    open(file.name, "wb").write(file.read())
                    st.session_state.accounts['images'][st.session_state.accountid-1].append(file.name)
                    st.write(f"**:green[Successfully] uploaded :blue[{file.name}]**.")
                    img = Image.open(file.name)
                    st.image(img)

                else:
                    st.write("**:red[Unsupported file type]. Please upload a .:blue[png] or .:blue[jpg] file.**")


            if st.button("**Or sync photos from your :blue[LenzoCam]**"):
                
                st.subheader(":green[Syncing] your photos. Please :blue[wait]...")

                uploadstage = "comparing"

                try:

                    st.write("***:blue[Comparing Photos...]***")
                    time.sleep(1)

                    st.write("***:blue[Identifying Photos to Upload...]***")
                    time.sleep(0.7)

                    st.write("***:blue[Uploading Photos...]***")
                    time.sleep(2)
                
                    try:
                        st.write("**:green[Sync Complete!]**")

                    except:
                        pass

                except:
                    st.write("**Upload :red[Canceled].**")

        elif mode == "**:red[Delete] Photos**":

            photos = st.session_state.accounts['images'][st.session_state.accountid-1]
            maxcols = 5

            if photos and len(photos) < 6:
                maxcols = len(photos)
            
            numcols = sidebar.number_input("How many columns do you want to view these photos in?", 1, maxcols, step=1)
            photo = sidebar.selectbox("**Which photo do you want to :red[delete]?**", photos)

            if sidebar.button("**:red[Delete Photo]**"):

                for i in range(len(photos)):
                    if photos[i] == photo:
                        st.session_state.accounts['images'][st.session_state.accountid-1].pop(i)
                        break

                sidebar.write("**Photo :red[Deleted] :green[Successfully].**")

                try:
                    time.sleep(5)
                    savedata(st.session_state.accounts)
                except:
                    savedata(st.session_state.accounts)

            st.write("---")

            @st.cache_data()
            def showPhotos(photos, numcols):

                cols = st.columns(numcols)
                colindex = 0
    
                for filename in photos:
                    
                    img = Image.open(filename)
                    cols[colindex].image(img, use_column_width=True, caption=filename)

                    colindex += 1

                    if colindex == numcols:
                        colindex = 0

            showPhotos(photos, numcols)

        else:

            photos = st.session_state.accounts['images'][st.session_state.accountid-1]
            maxcols = 5

            if photos and len(photos) < 6:
                maxcols = len(photos)
            
            numcols = sidebar.number_input("**How many columns do you want to view these photos in?**", 1, maxcols, step=1)

            st.write("---")

            @st.cache_data()
            def showPhotos(photos, numcols):

                cols = st.columns(numcols)
                colindex = 0
    
                for filename in photos:
                    
                    img = Image.open(filename)
                    cols[colindex].image(img, use_column_width=True, caption=filename)

                    colindex += 1

                    if colindex == numcols:
                        colindex = 0

            showPhotos(photos, numcols)

            photo = sidebar.selectbox("**Choose a photo to :blue[download]:**", photos)
            
            if sidebar.download_button("**:blue[Download Photo]**", open(photo, "rb").read(), photo):
                sidebar.write("**Downloaded Photo :green[Successfully]!**")

    if pageindex == 5:
        
        name = st.text_input(":blue[**Name:**]", st.session_state.name)
        email = st.text_input(":blue[**Email:**]", st.session_state.email)        
        phonenum = st.text_input(":blue[**Email:**]", st.session_state.phonenumber)        
        pwd = st.text_input(":blue[**Password:**]", st.session_state.password, type="password")

        if st.button("**:green[Save]**"):

            st.session_state.name = name
            st.session_state.email = email
            st.session_state.phonenumber = phonenum
            st.session_state.password =  pwd

            st.session_state.accounts["emails"][st.session_state.accountid-1] = st.session_state["email"]
            st.session_state.accounts["phonenumbers"][st.session_state.accountid-1] = st.session_state["phonenumber"]
            st.session_state.accounts["passwords"][st.session_state.accountid-1] = st.session_state["password"]
            st.session_state.accounts["names"][st.session_state.accountid-1] = st.session_state["name"]

            try:
                st.write("**Account information saved :green[successfully].**")
                time.sleep(5)
                savedata(st.session_state.accounts)

            except:
                savedata(st.session_state.accounts)

    if pageindex == 6:

        df = pd.DataFrame()

        df["Account ID"] = st.session_state.accounts['ids']
        df["Name"] = st.session_state.accounts['names']
        df["Email"] = st.session_state.accounts['emails']
        df["Phone Number"] = st.session_state.accounts['phonenumbers']

        st.dataframe(df, use_container_width=True, hide_index=True)

        if sidebar.button("**:red[Reset User Data]**"):
            
            for col in st.session_state.accounts:
                st.session_state.accounts[col] = []

            st.session_state.accounts = {
                'ids': [1],
                'emails': ['admin@lenzo.com'],
                'phonenumbers': ['(825) 762-6822'],
                'passwords': ['1162008'],
                'names': ['Admin'],
                'images': [['Aged Gold.png', 'Chrome Silver.png', 'Carbon Black.png', 'Cold Steel.png']]
            }

            try:
                sidebar.write("**User data :red[reset] :green[successfully].**")
                time.sleep(5)
                savedata(st.session_state.accounts)
            except:
                savedata(st.session_state.accounts)
