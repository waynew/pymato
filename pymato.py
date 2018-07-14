import cmd
import os
import sys
import time
from collections import namedtuple
from datetime import datetime, timedelta
from pathlib import Path

import pytz
from tzlocal import get_localzone

__version__ = '0.1.8'
POM_MINS = 25


def hms(seconds):
    '''
    Take a number of seconds and return hours, minutes, and seconds
    '''
    seconds = int(seconds)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return h, m, s


def pretty_hms(h=0, m=0, s=0):
    '''
    Return the provided h, m, and s in the format HhMmSs. If any of the
    values are 0, then they will be blank spaces unless *all* values are zero,
    in which case, return '      0s'.

    >>> pretty_hms()
    '       0s'
    >>> pretty_hms(0,0,0)
    '       0s'
    >>> pretty_hms(1,0,0)
    ' 1h      '
    >>> pretty_hms(1,2,5)
    ' 1h 2m 5s'
    >>> pretty_hms(1,2,50)
    ' 1h 2m50s'
    >>> pretty_hms(99,23,50)
    '99h23m50s'
    '''
    hrs = f'{h:>2}h' if h else ' '*3
    mins = f'{m:>2}m' if m else ' '*3
    secs = f'{s:>2}s' if s else ' '*3
    elapsed_time = f'{hrs}{mins}{secs}'
    return elapsed_time if elapsed_time.strip() else '       0s'


class LogEntry:
    def __init__(self, start, end, title):
        self.start = start
        self.end = end
        self.title = title

    def __repr__(self):
        return f'LogEntry(title={self.title!r}, start={self.start!r}, end={self.end!r})'

    def __lt__(self, other):
        return self.start < other.start

    def format(self, datefmt, tz=pytz.utc):
        start = self.start.astimezone(tz).strftime(datefmt)
        if self.end:
            end = self.end.astimezone(tz).strftime(datefmt)
        else:
            end = ' ' * len(start)
        return f'{start} {end} {self.title}'

    def elapsed_format(self, tz=pytz.utc):
        elapsed = self.end - self.start
        return f'{pretty_hms(*hms(elapsed.total_seconds())):>6} {self.title}'

    @property
    def elapsed_seconds(self):
        end = self.end or datetime.now(tz=pytz.utc)
        return (self.end-self.start).total_seconds()


class Pymato(cmd.Cmd):
    prompt = 'pymato> '
    def __init__(self, *args, logfile=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._logfile = logfile
        self.log = []
        #2018-01-04 16:16-06:00
        self.date_pat = '%Y-%m-%d %H:%M:%S%z'
        self._logfile.seek(0)
        for line in self._logfile:
            raw_timestamp_start, raw_timestamp_end, title = line[:24], line[25:49], line[49:]
            if raw_timestamp_end.strip() == '':
                end_timestamp = None
            else:
                end_timestamp = datetime.strptime(
                    raw_timestamp_end,
                    self.date_pat,
                )
            self.log.append(LogEntry(
                start=datetime.strptime(raw_timestamp_start, self.date_pat),
                end=end_timestamp,
                title=title.strip(),
            ))
        # TODO: Maybe make pymato a context manager? -W. Werner, 2018-01-04
        self._logfile.seek(0)
        self._logfile.truncate()
        self.log.sort()
        for entry in self.log:
            print(
                entry.format(self.date_pat),
                file=self._logfile,
            )

    def add_log(self, title, start, end):
        self.log.append(LogEntry(
            start=start,
            end=end,
            title=title,
        ))
        print(
            self.log[-1].format(self.date_pat),
            file=self._logfile,
        )
        self._logfile.flush()

    def do_log(self, line):
        '''
        Display a log of your time spent.
        '''
        def logfilter(entry): return True

        if line.strip():
            try:
                filterdate = datetime.strptime(line.strip(), '%Y-%m-%d').date()
                def logfilter(entry):
                    return entry.start.date() == filterdate
            except ValueError:
                def logfilter(entry):
                    return entry.title.lower() == line.lower()
        self.log.sort()
        printlogs = [log for log in sorted(self.log) if logfilter(log)]
        if printlogs:
            date = printlogs[0].start.date()
            print(date)
        total_time = 0
        for log in printlogs:
            if not logfilter(log):
                continue
            if log.start.date() != date:
                date = log.start.date()
                print(f'\n{date}')
            print(f'\t{log.elapsed_format(tz=get_localzone())}')
            total_time += log.elapsed_seconds

        print('-'*30)
        print(f'\t{pretty_hms(*hms(total_time)):>9} total pomodoro time')

    def do_track(self, line):
        '''
        Start tracking time on an open-ended task. ^c to stop. You will
        have the option to save (the default) or discard the time.
        '''
        start = datetime.now(pytz.utc)
        try:
            print('Task -', line)
            while True:
                diff = datetime.now(pytz.utc)-start
                print('\r', str(diff).split('.')[0], sep='', end='')
                time.sleep(1)
        except KeyboardInterrupt:
            end = datetime.now(pytz.utc)
            print('\n{} time spent, save?'.format(str(diff).split('.')[0]))
            choice = input('[y]/n: ').strip()
            if choice.lower() in ('y', 'yes', ''):
                self.add_log(title=line, start=start, end=end)

    def do_pom(self, line):
        '''
        Start recording a pom, with whatever description you provide.

        ^c interrupts your pom, though you can save your current progress.
        '''
        start = datetime.now(pytz.utc)
        end = start + timedelta(minutes=POM_MINS, seconds=0)
        try:
            print('Task -', line)
            while datetime.now(pytz.utc) <= end:
                diff = end-datetime.now(pytz.utc)
                print('\r', str(diff).split('.')[0], sep='', end='')
                time.sleep(1)
            print('\nDone!\a')
        except KeyboardInterrupt:
            end = datetime.now(pytz.utc)
            print('Aborted - save to log anyway?')
            choice = input('y/[n]: ')
            if choice.lower() in ('y', 'yes'):
                self.add_log(title=line, start=start, end=end)
        else:
            self.add_log(title=line, start=start, end=end)

    def do_version(self, line):
        print(f'pymato {__version__}')

    def do_quit(self, line):
        '''
        Quit
        '''
        return True

    def do_EOF(self, line):
        '''
        Quit
        '''
        return self.do_quit(line)

    do_q = do_quit


def main():
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
