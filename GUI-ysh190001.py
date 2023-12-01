#Author: Yash Hooda
#Date Created: 11/27/2023
#This Project was a group project for my CS 4347 Database Systems class. 
# Worked on the GUI Interface.
#Tested 5 random books as part of the process, created a checkout, checkin, and randomized borrower data as part of the interface.
# Was part of a group project for the class. This was only my part of the project. Not the full project.


#Import packages
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta
from tkinter import StringVar

#Search Books function to find books
def search_books():
    query = search_entry.get().lower()
   
    # Clear previous search results
    for item in tree.get_children():
        tree.delete(item)

    # Iterate through your data and find matches
    for book in library_data:
        if query in book["ISBN"].lower() or query in book["Book Title"].lower() or query in book["Author"].lower():
            tree.insert("", "end", text=book["ISBN"], values=(book["Book Title"], book["Author"], book["Genre"], book["Year"], book["Status"]))
           

# Function to create a new BORROWER
def create_borrower():
    # Prompt for borrower details
    borrower_name = simpledialog.askstring("Create Borrower", "Enter Borrower's Name:")
    borrower_ssn = simpledialog.askstring("Create Borrower", "Enter Borrower's SSN:")
    borrower_address = simpledialog.askstring("Create Borrower", "Enter Borrower's Address:")

    # Validate if all required fields are provided
    if not borrower_name or not borrower_ssn or not borrower_address:
        messagebox.showerror("Error", "Name, SSN, and address are required to create a new account.")
        return

    # Generate a new card_no (replace this with your actual logic)
    new_card_no = generate_new_card_no()

    # Check if the SSN is unique
    if is_ssn_unique(borrower_ssn):
        # Insert the new BORROWER into the database (replace this with your actual database update logic)
        insert_into_borrowers(new_card_no, borrower_name, borrower_ssn, borrower_address)

        messagebox.showinfo("Success", f"Borrower created successfully with Card Number: {new_card_no}")
    else:
        messagebox.showerror("Error", "A borrower with the same SSN already exists.")

# Function to generate a new card_no
def generate_new_card_no():
    return "C" + str(int(datetime.now().timestamp()))

# Function to check if the SSN is unique
def is_ssn_unique(borrower_ssn):
    existing_borrowers = {
        "123-45-6789": {"card_no": "C123456789"},
        "987-65-4321": {"card_no": "C987654321"},
    }

    return borrower_ssn not in existing_borrowers

# Function to insert a new BORROWER into the database
def insert_into_borrowers(card_no, name, ssn, address):
    #insert the new BORROWER into the BORROWERS table
    print(f"BORROWER created with Card Number: {card_no}, Name: {name}, SSN: {ssn}, Address: {address}")


#Add to cart function to add books to the cart.
def add_to_cart():
    selected_item = tree.selection()
    if selected_item:
         
            book_title = tree.item(selected_item, "values")[0]
            book_status = tree.item(selected_item, "values")[-1]
            if book_status == "Available":
                if book_title not in cart:
                    cart.append(book_title)
                    messagebox.showinfo("Added to cart", f" {book_title} was successfully added to your cart.")
                else:
                    messagebox.showwarning("This book is already in your cart.")
            else:messagebox.showerror("Book is Checked out. Please select another book")
    else:
         messagebox.showwarning("No book selected", "please select a book to add in your cart")



#Checkout books function to select books for checkout.
def checkout_books():
    selected_items = tree.selection()
   
#If books haven't been selected for checkout, return error.
    if not selected_items:
        tk.messagebox.showinfo("Checkout", "Please select at least one book for checkout.")
        return

    # Prompt for borrower's card number
    card_number = tk.simpledialog.askstring("Checkout", "Enter Borrower's Card Number:")
    if not card_number:
        return  # User canceled the input

    # Generate unique keys for each checkout
    checkout_ids = [str(datetime.now().timestamp()) for _ in selected_items]

    # Get today's date for date_out
    date_out = datetime.today().strftime("%Y-%m-%d")

    # Calculate due_date (14 days after date_out)
    due_date = (datetime.today() + timedelta(days=14)).strftime("%Y-%m-%d")

    # Update the BOOK_LOANS table 
    for item, checkout_id in zip(selected_items, checkout_ids):
        book_title = tree.item(item, "values")[0]  # Assuming the book title is in the first column
        # Insert the checkout information into the BOOK_LOANS table 
        print(f"Book '{book_title}' checked out with Checkout ID: {checkout_id}, Card Number: {card_number}, Date Out: {date_out}, Due Date: {due_date}")

