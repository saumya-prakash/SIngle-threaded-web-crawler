from Data import *

import mysql.connector as sqltor

mycon = sqltor.connect(user='saumya', passwd='2020', host='localhost', database='project')

curs = mycon.cursor()

query = ''' SELECT name, home_page from records WHERE id > 31 '''

curs.execute(query)

a = curs.fetchall()

curs.close()
mycon.close()

for i in a:
    name = i[0];
    hp = i[1];

    store = "/home/saumya/Desktop/DATA/"

    if os.path.isdir(store+name) == False:
        os.mkdir(store+name)

    os.chdir(store+name)

    print(name)
    try:
        if os.path.isfile("./aaa_logo") == False:
            web = Data(hp)
            web.get_logo()

    except Exception as e:
        print(e)

    print()
    os.chdir(store)

