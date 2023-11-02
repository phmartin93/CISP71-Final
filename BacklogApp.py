# ===================================IMPORTING===================================

# Import the required libaries
#   tkinter for the widgets
#   ttkthemes for a nicer layout
#   os to retreive file paths and directory content
#   re for regular expression functions
from tkinter import *
from tkinter import messagebox as mb
from tkinter.ttk import *
# from ttkthemes import ThemedTk
import os, re
# Import the Database class from the BacklogDatabase python file
from BacklogDatabase import Database

# ===================================APP FUNCTIONS===================================

# Function to connect to the database
#   - connectVar - string variable to determine what button was pressed 
def connect_database(connectVar):
    # Global variable that will become the database object
    global appDB
    # Variable to hold the database name
    databaseName = ''

    # If-else statement to determine which button was pressed
    #   Will get the entered or selected name and strip it of white space
    if connectVar == 'Create':
        databaseName = createEntry.get().strip()
    elif connectVar == 'Edit':
        databaseName = editVar.get()
    
    # If-statement to see if the file extension was entered
    #   Will add .db to the database name if extension was not entered
    if databaseName[len(databaseName)-3:] != '.db':
        databaseName += '.db'

    # Variable to store database name in lowercase for validation
    tempName = databaseName.lower()

    # If-statement to call validation method startValidate(), passing button variable and database name
    #   Creates a filepath directly to the database
    #   Creates database object using global variable appDB, passing the filepath
    if startValidate(connectVar, tempName):
        databasePath = folderPath+databaseName
        appDB = Database(databasePath)

        #If-statement to create a new database if the create button was pressed
        if connectVar == 'Create':
            appDB.createDatabase()

        # Show the main page and update database list
        #   Display message confirming database has been connected to
        showMain()
        updateDatabases()
        mb.showinfo('Database Connected', 'Successfully connected to the database.'
                    + '\nExample records are created for new databases.')

# Function to update database list using the file directory
#   Stores directory contents in the start page ComboBox object editMenu
def updateDatabases():
    newList = os.listdir(folderPath)
    editMenu['values'] = newList

# Function to add a record to the database
def add_record():
    # If-statement to validate adding a record
    #   Calls two validation mehtods, mainValidate() and addValidate()
    if mainValidate() and addValidate():
        # If-statement to confirm that the user wants to add the record
        if mb.askyesno('Add Game', 'You are about to add a new game to the database. '
                       + 'Continue?'):
            # Calls the addRecord() function in the database class
            #   Enters values taken from the widgets
            appDB.addRecord(vgTitleEntry.get().strip(), devEntry.get().strip(), genreVar.get(),
                            typeRadioVar.get(), statusVar.get(), ratingVar.get())
            
            # Calls function to clear widgets
            clearFields()
            # Calls function to display the updated database
            display_DB()
            # Tell the user the record was added successfully
            mb.showinfo('Add Game', 'The game was successfully added to the database.')
        else:
            # Tell user the record was not added
            mb.showinfo('Add Game', 'The game was not added to the database.')

# Function to update a database record
def update_record():
    # If-statement to validate updating a record
    #   Calls two validation mehtods, mainValidate() and updateValidate()
    if mainValidate() and updateValidate():
        # If-statement to confirm that the user wants to update the record
        if mb.askyesno('Update Game', 'You are about to update a game record. '
                    + 'Continue?'):
            # Calls the updateRecord() function in the database class
            #   Enters values taken from the widgets and the recordID variable
            appDB.updateRecord(vgTitleEntry.get().strip(), devEntry.get().strip(), genreVar.get(),
                                typeRadioVar.get(), statusVar.get(), ratingVar.get(), 
                                recordID)
            
            # Calls function to clear widgets
            clearFields()
            # Calls function to display the updated database
            display_DB()
            # Tell the user the record was updated successfully
            mb.showinfo('Update Game', 'The game record was succesfully updated.')
        else:
            # Tell user the record was not updated
            mb.showinfo('Update Game', 'The game record was not updated.')

