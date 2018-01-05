import cmd
import os
import sys
import time
from collections import namedtuple
from datetime import datetime, timedelta
from pathlib import Path

import pytz
from tzlocal import get_localzone


LogEntry = namedtuple('LogEntry', 'timestamp,title')


class Pymato(cmd.Cmd):
    prompt = 'pymato> '
    def __init__(self, *args, logfile=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._logfile = logfile
        self.log = []
        #2018-01-04 16:16:48.850268-06:00
        self.date_pat = '%Y-%m-%d %H:%M:%S.%f%z'
        self._logfile.seek(0)
        for line in self._logfile:
            raw_timestamp, title = line[:31], line[31:]
            self.log.append(LogEntry(
                datetime.strptime(raw_timestamp, self.date_pat),
                title.strip(),
            ))
        # TODO: Maybe make pymato a context manager? -W. Werner, 2018-01-04
        self._logfile.seek(0)
        self._logfile.truncate()
        self.log.sort()
        for entry in self.log:
            print(
                entry.timestamp.strftime(self.date_pat),
                entry.title,
                file=self._logfile,
            )

    def add_log(self, entry):
        self.log.append(LogEntry(datetime.now(pytz.utc), entry))
        print(
            self.log[-1].timestamp.strftime(self.date_pat),
            self.log[-1].title,
            file=self._logfile,
        )
        self._logfile.flush()

    def do_log(self, line):
        for log in self.log:
            print(log.timestamp.astimezone(get_localzone()), log.title)

    def do_pom(self, line):
        try:
            end = datetime.now() + timedelta(minutes=0, seconds=3)
            print('Task -', line)
            while datetime.now() <= end:
                diff = end-datetime.now()
                print('\r', str(diff).split('.')[0], sep='', end='')
                time.sleep(1)
            print('\nDone!\a')
        except KeyboardInterrupt:
            print('Aborted - save to log anyway?')
            choice = input('y/[n]: ')
            if choice.lower() in ('y', 'yes'):
                self.add_log(line)
        else:
            self.add_log(line)

    def do_quit(self, line):
        return True

    def do_EOF(self, line):
        return self.do_quit(line)

    do_q = do_quit


def main():
    # TODO: REMOVEME -W. Werner, 2018-01-04
    os.environ['TZ'] = 'America/Chicago'
    logfile = Path('pymato.log')
    logfile.touch(exist_ok=True)
    with logfile.open('r+') as f:
        mato = Pymato(logfile=f)
        if len(sys.argv) > 1:
            mato.onecmd(' '.join(sys.argv[1:]))
        else:
            Pymato(logfile=f).cmdloop()

if __name__ == '__main__':
    main()
