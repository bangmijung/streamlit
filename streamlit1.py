import re
import time
import json
import datetime
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_tags import st_tags
from streamlit_option_menu import option_menu
import openai

###################################################################################################
# 0. dataset
import os
json_lst = os.listdir("C:/Users/bangm/Desktop/AI융합캡스톤디자인과창업/info")
total_df = pd.DataFrame([])
for json_name in json_lst:
    with open("C:/Users/bangm/Desktop/AI융합캡스톤디자인과창업/info/"+json_name, "r",encoding='utf-8') as db_anno_json:
        db_anno = json.load(db_anno_json)
        db_anno_df = pd.DataFrame(db_anno["data"])
        total_df = pd.concat([total_df,db_anno_df],axis=0)
total_df.reset_index(drop=True, inplace=True)
###################################################################################################
# 1. page config & title
st.set_page_config(layout="centered", page_title="20180802방미정_중간과제", page_icon="⚡")
st.title("⚡ Query Up!")
st.text("AI융합캡스톤디자인과창업_20180802방미정_chatGPT활용_중간과제")
###################################################################################################
# 2. gpt info - api key, version
gpt_ver = st.radio(label = "GPT3.5-turbo or GPT3.5-turbo-16k or GPT4.0", options=["gpt-3.5-turbo", "gpt-3.5-turbo-16k","gpt-4"])
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
api_key = st.text_input(label="Open AI에서 발급받은 API KEY를 입력하세요!",type="password", placeholder="API KEY")
openai.api_key = api_key
st.divider()
###################################################################################################
# 3. horizontal menu - report, chat
selected2 = option_menu(None, ["Query decoder", "Chat with GPT"], 
    icons=['cloud-upload', 'gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal")
###################################################################################################
# 4. function - report, chat
def correct_indent(query, gpt_ver):
    messages = []
    try:
        f_string = f"{query} 쿼리의 인덴트를 수정해줘. 쿼리 외에는 아무 말도 하지 마"
        messages = []
        if f_string:
            messages.append(
                {"role": "user", "content": f_string},
            )
            chat = openai.ChatCompletion.create(
                model=gpt_ver, messages=messages
            )
            reply = chat.choices[0].message.content
    except:
        reply = ""
        pass
    return reply

def query_with_gpt(table_info_original, table_info, query, col_info, gpt_ver):
    messages = []
    try:
        f_string = f"""테이블 정보는 다음과 같아.
테이블명 : {str(table_info)}, 테이블명 의미 : {str(table_info)}
{str(col_info)}

위 테이블 정보를 바탕으로 {query} 쿼리를 해석해줘.
비전문가 입장에서 이해가 쉽게 최대한 쉬운 용어로 간결하게 설명해줘.
그리고 존댓말로 대답해줘."""
        messages = []
        if f_string:
            messages.append(
                {"role": "user", "content": f_string},
            )
            chat = openai.ChatCompletion.create(
                model=gpt_ver, messages=messages
            )
            reply = chat.choices[0].message.content
    except:
        reply = "fail"
        pass
    
    return reply

def submit_test():
    with st.expander('사용자가 입력한 Query', expanded=True) :
        my_bar = st.progress(0, text=None)
        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=None)
        my_bar.empty()
        
        with st.chat_message("ai"):
            st.write("**Query Up! Robot**")
            with st.spinner('⚡ Wait for it...'):
                # 코드 인덴트 교정
                time.sleep(0.1)
                st.write("당신이 입력한 쿼리의 들여쓰기를 교정한 결과는 다음과 같습니다.")
                st.code(correct_indent(text, gpt_ver), language='sql', line_numbers=True)
                st.caption("👋🏻 코드블럭 오른쪽 :blue[아이콘]을 클릭하면 query를 복사할 수 있습니다.")
                
                # 테이블 정보 조회
                time.sleep(0.1)
                pattern1 = re.compile("FROM (.*?) ")
                table_lst = pattern1.findall(text)
                if len(table_lst)>0:
                    options = st.multiselect(
                        'tables',
                        table_lst,
                        table_lst)
                    for target in table_lst:
                        st.write("당신이 입력한 쿼리에서 조회하는 테이블 정보는 다음과 같습니다.")
                        time.sleep(0.1)
                        target_df = total_df[total_df["table_names_original"].astype(str).str.contains(target)].reset_index(drop=True)
                        # 칼럼 별 이름, 한글이름, 데이터 타입 정보가 담긴 데이터프레임
                        col_info = [[x[1],y[1],z] for x, y, z in zip(target_df["column_names_original"][0],target_df["column_names"][0],target_df["column_types"][0])]
                        col_info[0] = ["table_names_original","table_names","type"]
                        st.data_editor(pd.DataFrame(col_info[1:],columns=col_info[0]))
                        st.write("👋🏻 코드블럭 오른쪽 :blue[아이콘]을 클릭하면 query를 복사할 수 있습니다.")
                else:
                    st.error("❗ 테이블 정보를 조회할 수 없어 입력된 SQL을 기반으로 해석하겠습니다.")
                    
            with st.spinner('⚡ Wait for it...'):
                st.info(query_with_gpt(target_df["table_names_original"][0],target_df["table_names"][0], text, col_info, gpt_ver))
                    
def chat_with_gpt():
    with st.container():
        if "openai_model" not in st.session_state:
            st.session_state["openai_model"] = gpt_ver

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
        try:
            if prompt := st.chat_input():
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.write("**User**")
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    st.write("**GPT**")
                    message_placeholder = st.empty()
                    full_response = ""
                    for response in openai.ChatCompletion.create(
                        model=st.session_state["openai_model"],
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ],
                        stream=True,
                    ):
                        full_response += response.choices[0].delta.get("content", "")
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
        except:
            st.info("입력하신 API KEY를 다시 확인해주세요!")
###################################################################################################
if selected2 == "Query decoder":
    with st.form(key="my_form") as form1:
        text = st.text_area(
            # Instructions
            "해석을 원하시는 SQL 쿼리를 입력하세요",
            "select * from testdb;",
            height=150,
            help="SQL 쿼리를 입력하세요!"
        )
        submit_button = st.form_submit_button(label="Submit", use_container_width = True)

    if submit_button:
        # 2. horizontal menu
        st.success("✅ SQL 쿼리가 정상적으로 입력되었습니다!")
        submit_test()
###################################################################################################
if selected2 == "Chat with GPT":
    chat_with_gpt()
###################################################################################################
