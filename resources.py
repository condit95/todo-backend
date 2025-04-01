from textwrap import indent
import json, os
from test_json import entry



def print_with_indent(value, indent=0):
    indentation = " " * indent
    print(indentation + str(value))

class Entry:
    def __init__(self, title, entries = None, parent=None):
        if entries is None:
            entries = []
        self.title = title
        self.entries = entries
        self.parent = parent

    def __str__(self):
        return self.title

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent+1)

    # -> dict
    def json(self):
        res = {
            'title': self.title,
            'entries': [entry.json() for entry in self.entries]
        }
        return res

    @classmethod
    def entry_from_json(cls, value: dict):
        new_entry = Entry(value['title'])
        for item in value.get('entries', []):
            new_entry.add_entry(cls.entry_from_json(item))
        return new_entry

    def save(self, path=''):
        with open(path, 'w', encoding='UTF-8') as file:
            json.dump(self.json(), file, ensure_ascii=False, indent=4)

    @classmethod
    def load(cls, filename):
        with open(filename, 'r', encoding='UTF-8') as file:
            json_dict = json.load(file)
            return cls.entry_from_json(json_dict)

class EntryManager:
    def __init__(self, data_path='/test'):
        self.data_path = data_path
        self.entries = []

    def save(self):
        for i in self.entries:
            name_directory = os.path.join(self.data_path,
                                   f'{i.title}.json')
            i.save(name_directory)


    def load(self):
        for i in os.listdir():
            if os.path.splitext(os.path.join(self.data_path,
                                             i)) == '.json':
                self.entries.append(Entry.load(i))

    def add_entry(self, title: str):
        new_entry = Entry(title)
        self.entries.append(new_entry)


if __name__ == '__main__':

    my_entry = Entry('Продукты')

    meet = Entry('Мясо')
    my_entry.add_entry(meet)

    sousages = Entry('Сосиски')
    meet.add_entry(sousages)

    egg = Entry('Яйцо')
    my_entry.add_entry(egg)


    milk = Entry('Молоко')
    my_entry.add_entry(milk)

    jogurt = Entry('Йогурт')
    milk.add_entry(jogurt)



    every_day_entry = Entry('Повседневные дела')

    sport_entry = Entry('Спорт')
    every_day_entry.add_entry(sport_entry)

    sport_entry_1 = Entry('Футбол')
    sport_entry.add_entry(sport_entry_1)

    sport_entry_2 = Entry('Тренажерный зал')
    sport_entry.add_entry(sport_entry_2)

    work = Entry('Работа')
    every_day_entry.add_entry(work)

    study = Entry('Учеба')
    every_day_entry.add_entry(study)

    manager = EntryManager()
    manager.add_entry(my_entry)
    manager.add_entry(every_day_entry)
    #manager.save()
    manager.load()
    for i in manager.entries:
        i.print_entries()



    # ensure_ascii печать русских букв
    # print(json.dumps(res, ensure_ascii=False, indent=2))


    # new_entry = Entry.entry_from_json(entry)
    # new_entry.print_entries()
    # print(new_entry.title)

