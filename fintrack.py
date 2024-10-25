import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import atexit
from datetime import datetime, timedelta

conn = sqlite3.connect('transactions.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
    ID INTEGER PRIMARY KEY,
    Date TEXT NOT NULL,
    Housing INTEGER NOT NULL,
    Transportation INTEGER NOT NULL,
    Food INTEGER NOT NULL,
    Clothes INTEGER NOT NULL,
    Healthcare INTEGER NOT NULL,
    PersonalCare INTEGER NOT NULL,
    Education INTEGER NOT NULL,
    DebtPayments INTEGER NOT NULL,
    SavingsInvestments INTEGER NOT NULL,
    Entertainment INTEGER NOT NULL,
    GiftsDonations INTEGER NOT NULL,
    Misc INTEGER NOT NULL

)''')

# cursor.execute("DELETE FROM transactions")

conn.commit()

options = [
    "Housing",
    "Transportation",
    "Food",
    "Clothes",
    "Healthcare",
    "PersonalCare",
    "Education",
    "DebtPayments",
    "SavingsInvestments",
    "Entertainment",
    "GiftsDonations",
    "Misc"
]

# cursor.execute("INSERT INTO transactions (Date, Housing, Transportation, Food, Clothes, Healthcare, PersonalCare, Education, DebtPayments, SavingsInvestments, Entertainment, GiftsDonations, Misc) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", ("10/17/2024",15,0,0,0,0,0,0,0,0,0,0,0))

# cursor.execute("UPDATE employees SET Age = 30 WHERE Name = 'Charlie'")

conn.commit()

cursor.execute("SELECT * FROM transactions")

# Fetch all results
rows = cursor.fetchall()

# Print the results
for row in rows:
    print(row)

print()

cursor.execute('''CREATE TABLE IF NOT EXISTS expenditures (
    ID INTEGER PRIMARY KEY,
    Date TEXT NOT NULL,
    Housing INTEGER NOT NULL,
    Transportation INTEGER NOT NULL,
    Food INTEGER NOT NULL,
    Clothes INTEGER NOT NULL,
    Healthcare INTEGER NOT NULL,
    PersonalCare INTEGER NOT NULL,
    Education INTEGER NOT NULL,
    DebtPayments INTEGER NOT NULL,
    SavingsInvestments INTEGER NOT NULL,
    Entertainment INTEGER NOT NULL,
    GiftsDonations INTEGER NOT NULL,
    Misc INTEGER NOT NULL,
    Total INTEGER NOT NULL
)''')

# cursor.execute("DELETE FROM expenditures")

# Commit the changes
conn.commit()


# cursor.execute("INSERT INTO expenditures (Date, Housing, Transportation, Food, Clothes, Healthcare, PersonalCare, Education, DebtPayments, SavingsInvestments, Entertainment, GiftsDonations, Misc, Total) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", ("10/17/2024",15,0,0,0,0,0,0,0,0,0,0,0,0))


conn.commit()

cursor.execute("SELECT * FROM expenditures")

# Fetch all results
rows = cursor.fetchall()

# Print the results
for row in rows:
    print(row)

print()


cursor.execute('''CREATE TABLE IF NOT EXISTS weeklyexpenditures (
    ID INTEGER PRIMARY KEY,
    Date TEXT NOT NULL,
    Housing INTEGER NOT NULL,
    Transportation INTEGER NOT NULL,
    Food INTEGER NOT NULL,
    Clothes INTEGER NOT NULL,
    Healthcare INTEGER NOT NULL,
    PersonalCare INTEGER NOT NULL,
    Education INTEGER NOT NULL,
    DebtPayments INTEGER NOT NULL,
    SavingsInvestments INTEGER NOT NULL,
    Entertainment INTEGER NOT NULL,
    GiftsDonations INTEGER NOT NULL,
    Misc INTEGER NOT NULL,    
    Total INTEGER NOT NULL
)''')

# cursor.execute("DELETE FROM weeklyexpenditures")

conn.commit()


new_row_id1 = 1 # forget how used this should revisit

conn.commit()

cursor.execute("SELECT * FROM weeklyexpenditures")

# Fetch all results
rows = cursor.fetchall()

# Print the results
for row in rows:
    print(row)

print()

conn.close()

uconn = sqlite3.connect('users.db')
ucursor = uconn.cursor()
# Read SQL table into DataFrame
#df = pd.read_sql_query("SELECT * FROM table_name", conn)
ucursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Salary INTEGER NOT NULL
)
''')

