import paramiko


class SshClient(object):
    def __init__(self, connect_info):
        self.connect_info = connect_info
        self.cli = paramiko.SSHClient()
        self.cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    def _connect(self):
        self.cli.connect(**self.connect_info)

    def _inspect(self):
        if self.cli.get_transport() is None:
            self._connect()

    def command(self, input):
        self._inspect()
        stdin, stdout, stderr = self.cli.exec_command(input)
        lines = stdout.readlines()
        for line in lines:
            print(line)
        # print(''.join(lines))

    def get_command(self, input_command):
        self._inspect()
        stdin, stdout, stderr = self.cli.exec_command(input_command)
        return stdout.readline().rstrip('\n')

    def close(self):
        self.cli.close()
