import streamlit as st
from streamlit_tags import st_tags

st.title("Test")
lst = ["1","2","6"]
st.multiselect("label",lst,lst)
keywords = st_tags(
    label='# Enter Keywords:',
    text='Press enter to add more',
    value=['Zero', 'One', 'Two'],
    suggestions=['five', 'six', 'seven', 
                 'eight', 'nine', 'three', 
                 'eleven', 'ten', 'four'],
    maxtags = 4,
    key='1')
