# contact_book.py - Contact Book Application
# Starter code for e003-exercise-data-structures

"""
Contact Book Application
------------------------
A simple contact management system using Python data structures.

Data Structure:
- Each contact is a dictionary with: name, phone, email, category, created_at
- All contacts are stored in a list

Complete the TODO sections below to finish the application.
"""

from datetime import datetime

# =============================================================================
# Initialize Contact Book
# =============================================================================
contacts: list[dict] = []


# =============================================================================
# DONE: Task 1 - Create the Contact Book
# =============================================================================

def add_contact(contacts: list[dict], name: str, phone: str, email: str, category: str) -> dict:
    """
    Add a new contact to the contact book.
    
    Args:
        contacts: The list of all contacts
        name: Contact's full name
        phone: Contact's phone number
        email: Contact's email address
        category: One of: friend, family, work, other
    
    Returns:
        The created contact dictionary
    """
    # DONE: Create a contact dictionary with all fields
    contact: dict = {
        "name": name,
        "phone": phone,
        "email": email,
        "category": category
    }

    # DONE: Add created_at timestamp using datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    contact["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # DONE: Append to contacts list
    contacts.append(contact)
    # DONE: Return the new contact
    return contact


# =============================================================================
# DONE: Task 2 - Display Contacts
# =============================================================================

def display_all_contacts(contacts: list[dict]) -> None:
    """
    Display all contacts in a formatted table.
    
    Output format:
    =============================================
                CONTACT BOOK (X contacts)
    =============================================
    #  | Name            | Phone         | Category
    ---|-----------------|---------------|----------
    1  | Alice Johnson   | 555-123-4567  | friend
    ...
    """

    # DONE: Print header with contact count
    contacts_header: str = f"""=============================================
                CONTACT BOOK ({len(contacts)} contacts)
=============================================
    """
    print(contacts_header)
    # DONE: Print table headers
    table_header: str = f"""#  | Name            | Phone         | Category
---|-----------------|---------------|----------"""
    print(table_header)

    # DONE: Loop through contacts and print each row
    count_spacer_len: int = len("1  ")
    name_spacer_len: int = len("Alice Johnson   ")
    phone_spacer_len: int = len("555-123-4567   ")
    category_spacer_len: int = len("")

    for i, contact in enumerate(contacts):
        print(f"{i+1:>{count_spacer_len}}| {contact["name"]:>{name_spacer_len}}|{contact["phone"]:^{phone_spacer_len}}| {contact["category"]:>{category_spacer_len}}")
    

    # DONE: Print footer
    
    print("=============================================")


def display_contact_details(contact: dict) -> None:
    """
    Display detailed information for a single contact.
    
    Output format:
    --- Contact Details ---
    Name:     [name]
    Phone:    [phone]
    Email:    [email]
    Category: [category]
    Added:    [created_at]
    ------------------------
    """
    # DONE: Print formatted contact details
    
    contact_details_str: str = f"""--- Contact Details ---
Name:     {contact["name"]}
Phone:    {contact["phone"]}
Email:    {contact["email"]}
Category: {contact["category"]}
Added:    {contact["created_at"]}
------------------------"""

    print(contact_details_str)



# =============================================================================
# DONE: Task 3 - Search Functionality
# =============================================================================

def search_by_name(contacts: list[dict], query: str) -> list:
    """
    Find contacts whose name contains the query string.
    Case-insensitive search.
    
    Returns:
        List of matching contacts
    """
    # DONE: Filter contacts where query is in name (case-insensitive)
    # Hint: Use list comprehension and .lower()
    
    return [contact for contact in contacts if contact["name"].lower() == query.lower()]


def filter_by_category(contacts: list[dict], category: str) -> list:
    """
    Return all contacts in a specific category.
    
    Returns:
        List of contacts matching the category
    """
    # DONE: Filter contacts by category
    return [contact for contact in contacts if contact["category"].lower() == category.lower()]



