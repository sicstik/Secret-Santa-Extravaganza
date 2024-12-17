import random
import Send_Email
import streamlit as st
import urllib.parse
import re

key_gift_concept = 'gift_concept'
key_participants = 'participants'
key_output_participants = 'output_participants'
key_output_finish = 'output_finish'

if key_gift_concept not in st.session_state:
    st.session_state[key_gift_concept] = {}
if key_participants not in st.session_state:
    st.session_state[key_participants] = {}
if key_output_participants not in st.session_state:
    st.session_state[key_output_participants] = {}
if key_output_finish not in st.session_state:
    st.session_state[key_output_finish] = ''

def extract_max_cost(input_string):
    # Use regex to find digits in the string
    match = re.search(r'\d+', input_string)

    if match:
        return int(match.group())  # Convert the matched digits to an integer
    else:
        return None  # Return None if no digits are found

def commit(body_text, is_amazon, chaotic):
    max_cost = extract_max_cost(st.session_state[key_gift_concept]['cost'])

    used_names = []
    i = 0
    receivers = list(st.session_state[key_participants].keys())
    random.shuffle(receivers)
    for name, email in st.session_state[key_participants].items():
        while True:
            if receivers[i] not in used_names and receivers[i] != name:
                message = f"""Subject: Super Friend Secret Santa Extravaganza!

Hi {name}! You are {receivers[i]}'s Secret Santa :D                
{body_text}
"""
                if is_amazon:
                    link = amazon_link(st.session_state[key_gift_concept]['gift_concept'], max_cost, chaotic)
                    message += f"\nAmazon Link for a random item meeting the theme and cost needs!:\n{link}"
                Send_Email.send_email_button(message, email)
                used_names.append(receivers[i])
                i += 1
                break
            else:
                random.shuffle(receivers)

def create_default_message():
    gift_concept = st.session_state[key_gift_concept]
    default_message = f"""
Gift Theme: 
{gift_concept['gift_concept']}

Cost:
Under {gift_concept['cost']}

Location:
{gift_concept['location']}

Date:
{gift_concept['date']}

Time:
{gift_concept['time']}
    """
    return default_message

def amazon_link(theme, max_cost, chaotic):
    base_url = "https://www.amazon.com/s?"

    # Search Parameters
    if chaotic:
        keywords = ''
    else:
        keywords = theme
    price_max = max_cost
    random_page = random.randint(1, 10)  # Random page number (1-10)

    # Amazon search query structure
    params = {
        "k": keywords,  # Search keywords
        "s": "price-asc-rank",  # Sort by price (ascending)
        "low-price": price_max/2,  # Min price
        "high-price": price_max,  # Max price
        "page": random_page,  # Random page to simulate randomness
        "i": "aps"  # 'aps' means 'All Products' to avoid apps/videos
    }

    # Encode the parameters into a URL string
    query_string = urllib.parse.urlencode(params)
    amazon_url = base_url + query_string

    return amazon_url

st.set_page_config(page_title="Secret Santa Extravaganza", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
        <style>
               .block-container {
                    padding-top: 3rem;
                    padding-bottom: 2rem;
                    padding-left: 15rem;
                    padding-right: 15rem;
                }
                .stDeployButton {
                        visibility: hidden;
                    }
                #MainMenu {visibility: hidden;}
        </style>
        """, unsafe_allow_html=True)

st.subheader(":green[Main Secret Santa Input]")

with st.container(height=400):
    input_gift_concept = st.text_input("Gift Theme:", placeholder='Every Day Items')
    input_cost = st.text_input("Gift Max Cost:", placeholder="$20")
    input_location = st.text_input("Location:", placeholder="House Address")
    input_date = st.text_input("Meetup Date:", placeholder="12/25")
    input_time = st.text_input("Meetup Time:", placeholder='2pm')
if st.button(":green[Apply]", use_container_width=True):
    gift_concept = st.session_state[key_gift_concept]
    gift_concept['gift_concept'] = input_gift_concept
    gift_concept['cost'] = input_cost
    gift_concept['location'] = input_location
    gift_concept['date'] = input_date
    gift_concept['time'] = input_time

    st.session_state[key_gift_concept] = gift_concept
    st.toast("Applied")

st.write(' ')

st.subheader(":green[Secret Santa Guests]")
c1, c2 = st.columns(2)
with c1:
    input_name = st.text_input("Input Participant:", key='name_input')
with c2:
    input_email = st.text_input("Input Participant Email:", key='email_input')
if st.button(":green[Add]", use_container_width=True):
    participants = st.session_state[key_participants]
    if input_name and input_email:
        participants[input_name] = input_email

        st.session_state[participants] = participants
    st.rerun()

st.write(":blue[Added Participants:]")
with st.container(height=200):
    i = 1
    for participant, email in st.session_state[key_participants].items():
        c1, c2 = st.columns((1, 3))
        with c1:
            st.write(f"{participant}: {email}\n")
        with c2:
            delete_button = st.button(":red[Delete]", key=f"{participant} {i}")
            if delete_button:
                del st.session_state[key_participants][participant]
                st.rerun()
        i += 1

if len(st.session_state[key_participants].keys()) > 1:
    st.subheader(":green[Email Message Review]")
    body_text = st.text_area("Body:", value=create_default_message(), height=500)
    amazon_checkbox = st.checkbox("Add Amazon Link to item based on theme")
    chaotic = st.checkbox("Chaotic Mode (Completely Random Amazon Link up to Max Cost)")
    send_button = st.button("Send Emails!")
    if send_button:
        commit(body_text, amazon_checkbox, chaotic)
        st.toast(":green[Success!!!!]")

else:
    st.write(":red[Need 2 or more participants to continue]")


# if __name__ == '__main__':
#     select_person()