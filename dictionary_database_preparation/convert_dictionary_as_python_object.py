import json
import mysql.connector
from datetime import datetime
import re
# this program convert the dictionary to a python dict (json).

if __name__ == '__main__':

    # mysql connection parameters
    mydb = mysql.connector.connect(
        host="192.168.1.84",
        user="myuser",
        password="mypass",
        database="dict"
    )
    mycursor = mydb.cursor()
    # mycursor.execute("SELECT word, main, collins FROM dict.dictionary where main is not null and main != 'N/A'  ")
    mycursor.execute("SELECT word, main FROM dict.dictionary where main is not null and main != 'N/A'  ")

    myresult = mycursor.fetchall()
    normal_dict = {} ;
    for w in myresult:
        word= w[0]
        defin = w[1]
        defin = defin.replace("<ul>", "").replace("<li>", "").replace("</li>", "\n").replace("</ul>", "");
        defin = re.sub(r'(<p.*</p>)', "", defin);
        # collins = w[2]
        # if (collins != 'N/A'):
        #     defin = defin + collins
        normal_dict[word] = defin

    now = datetime.now()

    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    print("# generated at " + current_time);
    print( "normal_dict = " +json.dumps(normal_dict))

    # mycursor.execute("SELECT word, main,collins FROM dict.dictionary where main is not null and main != 'N/A'  ")
    # myresult = mycursor.fetchall()
    # normal_dict = {} ;
    # for w in myresult:
    #     word= w[0]
    #     defin = w[1]
    #     defin = defin.replace("<ul>", "").replace("<li>", "").replace("</li>", "\n").replace("</ul>", "\n");
    #     defin = re.sub(r'(<p.*</p>)', "", defin);
    #     collins = w[2]
    #     normal_dict[word] = [defin, collins]