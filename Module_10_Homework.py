from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self)

class Name(Field):
    pass

class Phone(Field):
    pass

class Record:
    def __init__(self, name: Name, phone=None):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
    
    def add_phone(self, phone: Phone):
        ph_count = 0
        for phone_number in self.phones:
            if phone_number.value == phone.value:
                ph_count += 1
        if not ph_count:
            self.phones.append(phone)
            return f'Я додав номер {phone.value} до списку контактів у {self.name}'
        return f'Номер {phone.value} вже є у списку контактів у {self.name}'
    
    def change_phone(self, old_phone: Phone, new_phone: Phone):
        ph_count = 0
        for phone_number in self.phones:
            if phone_number.value == new_phone.value:
                ph_count += 1
        if ph_count:
            return f'Номер {new_phone.value}, який ти хочеш додати замість {old_phone.value}, вже є у списку контактів у {self.name}'
        for phone_number in self.phones:
            if phone_number.value == old_phone.value:
                phone_number.value = new_phone.value
                return f'Я замінив номер {old_phone.value} на {new_phone.value} у списку контактів у {self.name}'
        return f'Я не знайшов номер {old_phone.value} у списку контактів у {self.name}'
    
    def del_phone(self, phone: Phone):
        ph_count = 0
        for phone_number in self.phones:
            if phone_number.value == phone.value:
                ph_count += 1
        if ph_count:
            for i in range(len(self.phones)):
                if self.phones[i].value == phone.value:
                    self.phones.pop(i)
                    print(f'Я видалив номер {phone} у {self.name}')
                    return f'Я видалив номер {phone} у {self.name}'
                else:
                    continue
            print(f'Я не знайшов номер {phone} у {self.name}')
            return f'Я не знайшов номер {phone} у {self.name}'
        else:
            print(f'Номеру {phone.value}, який ти хочеш видалити, немає у списку контактів у {self.name}')
            return f'Номеру {phone.value}, який ти хочеш видалити, немає у списку контактів у {self.name}'
    
    def __str__(self):
        return f"{self.name}: {', '.join(str(phone) for phone in self.phones)}"
            

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record
        phones_print = ", ".join(str(phone_print) for phone_print in record.phones)
        return f'Я додав контакт "{record.name}" з номером {phones_print} до книги контактів'
    
    def search_info(self, search_query):
        print("\nEntering to the search function")
        print(f'search_query: "{search_query}"')
        search_results = []
        for key_ab in self.data:
            record_name = str(self.data[key_ab].name)
            # phones_list = ', '.join(str(phone) for phone in self.data[key_ab].phones)
            if search_query.lower() in record_name.lower():
                search_results.append(f'"{search_query}" знайдено у {record_name}')
                continue
            for phone in self.data[key_ab].phones:
                if search_query.lower() in str(phone).lower():
                    search_results.append(f'"{search_query}" знайдено у {record_name}: {str(phone).lower()}')
        if search_results:
            search_results = '\n'.join(search_results)
            return search_results
        return f'Я не зміг знайти нічого по запиту {search_query}'

    def delete_record(self, name):
        if name in self.data:
            del self.data[name]
            return f'Я видалив запис {name}'
        return f'Я не зміг знайти запис {name}'

    def show_all_contacts(self):
        if self.values():
            return "\n".join(str(r) for r in self.values())
        else:
            return 'Книга контактів пуста'

    def __str__(self):
        return "\n" + "\n".join(str(record) for record in self.data.values())

address_book = AddressBook()

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Я не знайшов контакт"
        except ValueError:
            return "Неправильний формат вводу"
        except IndexError:
            return "Ти вказав неправильний формат команди. Будь ласка, спробуй ще раз або введи info для допомоги"
    return wrapper


@input_error
def hello_command(*args):
    return "Чим можу допомогти?"


@input_error
def info_command(*args):
    info_text = '''Доступні команди:
hello -- я привітаюсь.
info -- інформація про доступні команди.
add Ім'я номер_телефону -- додам до списку контакт з номером телефону.
change Ім'я старий_номер_телефону новий_номер_телефону -- зміню номер телефону для контакту.
phone Ім'я -- покажу номер/-и телефону контакту.
search що_шукати -- спробую знайти те, що тобі потрібно.
delete Ім'я -- видалю запис.
show all -- покажу всі збережені контакти з номерами телефонів.
good bye або close або exit -- закінчу роботу
    '''
    return info_text


@input_error
def add_contact_command(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    record = address_book.get(str(name))
    if record:
        return record.add_phone(phone)
    record = Record(name, phone)
    return address_book.add_record(record)
    

@input_error
def contact_change_command(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    record = address_book.get(str(name))
    if record:
        return record.change_phone(old_phone, new_phone)
    return f'Книга контактів не містить контакт {name}'


@input_error
def phone_command(*args):
    name = args[0]
    record = address_book.get(str(name))
    if record:
        phones_x = address_book.get(str(name)).phones
        p_list = []
        for p in phones_x:
            p_list.append(str(p))
        phones_x_list = " ".join(p_list)
        return f"Номер/-и телефону/-ів для контакту {name}: {phones_x_list}"
    return f'Книга контактів не містить контакт {name}'


@input_error
def search_command(*args):
    if args:
        search_query = str(args[0])
    if search_query:
        return address_book.search_info(search_query)
    return "Будь ласка, напиши, що треба шукати"


@input_error
def delete_command(*args):
    if len(args) != 1:
        return "Будь ласка, введи команду для видалення у правильному форматі"
    name = args[0]
    record = address_book.get(str(name))
    if record:
        address_book.delete_record(str(name))
        return f"Я видалив запис {name}"
    return f"У адресній книзі немає контакту {name}"


@input_error
def show_all_contacts_command():
    return address_book.show_all_contacts()


@input_error
def bad_command(*args):
    return "Я не впізнав команду. Будь ласка, спробуй ще раз або введи info для допомоги"


@input_error
def exit_command(*args):
    return "Good bye!"


@input_error
def input_parser(user_input):
    for command, arguments in COMMANDS.items():
        for argument in arguments:
            if user_input.lower().startswith(argument):
                if user_input[:len(argument)] != argument:
                    user_input = argument + user_input[len(argument):]
                return command(*user_input.replace(argument, "").strip().split())
    return bad_command()


COMMANDS = {
        info_command: ["info"],
        hello_command: ["hello"],
        add_contact_command: ["add"],
        contact_change_command: ["change"],
        phone_command: ["phone"],
        search_command: ["search"],
        delete_command: ["delete"],
        show_all_contacts_command: ["show all"],
        exit_command: ["good bye", "close", "exit"]
        }
    

def main():
    print("Вітаю! Я бот-помічник.")
    while True:
        user_input = input('\nВведи команду ("info" для допомоги) >>> ')
        result = input_parser(user_input)
        print(result)
        if result == "Good bye!":
            break
    
if __name__ == "__main__":
    main()