import sqlite3 as sq
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
from sql_parser import *
from queries import Queries
import os

#change message to a sting that gets added to as it goes
# The file that the output will be appended to
# file_name = "output.txt"
msg = ""
out = "_output.txt"
# The different databases
try:
    print("Select database file")
    db = askopenfilename()
    print("Select model_query_file")
    model_f = askopenfilename()
    print("Select student_query_directory")
    student_d = askdirectory()
    os.chdir(student_d)
    student_f = os.listdir()
    m = Queries(model_f).queries()
    for q in student_f:
        i = 0
        s = Queries(q).queries()
        file_name = q.strip(".txt")
        # The model query and student query
        while i < len(m):
            m_query = m[i]
            s_query = s[i]
            i += 1
            msg = ""
            try:
                m_tree = parser.parse(m_query)
                m_join = check_join(m_tree)
                s_tree = parser.parse(s_query)
                msg += compare_join(m_tree, s_tree) + "\n"
                msg += compare_group(m_tree, s_tree) + "\n"
                msg += compare_having(m_tree, s_tree) + "\n"
                msg += compare_order(m_tree, s_tree) + "\n"
                if check_order(m_tree) and check_order(s_tree):
                    msg += compare_order_terms(m_tree, s_tree) + "\n"
                if m_join:
                    msg += compare_tables(m_tree, s_tree)
            # Replace this section with the parser and use it to find relevant information.#
            except Exception as e:
                msg += e
                msg += "\n"
            try:
                output = open(file_name + out, "a")
                conn = sq.connect(db)
                output.write("-----------------------------------------------------\n")
                m_result = conn.execute(proof_query(m_query)).fetchall()
                s_result = conn.execute(proof_query(s_query)).fetchall()
                if m_result == s_result: # if the results are the exact same
                    # Output the messages to a new file
                    output.write("Query is fully correct\n")
                elif m_join == False and False: # If the query is on a single table and not ordered
                    new_m, new_s = except_adding(m_query, s_query)
                    nm_result = conn.execute(new_m).fetchall()
                    ns_result = conn.execute(new_s).fetchall()
                    if len(nm_result) == 0 and len(ns_result) == 0: # If the student just has the wrong column names but the other parts are correct
                        # Store the comment in a list or dictionary to be reported to the user later
                        output.write("Query is correct except for the column names\n")
                    elif len(nm_result) == 0 and len(ns_result) > 0:
                        # Store the comment in a list or dictionary to be reported to the user later
                        output.write(msg + "Query contains all the necessary results along with unwanted results\nExample: " + str(ns_result[0]) + "\n")
                    elif len(nm_result) > 0 and len(ns_result) == 0:
                        # Store the comment in a list or dictionary to be reported to the user later
                        output.write(msg + "Query contains some but not all the necessary results\nExample" + str(nm_result[0]) + "\n")
                    else: # The query does not contain all the necessary results and contains unwanted results
                        # Store comment in a list or dictionary to be reported to the user
                        output.write(msg + "Query does not contain all the necessary results and contains unwanted results\n" +
                                     "Necessary example: " + str(nm_result[0]) + "\n" +
                                     "Unwanted example: " + str(ns_result[0]) + "\n")

                else: # the query has to deal with joins
                    # Check if the joins are the same
                    output.write(msg + "Query is incorrect, the model query has " + str(len(m_result)) + " results\nExample: " +
                                 str(m_result[0]) + "\nWhile " +
                                 "the student_query has " + str(len(s_result)) + " results\n" + "Example: " + str(s_result[0]) + "\n")

            except sq.Error as e:
                output.write(str(e))
    # Close the connection to the database and the file
    output.close()
    conn.close()
except Exception as e:
    print(e)