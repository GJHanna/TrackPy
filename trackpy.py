from csv import reader, writer, DictReader, DictWriter
from argparse import ArgumentParser
from os import chdir, path, getcwd
from time import time, localtime, asctime, strftime
from datetime import datetime
from dateutil.relativedelta import relativedelta

parser = ArgumentParser()
parser.add_argument('dir', help='add task')
parser.add_argument('-a', '--add', dest='task', nargs="+", action='store', help='add task')
parser.add_argument('-l', '--list', action='store_true', help='list all tasks')
parser.add_argument('-ld', '--done', action='store_true', help='list all done tasks')
parser.add_argument('-lnd', '--notdone', action='store_true', help='list all not done tasks')
parser.add_argument('-co', '--checkout', type=int, dest='taskd', action='store', help='mark task as done')

class CSVManager(object):
    fieldnames = ['task', 'status', 'added', 'finished', 'time']
    csv_file = '.task.csv'

    def __init__(self, row, l, ld, lnd, *args, **kwargs):
        if ((not path.isfile(self.csv_file)) or (path.isfile(self.csv_file) == 0)):
            self.__write()
        self.row = row
        self.l = l
        self.ld = ld
        self.lnd = lnd
    
    def read(self):
        try:
            self.headers()
            with open(self.csv_file, 'r') as f:
                reader = DictReader(f, delimiter='\t')
                i = 1

                for row in reader:                    
                    number = str(i) + ') '
                    task, status, added, finished, time = row[self.fieldnames[0]], \
                        row[self.fieldnames[1]], \
                            asctime(localtime(float(row[self.fieldnames[2]]))), \
                                row[self.fieldnames[3]], \
                                    row[self.fieldnames[4]]

                    if (finished != ''):
                        finished = asctime(localtime(float(finished)))
                    
                    if (status == 'D'):
                        color = '\033[92m'
                    
                    if (status == 'ND'):
                        color = '\033[91m'
                    
                    if (self.ld and status == 'D'):
                        print(
                            number                       +
                            task.ljust(55 - len(number)) +
                            color + status.ljust(10)     +
                            '\033[0m' 
                        )
                    
                    if (self.lnd and status == 'ND'):
                        print(
                            number                       +
                            task.ljust(55 - len(number)) +
                            color + status.ljust(10)     +
                            '\033[0m' 
                        )
                    
                    if (self.l):
                        print(
                            number                       +
                            task.ljust(55 - len(number)) +
                            color + status.ljust(10)     +
                            '\033[0m' + added.ljust(30)  +
                            finished.ljust(30)           +
                            '\033[93m' + time.ljust(5)   + 
                            '\033[0m'
                    )
                    
                    i += 1

            print('\n')
        
        except ValueError as err:
            print(err)
        except OSError as err:
            print(err)
        except Exception as err:
            print(err)
                
    def __write(self):
        with open(self.csv_file, 'w') as f:
            writer = DictWriter(f, fieldnames=self.fieldnames , delimiter='\t')
            writer.writeheader()

    def append(self):
        with open(self.csv_file, 'a') as f:
            writer = DictWriter(f, fieldnames=self.fieldnames , delimiter='\t')
            writer.writerow(self.row)
    
    def headers(self):
        if (self.ld or self.lnd ):
            print(
                '\n\033[94m'                         + 
                self.fieldnames[0].upper().ljust(55) +
                self.fieldnames[1].upper().ljust(10) +
                '\033[0m\n'
                )
        else:
            print(
                '\n\033[94m'                         + 
                self.fieldnames[0].upper().ljust(55) +
                self.fieldnames[1].upper().ljust(10) +
                self.fieldnames[2].upper().ljust(30) + 
                self.fieldnames[3].upper().ljust(30) +
                self.fieldnames[4].upper().ljust(5)  +
                '\033[0m\n'
                )

    def append_rows(self):
        with open(self.csv_file, 'a') as f:
            rows = writer(f, delimiter='\t')
            for datum in self.csv_data:
                rows.writerow(datum)

    def get_csv_data(self):
        self.csv_data = []
        with open(self.csv_file, 'r') as f:
            rows = reader(f, delimiter='\t')
            next(rows)
            for row in rows:
                self.csv_data.append(row)

        
    def check_out(self, n):
        try:
            self.get_csv_data()
            data_to_update = self.csv_data[n]
            
            if (data_to_update[1] != 'D'):
                data_to_update[1] = 'D'
                data_to_update[3] = time()

                start = datetime.fromtimestamp(float(data_to_update[2]))
                end   = datetime.fromtimestamp(float(data_to_update[3]))
                
                duration = relativedelta(end, start)
                output = ''

                if (duration.years):
                    output += '{}y '.format(duration.years)
                if (duration.months):
                    output += '{}m '.format(duration.months)
                if (duration.days):
                    if (duration.days < 9):
                        output += '0{}d '.format(duration.days)
                    else:
                        output += '{}d '.format(duration.days)
                if (duration.hours):
                    if (duration.hours < 9):
                        output += '0{}H '.format(duration.hours)
                    else:
                        output += '{}H '.format(duration.hours)
                if (duration.minutes):
                    if (duration.minutes < 9):
                        output += '0{}M '.format(duration.minutes)
                    else:
                        output += '{}M '.format(duration.minutes)

                data_to_update[4] = output
                
                self.csv_data[n] = data_to_update 
                self.__write()
                self.append_rows()

            else:
                raise TaskCheckedOutException

        except ValueError as err:
            exit('\033[91mFailed to check out\033[0m')
        except IndexError as err:
            exit("\033[91mTask doesn't exist in task file\033[0m")
        except TaskCheckedOutException as err:
            exit('\033[91mTask already checked-out\033[0m')

class TaskCheckedOutException(Exception):
    def __init__(self):
        pass

class Task(object):
    def __init__(self, task, l, ld, lnd, co, *args, **kwargs):
        self.task = task
        self.co = co
        self.__csv_manager = CSVManager(row=self.tokenize(), l=l, ld=ld, lnd=lnd)

    def append(self):
        self.__csv_manager.append()

    def read(self):
        self.__csv_manager.read()
    
    def check_out(self):
        if (self.co):
            self.__csv_manager.check_out(self.co - 1)

    def tokenize(self):
        return {
            'task' : self.task, 
            'status' : 'ND',
            'added' : time(),
        }

if __name__ == "__main__":
    try:
        args = parser.parse_args()
        chdir(args.dir)
        task_append = ''
        
        if (args.task):
            if (args.task > 0):
                task_append = ' '.join(args.task)
            else:
                task_append = args.task[0]

        task = Task(task=task_append, l=args.list, ld=args.done, lnd=args.notdone, co=args.taskd)
        
        if (args.task):
            task.append()
            exit()

        if (args.taskd):
            task.check_out()
            exit()
        
        if (args.list or args.done or args.notdone):
            task.read()
            exit()

    except Exception as err:
        print(err)