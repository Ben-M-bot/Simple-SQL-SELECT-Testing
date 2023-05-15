STARTS = ["SELECT", "INSERT", "DELETE"]

class Queries:

    def __init__(self, file):
        self._file = file
        self._queries = self.__get_queries()

    def __get_queries(self):
        r = open(self._file, "r")
        query = {}
        mul_line = False
        i = 0
        string = ""
        for line in r:
            i += 1
            if not mul_line:
                if line[0:6].upper() in STARTS:
                    string = line.replace("\n", "")
                    if string[-1] == ";":
                        query[i] = string
                        i += 1
                        continue
                    else:
                        mul_line = True
                        i += 1
            else:
                string += " "
                string += line.replace("\n", "")
                if string[-1] == ";":
                    query[i] = string
                    mul_line = False
                    i += 1
                    continue


        return query

    def queries(self):
        l = []
        for i in self._queries.values():
            l.append(i)
        return l



# q = Queries("../../test_text_file.txt")
# test = q.queries()
# print(test)
# print(q.queries())












