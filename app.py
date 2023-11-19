from selenium.webdriver.common.by import By

import korean_sentiment
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import streamlit as st
import pandas as pd
import altair as alt

# link = st.text_input("유튜브 링크 입력 >> ")
with st.form(key="form"):
    link = st.text_input("유튜브 링크 입력 >> ")
    button = st.form_submit_button("감성분석 시작")
if button == True:
    browser = webdriver.Chrome() # 여러분들은 아래 문장쓰지 말고, 이 문장 써주세요!
    # browser = webdriver.Chrome(install())
    browser.get(link)
    time.sleep(5)
    # 스크롤 살짝 내려서 댓글 불러오기
    browser.find_element(By.CSS_SELECTOR, "html").send_keys(Keys.PAGE_DOWN) # Keys.END : 스크롤 끝까지 내리기
    time.sleep(5) # 댓글 불러올 때까지 기다리기
    for i in range(5):
        browser.find_element(By.CSS_SELECTOR, "html").send_keys(Keys.END)  # Keys.END : 스크롤 끝까지 내리기
        time.sleep(3)
    # 댓글 크롤링
    comment = browser.find_elements(By.CSS_SELECTOR, "yt-formatted-string#content-text")
    sentiment_result = {"긍정":0, "중립":0, "부정":0}

    for i in comment:
        st.write(i.text)
        try:
            result = korean_sentiment.get_sentiment(i.text)
            sentiment_result[result["result"]] += 1
        except:
            continue
        st.write(result)
        st.write("---------------------------------")
    browser.close()

    # 딕셔너리를 DataFrame으로 변환
    df = pd.DataFrame(list(sentiment_result.items()), columns=['sentiment', 'count'])

    # Altair로 막대그래프 그리기
    chart = alt.Chart(df).mark_bar().encode(
        x='sentiment',
        y='count'
    ).properties(
    width=600  # 너비를 600으로 설정
    )

    # chart.show()
    st.altair_chart(chart)
