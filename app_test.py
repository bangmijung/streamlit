import re
import openai
import streamlit as st
from streamlit_tags import st_tags

# query = "SELECT NM_BUS_STOPD FROM GNJJ_BUS_INFO_GUIDE_I_STS WHERE BUS_STOPC = '381239013"
def chatGPT4(api_key, db_info, query):
    openai.api_key=api_key
    # 인덴트 수정
    messages = []
    order2 = f"""테이블 정보는 다음과 같아.
{db_info}
위 테이블 정보를 바탕으로 {query} 쿼리를 해석해줘"""
    try:
        if order1:
            messages.append(
                {"role": "user", "content": order2},
            )
            chat = openai.ChatCompletion.create(
                model="gpt-4", messages=messages
            )
            reply = chat.choices[0].message.content
            #print(f"ChatGPT:\n {reply}")
    except:
        reply = ""
        pass
    return reply
################################################################################################
st.title("⚡ Query Up!")
st.text("AI융합캡스톤디자인과창업_20180802방미정_chatGPT활용_중간과제")
################################################################################################
api_key = st.text_input(label="Open AI에서 발급받은 API KEY를 입력하세요!",type="password", placeholder="API KEY")
with st.form(key="my_form"):
    text1 = st.text_area(
        # Instructions
        "해석을 원하시는 SQL 쿼리를 입력하세요",
        # 'sample' variable that contains our keyphrases.
        "select * from testdb where num = 1; \n select * from testdb2 where num = 1;",
        # The height
        height=250,
        # The tooltip displayed when the user hovers over the text area.
        help="SQL 쿼리를 입력하세요!"
    )
    text2 = st.text_area(
        # Instructions
        "테이블 정보를 입력하세요",
        # 'sample' variable that contains our keyphrases.
        "",
        # The height
        height=150,
        # The tooltip displayed when the user hovers over the text area.
        help="DB정보를 입력하세요!"
    )
    submit_button = st.form_submit_button(label="Submit")
    if submit_button:
        reply = chatGPT4(api_key, text2, text1)
        st.title("⚡ Query Up!"+reply)
        pattern1 = re.compile("from (.*?)\s")
        labels_from_st_tags = st_tags(
            value=pattern1.findall(text1),
            maxtags=3,
            #suggestions=["사회/경제", "안전", "교통"],
            label="",
        )
        st.success("✅ SQL 쿼리가 입력되었습니다!")
        st.code(text1, line_numbers=True)

################################################################################################


