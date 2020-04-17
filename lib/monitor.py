from lib.ssh import SshClient


class Monitor(object):
    def __init__(self, connect_info):
        self.ssh = SshClient(connect_info)

    def info(self):
        print('\x1b[33m[CPU INFO]\x1b[0m')
        self.cpu_info()
        print()
        print('\x1b[33m[MEMORY INFO]\x1b[0m')
        self.memory_info()
        print()
        print('\x1b[33m[DISK INFO]\x1b[0m')
        self.disk_info()

    def cpu_info(self):
        total_cpu_count = self.ssh.get_command('grep -c processor /proc/cpuinfo')
        load_avg_ = self.ssh.get_command('cat /proc/loadavg')
        load_avg = load_avg_.split(' ')
        print(f'load_avg[{total_cpu_count}] {load_avg[0]} {load_avg[1]} {load_avg[2]}')

    def memory_info(self):
        result = self.ssh.get_commands('free -h')
        for line in result:
            print(line)

    def disk_info(self):
        result = self.ssh.get_commands('df -h')
        for line in result:
            print(line)

    def close(self):
        self.ssh.close()


if __name__ == '__main__':
    from config.config import Config
    super_computer = Monitor(Config.super_computer)
    super_computer.info()

