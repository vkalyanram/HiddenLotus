# import sqlite3
#
# # Connect to SQLite database
# conn = sqlite3.connect('agent.db')
# cursor = conn.cursor()
#
# # Create 'products' table
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS products (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         product_name TEXT NOT NULL,
#         category TEXT CHECK(category IN ("Banking", "Financial Services", "Insurance")) NOT NULL
#     )
# ''')
#
# # Create 'users' table with product reference
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT NOT NULL,
#         contact_number TEXT NOT NULL,
#         email TEXT NOT NULL,
#         category TEXT CHECK(category IN ("Banking", "Financial Services", "Insurance")) NOT NULL,
#         product_id INTEGER,
#         last_interaction TEXT,
#         follow_up_date TEXT,
#         notes TEXT,
#         FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL
#     )
# ''')
#
# # Create 'faqs' table linked to 'products'
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS faqs (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         question TEXT NOT NULL,
#         answer TEXT NOT NULL,
#         product_id INTEGER NOT NULL,
#         FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
#     )
# ''')
#
# # Insert sample products
# sample_products = [
#     ("Savings Account", "Banking"),
#     ("Personal Loan", "Banking"),
#     ("Credit Card", "Banking"),
#     ("Stock Trading", "Financial Services"),
#     ("Mutual Funds", "Financial Services"),
#     ("Retirement Plan", "Financial Services"),
#     ("Life Insurance", "Insurance"),
#     ("Health Insurance", "Insurance"),
#     ("Car Insurance", "Insurance")
# ]
#
# cursor.executemany('''
#     INSERT INTO products (product_name, category)
#     VALUES (?, ?)
# ''', sample_products)
#
# # Commit product entries to get their IDs
# conn.commit()
#
# # Fetch all product IDs
# cursor.execute("SELECT id, product_name FROM products")
# product_ids = {name: id for id, name in cursor.fetchall()}
#
# # Insert sample users with product references
# sample_users = [
#     ("John Doe", "+919876543210", "john.doe@example.com", "Banking", product_ids["Savings Account"], None, None, None),
#     ("Ramesh Kumar", "+919876543211", "ramesh.kumar@example.com", "Insurance", product_ids["Life Insurance"], None, None, None),
#     ("Priya Sharma", "+919876543212", "priya.sharma@example.com", "Financial Services", product_ids["Mutual Funds"], None, None, None),
#     ("Amit Patel", "+919876543213", "amit.patel@example.com", "Banking", product_ids["Personal Loan"], None, None, None),
#     ("Sneha Singh", "+919876543214", "sneha.singh@example.com", "Insurance", product_ids["Health Insurance"], None, None, None)
# ]
#
# cursor.executemany('''
#     INSERT INTO users (name, contact_number, email, category, product_id, last_interaction, follow_up_date, notes)
#     VALUES (?, ?, ?, ?, ?, ?, ?, ?)
# ''', sample_users)
#
# # Insert sample FAQs
# sample_faqs = [
#     ("What is the interest rate?", "The interest rate depends on the type of account.", product_ids["Savings Account"]),
#     ("How can I apply for a loan?", "You can apply online or visit our branch.", product_ids["Personal Loan"]),
#     ("What is the annual fee?", "The annual fee depends on the card type.", product_ids["Credit Card"]),
#     ("How to start stock trading?", "You need to open a Demat account.", product_ids["Stock Trading"]),
#     ("What are mutual funds?", "Mutual funds are investment schemes managed by professionals.", product_ids["Mutual Funds"]),
#     ("Is my retirement plan tax-free?", "Some retirement plans offer tax benefits.", product_ids["Retirement Plan"]),
#     ("What does life insurance cover?", "Life insurance provides financial protection for your family.", product_ids["Life Insurance"]),
#     ("Is pre-existing illness covered?", "It depends on the policy terms.", product_ids["Health Insurance"]),
#     ("Does car insurance cover accidents?", "Yes, depending on your policy.", product_ids["Car Insurance"])
# ]
#
# cursor.executemany('''
#     INSERT INTO faqs (question, answer, product_id)
#     VALUES (?, ?, ?)
# ''', sample_faqs)
#
# # Commit changes
# conn.commit()
#
# # Fetch and print all tables
# def print_table(table_name):
#     cursor.execute(f"SELECT * FROM {table_name}")
#     rows = cursor.fetchall()
#     print(f"\n{table_name} Table:")
#     for row in rows:
#         print(row)
#
# print_table("users")
# print_table("products")
# print_table("faqs")
#
# # Close connection
# conn.close()
