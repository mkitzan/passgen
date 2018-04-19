from sqlite3 import connect
from sys import argv, version_info


FLAGS = ['-w', '-l', '-s', '-d']
TABLES = ['eff', 'dw']
NUM_SEQ = ['1', '2', '3', '4', '5', '6']
ERROR = 'Flag "%s" appeared without a following argument\nEnter "passgen help" for usage'
HELP = """'passgen' generates a random diceware password

    Flag    Label       Value           Default     Explaination
    -------------------------------------------------------------------------------------------------
    '-w'    wordcount   int             6           number of diceware words to generate

    '-s'    symbols     int             0           number of symbols to randomly insert

    '-d'    delimeter   char            s           char to place between words
                                                    use 's' for spaces
                                                    use 'n' for no delimeter
    
    '-l'    list        dw/eff/mix      mix         wordlist to draw from 
                                                    dw:     standard diceware list
                                                    eff:    electronic frontier foundation
                                                    mix:    for each word, either dw or eff is picked"""


def get_symbol(curs):
    id_ = "".join([choice(NUM_SEQ) for i in range(2)])
    curs.execute('SELECT word FROM sym WHERE id=%s' % (id_))
    
    return curs.fetchall()[0]


def get_table():
    return choice(TABLES)


def get_word(curs, table):
    id_ = "".join([choice(NUM_SEQ) for i in range(5)])
    curs.execute('SELECT word FROM ' + table + ' WHERE id=%s' % (id_))
    
    return curs.fetchall()[0]


def read_args():
    args = {'-w':6, '-l':'mix', '-s':0, '-d':'s'}
    value = None

    if len(argv) == 1:
        return args

    if argv[1].lower() == 'help':
        print(HELP)
        exit()
    else:
        for el in reversed(argv[1:]):
            if el in FLAGS:
                if value is None:
                    print(ERROR % (el))
                    exit()
                else:
                    args[el] = value
                    value = None
            else:
                value = el
        
        return args
        
        
def passgen(args):
    try:
        wcount = int(args['-w'])
        table = args['-l']
        scount = int(args['-s'])
        delim = args['-d'][0] if len(args['-d']) > 1 else args['-d']
        
        delim = ' ' if delim == 's' else delim
        delim = '' if delim == 'n' else delim
        
        pw = ''
        db = connect('wordlist.db')
        curs = db.cursor()
        
        for i in range(wcount):
            pw += get_word(curs, get_table() if table == 'mix' else table)[0]
            pw += delim

        pw = [ch for ch in pw]

        for i in range(scount):
            pw.insert(choice(range(len(pw))), get_symbol(curs)[0])
            
        curs.close()
        db.close()

        print(''.join(pw))
        
    except ValueError as e:
        print(e)
        print(ERROR % ('unknown'))


def main():
    passgen(read_args())


if __name__ == '__main__':
    if version_info[0] > 2 and version_info[1] > 5:
        from secrets import choice
    else:
        from random import choice
        
    main()