# Function to delete a record
def delete_record():
    # If-statement to validate deleting a record
    #   Calls validation mehtod deleteValidate()
    if deleteValidate():
        # If-statement to confirm that the user wants to delete the record
        if mb.askokcancel('Delete Game', 'You are about to delete a game from the database.'
                            + "\nThis can't be undone. Continue?", icon='warning'):
            # Calls the deleteRecord() function in the database class, passing the recordID
            appDB.deleteRecord(recordID)

            # Calls function to clear widgets
            clearFields()
            # Calls function to display the updated database
            display_DB()
            # Tell the user the record was deleted successfully
            mb.showinfo('Delete Game', 'The game was succesfully deleted from the database.')
        else:
            # Tell user the record was not deleted
            mb.showinfo('Delete Game', 'The game was not deleted from the database.')

# Function to display the database inside the Treeview object tvBacklog
def display_DB():
    # For-loop to delete items inside the Treeview
    for row in tvBacklog.get_children():
        tvBacklog.delete(row)

    # Configure the tags that will determine the background of the Treeview row
    tvBacklog.tag_configure('oddrow', background='white')
    tvBacklog.tag_configure('evenrow', background='#e4e4e4')

    # Initialize count variable for for-loop
    count = 0

    # For-loop to fetch all records from the database
    for row in appDB.fetchDB():
        # If-statement to determine if the row is even or odd
        #   Inserts records values into the Treeview rows
        if count % 2 == 0:
            tvBacklog.insert('', 'end', iid=count, text=id, 
                             values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6] ,id), tags=('evenrow',))
        else:
            tvBacklog.insert('', 'end', iid=count, text=id, 
                             values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6] ,id), tags=('oddrow',))
        
        # Increment count variable
        count += 1

# Function to show the selected Treeview record inside the widgets
#   Takes *args variable to handle the TreeviewSelect event
def showRecord(*args):
    # Calls function to clear widgets
    clearFields()

    # Global variable to store the primary key ID
    global recordID 

    # For-loop to get the Treeview row values and insert them into the widgets
    for selection in tvBacklog.selection():
        item = tvBacklog.item(selection)
        rowID, vgTitle, developer, genre, type, status, rating = item['values'][0:7]
        
        recordID = rowID
        vgTitleEntry.insert(0, vgTitle)
        devEntry.insert(0, developer)
        genreVar.set(genre)
        typeRadioVar.set(type)
        statusVar.set(status)
        ratingVar.set(rating)

# Function to search database records
#   Takes the *args variable to handle the event created when the Enter key is pressed
def search_records(*args):
    # If-statement to validate the search
    #   Calls validation mehtod searchValidate()
    if searchValidate():
        # For-loop to delete items inside the Treeview
        for row in tvBacklog.get_children():
            tvBacklog.delete(row)

        # Initialize count variable for for-loop
        count = 0

        # For-loop to search records from the database
        #   Calls searchRecords function from the Database class, passing the search term
        for row in appDB.searchRecords(searchEntry.get()):
            # If-statement to determine if the row is even or odd
            #   Inserts records values into the Treeview rows
            if count % 2 == 0:
                tvBacklog.insert('', 'end', iid=count, text=id, 
                                values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6] ,id), tags=('evenrow',))
            else:
                tvBacklog.insert('', 'end', iid=count, text=id, 
                                values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6] ,id), tags=('oddrow',))
                
            # Increment count variable
            count += 1

# Function to sort all records or search results
def sort_records():
    # If-statement to validate the sort
    #   Calls validation mehtod sortValidate()
    if sortValidate():
        # For-loop to delete items inside the Treeview
        for row in tvBacklog.get_children():
            tvBacklog.delete(row)

        # Initialize count variable for for-loop
        count = 0

        # For-loop to sort records from the database
        #   Calls sortSearch function from the Database class
        #   Passes search term, sort column, and ascending or descending
        for row in appDB.sortSearch(searchEntry.get(), sortVar.get(), azVar.get()):
            # If-statement to determine if the row is even or odd
            #   Inserts records values into the Treeview rows
            if count % 2 == 0:
                tvBacklog.insert('', 'end', iid=count, text=id, 
                                values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6] ,id), tags=('evenrow',))
            else:
                tvBacklog.insert('', 'end', iid=count, text=id, 
                                values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6] ,id), tags=('oddrow',))
                    
            # Increment count variable
            count += 1

