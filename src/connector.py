from database import create_tables, insert_sms, get_all_sms
from models.sms import SMS


def main():
    create_tables()

    sms1 = SMS(message="Hello", sender="John")
    insert_sms(sms1)

    sms2 = SMS(message="How are you?", sender="Alice")
    insert_sms(sms2)

    all_sms = get_all_sms()
    for sms in all_sms:
        print(f"ID: {sms.id}, Message: {sms.message}, Sender: {sms.sender}")


if __name__ == "__main__":
    main()
