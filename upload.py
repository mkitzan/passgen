from sqlite3 import connect
from sys import argv


def create_table(db, table):
    curs = db.cursor()
    curs.execute('CREATE TABLE IF NOT EXISTS ' + table + ' (id INTEGER, word TEXT)')

    db.commit()
    
    
def upload(db, table , wordlist):
    template = 'INSERT INTO ' + table + ' VALUES("%s", "%s")'
    curs = db.cursor()

    with open(wordlist, 'r') as infile:
        for line in infile:
            line = line.strip('\n').split("\t")
            curs.execute(template % (line[0], line[1]))

    db.commit()
        

def main():
    db = connect('wordlist.db')
    table = argv[1]
    wordlist = argv[2]

    create_table(db, table)
    upload(db, table, wordlist)


if __name__ == '__main__':
    main()