# ===================================VALIDATION FUNCTIONS===================================

# Function to validate the start page
#   All variables are strings
#   - validateVar - determines what button was pressed
#   - databaseName - name of database
def startValidate(validateVar, databaseName):
    # Boolean variable
    startBool = True

    # Regular expression pattern to compare database names
    alphaNumPattern = re.compile('[^a-zA-Z0-9_-]')
    # Regular expression pattern to verify if special characters exist in database name
    specialPattern = re.compile('[@!#$%^&*()<>?/\|}{~:]')
    # Strip and lower createEntry value and store in variable validateString
    validateString = createEntry.get().lower().strip()

    databaseName = re.sub(alphaNumPattern, '', databaseName.lower())


    # If-statement to determine which button was pressed
    if validateVar == 'Create':
        # If-statement to determine if validateString is empty
        #   Display error message and deny validation if empty
        #   Deletes createEntry contents and sets focus on createEntry if empty
        if validateString == '':
            mb.showerror('Database Name Required', 'No database name was entered.'+
                         '\nPlease enter the name of the database.')
            startBool = False
            createEntry.delete(0, END)
            createEntry.focus_set()
        # Elif-statement to determine if validateString is contains special characters
        #   Display error message and deny validation if true
        #   Deletes createEntry contents and sets focus on createEntry if true
        elif specialPattern.search(validateString) != None:
            mb.showerror('Inavalid Database Name', 'Database names cannot contain special characters.'+
                         '\nPlease use only alphanumeric characters, underscores, and hyphens.')
            startBool = False
            createEntry.delete(0, END)
            createEntry.focus_set()
        else:
            # For-loop to iterate through directory contents
            for name in os.listdir(folderPath):
                # If-statement to determine if the database name is already in the directory
                #   Display error message and deny validation if it exists
                #   Deletes createEntry contents and sets focus on createEntry if it exists
                if databaseName == re.sub(alphaNumPattern, '', name.lower()):
                    mb.showerror('Duplicate Database', 'This database already exists.'+
                                '\nPlease enter another name for the database.')
                    startBool = False
                    createEntry.selection_range(0, END)
                    createEntry.focus_set()
                    # Break loop
                    break
    elif validateVar == 'Edit':
        # If-statement to determine if nothing is selected from the drop down menu
        #   Display error message and deny validation if empty
        #   Sets focus on editMenu if empty
        if editVar.get() == '':
            mb.showerror('Database Selection Required', 'No database was selected.'+
                         '\nPlease select a database from the dropdown menu.')
            startBool = False
            editMenu.focus_set()

    # Return Boolean variable to confirm or deny validation
    return startBool

# Fucntion to validate main page
def mainValidate():
    # Boolean variable
    mainBool = True

    # Strip vgTitleEntry value and store in variable title
    title = vgTitleEntry.get().strip()

    # If-statement to determine if title is empty
    #   Display error message and deny validation if empty
    #   Deletes vgTitleEntry contents and sets focus on vgTitleEntry if empty
    if title == '':
        mb.showerror('Title Required', 'No game title was entered. '
                     + 'Please enter the title of the game.')
        vgTitleEntry.delete(0, END)
        vgTitleEntry.focus_set()
        mainBool = False
    # Elif-statement to determine if no radio button was selected
    #   Display error message and deny validation if empty
    elif typeRadioVar.get() == '0':
        mb.showerror('Type Required', 'No type was selected. '
                     + 'Please select the type of the game.')
        mainBool = False
    # Elif-statement to determine if nothing from status drop down menu was selected
    #   Display error message and deny validation if empty
    #   Sets focus on statusDropDown if empty
    elif statusVar.get() == '':
        mb.showerror('Status Required', 'No status was selected. '
                     + 'Please choose the status of the game.')
        statusDropDown.focus_set()
        mainBool = False
    # Elif-statement to determine if a finished game was not rated
    #   Display error message and deny validation if not rated
    #   Sets focus on ratingDropDown if not rated
    elif (statusVar.get() == 'Finished' and ratingVar.get() == 'N/A'):
        mb.showerror('No Rating Entered', 'A finished game must have a rating.'
                     + '\nPlease select a rating that is not N/A.')
        ratingDropDown.focus_set()
        mainBool = False
    # Elif-statement to determine if an unfinished game was rated
    #   Display error message and deny validation if rated
    #   Sets focus on ratingDropDown if rated
    elif statusVar.get() != 'Finished' and ratingVar.get() != 'N/A':
        mb.showerror('Rating Not Allowed', "An unfinished game can't have a rating."
                     + '\nPlease select N/A as the rating for all unfinished games.')
        ratingDropDown.focus_set()
        mainBool = False

    # Return Boolean variable to confirm or deny validation
    return mainBool

