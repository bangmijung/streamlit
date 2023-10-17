import re
import time
import ast
import json
import datetime
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_tags import st_tags
from streamlit_option_menu import option_menu
import openai
###################################################################################################
# 0. page config & title
st.set_page_config(layout="centered", page_title="20180802방미정_중간과제", page_icon="⚡")
st.title("⚡ Query Up!")
st.text("AI융합캡스톤디자인과창업_20180802방미정_chatGPT활용_중간과제")
###################################################################################################
# 1. dataset
url = 'https://raw.githubusercontent.com/bangmijung/streamlit/main/total_db_info.csv'
total_df = pd.read_csv(url, sep="|", index_col=0)
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
    if api_key != "":
        messages = []
        try:
            f_string = f"{query} 이 쿼리의 인덴트를 읽기 쉽게 수정해줘. 쿼리 외에는 아무 말도 하지 마. ```같은 것도 쓰지 마"
            if f_string:
                messages.append({"role": "user", "content": f_string},)
                chat = openai.ChatCompletion.create(model=gpt_ver, messages=messages)
                reply = "-- 입력한 쿼리의 인덴트를 수정한 결과입니다.\n"+chat.choices[0].message.content
        except:
            reply = ""
            pass
    else:
        reply = "-- 입력한 쿼리의 원본입니다.\n"+query
    return reply
#--------------------------------------------------------------------------------------------------
def query_with_gpt(info_for_gpt, query):
    messages = []
    if info_for_gpt != []:
        hint = f"""테이블 정보는 테이블명 : 테이블 칼럼 정보 로 구성되어 있어. 테이블 정보는 [칼럼명, 한글이름, 타입] 리스트로 구성되어 있어.
테이블 정보는 {info_for_gpt}와 같아. 이 테이블 정보를 참고해서"""
    else:
        hint = "안타깝지만 우리에게 테이블 정보가 없는 상황이야. 자의적으로 해석하지 말고,"
    try:
        f_string = f"""{hint}
{query} 쿼리를 해석해줘.
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
#--------------------------------------------------------------------------------------------------
def submit_test():
    with st.expander('* Query Decoder', expanded=True) :
        
        # progress bar
        my_bar = st.progress(0, text=None)
        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=None)
        my_bar.empty()
        
        # assistant message
        with st.chat_message("ai"):
            st.write("**Query Up! Robot**")
            with st.spinner('⚡ Wait for it...'):
                # 코드 인덴트 교정 - api키 입력 여부에 따라 다름
                time.sleep(0.1)
                if api_key == "":
                    st.write("API KEY를 입력하지 않아 당신이 입력한 쿼리의 들여쓰기를 교정할 수 없습니다.")
                else:
                    st.write("당신이 입력한 쿼리의 :blue[들여쓰기를 교정한 결과]는 다음과 같습니다.")
                st.code(correct_indent(text, gpt_ver), language='sql', line_numbers=True)
                st.caption("👋🏻 코드블럭 오른쪽 :blue[아이콘]을 클릭하면 query를 복사할 수 있습니다.")
                
        # assistant message
        with st.chat_message("ai"):
            st.write("**Query Up! Robot**")
            with st.spinner('⚡ Wait for it...'):
                
                # GPT가 참고할 테이블 정보 딕셔너리
                info_for_gpt = {}
                
                # 테이블 정보 조회
                time.sleep(0.1)
                st.write("당신이 입력한 쿼리에서 조회하는 :blue[테이블 정보]는 다음과 같습니다.")
                pattern1 = re.compile(r'(?i)(?:FROM|JOIN)\s+`?([a-zA-Z_][a-zA-Z0-9_]*)`?')
                table_lst = pattern1.findall(text)
                if len(table_lst)>0:
                    options = st.multiselect('tables', table_lst, table_lst)
                    for target in table_lst:
                        time.sleep(0.1)
                        try:
                            target_df = total_df[total_df["table_names_original"].astype(str).str.contains(target)]
                            # 출처, 데이터베이스 ID, 같은 스키마를 공유하는 테이블명
                            st.write("✔ 출처 : "+target_df["source"].item())
                            st.write("✔ 데이터베이스 ID : "+target_df["db_id"].item())
                            st.write("✔ 테이블명 : "+target_df["table_names_original"].item())
                            # 칼럼 별 이름, 한글이름, 데이터 타입 정보가 담긴 데이터프레임
                            st.write(pd.DataFrame(ast.literal_eval(target_df["info_lst"].item()),columns=["column_names_original", "column_names", "type"]))
                            info_for_gpt.update({target_df["table_names"].item():target_df["info_lst"].item()})
                        except:
                            st.error(f"❗ {target}에 대한 테이블 정보가 없습니다.")
                else:
                    st.error("❗ 입력하신 쿼리에서 발견한 다음 테이블 정보가 없습니다.")
                    options = st.multiselect('tables', table_lst, table_lst)
                    
        # assistant message
        with st.chat_message("ai"):
            st.write("**Query Up! Robot**")
            with st.spinner('⚡ Wait for it...'):
                st.info(query_with_gpt(info_for_gpt, text))
#--------------------------------------------------------------------------------------------------                    
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
# 6. report
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
# 7. chat
if selected2 == "Chat with GPT":
    chat_with_gpt()
###################################################################################################
