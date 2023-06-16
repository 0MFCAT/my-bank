import sqlite3


def create_database():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE users(
            first_name text,
            last_name text,
            year_of_birth integer,
            country text,
            email text,
            password text
            )""")

    cursor.execute("""CREATE TABLE bank_data(
            bank_id integer,
            USD real,
            USDT real,
            BTC real
            )""")

    conn.commit()
    conn.close()


def return_loggins():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT email, password FROM users")
    data = cursor.fetchall()
    conn.close()
    return data


def construct_user(user_email, user_password):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * from users WHERE email = (?) AND password = (?)", (user_email, user_password))
    data = cursor.fetchall()
    print(data)
    conn.close()
    return data


def main():
    pass
    # create_database()


'''
    example_users = [
        ("Juan Manuel", "González Vega", 1998, "CUB", "juanmgv98@gmail.com", "QWERTY"),
        ("Dorian", "Gay Perez", 1998, "CUB", "dorianperez@gmail.com", "12345"),
        ("Alejandro", "Marrero Garcia", 1997, "CUB", "manko@gmail.com", "axax"),
        ("Andy Daniel", "Matamoros", 1998, "CUB", "rata@gmail.com", "menores13")
    ]
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO users VALUES (?,?,?,?,?,?)", example_users)



    conn.commit()
    conn.close()
'''

if __name__ == "__main__":
    main()
