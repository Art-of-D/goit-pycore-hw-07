from internal.addressbook import AddressBook
from internal.record import Record

def load_contacts():
    contacts = AddressBook()
    try:
        with open("./assistant/storage/phonebook.txt", "r") as file:
            for line in file:
                fields = line.strip().split(",")
                if len(fields) < 3:
                    print("Skipping invalid contact: {}".format(line))
                    continue
                name = fields[0].strip()
                phones = [field.strip() for field in fields[1:-1] if field.strip()]
                birthday = fields[-1].strip()
                contact = Record(name)
                for phone in phones:
                    try:
                        contact.add_phone(phone)
                    except ValueError as e:
                        print(f"Skipping invalid phone '{phone}': {e}")
                if birthday != "None":
                    contact.set_birthday(birthday)
                contacts.add_record(contact)
            return contacts
    except FileNotFoundError:
        print("No contacts found. Please add new contact.")
        return contacts

def record_contacts(contacts):
  with open("./assistant/storage/phonebook.txt", "w") as file:
    try :
        print("Saving contacts...")
        if len(contacts) == 0:
            print("No contacts to save.")
            return
        records = "\n".join(f"{value.get_name()}, {', '.join(phone.get_value() for phone in value.get_phones())}, {value.get_birthday()}" for key, value in contacts.items())
        file.write(records)
    except Exception as e:
        print(f"Error saving contacts: {e}")
    finally:
        contacts = {}

def parse_input(user_input):
    if not user_input:
        print("Please enter a command.")
        return "commands", []
    else: 
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, *args


def main():
    
    print("Welcome to the assistant bot!")
    ab = load_contacts()
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            record_contacts(ab)
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            new_contact = Record(args[0])
            if len(args) > 1: 
                print(new_contact.add_phone(args[1]))

            print(ab.add_record(new_contact))
        elif command == "change":
            print(ab.edit_phone(args[0], args[1]))
        elif command == "delete":
            print(ab.delete(args[1]))
        elif command == "remove":
            print(ab.delete_phone(args[0], args[1]))
        elif command == "all":
            print(ab.list_contacts())
        elif command == "find":
            print(ab.find(args[0]))
        elif command == "phone":
            print(ab.find_phone(args[0]))
        elif command == "add-birthday":
            print(ab.add_birthday(args[0], args[1]))
        elif command == "show-birthday":
            print(ab.show_birthday(args[0]))
        elif command == "birthdays":
            print(ab.birthdays())
        elif command == "commands":
            print("Available commands: hello, add, change, delete, all, find - for name search, phone - for the phone search, remove, close OR exit")
        else:
            print("Invalid command. If you need help, type 'commands'.")

if __name__ == "__main__":
    main()