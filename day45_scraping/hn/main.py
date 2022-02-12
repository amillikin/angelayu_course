from bs4 import BeautifulSoup
import requests


response = requests.get("https://news.ycombinator.com/news")
yc_html = response.text

soup = BeautifulSoup(yc_html, 'html.parser')

titles = soup.find_all(class_="titlelink")
subtext = soup.find_all(class_="subtext")

scores = []
for item in subtext:
    score = item.find(name="span", class_="score")
    if score is None:
        scores.append(0)
    else:
        scores.append(int(score.getText().split()[0]))

stories = {
    titles[i].getText(): [titles[i].get("href"),
                          scores[i]]
    for i in range(len(titles))
}

highest_score = max(scores)
for story in stories.items():
    if story[1][1] == highest_score:
        print(f"{story[0]}\n{story[1][0]}")
