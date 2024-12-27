import os
from simple_salesforce import Salesforce

# Load environment variables
username = os.getenv('SALESFORCE_USERNAME_1')
password = os.getenv('SALESFORCE_PASSWORD_1')
security_token = os.getenv('SALESFORCE_SECURITY_TOKEN_1')

if not (username and password and security_token):
    print("Please set the SALESFORCE_USERNAME_1, SALESFORCE_PASSWORD_1, and SALESFORCE_SECURITY_TOKEN_1 environment variables.")
    exit(1)

# Authenticate with Salesforce
sf = Salesforce(username=username, password=password, security_token=security_token)
print(f"Authentication successful for user: {username}")

# Get total number of contacts
contact_count = sf.query("SELECT COUNT() FROM Contact")['totalSize']
print(f"Total contact records: {contact_count}")

def query_contacts(search_term):
    try:
        search_fields = ["FirstName", "LastName", "Account.Name", "Email"]
        query_parts = [f"{field} LIKE '%{search_term}%'" for field in search_fields]
        query = f"SELECT Id, FirstName, LastName, Account.Name, Email, Title, Description FROM Contact WHERE {' OR '.join(query_parts)}"
        
        results = sf.query(query)
        for record in results['records']:
            print(f"{len(results['records']) - results['records'].index(record)}. Contact ID: {record['Id']}")
            print(f"   FirstName: {record.get('FirstName', 'N/A')}")
            print(f"   LastName: {record.get('LastName', 'N/A')}")
            print(f"   Account Name: {record['Account']['Name'] if record['Account'] else 'N/A'}")
            print(f"   Email: {record.get('Email', 'N/A')}")
            print(f"   Title: {record.get('Title', 'N/A')}")
            print(f"   Description: {record.get('Description', 'N/A')}")
            print("-" * 60)
        return results
    except Exception as e:
        print(f"Error querying contacts: {e}")


def edit_contact(contact_id):
    try:
        print("\nEditing contact (press Enter to keep current value):")
        
        # Get current contact details
        contact = sf.Contact.get(contact_id)
        
        # Step through editable fields
        first_name = input(f"First Name [{contact.get('FirstName', '')}]: ").strip()
        last_name = input(f"Last Name [{contact.get('LastName', '')}]: ").strip()
        title = input(f"Title [{contact.get('Title', '')}]: ").strip()
        email = input(f"Email [{contact.get('Email', '')}]: ").strip()
        
        print("Description (Ctrl+D to finish):")
        description = []
        try:
            while True:
                line = input()
                description.append(line)
        except EOFError:
            pass
        description = '\n'.join(description).strip()
        
        # Prepare update data
        update_data = {}
        if first_name: update_data['FirstName'] = first_name
        if last_name: update_data['LastName'] = last_name
        if title: update_data['Title'] = title
        if email: update_data['Email'] = email
        if description: update_data['Description'] = description
        
        if update_data:
            sf.Contact.update(contact_id, update_data)
            print("\nContact updated successfully!")
            # Show updated contact
            updated_contact = sf.Contact.get(contact_id)
            print(f"\nUpdated Contact Details:")
            print(f"  FirstName: {updated_contact.get('FirstName', 'N/A')}")
            print(f"  LastName: {updated_contact.get('LastName', 'N/A')}")
            print(f"  Title: {updated_contact.get('Title', 'N/A')}")
            print(f"  Email: {updated_contact.get('Email', 'N/A')}")
            print(f"  Description: {updated_contact.get('Description', 'N/A')}")
        else:
            print("\nNo changes made.")
            
    except Exception as e:
        print(f"Error editing contact: {e}")

def main_menu():
    while True:
        print("\n1. Query and Edit Contacts")
        print("2. Exit")
        choice = input("Enter your choice (1 or 2): ")

        if choice == '1':
            search_term = input("\nEnter search criteria: \n").strip()
            results = query_contacts(search_term)
            if results and results['records']:
                try:
                    contact_num = input("\nEnter contact number to edit (or Enter to continue): ").strip()
                    if contact_num:
                        selected_contact = results['records'][-int(contact_num)]
                        edit_contact(selected_contact['Id'])
                except (ValueError, IndexError):
                    print("Invalid contact number")
        elif choice == '2':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main_menu()