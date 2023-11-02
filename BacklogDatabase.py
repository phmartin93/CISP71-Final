# Import the required libraries
import sqlite3
import tkinter.messagebox as mb

# Create class called Database
#   Database will handle all the SQL queries and database connections
#   It requires a filepath to be passed to it to get started 
class Database:
    # Constructor
    #   - databasePath - string variable atht is the database filepath
    def __init__(self, databasePath):
        # Connect to the database using the filepath
        self.conn = sqlite3.connect(databasePath)
        # Create a cursor object to interact with the database
        self.cursorDB = self.conn.cursor()

    # Function to create a table for a new database and populate it with dummy records
    def createDatabase(self):
        # SQL query to create a table
        createQuery = '''
            CREATE TABLE IF NOT EXISTS "Backlog" (
                "ID"	    INTEGER,
                "Title"	    TEXT NOT NULL,
                "Developer"	TEXT,
                "Genre"	    TEXT,
                "Type"	    TEXT,
                "Status"	TEXT,
                "Rating"	TEXT,
                PRIMARY KEY("ID" AUTOINCREMENT)
            );'''

        # Try-except block to catch any exceptions
        try:
            # Execute query
            self.cursorDB.execute(createQuery)

            # Add dummy records to populate database
            self.addRecord('Call of Duty: Modern Warfare 2', 'Infinity Ward', 'Shooter', 'Base', 'Playing', 'N/A')
            self.addRecord('Tekken 8', 'Bandai Namco', 'Fighting', 'Base', 'Unreleased', 'N/A')
            self.addRecord('Mosnter Hunter World: Iceborne', 'Capcom', 'RPG', 'Expansion', 'Backlog', 'N/A')
            self.addRecord('Hades', 'Supergiant Games', 'Roguelike', 'Base', 'Finished', '10')

            # Commit changes
            self.conn.commit()
        except:
            # Display error message and rollback database
            mb.showerror('Error', 'Error in operation.' 
                         + '\nRolling back database')
            self.conn.rollback()

    # Function to add a record to the database
    #   All variables are strings
    #   - vgTitle - title of video game
    #   - developer - developer of video game
    #   - genre - genre of video game
    #   - type - base game or expansion DLC
    #   - status - current backlog status
    #   - rating - video game rating
    def addRecord(self, vgTitle, developer, genre, type, status, rating):
        # SQL query to insert a new record into the database
        insertQuery = '''
            INSERT INTO Backlog(Title,Developer,Genre,Type,Status,Rating) 
                values(?,?,?,?,?,?);'''
        
        # Try-except block to catch any exceptions
        try:
            # Execute query and commit changes
            self.cursorDB.execute(insertQuery,
                    (vgTitle, developer, genre, type, status, rating,))
            self.conn.commit()
        except:
            # Display error message and rollback database
            mb.showerror('Error', 'Error in operation.' 
                         + '\nRolling back database')
            self.conn.rollback()

    # Function to update a database record
    #   All variables are strings except recordID. recordID is an integer
    #   - vgTitle - title of video game
    #   - developer - developer of video game
    #   - genre - genre of video game
    #   - type - base game or expansion DLC
    #   - status - current backlog status
    #   - rating - video game rating
    #   - recordID - primary key of the record
    def updateRecord(self, vgTitle, developer, genre, type, status, rating, recordID):
        # SQL query to update a database record
        updateQuery = '''
            UPDATE Backlog
            SET Title = ?,
            Developer = ?,
            Genre = ?,
            Type = ?,
            Status = ?,
            Rating = ?
            WHERE ID = ?;'''
        
        # Try-except block to catch any exceptions
        try:
            # Execute query and commit changes
            self.cursorDB.execute(updateQuery, (vgTitle, developer, genre, type, status, rating, recordID,))
            self.conn.commit()
        except:
            # Display error message and rollback database
            mb.showerror('Error', 'Error in operation.' 
                         + '\nRolling back database')
            self.conn.rollback()

    # Function to delete a record from the database
    #   recordID - integer variable that is primary key of the record
    def deleteRecord(self, recordID):
        # SQL query to delete a record from the database
        deleteQuery = 'DELETE FROM Backlog WHERE ID=?;'

        # Try-except block to catch any exceptions
        try:
            # Execute query and commit changes
            self.cursorDB.execute(deleteQuery, (recordID,))
            self.conn.commit()
        except:
            # Display error message and rollback database
            mb.showerror('Error', 'Error in operation.' 
                         + '\nRolling back database')
            self.conn.rollback()

    # Function to retrieve all records in the database
    def fetchDB(self):
        # Execute a SQL query to retrieve all records in the database
        self.cursorDB.execute('SELECT *, oid from Backlog')
        # Variable to store query results
        rows = self.cursorDB.fetchall()

        # Return the query results
        return rows

    # Function to retrieve specific records in the database
    #   searchRecord - string variable that is the search term
    def searchRecords(self, searchRecord):
        # SQL query to retrieve specific records in the database
        searchQuery = f'''
            SELECT *, oid FROM Backlog WHERE Title LIKE "%{searchRecord}%"
            OR Developer LIKE "%{searchRecord}%"
            OR Genre LIKE "%{searchRecord}%"
            OR Type LIKE "%{searchRecord}%"
            OR Status LIKE "%{searchRecord}%"
            OR Rating LIKE "%{searchRecord}%";'''

        # Execute query
        self.cursorDB.execute(searchQuery)
        # Variable to store query results
        rows = self.cursorDB.fetchall()

        # Return the query results
        return rows
    
    # Fucntion to sort results of a select query
    #   All variables are strings
    #   searchRecord - search term
    #   sortColumn - column to sort by
    #   sortType - ascending or descending
    def sortSearch(self, searchRecord, sortColumn, sortType):
        # SQL query to sort records in the database
        sortSearchQuery = f'''
            SELECT *, oid FROM Backlog WHERE Title LIKE "%{searchRecord}%"
            OR Developer LIKE "%{searchRecord}%"
            OR Genre LIKE "%{searchRecord}%"
            OR Type LIKE "%{searchRecord}%"
            OR Status LIKE "%{searchRecord}%"
            OR Rating LIKE "%{searchRecord}%"
            ORDER BY {sortColumn} {sortType};'''

        # Execute query
        self.cursorDB.execute(sortSearchQuery)
        # Variable to store query results
        rows = self.cursorDB.fetchall()

        # Return the query results
        return rows
    
    # Function to manually close the database connection
    def closeConnection(self):
        self.conn.close()

    # Destructor method to close the database connection when app is closed
    def __del__(self):
        self.conn.close()