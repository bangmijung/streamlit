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
st.set_page_config(layout="centered", page_title="MBTMI vs ChatGPT4", page_icon="💾")
st.title("🥇 ChatGPT3.5 vs ChatGPT4")
st.text("구독 없이 GPT4와 대화할 수 있는 환경입니다. 대화내용은 저장되지 않으니 조심하세요~")
###################################################################################################
gpt_ver = st.radio(label = "GPT3.5-turbo or GPT3.5-turbo-16k or GPT4.0", options=["gpt-3.5-turbo", "gpt-3.5-turbo-16k","gpt-4"])
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
api_key = st.text_input(label="Open AI에서 발급받은 API KEY를 입력하세요!",
                        type="password", placeholder="API KEY")
openai.api_key = api_key
st.divider()
###################################################################################################
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
if api_key!="":
  chat_with_gpt()
###################################################################################################
