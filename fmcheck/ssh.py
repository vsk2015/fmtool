"""

This module implements methods for SSH sessions.

"""
import re
import pexpect
import logging
from pexpect import pxssh


class SSH(object):

    """SSH Module"""
    TIMEOUT_ERROR_MESSAGE = 'Timed out looking for expected output'
    EOF_ERROR_MESSAGE = 'EOF reached'
    ERROR_MESSAGE = 'Something went wrong'
    ERROR_MESSAGE_SUFFIX = '| For {}@{} port ({})'

    def __init__(self, ip, user, port=22, password=None, prompt=None, timeout=30):
        self.ip = ip
        self.user = user
        self.port = port
        self.password = password
        self.prompt = prompt
        self.timeout = timeout
        self.session_open = False
        self.child = None

    def is_session_open(self):
        return self.session_open

    def expect(self, *args, **kwargs):
        _kwargs = kwargs.copy()
        kwargs.setdefault('timeout', self.timeout)
        for k in ('timeout_error_message', 'eof_error_message', 'error_message'):
            kwargs.pop(k, None)
        try:
            return self.child.expect(*args, **kwargs)
        # Here we are just cleanly printing errors and raising the exception
        except pexpect.TIMEOUT as e:
            error_message= _kwargs.get('timeout_error_message', self.TIMEOUT_ERROR_MESSAGE)
        except pexpect.EOF as e:
            error_message= _kwargs.get('eof_error_message', self.EOF_ERROR_MESSAGE)
        except pexpect.ExceptionPexpect as e:
            error_message= _kwargs.get('error_message', self.ERROR_MESSAGE)
        logging.error(self.format_error_message(error_message))
        logging.error(self.child.before)
        if e:
            raise e
        return None

    def format_error_message(self, message):
        return message + self.ERROR_MESSAGE_SUFFIX.format(self.user, self.ip, self.port)

    def execute_single_command(self, command, output=False):
        try:
            s = pxssh.pxssh()
            s.login(self.ip, self.user, self.password)
            s.sendline(command)
            logging.debug("%s@%s > %s", self.user, self.ip, command)
            try:
                s.prompt()
            except Exception, msg:
                logging.debug(msg)
            logging.debug(s.before)
            if output:
                return s.before
            s.logout()
            return True
        except pxssh.ExceptionPxssh, msg:
            logging.error(str(msg))
            return False

    def create_session(self):
        ssh_command = 'ssh -o PreferredAuthentications=password ' \
                      '-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -p {} {}@{}'.format(
            self.port, self.user, self.ip)
        logging.debug('SSH: connecting to %s', ssh_command)
        self.child = pexpect.spawn(ssh_command)
        result = self.expect(
            [pexpect.TIMEOUT, unicode('(?i)password')], timeout=self.timeout,
            eof_error_message='ERROR: could not connect to noviflow via SSH')
        if result is not None:
            self.child.sendline(self.password)
            if self.expect([pexpect.TIMEOUT, unicode(self.prompt)], timeout=self.timeout,
                            timeout_error_message='Cannot get prompt after entering password') is not None:
                logging.debug('SSH session created with success')
                self.session_open = True
                return True
        return False

    def execute_command(self, command, prompt=None, timeout=None, eof=False):
        if not self.session_open:
            self.create_session()

        prompt = prompt if prompt else self.prompt
        timeout = timeout if timeout else self.timeout

        logging.debug('SSH: (%s) executing command %s , prompt %s, timeout %s',
                      self.ip, command, prompt, timeout)
        self.child.sendline(command)
        expect_options = [pexpect.TIMEOUT, unicode(prompt)] if not eof else [
            pexpect.TIMEOUT, unicode(prompt), pexpect.EOF]
        if self.expect(expect_options, timeout=timeout) is not None:
            logging.debug(
                'SSH: (%s) command executed. Output is: \n %s', self.ip, self.child.before)
            return self.child.before

    def close(self):
        logging.debug('SSH: (%s) closing connection.', self.ip)
        self.session_open = False
        self.child.sendline('exit')
        self.expect([pexpect.TIMEOUT, pexpect.EOF])
        self.child.close()


class NoviflowSSH(SSH):
    def __init__(self, ip, user, port, password=None, prompt=None, timeout=3):
        SSH.__init__(self, ip, user, port, password,
                     prompt if prompt else "#", timeout)

    def create_session(self):
        result = super(NoviflowSSH, self).create_session()
        if result:
            result = self.execute_command('show config switch hostname')
            if result:
                regex = re.compile(r'Hostname:\s*(\S+)', re.IGNORECASE)
                match = regex.findall(self.child.before)
                self.prompt = '{}#'.format(match[0]) if match else self.prompt
                logging.debug('NOVIFLOW: current prompt %s', self.prompt)

                result = self.execute_command('show config page')
                if result:
                    pageRegex = re.compile(r'(off)', re.IGNORECASE)
                    pageConfig = pageRegex.findall(self.child.before)
                    if not pageConfig:
                        logging.debug("NOVIFLOW: disabling config page ")
                        return self.execute_command('set config page off')
                    else:
                        return result
