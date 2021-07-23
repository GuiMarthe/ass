from youtube_dl import YoutubeDL
import urllib
from bs4 import BeautifulSoup
from urllib.parse import quote

def download_video(link, filepath):
    """
    Downloads a video and saves in filepath.
    """
    ydl = YoutubeDL({"outtmpl": f"{filepath}"})
    ydl.download([link])


def download_html(link):
    resp = urllib.request.urlopen(link)
    r = resp.read()
    with open("downloaded.html", "wb") as f:
        f.write(r)
    print("arquivo salvo...")


def get_links():
    with open("downloaded.html", "rb") as html_file:
        html = html_file.read()
    soup = BeautifulSoup(html, "html.parser")
    list_of_links = soup.find_all("a")
    return list_of_links


def display_text(list_of_links):
    i = 0
    for link in list_of_links:
        print(i, "--> ", link.text)
        i += 1


def check_link(text):
    if text == "pdf":
        return True
    if text.startswith("Lista"):
        return True
    if text.strip() == "(Gabarito)":
        return True
    return False


def create_url_from_tag(tag):
    url_part = tag.attrs['href']
    return url_part

def create_file_name_from_url(url):
    return url.split('/')[-1]

def dowload_pdf_from_link(url_part):
    safe_url = create_safe_url(url_part)
    return urllib.request.urlopen(safe_url).read()

def create_safe_url(url):
    return 'https://www.ime.usp.br/~patriota/' + quote(url)

def download_pdfs_from_list(list_of_links):
    for tag in list_of_links:
        if check_link(tag.text):
            url_part = create_url_from_tag(tag)
            file_name =  create_file_name_from_url(url_part)
            print('baixando ', url_part, 'e salvando como', file_name)
            pdf_html_response = dowload_pdf_from_link(url_part)# importante
            with open('./pdfs/' + file_name, 'wb') as fp:
                fp.write(pdf_html_response)
            continue


if __name__ == '__main__':

    ll = get_links()
    download_pdfs_from_list(ll)
