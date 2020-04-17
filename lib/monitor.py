from lib.ssh import SshClient


class Monitor(object):
    def __init__(self, connect_info):
        self.ssh = SshClient(connect_info)

    def cpu_info(self):
        total_cpu_count = self.ssh.get_command('grep -c processor /proc/cpuinfo')
        load_avg_ = self.ssh.get_command('cat /proc/loadavg')
        load_avg = load_avg_.split(' ')
        print(f'load_avg[{total_cpu_count}] {load_avg[0]} {load_avg[1]} {load_avg[2]}')

    def close(self):
        self.ssh.close()
