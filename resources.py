import os
import json


class Entry:
    def __init__(self, title, entries=None, parent=None):
        self.title = title
        if entries is None:
            entries = []
        self.entries = entries
        self.parent = parent

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent + 1)

    def json(self):
        res = {
            'title': self.title,
            'entries': [entryy.json() for entryy in self.entries],
        }
        return res

    @classmethod
    def from_json(cls, value: dict):
        entry_new = cls(value['title'])
        for item in value.get('entries', []):
            entry_new.add_entry(cls.from_json(item))
        return entry_new

    def save(self, path):
        with open(os.path.join(path, f'{self.title}.json'), 'w') as file:
            file.write(json.dumps(self.json()))

    @classmethod
    def load(cls, filename):
        with open(filename, 'r') as file:
            data = file.read()
        return cls.from_json(json.loads(data))

    def __str__(self):
        return self.title


class EntryManager:
    def __init__(self, data_path):
        self.data_path = data_path
        self.entries = []

    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)

    def load(self):
        for file_json in os.listdir(self.data_path):
            if file_json.endswith(".json"):
                self.entries.append(Entry.load(os.path.join(self.data_path, file_json)))

    def add_entry(self, title: str):
        self.entries.append(Entry(title))


def print_with_indent(value, indent=0):
    tab = '\t' * indent
    print(f'{tab}{value}')
