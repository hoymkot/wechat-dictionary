import requests
import logging
import mysql.connector
import time
import config_mysql

# A program that pull the English Chinese dictionary from youdao.com.
#
# To run this program, we first need to prepare a list of English words (words_alpha.txt),
# Then, create a mysql database table dict. dictionary
#
# mysql> desc dict.dictionary;
# +-------------+-------------+------+-----+-------------------+-----------------------------------------------+
# | Field       | Type        | Null | Key | Default           | Extra                                         |
# +-------------+-------------+------+-----+-------------------+-----------------------------------------------+
# | id          | int         | NO   | PRI | NULL              | auto_increment                                |
# | word        | varchar(45) | NO   | UNI | NULL              |                                               |
# | main        | mediumtext  | YES  |     | NULL              |                                               |
# | collins     | longtext    | YES  |     | NULL              |                                               |
# | created_on  | timestamp   | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED                             |
# | modified_on | timestamp   | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED on update CURRENT_TIMESTAMP |
# +-------------+-------------+------+-----+-------------------+-----------------------------------------------+
# 6 rows in set (0.00 sec)
#
# Thirdly, update the mysql connection parameters in this code
# mydb = mysql.connector.connect(
#         host="192.168.1.84",
#         user="myuser",
#         password="mypass",
#         database="dict"
#     )
#
# Note that, there are 370102 words in word_alpha.txt and this is a single thread process. This program will takes
# approximately two weeks to complete. We can use a multi-threaded approach, but youdao.com may block us if there are
# too many concurrent requests.
#
# After we finish fetching the dictionary, we can run another program to output a python dictionary.
#
# This program works as of 2021-01-10, but it may not work if Youdao has major UI change.
# It really doesn't matter for me because I only need to do this once.

def parse_def(text):
    # section one
    begin = text.find('<div class="trans-container">')
    if (begin == -1):
        return ("N/A","N/A");
    begin = begin + len('<div class="trans-container">')
    end = text.find("</div>",begin)
    primary_trans = text[begin:end].replace('\n','').replace('\t','').replace('  ', '');
    text = text[end +len("</div>"):]

    # section two
    collins = '';
    begin = text.find('<div class="collinsMajorTrans">')
    while(begin != -1):
        begin = begin + len('<div class="collinsMajorTrans">')
        end = text.find("</div>",begin)
        collins = collins + text[begin:end].replace('\n', '').replace('\t', '').replace('  ', '');
        text = text[end+len("</div>"):]

        example_begin = text.find('<div class="exampleLists">')
        begin = text.find('<div class="collinsMajorTrans">')
        if ( example_begin != -1 and ( begin == -1 or example_begin < begin)):
            # this section has an example list
            #example_begin = example_begin + len('<div class="exampleLists">');
            end_first = text.find('</div>');
            end_first = end_first + len('</div>');
            end_last = text.find('</div>', end_first);
            example = text[example_begin:end_last].replace('\n', '').replace('\t', '').replace('  ', '') + '</div>';
            collins = collins + example
            end_last = end_last + len('</div>');
            text = text[end_last:]
            begin = text.find('<div class="collinsMajorTrans">')

    return (primary_trans,collins);


def fetch_definition(word):
    url = 'http://dict.youdao.com/w/';
    resp = requests.get(url + word)

    if resp.status_code != 200:
        # This means something went wrong.
        logging.warning('GET word {}'.format(resp.status_code))
        return -1
    else:
        text = resp.text;
        try:
            return parse_def(text);
        except Exception as exp:
            logging.warning(exp);
            logging.warning(text);
            return -1;


def init():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', filename='../../activity.log', level=logging.INFO)


if __name__ == '__main__':

    init()
    start_time = time.time()
    # mysql connection parameters
    mydb = mysql.connector.connect(
        host=config_mysql.config["host"],
        user=config_mysql.config["user"],
        password=config_mysql.config["password"],
        database=config_mysql.config["database"]
    )
    mycursor = mydb.cursor()


    mycursor.execute("SELECT id , word FROM dict.dictionary where main is null order by word asc limit 1;")
    myresult = mycursor.fetchall()
    while (len(myresult) > 0):
        for w in myresult:
            word= w[1].replace('\r', '')
            id = w[0]
            logging.info("fetching: " + word)
            defin = fetch_definition(word)

            if (defin != -1):
                sql = "update dict.dictionary set main = %s , collins = %s where id = %s";
                params = defin + (id, );
                mycursor.execute(sql, params)
                mydb.commit()
                # time.sleep(4)
        mycursor.execute("SELECT id , word FROM dict.dictionary where main is null order by word asc limit 10;")
        myresult = mycursor.fetchall()


    print("run time %s seconds"  %  (time.time() - start_time));