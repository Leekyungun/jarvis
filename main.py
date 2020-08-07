import datetime
import time
import sys
import os
from multiprocessing import Process

import telegram

BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIRECTORY)

from lib.monitor import Monitor
from config.config import Config


class Server(Process):
    def __init__(self, connect_info, process_list):
        super(Process, self).__init__()
        self.process_list = process_list
        self.server_monitor = Monitor(connect_info=connect_info)
        self.bot = telegram.Bot(token=Config.TELEGRAM_TOKEN)
        self.chat_id = Config.TELEGRAM_CHAT_ID

    def run(self):
        while True:
            time.sleep(5)
            for process in self.process_list:
                if not self.server_monitor.exist_process(process):
                    print(f'<<< {process} >>> is not working')
                    self.bot.sendMessage(chat_id=Config.TELEGRAM_CHAT_ID, text=f'<<< {process} >>> is not working')
            print(f'process check : {datetime.datetime.now()}')


if __name__ == '__main__':
    cce_prod = Server(connect_info=Config.cce_prod,
                      process_list=['cce_eth_websocket', 'cce_detected_deposit', 'cce_withdraw_pending_check', 'cce_detected_create_address'])
    cce_prod.start()
    time.sleep(0.5)  # 임시, print 출력시 구분하기 위함
    hbc_prod = Server(connect_info=Config.hbc_prod,
                      process_list=['hbc_detected_deposit', 'hbc_detected_create_address', 'hbc_withdraw_confirm_check',
                                    'hbc_request_address', 'hbc_withdraw', 'hbc_eth_websocket'])
    hbc_prod.start()

    while True:
        time.sleep(10)
