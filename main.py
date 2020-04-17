from lib.monitor import Monitor
from config.config import Config

super_computer = Monitor(connect_info=Config.super_computer2)
super_computer.info()