def find_by_phone(contacts: list[dict], phone: str) -> dict|None:
    """
    Find a contact by exact phone number.
    
    Returns:
        The contact dictionary if found, None otherwise
    """
    # DONE: Search for contact with matching phone
    for contact in contacts:
        if contact["phone"] == phone:
            return contact
    
    return None


# =============================================================================
# TODO: Task 4 - Update and Delete
# =============================================================================

def update_contact(contacts: list[dict], phone: str, field: str, new_value: str) -> bool:
    """
    Update a specific field of a contact.
    
    Args:
        contacts: The list of all contacts
        phone: Phone number to identify the contact
        field: The field to update (name, phone, email, or category)
        new_value: The new value for the field
    
    Returns:
        True if updated, False if contact not found
    """
    # DONE: Find contact by phone
    target_contact = find_by_phone(contacts, phone)

    # if condition True, contact not found by phone 
    if target_contact is None:
        return False

    # DONE: Update the specified field
    target_contact[field] = new_value

    # DONE: Return success/failure

    # already returning failure before attempting to update field to avoid error
    return True


def delete_contact(contacts: list[dict], phone: str) -> bool:
    """
    Delete a contact by phone number.
    
    Returns:
        True if deleted, False if not found
    """
    # TODO: Find and remove contact with matching phone
    
    target_contact: dict = find_by_phone(contacts, phone)
    
    # not found, return False
    if target_contact is None:
        return False
    
    # remove contact
    contacts.remove(target_contact)


# =============================================================================
# TODO: Task 5 - Statistics
# =============================================================================

def display_statistics(contacts):
    """
    Display statistics about the contact book.
    
    Output:
    --- Contact Book Statistics ---
    Total Contacts: X
    By Category:
      - Friends: X
      - Family: X
      - Work: X
      - Other: X
    Most Recent: [name] (added [date])
    -------------------------------
    """
    # DONE: Count total contacts
    total_contacts: int = len(contacts)

    # DONE: Count contacts by category
    categories: dict = {}

    # either increment category score, or initialize to 1 if it's first time coming across it
    for contact in contacts:
        try:
            categories[contact["category"]] += 1
        except KeyError:
            categories[contact["category"]] = 1

    # DONE: Find most recently added contact
    most_recent_contact: dict|None = None
    for contact in contacts:
        created_at_obj: datetime.datetime = datetime.strptime(contact["created_at"], "%Y-%m-%d %H:%M:%S")
        
        # if first iteration, initialize most_recent_contact to first contact & start next iteration
        if most_recent_contact is None:
            most_recent_contact = contact
            continue

        else:
            recent_created_at_obj: datetime.datetime = datetime.strptime(most_recent_contact["created_at"], "%Y-%m-%d %H:%M:%S")
            # compare created ats, "greater" time will be most recent
            if created_at_obj > recent_created_at_obj:
                most_recent_contact = contact

    print("--- Contact Book Statistics ---")
    print(f"Total Contacts: {total_contacts}")
    print("By Category: ")

    # sort categories in descending manner to be listed
    sorted_categories: dict = {k: v for k, v in sorted(categories.items(), key=lambda x: x[1], reverse=True)}
    for category, num in sorted_categories.items():
        print(f"\t- {category+":":<10} {num}")

    print(f"Most Recent: {most_recent_contact["name"]} (added {most_recent_contact["created_at"]})")

# =============================================================================
# STRETCH GOAL: Interactive Menu
# =============================================================================

def display_menu():
    """Display the main menu."""
    print("\n========== CONTACT BOOK ==========")
    print("1. View all contacts")
    print("2. Add new contact")
    print("3. Search contacts")
    print("4. Update contact")
    print("5. Delete contact")
    print("6. View statistics")
    print("0. Exit")
    print("==================================")