# Function to validate adding a record
def addValidate():
    # Boolean variable
    addBool = True

    # Variable to store all database racords
    rows = appDB.fetchDB()
    # Regular expression to remove all special characters from vgTitleEntry value
    vgTitle = re.sub(r'[^a-zA-Z0-9]', '', vgTitleEntry.get())

    # For-loop to iterate through all database records
    for row in rows:
        # If-statement to compare record title and user entry without special characters and spaces
        #   Display error message and deny validation if title and entry are the same
        #   Higlights and sets focus on vgTitleEntry
        if re.sub(r'[^a-zA-Z0-9]', '', row[1].lower()) == vgTitle.lower():
            mb.showerror('Duplicate Title', 'This game is already in the database. '
                     + '\nPlease enter another game title.'
                     + '\n\nFor games with the same name, please enter the release year.'
                     +'\n\nEx: Call of Duty: Modern Warfare 2 (2009)')
            addBool = False
            vgTitleEntry.focus_set()
            vgTitleEntry.selection_range(0, END)
            # Break loop
            break
    
    # Return Boolean variable to confirm or deny validation
    return addBool

# Function to validate updating a record
def updateValidate():
    # Boolean variable
    updateBool = True

    # Variable to store all database racords
    rows = appDB.fetchDB()
    # Variable to strip and store vgTitleEntry value
    title = vgTitleEntry.get().strip()

    # For-loop to iterate through all database records
    for row in rows:
        # If-statement to compare title and record ID pair
        #   Display error message if titles are the same but the record IDs are different
        #   Deny validation
        #   Higlights and sets focus on vgTitleEntry
        if row[1].lower() == title.lower() and row[0] != recordID:
            mb.showerror('Duplicate Title', 'This game is already in the database. '
                     + '\nPlease enter another game title.')
            updateBool = False
            vgTitleEntry.focus_set()
            vgTitleEntry.selection_range(0, END)
            # Break loop
            break

    # Return Boolean variable to confirm or deny validation
    return updateBool

# Function to validate deleting a record
def deleteValidate():
    # Boolean variable
    deleteBool = True

    # If-statement to check record ID
    #   Display error message and deny validation if record ID = -1
    if recordID == -1:
        mb.showerror('No Record Selected', 'No record was selected.'
                     + '\nPlease select a record from the window above to delete.')
        deleteBool = False

    # Return Boolean variable to confirm or deny validation
    return deleteBool

# Function to validate a search
def searchValidate():
    # Boolean variable
    searchBool = True

    # If-statement to check if searchEntry is empty
    #   Display error message and deny validation if empty
    #   Sets focus on searchEntry
    if searchEntry.get().strip() == '':
        mb.showerror('Search Term Required', 'Search bar was left blank.'
                     + '\nPlease enter a search term in the search bar.')
        searchEntry.focus_set()
        searchBool = False

    # Return Boolean variable to confirm or deny validation
    return searchBool

