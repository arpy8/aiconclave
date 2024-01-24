import json
import time
import requests
import streamlit as st
from streamlit_option_menu import option_menu

from aiconclave.constants import *
import aiconclave.games.tekken as tkk
import aiconclave.games.pin_ball as pb
import aiconclave.games.road_rash as rr
import aiconclave.games.motor_rider as mr
import aiconclave.games.chrome_dino as cd


css_style = {
    "icon": {"color": "white"},
    "nav-link": {"--hover-color": "grey"},
    "nav-link-selected": {"background-color": "#3f9699"},   
}

st.set_page_config(page_title="AI Conclave", page_icon="https://avatars.githubusercontent.com/u/80619013?s=200&v=4")

misc_11, misc_12, misc_13 = st.columns(3)

with misc_11, misc_13:
    st.empty()

with misc_12:
    st.image("https://aiconclave.aivitb.com/img/aic%202.png")

with st.sidebar:
    st.write("<br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
    selected_task = option_menu(
        menu_title=None,
        options=["Home", "Settings", "Halp"],
        icons=["house", "gear", "person"],
        styles=css_style
    )

if selected_task == "Home":
    st.write("<center><h1>Mediapipe Scripts Control Panel</h1></center><br>", unsafe_allow_html=True)
    
    if st.button("Tekken Game", use_container_width=True):
        tkk.main()
    if st.button("Road Rash", use_container_width=True):
        rr.main()
    if st.button("Chrome Dino", use_container_width=True):
        cd.main()
    if st.button("Pin Ball", use_container_width=True):
        pb.main()
    if st.button("Motor Rider", use_container_width=True):
        mr.main()

    st.write("<br><br>", unsafe_allow_html=True)

    if st.button("FAILSAFE", use_container_width=True):
        st.toast("""yeah this doesn't work lol, close the terminal window to stop the script""")
        exit()


elif selected_task == "Settings":
    st.write("<center><h1>Game Constants</h1></center>", unsafe_allow_html=True)
    
    with open(path_converter('assets/config.json'), 'r') as json_file:
        data = json.load(json_file)

    st.write("## Tekken")
    tekken_random_lower = st.number_input("Tekken Random Lower Value", value=data["TEKKEN"]["RANDOM_LOWER"], step=10, key="tekken_random_lower")
    tekken_random_upper = st.number_input("Tekken Random Upper Value", value=data["TEKKEN"]["RANDOM_UPPER"], step=10, key="tekken_random_upper")
    tekken_threshold = st.number_input("Tekken Threshold", value=data["TEKKEN"]["THRESHOLD"], step=10, key="tekken_threshold")
    tekken_rpunch_angle_lthresh = st.number_input("Tekken Right Punch Angle Lower Threshold", value=data["TEKKEN"]["RPUNCH_ANGLE_LTHRESH"], step=5, key="tekken_rpunch_angle_lthresh")
    tekken_rpunch_angle_uthresh = st.number_input("Tekken Right Punch Angle Upper Threshold", value=data["TEKKEN"]["RPUNCH_ANGLE_UTHRESH"], step=5, key="tekken_rpunch_angle_uthresh")
    tekken_lpunch_angle_lthresh = st.number_input("Tekken Left Punch Angle Lower Threshold", value=data["TEKKEN"]["LPUNCH_ANGLE_LTHRESH"], step=5, key="tekken_lpunch_angle_lthresh")
    tekken_lpunch_angle_uthresh = st.number_input("Tekken Left Punch Angle Upper Threshold", value=data["TEKKEN"]["LPUNCH_ANGLE_UTHRESH"], step=5, key="tekken_lpunch_angle_uthresh")
    data["TEKKEN"]["RANDOM_LOWER"] = tekken_random_lower
    data["TEKKEN"]["RANDOM_UPPER"] = tekken_random_upper
    data["TEKKEN"]["THRESHOLD"] = tekken_threshold
    data["TEKKEN"]["RPUNCH_ANGLE_LTHRESH"] = tekken_rpunch_angle_lthresh
    data["TEKKEN"]["RPUNCH_ANGLE_UTHRESH"] = tekken_rpunch_angle_uthresh
    data["TEKKEN"]["LPUNCH_ANGLE_LTHRESH"] = tekken_lpunch_angle_lthresh
    data["TEKKEN"]["LPUNCH_ANGLE_UTHRESH"] = tekken_lpunch_angle_uthresh

    st.write("## Road Rash")
    road_rash_x_threshold = st.number_input("Road Rash Accelerate Threshold", value=data["ROAD_RASH"]["X_THRESHOLD"], step=10, key="road_rash_x_threshold")
    road_rash_left_threshold = road_rash_right_threshold = st.number_input("Road Rash Left/Right Threshold", value=data["ROAD_RASH"]["LEFT_THRESHOLD"], step=10, key="road_rash_left_threshold")
    data["ROAD_RASH"]["X_THRESHOLD"] = road_rash_x_threshold
    data["ROAD_RASH"]["LEFT_THRESHOLD"] = data["ROAD_RASH"]["RIGHT_THRESHOLD"] = road_rash_left_threshold

    st.write("## Chrome Dino")
    dino_jump_threshold = st.number_input("Dino Jump Threshold", value=data["CHROME_DINO"]["UP_THRESHOLD"], step=10, key="dino_jump_threshold")
    data["CHROME_DINO"]["UP_THRESHOLD"] = dino_jump_threshold

    st.write("## Pin Ball")
    pinball_left_threshold = pinball_right_threshold = st.number_input("Pin Ball Left/Right Threshold", value=data["PIN_BALL"]["LEFT_THRESHOLD"], step=10, key="pinball_left_threshold")
    data["PIN_BALL"]["LEFT_THRESHOLD"] = data["PIN_BALL"]["RIGHT_THRESHOLD"] = pinball_left_threshold

    st.write("## Motor Rider")
    motor_left_threshold = motor_right_threshold = st.number_input("Motor Left/Right Threshold", value=data["MOTOR_RIDER"]["LEFT_THRESHOLD"], step=10, key="motor_left_threshold")
    motor_down_threshold = st.number_input("Motor Down Threshold", value=data["MOTOR_RIDER"]["DOWN_THRESHOLD"], step=10, key="motor_down_threshold")
    data["MOTOR_RIDER"]["LEFT_THRESHOLD"] = data["MOTOR_RIDER"]["RIGHT_THRESHOLD"] = motor_left_threshold
    data["MOTOR_RIDER"]["DOWN_THRESHOLD"] = motor_down_threshold


    with open(path_converter('assets/config.json'), 'w') as json_file:
        json.dump(data, json_file, indent=2)
        

elif selected_task == "Halp": 
    st.text_input("Enter your name here *", key="name")    
    st.text_input("Enter your query here", key="query")
    st.text_input("Where you at?", key="loc")
    
    st.button("Submit", key="submit")

    if st.session_state.submit and st.session_state.name:
        requests.post(
            url="https://universal-api.onrender.com/data", 
            headers = {
                "Authorization": AUTH_TOKEN
            },
            json={
                "id": ID,
                "message": MESSAGE_TEMPLATE.format(st.session_state.name, st.session_state.query, st.session_state.loc)
            }
        )
        
        st.toast("request received, omw 🏃‍♂️🏃‍♂️💨")
        
        misc_21, misc_22, misc_23 = st.columns(3)
        with misc_21, misc_23:
            st.empty()
        with misc_22:
            salute = st.empty()
            salute.image("https://i.imgflip.com/2/7iiiq9.jpg")
            time.sleep(4)
            salute.empty()
        
    elif st.session_state.submit and not st.session_state.name:
        st.toast("enter your name 🗣️")