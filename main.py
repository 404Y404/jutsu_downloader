from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


link = input("Введите ссылку: ")
folder = input("Введите путь сохранения: ")
start, end = map(int,
                 input("Введите от какой до какой серии через - (1-12): ").split("-"))
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=data")
prefs = {"download.default_directory": folder}
options.add_experimental_option("prefs", prefs)
# options.add_argument('headless')
js = """
let download = document.createElement("a");
download.setAttribute("href", "{}")
download.setAttribute("id", "downloadd")
download.setAttribute("download", "{}");
download.innerText = "download";
document.body.appendChild(download);
"""
browser = webdriver.Chrome(chrome_options=options)
link = link.split("/episode", maxsplit=1)[0]

for n in range(start, end + 1):
    try:
        browser.get(f"{link}/episode-{n}.html")
        video = browser.find_element(
            By.CSS_SELECTOR, 'video > source[res="480"]')
        video = video.get_attribute('src')
        browser.get(video)
        sleep(1)
        browser.execute_script(js.format(video, f"{n}.mp4"))
        sleep(1)
        browser.find_element(By.CSS_SELECTOR, "#downloadd").click()
    except Exception as e:
        print(e)
        print("[!] Серия не найдена")
