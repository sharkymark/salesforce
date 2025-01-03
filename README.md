# Salesforce CLI App

A Python command-line interface for interacting with Salesforce.com

## Features
- Authenticate using environment variables
- Display total contact count
- Query contacts by FirstName, LastName, Account.Name, or Email
- Edit contacts with field-by-field updates
  - Multiline Description input using Ctrl+D
  - Preserve original values for unchanged fields
- Verify updates after saving changes
- Backup all contacts to files (sorted by Account and LastName)
  - contacts_backup.txt: Human-readable format
  - contacts_backup.csv: Machine-readable format with column headers

## Setup

1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv_salesforce
   source venv_salesforce/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set required environment variables:
   ```bash
   export SALESFORCE_USERNAME_1="your_username"
   export SALESFORCE_PASSWORD_1="your_password"
   export SALESFORCE_SECURITY_TOKEN_1="your_security_token"
   ```

## Usage

Run the application:
```bash
python salesforce.py
```

### Menu Options
1. Query Contacts
   - Enter search criteria
   - View matching contacts
   - Option to edit a contact
2. Backup Contacts
   - Export all contacts to both contacts_backup.txt and contacts_backup.csv (overwrites existing files)
   - Includes: FirstName, LastName, Account.Name, Email, Title, Phone, Description
   - CSV format includes column headers for easy import
   - Sorted by Account.Name then LastName
3. Exit

### Editing Contacts
- After querying, select a contact to edit
- Step through editable fields:
  - FirstName
  - LastName
  - Title
  - Email
  - Description (multiline input with Ctrl+D)
- Press Enter to keep current value
- Changes are saved and verified

## Requirements
- Python 3.x
- simple_salesforce package