#Successful checkout
    tk.messagebox.showinfo("Checkout", "Books checked out successfully.")
   
   
#Prompt for card number method
def prompt_for_card_number():
    return tk.simpledialog.askstring("Checkout", "Enter Borrower's Card Number:")

#Get active loans method
def get_active_loans_count(card_number):
    #retrieve the count of active loans for the given borrower
    #simulate the data
    borrower_loans = {
        "123": [{"status": "active"}, {"status": "active"}, {"status": "returned"}],
        "456": [{"status": "active"}, {"status": "active"}],
    }

    return sum(1 for loan in borrower_loans.get(card_number, []) if loan.get("status") == "active")



# Create a main window
root = tk.Tk()
root.title("Library Database")

# Add a search field and button
search_frame = ttk.Frame(root)
search_frame.pack(pady=10)

search_label = ttk.Label(search_frame, text="Search:")
search_label.grid(row=0, column=0)

search_entry = ttk.Entry(search_frame)
search_entry.grid(row=0, column=1)

search_button = ttk.Button(search_frame, text="Search", command=search_books)
search_button.grid(row=0, column=2)

button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

add_to_cart_button = ttk.Button(button_frame, text = "Add to cart", command=add_to_cart)
add_to_cart_button.grid(row=0, column=0, padx=5)


# Library Data function, tested 5 random books.
library_data = [
    {"ISBN": "1", "Book Title": "Harry Potter", "Author": "J.K. Rowling", "Genre": "Fantasy", "Year": "1997", "Status": "Checked Out"},
    {"ISBN": "2", "Book Title": "To Kill a Potter", "Author": "Harper Lee", "Genre": "Fiction", "Year": "1960", "Status": "Available"},
    {"ISBN": "3", "Book Title": "1984", "Author": "George Orwell", "Genre": "Dystopian", "Year": "1949", "Status": "Available"},
    {"ISBN": "4", "Book Title": "Why AI is the future and gonna change the world", "Author": "Yash Hooda", "Genre": "Non-Fiction", "Year": "2023", "Status": "Available"},
    {"ISBN": "5", "Book Title": "The Lord of the Rings", "Author": "J. R. R. Tolkien", "Genre": "Non-Fiction", "Year": "1955", "Status": "Checked Out"},
   
]

cart = []

# Create a treeview to display the data
tree = ttk.Treeview(root)
tree["columns"] = ("Book Title", "Author", "Genre", "Year", "Status")

# Define columns
tree.column("#0", width=0, stretch=tk.NO)
tree.column("Book Title", anchor=tk.W, width=150)
tree.column("Author", anchor=tk.W, width=100)
tree.column("Genre", anchor=tk.W, width=100)
tree.column("Year", anchor=tk.W, width=70)
tree.column("Status", anchor=tk.W, width=80)

# Add headings
tree.heading("#0", text="", anchor=tk.W)
tree.heading("Book Title", text="Book Title", anchor=tk.W)
tree.heading("Author", text="Author", anchor=tk.W)
tree.heading("Genre", text="Genre", anchor=tk.W)
tree.heading("Year", text="Year", anchor=tk.W)
tree.heading("Status", text="Status", anchor=tk.W)

