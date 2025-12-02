from trafilatura import fetch_url, html2txt

url = "https://ashpublications.org/blood/article/112/13/4793/24896/Stem-cell-concepts-renew-cancer-research"

print(html2txt(fetch_url(url)))