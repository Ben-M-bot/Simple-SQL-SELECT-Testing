from lark import Lark


grammar = """
        !select: "SELECT"i [DISTINCT | ALL] results_column [CM results_column]* [from] [where] [group] [having] [order] ";"
        results_column: expr [[AS] col_alias] | "*" | table_name "." | res_op LPR expr RPR [AS col_alias]
        from: [FROM table_or_subquery [CM table_or_subquery]* | FROM join_clause]
        join_clause: table_or_subquery [join_operator table_or_subquery join_constraint]*
        join_operator: CM | [NATURAL] [(LEFT|RIGHT|FULL) [OUTER] | INNER] JOIN | CROSS JOIN
        join_constraint: [ON expr | USING LPR column_name [CM column_name]* RPR]
        table_or_subquery: table_name [[AS] table_alias] | LPR select RPR | LPR table_or_subquery [CM table_or_subquery]* RPR
        where: [WHERE expr]
        group: [GROUP BY expr [CM expr]*]
        having: ["HAVING" expr]
        order: [ORDER BY order_term [CM order_term]*]
        order_term: expr [ASC | DESC]
        expr: literal_value | [table_name "."] column_name | unary_op expr | expr binary_op expr 
        | expr (ISNULL|NOTNULL|NOT NULL) | LPR expr [CM expr]* RPR | expr [NOT] LIKE expr
        | expr IS [NOT] [DISTINCT FROM] expr | [NOT] [EXISTS] LPR select RPR | expr unary_op expr
        | expr [NOT] BETWEEN expr AND expr | expr (AND|OR) expr | expr [NOT] IN LPR (select|expr [CM expr]*) RPR
        literal_value: /[0-9]+/ | /'[%?\w+_?-?\s?\w*]+'/ | NULL | TRUE | FALSE 
        table_name: /[\w+_?\w*]+/
        col_alias: /'?[\w+_?-?\s?\w*]+'?/
        table_alias: /[\w+_?\w*]+/
        column_name: /[\w+_?\w*]+/
        binary_op: /\s(>=|<=|>|<|=|!=)\s/
        unary_op: /[-|\/|\+|\*]/
        SELECT: "SELECT"i
        FROM: "FROM"i
        WHERE: "WHERE"i
        BETWEEN: "BETWEEN"i
        AND: "AND"i
        NOT: "NOT"i
        NULL: "NULL"i
        FULL: "FULL"i
        LEFT: "LEFT"i
        RIGHT: "RIGHT"i
        INNER: "INNER"i
        OUTER: "OUTER"i
        ON: "ON"i
        USING: "USING"i
        CROSS: "CROSS"i
        JOIN: "JOIN"i
        NATURAL: "NATURAL"i
        EXISTS: "EXISTS"i
        LIKE: "LIKE"i
        DISTINCT: "DISTINCT"i
        IS: "IS"i
        NOTNULL: "NOTNULL"i
        ISNULL: "ISNULL"i
        FALSE: "FALSE"i
        TRUE: "TRUE"i
        AS: "AS"i
        ALL: "ALL"i
        ASC: "ASC"i
        DESC: "DESC"i
        HAVING: "HAVING"i
        ORDER: "ORDER"i
        GROUP: "GROUP"i
        !res_op: "COUNT"i | "SUM"i | "MIN"i | "MAX"i | "AVG"i
        OR: "OR"i
        IN: "IN"i
        BY: "BY"i
        CM: ", "
        LPR: /\s?\(/
        RPR: /\)\s?/
        %ignore " "
"""
parser = Lark(grammar, start='select', maybe_placeholders=False)
# print(parser.parse("SELECT first_name, last_name FROM Students WHERE age = 25;").pretty())


def check_join(tree):
    """
    Checks if a join clause is used in the query
    :param tree: Lark parse tree
    :return: True if Join is in the query, else False
    """
    for i in tree.find_data('join_clause'):
        return True
    return False


def compare_join(tree_one, tree_two):
    t1 = check_join(tree_one)
    t2 = check_join(tree_two)
    if t1 and t2:
        return "JOIN: Both queries have a JOIN clause"
    elif t1 and not t2:
        return "JOIN: Student query is missing a JOIN clause"
    elif not t1 and t2:
        return "JOIN: Student query has a JOIN clause not in model query"
    return "JOIN: Neither query has a JOIN clause"


def get_join_names(tree):
    """
    Returns a list of the tables used in a JOIN query
    :param tree: parse tree
    :return: list of table names
    """
    tables = []
    for i in tree.find_data('join_clause'):
        for j in i.find_data('table_name'):
            if j.children[0] not in tables:
                tables.append(j.children[0].value)
    return tables


