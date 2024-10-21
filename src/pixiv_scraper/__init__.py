import requests
import time
import pandas as pd
import bar_chart_race as bcr


def preprocess():
    with open("uma.csv", "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open("name.csv", "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line.split(",")[1] + "\n")


# pixivを期間ごとにウマ娘の名前で検索して件数を調べる。
# リクエストは毎秒1回までに制限されている。
def search_pixiv_uma_musume():
    umamusume_names = []
    with open("name.csv", "r", encoding="utf-8") as f:
        for line in f:
            umamusume_names.append(line.strip())

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.pixiv.net/",
    }
    with open("data.csv", "a") as f:
        for name in umamusume_names[18:]:
            tag = name + "(ウマ娘)"
            data = [tag]
            for year in range(2021, 2025):
                for month in range(1, 13):
                    start_date = f"{year}-{str(month).zfill(2)}-01"
                    end_date = f"{year}-{str(month).zfill(2)}-31"
                    url = f"https://www.pixiv.net/ajax/search/artworks/{tag}?word={tag}&order=date_d&mode=all&p=1&s_mode=s_tag&type=all&lang=ja&order=date_d&scd={start_date}&ecd={end_date}"
                    response = requests.get(url, headers=headers)
                    json_data = response.json()
                    try:
                        total = json_data["body"]["illustManga"]["total"]
                    except KeyError:
                        print("KeyError")
                        total = 0
                    data.append(total)
                    print(f"{tag}\t{start_date} ~ {end_date}\t{total}件")
                    time.sleep(1)
            data = ",".join(map(str, data))
            print(data)
            f.write(data + "\n")


# タグ件数を集計する
def count_tags():
    tags_dict = {}
    with open("tags.csv") as f:
        for line in f:
            tags = line.strip().split(",")
            for tag in tags:
                if tag in tags_dict:
                    tags_dict[tag] += 1
                else:
                    tags_dict[tag] = 1
    for tag, count in sorted(tags_dict.items(), key=lambda x: x[1], reverse=True):
        print(tag, count)


# Not works
def barchartracification():
    df = pd.read_csv("data.csv")
    df = df.transpose()
    print(df)
    bcr.bar_chart_race(df=df, n_bars=10, filename="bcr.mp4")


def main():
    search_pixiv_uma_musume()
    count_tags()
    # barchartracification()


main()