# Fucntion to validate a sort
def sortValidate():
    # Boolean variable
    sortBool = True

    # If-statement to check if a sort column was selected
    #   Display error message and deny validation if empty
    #   Sets focus on sortDropDown
    if sortVar.get() == 'Sort by...':
        mb.showerror('Sort Category Required', 'A category was not selected.'
                     + '\nPlease pick a category to sort the records by.')
        sortDropDown.focus_set()
        sortBool = False

    # Return Boolean variable to confirm or deny validation
    return sortBool

# Function to confirm returning to the start page or exiting the app
#   - key - string variable that determines what button was pressed
def exitConfirm(key):
    # If-else statement to determine which button was pressed
    #   Ask for confirmation
    if key == 'Back':
        if mb.askyesno('Back to Start', 'You are about to go back to the start page.'
                    + '\nAny unsaved work will be deleted. Continue?'):
            # Close the connection to the current database
            appDB.closeConnection()
            # Return to start page by calling function showStart()
            showStart()
    elif key == 'Exit':
        if mb.askyesno('Exit App', 'You are about to exit the application.'
                    + '\nAny unsaved work will be deleted. Continue?', icon='warning'):
            # Close app
            root.quit()

# ===================================CLEAR & RESET FUNCTIONS===================================

# Function to clear record fields from both pages
#   Does not clear the search box
def clearFields():
    # Clear and reset all text entrie, radio buttons, and drop down menus
    #   Start Page clear
    createEntry.delete(0, END)
    editVar.set('')

    #   Main Page clear
    vgTitleEntry.delete(0, END)
    devEntry.delete(0, END)
    typeRadioVar.set('0')
    genreVar.set('')
    statusVar.set('')
    ratingVar.set('N/A')

    # Reset the recordID to -1
    global recordID 
    recordID = -1

    # Set focus on title entry field
    vgTitleEntry.focus_set()

# Function to reset the Treeview and clear the search entry
#   Does not clear the record fields
def resetTree():
    # Call function to reset Treeview to display all records
    display_DB()

    # Clear and reset all text entrie, radio buttons, and drop down menus
    searchEntry.delete(0, END)
    sortVar.set('Sort by...')
    azVar.set('ASC')

    # Set focus on search bar
    searchEntry.focus_set()

# Function to display the start page
def showStart():
    # Displays start page
    startPage.lift()
    # Calls function to clear and reset all fields
    clearFields()
    # Set focus on create entry field
    createEntry.focus_set()

# Function to display the main page
def showMain():
    # Displays main page
    mainPage.lift()
    # Calls function to clear and reset all fields
    clearFields()
    # Calls function to display database records
    display_DB()
    # Set focus on title entry field
    vgTitleEntry.focus_set()

# ===================================START OF APP CREATION===================================

# ===================================VARIABLES===================================

# Variable to store the filepath to where the program is being executed from
masterPath = os.path.dirname(os.path.realpath(__file__))
# Variable to store the filepath to the databases
folderPath = masterPath+'\Databases\\'

# List to store all database names
databaseList = os.listdir(folderPath)

# List to store genre drop down menu values
genreList = ['', 'Action', 'Adventure', 'Fighting', 
             'Horror', 'Platformer', 'Puzzle', 'Rhythm', 
             'Roguelike', 'RPG', 'Shooter', 'Simulation', 
             'Sports', 'Strategy', 'Survival']