def check_join_constraint(tree):
    """Checks for the ON constraint and returns it if there is one else it returns False"""
    for i in tree.find_data('join_constraint'):
        if i != []:
            return i.children[0].value
    return False


def check_group(tree):
    """
    Checks if the query has a group by clause
    :param tree: Lark parse tree
    :return: True if there is a group by clause, else False
    """
    for i in tree.find_data('group'):
        if i.children != []:
            return True
    return False


def compare_group(tree_one, tree_two):
    t1 = check_group(tree_one)
    t2 = check_group(tree_two)
    if t1 and t2:
        return "GROUP BY: Both queries have a GROUP BY clause"
    elif t1 and not t2:
        return "GROUP BY: Student query is missing a GROUP BY clause"
    elif not t1 and t2:
        return "GROUP BY: Student query has a GROUP BY clause not in model query"
    return "GROUP BY: Neither query has a GROUP BY clause"


def check_having(tree):
    """
    Checks if the query has a HAVING clause
    :param tree: Lark parse tree
    :return: True if there is a HAVING clause, else False
    """
    for i in tree.find_data('having'):
        if i.children != []:
            return True
    return False


def compare_having(tree_one, tree_two):
    t1 = check_having(tree_one)
    t2 = check_having(tree_two)
    if t1 and t2:
        return "HAVING: Both queries have a HAVING clause"
    elif t1 and not t2:
        return "HAVING: Student query is missing a HAVING clause"
    elif not t1 and t2:
        return "HAVING: Student query has a HAVING clause not in model query"
    return "HAVING: Neither Query have a HAVING clause"


def check_order(tree):
    for i in tree.find_data('order'):
        if i.children != []:
            return True
    return False


def compare_order(tree_one, tree_two):
    t1 = check_order(tree_one)
    t2 = check_order(tree_two)
    if t1 and t2:
        return  "ORDER BY: Both queries have an ORDER BY clause"
    elif t1 and not t2:
        return "ORDER BY: Student query is missing an ORDER BY clause"
    elif not t1 and t2:
        return "ORDER BY: Student query has an ORDER BY clause not in model query"
    return "ORDER BY: Neither query has an ORDER BY clause"


def get_order_terms(tree):
    terms = []
    for i in tree.find_data('order_term'):
        try:
            terms.append(i.children[-1].value)
            for j in i.find_data('column_name'):
                terms.append(j.children[0].value)
        except:
            for j in i.find_data('column_name'):
                terms.append(j.children[0].value)
    return terms


def compare_order_terms(tree_one, tree_two):
    t1_terms = get_order_terms(tree_one)
    t2_terms = get_order_terms(tree_two)
    if t1_terms == t2_terms:
        return "Both queries use the same order terms: " + str(t1_terms)
    elif t1_terms[-2] == "ASC" and t2_terms[-2] != t1_terms[-2]:
        return "Model query uses ASC while student query does not"
    elif t1_terms[-2] == "DESC" and t2_terms[-2] != t1_terms[-2]:
        return "Model query uses DESC while student query does not"
    return "Model and student query use different ordering terms.\nModel terms: " + str(t1_terms)   +\
           "\nStudent terms: " + str(t2_terms)


def compare_tables(tree_one, tree_two):
    """
    Compares two lists of tables
    :param tree_one: first list of table names
    :param tree_two: second list of table names
    :return: True if the tables are the same else it returns the first table that is different between them within a str
    """
    t1 = get_join_names(tree_one)
    t2 = get_join_names(tree_two)
    if t1 != t2:
        for i in t1:
            if i not in t2:
                return "Table <" + i + "> is not in student query"
    return "Tables used are the same"


def change(s1, s2):
    """
    Changes the Select statement of the second query to be hte same as the first query.
    Finds the index before the FROM and the slices everything from the sample query and then replaces the SELECT of the
    student query with the first slice to enable Excepts to work as intended.
    :param s1:
    :param s2:
    :return:
    """
    o1 = s1.upper().find("ORDER")
    o2 = s2.upper().find("ORDER")
    s1 = s1[0:o1]
    s2 = s2[0:o2]
    i1 = s1.upper().find("FROM")
    i2 = s2.upper().find("FROM")
    sli1 = s1[0:i1]
    sli2 = s2[i2:-1]
    sli1 += sli2
    return s1, sli1


def except_adding(s1, s2):
    """
    adds an except between the queries in both ways and returns 2 strings of the queries

    :return: modified queries, s3 is the first query except the second and str2 is the second query except the first
    """
    s1, str2 = change(s1, s2)
    s1 = s1.strip(";")
    s3 = s1 + " EXCEPT " + str2
    st = str2.strip(";")
    str2 = st + " EXCEPT " + s1 + ";"
    return s3, str2

def proof_query(q):
    s = q.strip(";")
    s += " ;"
    return s