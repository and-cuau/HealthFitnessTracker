import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import atexit

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

cursor.execute("DELETE FROM weeklyexpenditures")

conn.commit()

# cursor.execute("INSERT INTO weeklyexpenditures (Date, Housing, Transportation, Food, Clothes, Healthcare, PersonalCare, Education, DebtPayments, SavingsInvestments, Entertainment, GiftsDonations, Misc, Total) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", ("week1",0,0,0,0,0,0,0,0,0,0,0,0,0))
new_row_id1 = 1

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
    data = request.json['data']
    print(f"Received: {data}")
    print()

    words = data.split(" ")

    date = words[0]
    type = words[1]
    amount = int(words[2])

    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()


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
        new_row_id1 += 1
    

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

    # dayexps_dict = dict()
    # dayexps_dict[date] =  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # for option in options:
    #     cursor.execute(f"""
    #     SELECT {option}
    #     FROM expenditures
    #     WHERE Date = ?
    #     """, (date,))
    #     result = cursor.fetchone()
    #     dayexps_dict[date].append(result[0])



    # cursor.execute('''INSERT INTO expenditures (
    #          Date, Housing, Transportation, Food, Clothes, Healthcare, 
    #          PersonalCare, Education, DebtPayments, SavingsInvestments, 
    #          Entertainment, GiftsDonations, Misc
    #      ) VALUES (?, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)''', 
    #      (date,))

    #exp_dict = dict()

    exp_dict = dict()
    exp_dict["week1"] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
   
    if (new_row_id1 % 3 == 0):    # weekly sum calculation
        exp_dict = dict()
        exp_dict["week1"] = []
       # exp_dict[date] = []
        for option in options:
            cursor.execute( f"""
            SELECT SUM({option}) AS total_sum
            FROM (
                SELECT {option}
                FROM expenditures
                ORDER BY id DESC
                LIMIT 7
                ) AS subquery
            """)
            result = cursor.fetchone()
            cursor.execute(f"UPDATE weeklyexpenditures SET {option} = {option} + ? WHERE Date = ?", (result[0], "week1"))
            cursor.execute(f"UPDATE weeklyexpenditures SET Total = Total + ? WHERE Date = ?", (result[0], "week1"))
        
        conn.commit()
        cursor.execute("SELECT * FROM weeklyexpenditures")

        rows = cursor.fetchall()
        # Print the results
        print("test this print")
        for row in rows:
            print(row)

        print()

    
        for option in options:
            cursor.execute(f"""
            SELECT {option}
            FROM weeklyexpenditures
            WHERE Date = ?
            """, ("week1",))
            result = cursor.fetchone()
            exp_dict["week1"].append(result[0]) # error here result is nonetype

        cursor.execute(f"""
        SELECT Total
        FROM weeklyexpenditures
        WHERE Date = ?
        """, ("week1",))
        result = cursor.fetchone()
        exp_dict["week1"].append(result[0])

        print("test: ")
        print(exp_dict)
        print("end test")

   
    cursor.execute('''INSERT INTO transactions (
             Date, Housing, Transportation, Food, Clothes, Healthcare, 
             PersonalCare, Education, DebtPayments, SavingsInvestments, 
             Entertainment, GiftsDonations, Misc
         ) VALUES (?, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)''', 
         (date,))
    
    new_row_id = cursor.lastrowid

    cursor.execute(f"UPDATE transactions SET {type} = ? WHERE Id = ?", (amount, new_row_id))

    conn.commit()

    cursor.execute("SELECT * FROM transactions")

    # Fetch all results
    rows = cursor.fetchall()

  # Print the results
    for row in rows:
      print(row)


    conn.close()

    print("test 2: ")
    print(str(exp_dict))
    print("end test")
    
    my_dict = {'week1': 1}
    my_dict2 = {'week1': [1, 2, 3, 4, 5]}

    
    return jsonify(exp_dict)
    # return jsonify({'week1': 'kcuf'}) # this works
    # return jsonify({'reverstr : fuck'})




@app.route('/test', methods=['POST'])
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
    return jsonify({'week1': 'test'}) # this works
   

if __name__ == '__main__':
    app.run(debug=True)

# data = {'Date': ['2024-10-01', '2024-10-02', '2024-10-03'],
#         'Description': ['Salary', 'Groceries', 'Subscription'],
#         'Amount': [3000, -150, -10]}


# df = pd.DataFrame(data)
# print(df)

# df.to_sql('table_name', conn, if_exists='replace', index=False)







# Displaying the DataFrame
