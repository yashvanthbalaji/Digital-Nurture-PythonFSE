# Digital Nurture 5.0 | Module 3: Database Integration
# Hands-On 4 - Task 3: N+1 Problem
# Name   : BALAJI A

import mysql.connector
import time

connection = mysql.connector.connect(
    host     = 'localhost',
    user     = 'root',
    password = '143143143',
    database = 'college_db'
)

cursor = connection.cursor()

# Step 56: Simulate N+1 Problem
print("=== Version 1: N+1 Problem ===")

query_count = 0
start_time  = time.time()

cursor.execute("SELECT * FROM enrollments")
enrollments = cursor.fetchall()
query_count += 1

for enrollment in enrollments:
    student_id = enrollment[1]
    cursor.execute(
        "SELECT first_name, last_name FROM students WHERE student_id = %s",
        (student_id,)
    )
    cursor.fetchone()
    query_count += 1

end_time = time.time()

print(f"{query_count} queries executed")
print(f"Time taken: {round(end_time - start_time, 4)} seconds")

# Step 57: Fix N+1 using a single JOIN query
print("\n=== Version 2: Fixed with JOIN ===")

query_count_v2 = 0
start_time_v2  = time.time()

cursor.execute("""
    SELECT e.enrollment_id,
           s.first_name,
           s.last_name,
           e.grade
    FROM enrollments e
    INNER JOIN students s ON e.student_id = s.student_id
""")
results = cursor.fetchall()
query_count_v2 += 1

end_time_v2 = time.time()

print(f"{query_count_v2} queries executed")
print(f"Time taken: {round(end_time_v2 - start_time_v2, 4)} seconds")

# Step 58: Compare round-trips between both versions

print("\n=== Comparison ===")
print(f"Version 1 (N+1)  - Total queries   : {query_count}")
print(f"Version 2 (JOIN) - Total queries   : {query_count_v2}")
print(f"Queries saved                       : {query_count - query_count_v2}")

# Step 59: Real world impact with 10,000 enrollments
# N+1 version  : 1 (fetch all) + 10,000 (one per row) = 10,001 queries
# JOIN version  : 1 query only
# Extra queries : 10,000 unnecessary database round-trips

cursor.close()
connection.close()