def main():
    """Main function with interactive menu."""
    # TODO: Implement menu loop
    # Use while True and break on exit choice

    while True:
        display_menu()

        choice: str = input("Enter choice (int): ")

        # If fail to convert to integer, prompt user to enter one
        try:
            choice = int(choice)
        except TypeError:
            print("Please enter an integer.")
            continue

        # If fail to enter valid option, prompt user to enter one
        if choice not in range(7):
            print("Please enter valid option number.")
            continue
    
        # if we get here, the user's option was valid

        match choice:
            case 1: # view contacts
                display_all_contacts(contacts)
            case 2: # add contact
                name: str = input("Enter the contact's name: ")
                phone: str = input("Enter the contact's phone: ")
                email: str = input("Enter the contact's email: ")
                category: str = input("Enter the contact's category: ")

                add_contact(contacts, name, phone, email, category)
                print(f"Added {name} to contacts.")
            case 3: # search contacts
                query: str = input("Enter name of contact to search: ")

                matching_contacts: list[dict] = search_by_name(contacts, query)
                print("Here is a list of contacts with a matching name: ")
                [print(f"\t{x+1}) {contact}") for x, contact in enumerate(matching_contacts)]
            

            case 4: # update contact
                phone: str = input("Enter the contact's phone: ")
                field: str = input("Enter the contact field to change: ")
                new_value: str = input("Enter the new field value: ")

                if update_contact(contacts, phone, field, new_value):
                    print("Successfully updated contact info.")
                else:
                    print("Unable to find contact with matching phone.")

            case 5: # delete contact
                phone: str = input("Enter the contact's phone: ")

                if delete_contact(contacts, phone):
                    print("Successfully deleted contact.")
                else:
                    print("Unable to find contact with matching phone.")

            case 6: # View statistics
                display_statistics(contacts)

            case 0: # exit 
                print("Thank you for using the best content book created to date.")
                exit()


        input("Press enter to continue.")

# =============================================================================
# Test Code - Add sample data and test functions
# =============================================================================

if __name__ == "__main__":
    print("Contact Book Application")
    print("=" * 40)

    # contacts: list = []
    
    # DONE: Add at least 5 sample contacts
    add_contact(contacts, "Alice Johnson", "555-123-4567", "alice@example.com", "Friend")
    add_contact(contacts, "Tommy Jenkins", "323-531-5020", "tommy@tommy.tommy", "Friend")
    add_contact(contacts, "Stephanie Pearce", "111-111-2222", "piercethestephanie@ptv.com", "Family")
    add_contact(contacts, "Jack Greene", "867-530-9123", "jgreenethemean@nice.xyz", "Work")
    add_contact(contacts, "Haley Mann", "321-321-4321", "haleym@aol.org", "Work")
    add_contact(contacts, "Snowball Well", "246-802-4680", "the.animals.are.well@aok.com", "Work")
    add_contact(contacts, "Orville Red", "000-111-2222", "orville_theoneandonly@wikipedia.org", "Other")

    # DONE: Test your functions
    TEST: bool = False
    if TEST:
        print("Testing display_all_contacts")
        display_all_contacts(contacts)

        print("\nTesting display_contact_details")
        display_contact_details(contacts[0])

        print("\nTesting search_by_name")
        print(search_by_name(contacts, "Jack Greene"))

        print("\nTesting filter_by_category")
        print(filter_by_category(contacts, "Work"))

        print("\nTesting find_by_phone")
        print(find_by_phone(contacts, "000-111-2222"))

        print("\nTesting update_contact")
        update_contact(contacts, "000-111-2222", "name", "Father Popcorn")
        display_contact_details(find_by_phone(contacts, "000-111-2222"))

        print("\nTesting delete_contact")
        delete_contact(contacts, "000-111-2222")
        display_all_contacts(contacts)

        print("\nTesting display_statistics")
        display_statistics(contacts)
        print(contacts[-1]["created_at"])

    # STRETCH: Uncomment to run interactive menu
    main()
