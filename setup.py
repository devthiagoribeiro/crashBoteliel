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
            win_seguidos += 1
            total_win += 1
            loss_seguidos = 0
            assertividade = total_win*100/(total_win + total_loss)
            bot.sendMessage(chat_id, f'🎰PLACAR\nVitórias seguidas: {win_seguidos}\nTotal de vitórias: {total_win}\nTotal de derrotas: {total_loss}\nAssertividade: {assertividade}%')
        else:
            bot.sendMessage(channelid, '🔄Vamos para o gale 1')
    elif (lista[11] == 1.00) and (lista[10] >= 2.00):
        if (lista[0] >= 2.00) and (lista[1] < 2.00):
            bot.sendMessage(channelid, f'🏆Win!!')
            win_seguidos += 1
            total_win += 1
            loss_seguidos = 0
            assertividade = total_win*100/(total_win + total_loss)
            bot.sendMessage(channelid, f'🎰PLACAR\nVitórias seguidas: {win_seguidos}\nTotal de vitórias: {total_win}\nTotal de derrotas: {total_loss}\nAssertividade: {assertividade}%')
        elif (lista[0] < 2.00) and (lista[1] < 2.00):
            bot.sendMessage(channelid, '❌Loss!!')
            win_seguidos = 0
            loss_seguidos += 1
            total_loss += 1
            assertividade = total_win*100/(total_win + total_loss)
            bot.sendMessage(channelid, f'🎰PLACAR:\nDerrotas seguidas: {loss_seguidos}\nTotal de vitórias: {total_win}\nTotal de derrotas: {total_loss}\nAssertividade: {assertividade}%')
def rodarBot():
    page = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH') ,options=options)
    page.get('https://blaze.com/pt/games/crash')
    sleep(5)
    while True:
        win_seguidos = 0
        loss_seguidos = 0
        total_win = 0
        total_loss = 0
        for x in range(100):
            entries = page.find_element(By.XPATH, '//*[@id="crash-recent"]/div[2]/div[2]').get_attribute('textContent')
            results = entries.split('X')
            floats = list(map(lambda x: float(x), results[:15]))
            print(floats)
            analise(floats)
            results_b = results
            while (results_b[0] == results[0]) and (results_b[1] == results[1]):
                ppg = page.find_element(By.XPATH, '//*[@id="crash-recent"]/div[2]/div[2]').get_attribute('textContent')
                results_b = ppg.split('X')
        page.refresh()
        wait_selector = ''
        while wait_selector != '2x':
            wait_selector = page.find_element(By.XPATH, '//*[@id="crash-controller"]/div[1]/div[2]/div[1]/div[1]/button[2]').get_attribute('textContent')
            sleep(.5)
        sleep(.5)

rodarBot()
