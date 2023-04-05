from collections import UserDict

class Field:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        self.value = value

class Phone(Field):
    def __init__(self, value):
        self.value = value

class Record:
    def __init__(self, name, phone=None):
        self.name = name
        self.phones = [phone] if phone else []
    
    def add_phone(self, phone):
        self.phones.append(phone)
    
    def change_phone(self, phone, ind):
        self.phones[ind] = phone
    
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    
    def change_record(self, name, record):
        self.data[name.value] = record

    def search_records(self, name):
        search_records = []
        for key in self.data:
            if name.lower() in key.lower():
                search_records.append(self.data[key])
        return search_records
contacts = AddressBook()

def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return 'No name or phone, try again or enter help'
        except KeyError:
            return 'No name or phone, try again or enter help'        
    return inner  

def hello(args) -> str:
    return 'How can I help you?'

def help(args) -> str:
    return '''
    hello -- just hello
    add name phone -- add new contact
    change name phone -- change contact phone
    phone name -- print contact phone
    show all -- print all contacts
    exit, goodbye, close -- exit program'''

@input_error
def add(args) -> str:
    name = Name(args[0])
    phone = Phone(args[1])
    if name.value in contacts:
        record = contacts[name.value]
        record.add_phone(phone)
        return f'Another phone for contact {name.value} added'
    else:
        record = Record(name)
        record.add_phone(phone)
        contacts.add_record(record)
        return f'Contact {name.value} added successfully.'

@input_error
def change(args) -> str:
    name = Name(args[0])
    phone = Phone(args[1])
    record = contacts[name.value]
    record.change_phone(phone, 0)
    return f'Contact {name.value} modified successfully.'

@input_error
def phone(args) -> str:
    name = Name(args[0])
    result = contacts.search_records(name.value)
    if result:
        for record in result:
            return f"{', '.join(str(phone) for phone in record.phones)}"

    return f'Have not contact {name.value}'

def show_all(args) ->str:
    result = ''
    for name in contacts.data:
        record = contacts.data[name]
        result += f"{record.name.value}: {', '.join(str(phone) for phone in record.phones)}\n"
    return result.strip()

def unknown_command(*args):
    return "Invalid command"

COMMANDS = {hello: 'hello', help: 'help', add: 'add', change: 'change', phone: 'phone', show_all: 'show all'}


def command_handler(input_com: str):
    for func, val in COMMANDS.items():
        if input_com.lower().startswith(val):
            args = input_com.replace(val, '').strip().split(' ')
            return func, args
    return unknown_command, None

def main():
    while True:
        command = input('>>>')
        EXIT = ['exit', 'goodbye', 'close']
        if command.lower() in EXIT:
            print('Good bye')
            break
        func, args = command_handler(command)
        print(func(args))
        
        
        

if __name__ == '__main__':
    main()