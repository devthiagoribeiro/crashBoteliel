from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import telepot
import os

options = webdriver.ChromeOptions()
options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('start-maximized')

bot_token = os.environ.get('BOT_TOKEN')
channelid = os.environ.get('CHANNEL_ID')
link_blaze = '<a href="https://blaze.com/pt/games/crash">💻Blaze</a>'
bot = telepot.Bot(bot_token)

def analise(lista):
    if (lista[7] == 1.00) and (lista[6] >= 2.00):
        bot.sendMessage(channelid, text=f'🚨Atenção🚨\n🎰Possível entrada...\n⏳Aguardar confirmação\n{link_blaze}', parse_mode='HTML', disable_web_page_preview=True)
    elif (lista[9] == 1.00) and (lista[8] >= 2.00):
        bot.sendMessage(channelid, f'☑️Entrada confirmada\n📈Entrar com auto retirada em 2x')
    elif (lista[10] == 1.00) and (lista[9] >= 2.00):
        if lista[0] >= 2.00:
            bot.sendMessage(channelid, f'🏆Win!!')
        else:
            bot.sendMessage(channelid, '🔄Vamos para o gale 1')
    elif (lista[11] == 1.00) and (lista[10] >= 2.00):
        if lista[0] >= 2.00:
            bot.sendMessage(channelid, f'🏆Win!!')
        else:
            bot.sendMessage(channelid, '❌Loss!!')
def rodarBot():
    page = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH') ,options=options)
    page.get('https://blaze.com/pt/games/crash')
    print('abrindo navegador')
    sleep(5)
    while True:
        entries = page.find_element(By.XPATH, '//*[@id="crash-recent"]/div[2]/div[2]').get_attribute('textContent')
        results = entries.split('X')
        floats = [float(x) for x in results[0:15]]
        print(floats)
        analise(floats)
        results_b = results
        while (results_b[0] == results[0]) and (results_b[1] == results[1]):
            ppg = page.find_element(By.XPATH, '//*[@id="crash-recent"]/div[2]/div[2]').get_attribute('textContent')
            results_b = ppg.split('X')
        page.refresh()
        while page.find_element(By.XPATH, '//*[@id="crash-controller"]/div[1]/div[2]/div[1]/div[1]/button[2]').get_attribute('textContent') != '2x':
            sleep(.5)
        sleep(.5)
while True:
    try:
        rodarBot()
    except:
        print('Reiniciando sistema...')