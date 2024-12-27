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

def query_contacts(search_term):
    try:
        search_fields = ["FirstName", "LastName", "Account.Name", "Email"]
        query_parts = [f"{field} LIKE '%{search_term}%' OR" for field in search_fields]
        query = f"SELECT Id, FirstName, LastName, Account.Name, Email, Title, Description FROM Contact WHERE {' AND '.join(query_parts[:-1])}"
        
        results = sf.query(query)
        for record in results['records']:
            print(f"Contact ID: {record['Id']}")
            print(f"  FirstName: {record.get('FirstName', 'N/A')}")
            print(f"  LastName: {record.get('LastName', 'N/A')}")
            print(f"  Account Name: {record['Account']['Name'] if record['Account'] else 'N/A'}")
            print(f"  Email: {record.get('Email', 'N/A')}")
            print(f"  Title: {record.get('Title', 'N/A')}")
            print(f"  Description: {record.get('Description', 'N/A')}")
            print("-" * 40)
    except Exception as e:
        print(f"Error querying contacts: {e}")


def main_menu():
    while True:
        print("\n1. Query Contacts")
        print("2. Exit")
        choice = input("Enter your choice (1 or 2): ")

        if choice == '1':
            search_term = input("Enter search criteria: ").strip()
            query_contacts(search_term)
        elif choice == '2':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main_menu()