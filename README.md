# Personal Contact Book

Save names with an optional phone number and email address; list your contacts,
search for a name, email, or phone number, and remove an entry by its ID.

```text
python main.py add "Alex Morgan" --phone "555-0100" --email "alex@example.com"
python main.py add "Sam Lee" --email "sam@example.com"
python main.py list
python main.py search "Alex"
python main.py delete 1
```

Contacts are saved in `contacts.json`. Contact details are private and the data
file is excluded from Git. Avoid using the example details as real contact data.
