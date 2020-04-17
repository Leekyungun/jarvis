from lib.monitor import Monitor
from config.config import Config

super_computer = Monitor(Config.super_computer)
super_computer.info()