ucursor.execute("DELETE FROM users")

# Commit the changes
uconn.commit()

ucursor.execute("INSERT INTO users (Name, Salary) VALUES ('Andre', 80000)")
ucursor.execute("INSERT INTO users (Name, Salary) VALUES ('Pepper', 120000)")
ucursor.execute("INSERT INTO users (Name, Salary) VALUES ('Johnson', 75000)")

uconn.commit()

ucursor.execute("SELECT * FROM users")

# Fetch all results
rows = ucursor.fetchall()

# Print the results
for row in rows:
    print(row)

uconn.close()



app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

@app.route('/api', methods=['POST'])
def process_data():
    global new_row_id1
    print(f"this is my rowid b4 processing: {new_row_id1}")
    data = request.json['data']
    print(f"Received: {data}")
    print()

    words = data.split(" ")

    date = words[0]
    date_object = datetime.strptime(date, "%m/%d/%Y")
    type = words[1]
    amount = int(words[2])

    conn = sqlite3.connect('transactions.db')
    # conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    #------------------------------- EXP INSERT---------------------------------------------------------------------------------------------------------------------------------

    cursor.execute("SELECT COUNT(*) FROM expenditures WHERE Date = ?", (date,))
    exists = cursor.fetchone()[0] > 0
    if exists:
        cursor.execute(f"UPDATE expenditures SET {type} = {type} + ? WHERE Date = ?", (amount, date))
        cursor.execute(f"UPDATE expenditures SET Total = Total + ? WHERE Date = ?", (amount, date))
    else:
        # Insert a new row if the date does not exist

        cursor.execute('''INSERT INTO expenditures (
             Date, Housing, Transportation, Food, Clothes, Healthcare, 
             PersonalCare, Education, DebtPayments, SavingsInvestments, 
             Entertainment, GiftsDonations, Misc, Total
        ) VALUES (?, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)''', 
        (date,))

        cursor.execute(f"UPDATE expenditures SET {type} = {type} + ? WHERE Date = ?", (amount, date))
        cursor.execute(f"UPDATE expenditures SET Total = Total + ? WHERE Date = ?", (amount, date))
        cursor.execute("SELECT last_insert_rowid()")
        new_row_id1 = cursor.fetchone()[0]
        print(f"The last inserted row ID is: {new_row_id1}")

    conn.commit()

    cursor.execute("SELECT * FROM expenditures")

    # Fetch all results
    rows = cursor.fetchall()

    # Print the results
    for row in rows:
      print(row)

    print()
    print("new row id" + str(new_row_id1))
    print()

    #-------------------------------WEEKLY EXP INSERT-----------------------------------------------------------------------------------------------------------------------------------------------

    cursor.execute(f'SELECT COUNT(*) FROM weeklyexpenditures')
    row_count = cursor.fetchone()[0]  # Get the first element of the result

    #Check if the table is empty
    if row_count == 0:
        print(f'The table weeklyexps is empty.')
        cursor.execute("INSERT INTO weeklyexpenditures (Date, Housing, Transportation, Food, Clothes, Healthcare, PersonalCare, Education, DebtPayments, SavingsInvestments, Entertainment, GiftsDonations, Misc, Total) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (date,0,0,0,0,0,0,0,0,0,0,0,0,0))
    else:
        print(f'The table weeklyexps has {row_count} rows.')

    print("test the date here")
    print(date)

    cursor.execute("SELECT Date FROM weeklyexpenditures ORDER BY ID DESC LIMIT 1")
    result = cursor.fetchone()
    lastdate = result[0]
    lastdateobj = datetime.strptime(lastdate, "%m/%d/%Y")

    date_difference = date_object - lastdateobj
    days = date_difference.days

    cursor.execute("SELECT COUNT(*) From expenditures WHERE Date = ?",(date,))
    exists = cursor.fetchone()[0] > 0
    print(days)

    if days > 6:
        new_date = lastdateobj + timedelta(days=7)

        new_date_str = new_date.strftime("%m/%d/%Y")

        cursor.execute('''INSERT INTO weeklyexpenditures (
             Date, Housing, Transportation, Food, Clothes, Healthcare, 
             PersonalCare, Education, DebtPayments, SavingsInvestments, 
             Entertainment, GiftsDonations, Misc, Total
        ) VALUES (?, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)''', 
        (new_date_str,))

        cursor.execute(f"UPDATE weeklyexpenditures SET {type} = {type} + ? WHERE Date = ?", (amount, new_date_str))
        cursor.execute(f"UPDATE weeklyexpenditures SET Total = Total + ? WHERE Date = ?", (amount, new_date_str))
        cursor.execute("SELECT last_insert_rowid()") 
        print("if passed")
    else:
        print("else passed")
        cursor.execute(f"UPDATE weeklyexpenditures SET {type} = {type} + ? WHERE Date = ?", (amount, lastdate))
        cursor.execute(f"UPDATE weeklyexpenditures SET Total = Total + ? WHERE Date = ?", (amount, lastdate))
    

    conn.commit()

    cursor.execute("SELECT * FROM weeklyexpenditures")

    # Fetch all results
    rows = cursor.fetchall()

  # Print the results
    for row in rows:
      print(row)

    print()

    cursor.execute('''INSERT INTO transactions (
             Date, Housing, Transportation, Food, Clothes, Healthcare, 
             PersonalCare, Education, DebtPayments, SavingsInvestments, 
             Entertainment, GiftsDonations, Misc
         ) VALUES (?, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)''', 
         (date,))

    cursor.execute(f"UPDATE transactions SET {type} = ? WHERE Date = ?", (amount, date))

    conn.commit()

    cursor.execute("SELECT * FROM transactions")

    # Fetch all results
    rows = cursor.fetchall()

  # Print the results
    for row in rows:
      print(row)

    # Removed expenditures dictionary code

    # removed transactions dictionary code

    conn.close()

    my_dict = {'week1': 1}
    my_dict2 = {'week1': [1, 2, 3, 4, 5]}
    
    return jsonify({'week1': 'test'})
    # return jsonify(exp_dict) # this works
    # return jsonify({'week1': 'test'}) # this works
    # return jsonify({'reverstr : test'})


@app.route('/exp', methods=['POST'])
def sendExpenditureData():

    conn = sqlite3.connect('transactions.db')
    conn.row_factory = sqlite3.Row # test this new cursor avoid <sqlite3.Row object at 0x0000022A108C2DD0> error
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM expenditures")
    rows = cursor.fetchall()
    result_dict = [dict(row) for row in rows]


    print("Test of sql table to py dict: ")
    print(result_dict)
    print("End test of st to pd")
    print()

    return jsonify(result_dict)


@app.route('/wexp', methods=['POST'])
def sendWeeklyExpenditureData():
     
    conn = sqlite3.connect('transactions.db')
    conn.row_factory = sqlite3.Row # test this new cursor avoid <sqlite3.Row object at 0x0000022A108C2DD0> error
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM weeklyexpenditures")
    rows = cursor.fetchall()
    result_dict = [dict(row) for row in rows]


    print("Test of sql table to py dict: ")
    print(result_dict)
    print("End test of st to pd")
    print()

    return jsonify(result_dict)






@app.route('/trans', methods=['POST'])
def process_data3():
    print("test passed")
    trans_dict = dict()
    j = 1
    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM transactions")
    row_count = cursor.fetchone()[0]  # Fetch the count value

    while (j <= row_count): 
         for option in options:
             cursor.execute(f"""
                 SELECT date, {option}
                 FROM transactions
                 WHERE ID = {j}
                 """)
             result = cursor.fetchone()
             if result[1] != 0:
                if result[0] in trans_dict:
                    trans_dict[result[0]].append((option, result[1]))
                else:
                    trans_dict[result[0]] = [(option, result[1])]
         j = j + 1

    print("test of transdict")
    print(str(trans_dict))
    return jsonify(trans_dict)
    #return jsonify({'week1': 'test'}) # this works
   

if __name__ == '__main__':
    app.run(debug=True)

# data = {'Date': ['2024-10-01', '2024-10-02', '2024-10-03'],
#         'Description': ['Salary', 'Groceries', 'Subscription'],
#         'Amount': [3000, -150, -10]}


# df = pd.DataFrame(data)
# print(df)

# df.to_sql('table_name', conn, if_exists='replace', index=False)




# Displaying the DataFrame
