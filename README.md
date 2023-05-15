# Simple-SQL-SELECT-Testing
A tool to help automate the testing of simple SELECT sql queries commonly used by students learning SQL for the first time. Designed from the perspective of helping a lecturer/teacher correct batches students queries at a time. Compares he outputs of the queries as well as the syntactic stucture.

Project uses SQLite in python to perform the comparisons as well as a Lark parser.
A model query (a correct query) is needed for every student query and vise versa to ensure the corresponding queries are compared against each other.
The queries should start with no gaps from the edge of the line. Can accept multiline queries as well as single line queries.
When run the user will be asked to provide a SQLite database, model query file and student query directory in that order.
Lark parser used to compare the syntax while the EXCEPT keyword in SQL is used to help compare outputs in applicable situations.
Outputs of the comparisons will be returned in the same directory as the student queries. Each student file will have a unique ouput file with the original name getting _outputs.txt added to it.
Outputs will be in the same order aas the queries and clearly seperated from eaach other by a ------- line.
