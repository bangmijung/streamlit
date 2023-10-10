import streamlit as st
from streamlit_tags import st_tags

st.title("Test")
#lst = ["1","2","6","7"]
#st.multiselect("label",lst,lst)
#########################################################################
st.title("⚡ Query Up!")
st.text("AI융합캡스톤디자인과창업_20180802방미정_chatGPT활용_중간과제")
#########################################################################
api_key = st.text_input(label="Open AI에서 발급받은 API KEY를 입력하세요!",type="password", placeholder="API KEY")
with st.form(key="my_form"):
    text = st.text_area(
        # Instructions
        "해석을 원하시는 SQL 쿼리를 입력하세요",
        # 'sample' variable that contains our keyphrases.
        "select * from testdb where num = 1; \n select * from testdb2 where num = 1;",
        # The height
        height=250,
        # The tooltip displayed when the user hovers over the text area.
        help="SQL 쿼리를 입력하세요!"
    )
    submit_button = st.form_submit_button(label="Submit")
#########################################################################
keywords = st_tags(
    label='# Enter Keywords:',
    text='Press enter to add more',
    value=['Zero', 'One', 'Two'],
    suggestions=['five', 'six', 'seven', 
                 'eight', 'nine', 'three', 
                 'eleven', 'ten', 'four'],
    maxtags = 4,
    key='1')
