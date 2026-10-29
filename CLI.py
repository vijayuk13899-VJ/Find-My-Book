# I acknowledge the use of Microsoft Copilot (AI) to assist me in reviewing.
# The final implementation, testing, and submission were completed independently.

import csv
import os

# Function to load subjects and their classmarks from a CSV file
def load_subjects(filename):
    subjects = []
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row because we only care about the data
            for row in reader:
                # Make sure we have at least two columns before using them
                if len(row) >= 2:
                    # Store subject name and classmark (always uppercase for consistency)
                    subjects.append({'subject': row[0], 'classmark': row[1].upper()})
    except FileNotFoundError:
        # Friendly error if the file is missing
        print(f"Oops! Couldn't find the file '{filename}'. Please check the filename and try again.")
    except Exception as e:
        # Catch any other unexpected errors
        print(f"Something went wrong while loading subjects: {e}")
    return subjects

# Function to load locations from a CSV file
def load_locations(filename):
    locations = {}
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row
            for row in reader:
                # Only process rows that have at least two values
                if len(row) >= 2:
                    # Store classmark as key and location as value
                    locations[row[0].upper()] = row[1]
    except FileNotFoundError:
        print(f"Oops! Couldn't find the file '{filename}'. Please check the filename and try again.")
    except Exception as e:
        print(f"Something went wrong while loading locations: {e}")
    return locations



# Function to display the menu and get user's choice
def get_menu_choice(valid_choices={'1', '2', '3'}):
    while True:
        print("\nHow would you like to search?")
        print("1. By subject name")
        print("2. By classmark")
        print("3. By location")
        choice = input("Please enter 1, 2, or 3: ").strip()
        if choice in valid_choices:
            return choice
         # If user types something invalid, gently remind them
        print("Hmm, that doesn't look right. Try entering 1, 2, or 3.\n")

# Function to ask what the user wants to do after a search
def ask_search_next_step():
    while True:
        print("\nWhat would you like to do next?")
        print("1. Search again")
        print("2. Exit the app")
        next_choice = input("Enter 1 to search again or 2 to quit: ").strip()
        if next_choice in {'1', '2'}:
            return next_choice
        print("Sorry, I didn't catch that. Please enter 1 or 2.\n")

# Main program loop
def main():
    print("Welcome to the Library Lookup Tool ")
    
    # Figure out where this script is running from
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Build file paths for subjects and locations CSVs
    subjects_file = os.path.join(script_dir, 'subjects.csv')
    locations_file = os.path.join(script_dir, 'locations.csv')
    
    # Load data from CSV files
    subjects = load_subjects(subjects_file)
    locations = load_locations(locations_file)


    # If either file failed to load, stop the program politely
    if not subjects or not locations:
        print("Uh-oh! Looks like we couldn't load the data. Please check your CSV files and try again.")
        return

    # Keep looping until the user decides to quit
    while True:
        choice = get_menu_choice()

        # Search by subject name
        if choice == '1':
            query = input("Type subject name (or part of it): ").strip().lower()
            if not query:
                print("You need to enter something to search for.")
            else:
                # Find all subjects that contain the search term
                matches = [
                    f"{item['classmark']} - {locations.get(item['classmark'], 'Unknown location')} - {item['subject']}"
                    for item in subjects if query in item['subject'].lower()
                ]
                if matches:
                    print("\nHere are the matches we found:")
                    for match in matches:
                        print(match)
                else:
                    print("No subjects matched your search.")
        # Search by classmark
        elif choice == '2':
            query = input("Enter the classmark: ").strip().upper()
            if not query:
                print("Classmark can't be empty.")
            else:
                # Look for exact classmark matches
                matches = [
                    f"{query} - {locations.get(query, 'Unknown location')} - {item['subject']}"
                    for item in subjects if query == item['classmark']
                ]
                if matches:
                    print("\nHere's what we found:")
                    for match in matches:
                        print(match)
                else:
                    print("No subjects found with that classmark.")

        # Search by location
        elif choice == '3':
            query = input("Enter the location name (or part of it): ").strip().lower()
            if not query:
                print("Location can't be empty.")
            else:
                # Find subjects based on location search
                matches = [
                    f"{item['classmark']} - {locations.get(item['classmark'], 'Unknown location')} - {item['subject']}"
                    for item in subjects if query in locations.get(item['classmark'], '').lower()
                ]
                if matches:
                    print("\nHere are the subjects at that location:")
                    for match in matches:
                        print(match)
                else:
                    print("No subjects found at that location.")

     # Ask user what they want to do next
        next_step = ask_search_next_step()
        if next_step == '2':
            print("\nThanks for using the Library Lookup Tool. Have a great day!")
            break

# Run the app safely
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Handle Ctrl+C or Ctrl+D gracefully
        print("\nGoodbye!")
    except Exception as e:
        # Catch any other unexpected errors
        print("Something unexpected happened:", e)