# Inserting sample data into the treeview
tree.insert("", "end", text="1", values=("Harry Potter", "J.K. Rowling", "Fantasy", "1997", "Checked Out"))
tree.insert("", "end", text="2", values=("To Kill a Potter", "Harper Lee", "Fiction", "1960", "Available"))
tree.insert("", "end", text="3", values=("1984", "George Orwell", "Dystopian", "1949", "Available"))
tree.insert("", "end", text="4", values=("Why AI is the future and gonna change the world", "Yash Hooda", "Non-Fiction", "2023", "Available"))
tree.insert("", "end", text="5", values=("The Lord of the Rings", "J. R. R. Tolkien", "Non-Fiction", "1955", "Checked Out"))

# Place the treeview
tree.pack(padx=10, pady=10)


# Add a button for checking out books
checkout_button = ttk.Button(root, text="Checkout Selected Books", command=checkout_books)
checkout_button.pack(pady=10)


# Check-in books function
def checkin_books():
    selected_items = tree.selection()

    # If no books have been selected for check-in, return an error.
    if not selected_items:
        messagebox.showinfo("Check-in", "Please select at least one book for check-in.")
        return

    # Prompt for search criteria
    search_criteria = tk.simpledialog.askstring("Check-in", "Enter ISBN, Card Number, or Borrower Name:")

    # Search for matching BOOK_LOANS tuples based on the search criteria
    matching_loans = search_book_loans(search_criteria)

    # If no matching loans found, show a message
    if not matching_loans:
        messagebox.showinfo("Check-in", "No matching loans found.")
        return

    # Display the matching loans and prompt for selection
    selected_loan = select_book_loan(matching_loans)

    # If a loan is selected, proceed with check-in
    if selected_loan:
        # Get today's date for date_in
        date_in = datetime.today().strftime("%Y-%m-%d")

        # Update the BOOK_LOANS table 
        book_title = selected_loan["Book Title"]
        card_number = selected_loan["Card Number"]
        checkout_id = selected_loan["Checkout ID"]
        update_book_loans(checkout_id, date_in)

        messagebox.showinfo("Check-in", f"Book '{book_title}' checked in successfully for Card Number: {card_number}")

# Define an empty function for update_book_loans
def update_book_loans(checkout_id, date_in):
    # Pass the function 
    pass


# Function to search for matching BOOK_LOANS tuples based on search criteria
def search_book_loans(search_criteria):
    # Stores bank loans data.
    book_loans_data = [
        {"Checkout ID": "1", "Card Number": "123", "Book Title": "Harry Potter", "ISBN": "1", "Date Out": "2023-01-01", "Due Date": "2023-01-15", "Date In": None},
        {"Checkout ID": "2", "Card Number": "456", "Book Title": "To Kill a Mockingbird", "ISBN": "2", "Date Out": "2023-02-01", "Due Date": "2023-02-15", "Date In": "2023-02-10"},
        # Add more data if needed
    ]

    # Search for matching loans based on ISBN, Card Number, or Borrower Name
    matching_loans = [loan for loan in book_loans_data
                      if search_criteria.lower() in loan["ISBN"].lower()
                      or search_criteria.lower() in loan["Card Number"].lower()
                      or search_criteria.lower() in loan["Book Title"].lower()]

    return matching_loans

# Function to display matching loans and prompt for selection
def select_book_loan(matching_loans):
    # Create a new window to display the matching loans
    select_window = tk.Toplevel(root)
    select_window.title("Select Book Loan")

    # Create a treeview to display the matching loans
    select_tree = ttk.Treeview(select_window)
    select_tree["columns"] = ("Book Title", "Card Number", "Checkout ID", "Date Out", "Due Date")

    # Define columns
    select_tree.column("#0", width=0, stretch=tk.NO)
    select_tree.column("Book Title", anchor=tk.W, width=150)
    select_tree.column("Card Number", anchor=tk.W, width=100)
    select_tree.column("Checkout ID", anchor=tk.W, width=100)
    select_tree.column("Date Out", anchor=tk.W, width=100)
    select_tree.column("Due Date", anchor=tk.W, width=100)

    # Add headings
    select_tree.heading("#0", text="", anchor=tk.W)
    select_tree.heading("Book Title", text="Book Title", anchor=tk.W)
    select_tree.heading("Card Number", text="Card Number", anchor=tk.W)
    select_tree.heading("Checkout ID", text="Checkout ID", anchor=tk.W)
    select_tree.heading("Date Out", text="Date Out", anchor=tk.W)
    select_tree.heading("Due Date", text="Due Date", anchor=tk.W)

    # Insert matching loans into the treeview
    for loan in matching_loans:
        select_tree.insert("", "end", values=(loan["Book Title"], loan["Card Number"], loan["Checkout ID"], loan["Date Out"], loan["Due Date"]))

    # Function to handle item selection and close the window
    def on_select():
        selected_item = select_tree.selection()

        if selected_item:
            selected_loan = matching_loans[selected_item[0]]
            select_window.destroy()
            # Call your check-in logic using selected_loan
            checkin_selected_books(selected_loan)

    # Add a button to trigger the selection
    select_button = ttk.Button(select_window, text="Select", command=on_select)
    select_button.pack(pady=10)

    # Run the window's main loop
    select_window.mainloop()
   
