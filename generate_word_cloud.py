from wordcloud import WordCloud,STOPWORDS
def generate_word_cloud(revs):
    text = ' '.join([rev['mini_review'].replace(' ', '_').replace("-","_") for rev in revs])
    wc = WordCloud(
        background_color="black",
        stopwords=STOPWORDS,
        height=600,
        width=800,
        prefer_horizontal=1
    ).generate(text)
    wc.to_file("./static/wc.png")
    print("Word cloud generated.")
