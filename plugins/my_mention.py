# coding: utf-8

from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
import re

options = Options()
options.add_argument('--headless') #headlessにするといちいちseleniumが開かなくなって裏でスクレイピングするようになる


driver = webdriver.Chrome('chromedriver.exeのパスを記述',options=options)



@respond_to('バージョン')
def mention_func(message):

    driver.get('https://support.blancco.com/pages/viewpage.action?pageId=26214508')

#4秒くらい待たないと拾ってくれない
    sleep(4)

#blanccoのバージョン取得
    blancco_version = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[4]/div[1]/div[2]/div[3]/div[2]/div[3]/div/div[5]/article/div/div/div/div/div[2]/div/div[2]/div[1]/div/a[1]/h2")
    blancco_version_url = blancco_version.find_element_by_xpath("..")

#前回取得したバージョンをtxtファイルで保存して更新分だけ上書きして保存
    blancco_file = "blancco.txt"

    try:
        f = open(blancco_file, "r", encoding='utf-8')
        old_version = f.read()
    except:
        old_version = ""
        message.reply("以前のバージョンが分かりません。" + "\n" + "ファイルを新しく作成しました。")


    if blancco_version.text == old_version:

        message.reply("バージョンの更新はありません。" + "\n" + "<" + blancco_version.text + ">")

    elif re.search(r"Blancco Mobile Diagnostics and Erasure", blancco_version.text):   #更新はblanccoのバージョン更新だけ上書き保存
            new_version = open(blancco_file, "w", encoding='utf-8')
            new_version.write(blancco_version.text)
            new_version.close()
            message.reply("新しいバージョンの更新があります！" + "\n" + "<" + blancco_version.text + ">" +"\n" +"(" +  blancco_version_url.get_attribute("href") + ")")

    else:
         message.reply("バージョンの更新はありません。" + "\n" + "<" + blancco_version.text + ">")


