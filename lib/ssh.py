import paramiko


class SshClient(object):
    def __init__(self, connect_info):
        self.connect_info = connect_info
        self.cli = paramiko.SSHClient()
        self.cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    def _connect(self):
        if 'password' in self.connect_info:
            self.cli.connect(hostname=self.connect_info['hostname'],
                             username=self.connect_info['username'],
                             password=self.connect_info['password'])
        else:
            private_key = paramiko.RSAKey.from_private_key_file(self.connect_info['private_key_file'])
            self.cli.connect(hostname=self.connect_info['hostname'],
                             username=self.connect_info['username'],
                             pkey=private_key)

    def _inspect(self):
        if self.cli.get_transport() is None:
            self._connect()

    def command(self, input_data):
        self._inspect()
        stdin, stdout, stderr = self.cli.exec_command(input_data)
        lines = stdout.readlines()
        # for line in lines:
        #     print(line)
        print(''.join(lines))

    def get_command(self, input_command):
        self._inspect()
        stdin, stdout, stderr = self.cli.exec_command(input_command)
        return stdout.readline().rstrip('\n')

    def get_commands(self, input_command):
        self._inspect()

        stdin, stdout, stderr = self.cli.exec_command(input_command)
        lines = stdout.readlines()

        results = list()
        for line in lines:
            results.append(line.rstrip('\n'))

        return results

    def close(self):
        self.cli.close()


if __name__ == '__main__':
    from config.config import Config

    ssh = SshClient(Config.holdem_prod)
    result = ssh.get_commands('ls -al')
    for line in result:
        print(line)
