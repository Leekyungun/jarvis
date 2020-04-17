from lib.ssh import SshClient
from lib import utils


class Monitor(object):
    def __init__(self, connect_info):
        self.name = connect_info['name']
        self.ssh = SshClient(connect_info)

    def info(self):
        print(f'\x1b[35m[{self.name}]\x1b[0m')
        print('\x1b[33m[CPU INFO]\x1b[0m')
        self.cpu_info()
        print()
        print('\x1b[33m[MEMORY INFO]\x1b[0m')
        self.memory_info()
        print()
        print('\x1b[33m[DISK INFO]\x1b[0m')
        self.disk_info()
        print()
        self.close()

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

    def process_info(self, input_data):
        assert type(input_data) != str()

        result = self.ssh.get_commands(f'ps -ef |grep {input_data}')
        for line in result:
            print(line)

    def is_exist_process(self, input_data):
        assert type(input_data) != str()

        output_flag = False
        result = self.ssh.get_commands(f'ps -ef | grep {input_data}')
        for line in result:
            if line.find('grep') != -1:
                continue
            else:
                output_flag = True

        return output_flag

    def exist_process(self, input_data):
        assert type(input_data) != str()

        process = self.is_exist_process(input_data)

        if process:
            print(f'\x1b[32m{input_data}\x1b[0m')
        else:
            print(f'\x1b[31m{input_data}\x1b[0m')

    def check_process(self, input_data):
        assert type(input_data) != list()

        print('\x1b[33m[Check Process]\x1b[0m')
        for process in process_list:
            self.exist_process(process)

    def close(self):
        self.ssh.close()


if __name__ == '__main__':
    from config.config import Config

    super_computer = Monitor(name='super_computer2', connect_info=Config.super_computer2)
    super_computer.info()

    process_list = ['socket_client_well', 'redis']
    super_computer.check_process(process_list)