# Add a button for checking in books
checkin_button = ttk.Button(root, text="Checkin Selected Books", command=checkin_books)
checkin_button.pack(pady=10)

# Define an empty function for checkin_selected_books
def checkin_selected_books(selected_loan):
    # Pass function to checkin_selected_books
    pass

#checkout selected books function  
def checkout_selected_books():
    selected_items = tree.selection()

   #If items fail to be selected for checkout, return error.
    if not selected_items:
        messagebox.showinfo("Checkout", "Please select at least one book for checkout.")
        return

    #call the prompt for card number function to generate card number.
    card_number = prompt_for_card_number()
    #If card number failed to generate.
    if not card_number:
        return  # User canceled the input

    # Check the number of active loans for the borrower
    active_loans_count = get_active_loans_count(card_number)

   #If the user has at least 3 active loans, then deny the checkout request and return an error message.
    if active_loans_count >= 3:
        messagebox.showinfo("Checkout", f"The borrower has reached the maximum limit of 3 active loans.")
        return

    # Process the checkout
    process_checkout(selected_items, card_number)

#Process the checkout function.
def process_checkout(selected_items, card_number):
    # Check for fines
    if has_fines(card_number):
        messagebox.showinfo("Checkout", "Cannot proceed with checkout. Borrower has outstanding fines.")
        return

    # Generate unique keys for each checkout
    checkout_ids = [str(datetime.now().timestamp()) for _ in selected_items]

   #Assign a due date for the book.
    date_out = datetime.today().strftime("%Y-%m-%d")
    due_date = (datetime.today() + timedelta(days=14)).strftime("%Y-%m-%d")

    # Update the BOOK_LOANS table.
    for item, checkout_id in zip(selected_items, checkout_ids):
        book_title = tree.item(item, "values")[0]  # Assuming the book title is in the first column
        # Insert the checkout information into the BOOK_LOANS table
        #insert data into the BOOK_LOANS table
        insert_into_book_loans(checkout_id, card_number, book_title, date_out, due_date)

    messagebox.showinfo("Checkout", "Books checked out successfully.")

#Insert data into book loans function.
def insert_into_book_loans(checkout_id, card_number, book_title, date_out, due_date):
    print(f"Book '{book_title}' checked out with Checkout ID: {checkout_id}, Card Number: {card_number}, Date Out: {date_out}, Due Date: {due_date}")

# Check for fines
def has_fines(card_number):
    #Fines data.
    fines_data = {
        "123": {"amount": 10},
        "456": {"amount": 0},
    }

   #Retrieve fines data from card number.
    borrower_fines = fines_data.get(card_number, {"amount": 0})
   
    if borrower_fines["amount"] > 0:
        return True  # Borrower has fines
    else:
        return False  # No fines
    

# Create a button to trigger the creation of a new BORROWER
create_borrower_button = ttk.Button(button_frame, text="Create New Borrower", command=create_borrower)
create_borrower_button.grid(row=0, column=1, padx=5)

# Run the main loop
root.mainloop()
