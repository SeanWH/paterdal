import sqlite3


class BuildWordListDb:
    """
    Imports the file 'wordlist.txt' into 'wordlist.db'
    """

    def __init__(self):
        self.db_name = "wordlist.db"
        self.file_name = "wordlist.txt"
        self.word_dictionary = {}

    def run(self):
        """
        Does what it says...
        :return:
        """
        self.word_dictionary = self.read_file(self.file_name)
        self.write_db(self.word_dictionary)

    def read_file(self, filename):
        """
        Reads the file 'filename' into a dictionary and returns it
        :param filename:
        :return:
        """
        word_dictionary = {}

        with open(filename, 'r') as file:
            for line in file:
                key = line[0]
                if key not in word_dictionary.keys():
                    word_dictionary[key] = [line]
                else:
                    words = word_dictionary[key]
                    words.append(line)
                    word_dictionary[key] = words

        return word_dictionary

    def write_db(self, word_dictionary):
        """
        Writes the word dictionary as a sqlite database
        :param word_dictionary:
        :return:
        """
        idx = 0
        db = sqlite3.connect(self.db_name)
        db_cursor = db.cursor()
        try:
            db_cursor.execute(
                "CREATE TABLE words" +
                "(id, alpha_idx, word, used_date, guesses, guessed, " +
                "PRIMARY KEY(id, alpha_idx, word))"
            )
        except sqlite3.OperationalError:
            # Most likely thrown because the table already exists
            pass

        for key in word_dictionary.keys():
            words = word_dictionary[key]
            for word in words:
                data = idx, key, word, "", 0, ""
                try:
                    db_cursor.execute(
                        "INSERT INTO words VALUES(?, ?, ?, ?, ?, ?)", data
                        )
                except sqlite3.IntegrityError:
                    # Usually because PK already exists
                    print("Word already in database.")
                idx += 1

        db.commit()
        db.close()

builder = BuildWordListDb()
builder.run()