# List to store status drop down menu values
statusList = ['', 'Unreleased', 'Backlog', 'Playing', 'Finished']
# List to store rating drop down menu values
ratingList = ['', 'N/A', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
# List to store sort drop down menu values
sortList = ['', 'Title', 'Developer', 'Genre', 'Type', 'Status', 'Rating']

# Variable to store the primary key
#   Initialized to have -1, meaning no record has been selected yet
recordID = -1

# ===================================MAIN APP WINDOW===================================

# Create Tk object, which will be the base window for the app
#   Use ThemedTk if ttkthemes library can be installed
#   Use Tk if ttkthemes library cannot be installed
# root = ThemedTk()
root = Tk()
# Define the size of the app window
root.geometry('700x650')

# ===================================ICON & TITLE===================================

# Variable to store icon image
icon = PhotoImage(file = masterPath+'\Icons\\mario.png')
# Insert the icon
root.iconphoto(False, icon)
# Insert the app's title
root.title('Video Game Backlog')

# ===================================STYLES===================================

# Create style object to configure styles
style = Style()
# Set the theme for the app
#   Use arc style if root is a ThemeTk object
#   Use clam style if root is a Tk object
# style.theme_use('arc')
style.theme_use('clam')

# Treeview heading style
style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
# Treeview row style
style.configure('Treeview', font=(None, 10), rowheight=30)
# Record entry label style
style.configure('Bold.TLabel', font=('Sans-serif', 9, 'bold'))

# ===================================FRAMES===================================

# Frame to hold the start page contents
startPage = Frame(root)
# Frame to hold the main page contents
mainPage = Frame(root)

# Frame to hold start page widgets
startContainer = Frame(startPage)
# Frame to hold main page widgets
mainContainer = Frame(mainPage)

# Label frame to hold database creation widgets
createContainer = LabelFrame(startContainer, text='Create New Database')
# Label frame to hold database edit widgets
editContainer = LabelFrame(startContainer, text='Edit Existing Database')
# Separator to separate the create and edit frames
separator = Separator(startContainer, orient='horizontal')

# Frame to hold main page title
titleContainer = Frame(mainContainer)
# Frames to hold main page widgets
entryContainer = LabelFrame(mainContainer, text='Records')
firstRowContainer = Frame(entryContainer)
secondRowContainer = Frame(entryContainer)

# Frame to hold main page record command button
buttonContainer = LabelFrame(mainContainer, text='Commands')
# Frame to hold main page Treeview
tvContainer = Frame(mainContainer)
# Frames to hold main page search and sort widgets
sortSearchContainer = LabelFrame(mainContainer, text='Search & Sort')
searchContainer = Frame(sortSearchContainer)
sortContainer = Frame(sortSearchContainer)
# Frame to hold main page back and exit buttons
backContainer = Frame(mainContainer)

# ===================================START PAGE===================================

# Create widgets that will create a database based on user entry
createEntry = Entry(createContainer)
createButton = Button(createContainer, text='Create', command=lambda x='Create':connect_database(x))
# Bind enter/return key so user can press the enter/return key instead of pressing the button
createEntry.bind('<Return>', lambda event: connect_database('Create'))

# Edit widgets that will select a database based on user selection
editVar = StringVar(editContainer)
# Combobox instead of OptionMenu to dynamically update the database names when a new one is created
editMenu = Combobox(editContainer, width=20, textvariable=editVar, values=databaseList, state='readonly')
editButton = Button(editContainer, text='Edit', command=lambda x='Edit':connect_database(x))

# Place widgets
createEntry.grid(row=0, column=0, padx=10, pady=5)
createButton.grid(row=0, column=1, padx=10, pady=5)

editMenu.grid(row=0, column=0, padx=10, pady=5)
editButton.grid(row=0, column=1, padx=10, pady=5)

# ===================================MAIN PAGE===================================

# ===================================LABELS===================================

# Title label for the main page
titleLB = Label(titleContainer, text='Video Game Backlog', font=('OCR A Extended', 24, 'bold'))

# Labels for the record entry widgets
vgTitleLB = Label(firstRowContainer, text='Title:*', style='Bold.TLabel')
devLB = Label(firstRowContainer, text='Developer:', style='Bold.TLabel')
genreLB = Label(firstRowContainer, text='Genre:', style='Bold.TLabel')
typeLB = Label(secondRowContainer, text='Type:*', style='Bold.TLabel')
statusLB = Label(secondRowContainer, text='Status:*', style='Bold.TLabel')
ratingLB = Label(secondRowContainer, text='Rating:', style='Bold.TLabel')

# ===================================ENTRIES===================================

# Entry fields for record entry
vgTitleEntry = Entry(firstRowContainer)
devEntry = Entry(firstRowContainer)
ratingEntry = Entry(secondRowContainer)

# Entry field for search bar
searchEntry = Entry(searchContainer)
# Bind enter/return key so user can press the enter/return key instead of pressing the button
searchEntry.bind('<Return>', search_records)

# ===================================BUTTONS===================================

# Command buttons for record entry
addButton = Button(buttonContainer, text='Add', command=add_record)
updateButton = Button(buttonContainer, text='Update', command=update_record)
deleteButton = Button(buttonContainer, text='Delete', command=delete_record)
clearButton = Button(buttonContainer, text='Clear', command=clearFields)

# Command buttons for search and sort
searchButton = Button(searchContainer, text='Search', command=search_records)
resetButton = Button(searchContainer, text='Reset', command=resetTree)
sortButton = Button(sortContainer, text='Sort', command=sort_records)

# Button to reutrn to the start page
backButton = Button(backContainer, text='Back', command= lambda x='Back':exitConfirm(x))
# Button to close the app
exitButton = Button(backContainer, text='Exit', command= lambda x='Exit':exitConfirm(x))

# ===================================DROP DOWN MENUS===================================

# Genre selection drop down menu
genreVar = StringVar(firstRowContainer)
genreDropDown = OptionMenu(firstRowContainer, genreVar, *genreList)

# Status selection drop down menu
statusVar = StringVar(secondRowContainer)
statusDropDown = OptionMenu(secondRowContainer, statusVar, *statusList)

# Rating selection drop down menu
ratingVar = StringVar(secondRowContainer, 'N/A')
ratingDropDown = OptionMenu(secondRowContainer, ratingVar, *ratingList)

# Sort column selection drop down menu
sortVar = StringVar(sortContainer, 'Sort by...')
sortDropDown = OptionMenu(sortContainer, sortVar, *sortList)

# ===================================RADIO BUTTONS===================================

# Type selection radio butttons
typeRadioVar = StringVar(secondRowContainer, ' ')
baseRadio = Radiobutton(secondRowContainer, text='Base', variable=typeRadioVar, value='Base')
expansionRadio = Radiobutton(secondRowContainer, text='Expansion', variable=typeRadioVar, value='Expansion')

# Sort type selection radio butttons
azVar = StringVar(sortContainer, 'ASC')
AZRadio = Radiobutton(sortContainer, text='A to Z', variable=azVar, value='ASC')
ZARadio = Radiobutton(sortContainer, text='Z to A', variable=azVar, value='DESC')

# ===================================TREEVIEW===================================

# Treeview columns tuple
columns = ('#1', '#2', '#3', '#4', '#5', '#6', '#7')

# Create and pack scrollbar for the Treeview
tvScroll = Scrollbar(tvContainer)
tvScroll.pack(side=RIGHT, fill=Y)

# Create Treeview
tvBacklog = Treeview(tvContainer, show='headings', height='5', selectmode='browse', 
                     columns=columns, yscrollcommand=tvScroll.set, style="mystyle.Treeview")

# Configure scrollbar for Treeview
tvScroll.config(command=tvBacklog.yview)

# Create Treeview headings and columns
tvBacklog.heading('#1', text='ID', anchor='center')
tvBacklog.column('#1', width=0, anchor='center', stretch=True)

tvBacklog.heading('#2', text='Title', anchor='center')
tvBacklog.column('#2', width=200, anchor=W, stretch=True)

tvBacklog.heading('#3', text='Developer', anchor='center')
tvBacklog.column('#3',width=130, anchor='center', stretch=True)

tvBacklog.heading('#4', text='Genre', anchor='center')
tvBacklog.column('#4',width=80, anchor='center', stretch=True)

tvBacklog.heading('#5', text='Type', anchor='center')
tvBacklog.column('#5',width=70, anchor='center', stretch=True)

tvBacklog.heading('#6', text='Status', anchor='center')
tvBacklog.column('#6',width=80, anchor='center', stretch=True)

tvBacklog.heading('#7', text='Rating', anchor='center')
tvBacklog.column('#7', width=50, anchor='center', stretch=True)

# Display only selected columns
#   Hidden column contains the ID primary key
tvBacklog['displaycolumns']=('#2', '#3', '#4', '#5', '#6', '#7')

# Pack the Treeview
tvBacklog.pack(expand=True, fill='y')

# Bind TreeviewSelect event to show the selected record in the record entry widgets
tvBacklog.bind('<<TreeviewSelect>>', showRecord)

# ===================================CREATING LAYOUT FOR BOTH PAGES===================================

# Place start and main pages
startPage.place(in_=root, x=0, y=0, relwidth=1, relheight=1)
mainPage.place(in_=root, x=0, y=0, relwidth=1, relheight=1)

# Place start and main pages' base containers
#   Containers will attempt to stay centered on the page
startContainer.place(relx=.5, rely=.5, relwidth = 0.5,anchor= CENTER)
mainContainer.place(relx=.5, rely=.5,anchor= CENTER)

# Pack start page widget containers and separator in order
createContainer.pack()
separator.pack(fill='x', expand=True, pady=20)
editContainer.pack()

# Pack main page widget containers in order
titleContainer.pack()
tvContainer.pack()

entryContainer.pack(expand=True, pady=(20, 10))
firstRowContainer.pack(fill='x', expand=True, padx=30, pady=5)
secondRowContainer.pack(fill='x', expand=True, padx=30, pady=(5,10))

buttonContainer.pack(pady=(0,10))

sortSearchContainer.pack(pady=(0,20))
searchContainer.pack(fill='x', expand=True, padx=30, pady=5)
sortContainer.pack(fill='x', expand=True, padx=30, pady=(5,10))

backContainer.pack()

# ===================================PACKING WIDGETS===================================

# Specify the grid positioning for each main page widget
#   Rows help indicate separation of widget location
titleLB.grid(row=0, column=0, pady=(0,15))

vgTitleLB.grid(row=1, column=0, padx=(5,0), sticky=E)
vgTitleEntry.grid(row=1, column=1, padx=(5,5), sticky=W)

devLB.grid(row=1, column=2, padx=(20,0), sticky=E)
devEntry.grid(row=1, column=3, padx=(5,5), sticky=W)

genreLB.grid(row=1, column=4, padx=(20,0), sticky=E)
genreDropDown.grid(row=1, column=5, padx=(5,5), sticky=W)
genreDropDown.config(width=10)

typeLB.grid(row=2, column=0, padx=(5,0), sticky=E)
baseRadio.grid(row=2, column=1, padx=(5,6), sticky=W)
expansionRadio.grid(row=2, column=2, padx=(0,5), sticky=W)

statusLB.grid(row=2, column=3, padx=(20,0), sticky=E)
statusDropDown.grid(row=2, column=4, padx=(5,0), sticky=W)
statusDropDown.config(width=10)

ratingLB.grid(row=2, column=5, padx=(55,0), sticky=E)
ratingDropDown.grid(row=2, column=6, padx=(5,0), sticky=W)

addButton.grid(row=3, column=0, padx=(10,5), pady=(3,8))
updateButton.grid(row=3, column=1, padx=(5,5), pady=(3,8))
deleteButton.grid(row=3, column=2, padx=(5,5), pady=(3,8))
clearButton.grid(row=3, column=3, padx=(5,10), pady=(3,8))

searchEntry.grid(row=4, column=0, padx=(0,5))
searchButton.grid(row=4, column=1, padx=(9,5))
resetButton.grid(row=4, column=2, padx=(9,0))

sortDropDown.grid(row=5, column=0, padx=(0,5))
sortDropDown.config(width=10)
AZRadio.grid(row=5, column=1, padx=(5,0))
ZARadio.grid(row=5, column=2, padx=(0,5))
sortButton.grid(row=5, column=3, padx=(5,0))

backButton.grid(row=6, column=0)
exitButton.grid(row=6, column=1, padx=(5,0))

# ===================================APP START===================================

# Call function to show the start page
showStart()
# Start the app
root.mainloop()