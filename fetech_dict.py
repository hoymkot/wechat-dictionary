import requests
import logging
import mysql.connector
import time



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
        return parse_def(text);


def init():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', filename='../activity.log', level=logging.INFO)


if __name__ == '__main__':

    init()
    start_time = time.time()

    mydb = mysql.connector.connect(
        host="192.168.1.84",
        user="myuser",
        password="mypass",
        database="dict"
    )
    mycursor = mydb.cursor()


    mycursor.execute("SELECT id , word FROM dict.dictionary where main is null order by word asc limit 10;")
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