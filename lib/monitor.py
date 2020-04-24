from lib.ssh import SshClient
from lib import utils


class Monitor(object):
    def __init__(self, connect_info):
        self.name = connect_info['name']
        self.ssh = SshClient(connect_info)

    def info(self):
        utils.color_print('blue', '\n' + '=' * (len(self.name) + 2))
        utils.color_print('blue', f'|{self.name}|')
        utils.color_print('blue', '=' * (len(self.name) + 2))

        utils.color_print('yellow', '[CPU Process]')
        self.cpu_info()
        print()
        utils.color_print('yellow', '[MEMORY Process]')
        self.memory_info()
        print()
        utils.color_print('yellow', '[DISK Process]')
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
            utils.color_print('green', input_data)
        else:
            utils.color_print('red', input_data)

    def check_process(self, input_data):
        assert type(input_data) != list()

        utils.color_print('yellow', '[Check Process]')
        for process in input_data:
            self.exist_process(process)

    def delete_log_files(self, directory, expire_date):
        assert type(directory) != str()
        assert type(expire_date) != int()

        if directory == '/':
            return 'Please specify a detailed location.'

        self.disk_info()
        delete_file_count = self.ssh.get_command(f'find {directory} -name "*.log" -mtime +{expire_date} | wc -l')
        self.ssh.command(f'find {directory} -name "*.log" -mtime +{expire_date} -exec rm -f {{}} \\;')
        utils.color_print('yellow', f'deleted file count : {delete_file_count}')
        self.disk_info()

    def close(self):
        self.ssh.close()


if __name__ == '__main__':
    from config.config import Config

    super_computer = Monitor(connect_info=Config.super_computer2)
    super_computer.info()

    process_list = ['socket_client_well', 'redis']
    super_computer.check_process(process_list)
