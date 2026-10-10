import argparse
import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("contacts.json")


def main():
    parser = argparse.ArgumentParser(description="Keep a searchable local address book.")
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add", help="Add a contact.")
    add.add_argument("name")
    add.add_argument("--phone", default="")
    add.add_argument("--email", default="")
    commands.add_parser("list", help="Show all contacts.")
    search = commands.add_parser("search", help="Search names, phone numbers, and email addresses.")
    search.add_argument("query")
    delete = commands.add_parser("delete", help="Remove a contact by ID.")
    delete.add_argument("id", type=int)
    args = parser.parse_args()
    if DATA_FILE.exists():
        with DATA_FILE.open(encoding="utf-8") as file:
            contacts = json.load(file)
    else:
        contacts = []

    if args.command == "add":
        if any(contact["name"].casefold() == args.name.casefold() for contact in contacts):
            parser.error(f'A contact with the name "{args.name}" already exists.')
        contact_id = max((contact["id"] for contact in contacts), default=0) + 1
        contact = {"id": contact_id, "name": args.name, "phone": args.phone, "email": args.email}
        contacts.append(contact)
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(contacts, file, indent=2, ensure_ascii=False)
        print(f"Added contact {contact_id}: {args.name}")
    elif args.command in ("list", "search"):
        matching = contacts
        if args.command == "search":
            query = args.query.casefold()
            matching = [
                contact for contact in contacts
                if query in contact["name"].casefold()
                or query in contact["phone"].casefold()
                or query in contact["email"].casefold()
            ]
        if not matching:
            print("No matching contacts.")
        for contact in matching:
            details = " | ".join(value for value in (contact["phone"], contact["email"]) if value)
            print(f'[{contact["id"]}] {contact["name"]}' + (f" | {details}" if details else ""))
    else:
        contact = next((item for item in contacts if item["id"] == args.id), None)
        if contact is None:
            parser.error(f"No contact has ID {args.id}.")
        contacts.remove(contact)
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(contacts, file, indent=2, ensure_ascii=False)
        print(f'Removed contact: {contact["name"]}')


if __name__ == "__main__":
    main()
