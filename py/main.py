# This is the main script of the stock scraper
import datetime
import time
import sched
import praw
import psycopg2

from datetime import date

#gets our nlp stuff
from nlp_test import init, get_sent, test
# gets all the tickers from the tickers  file
def get_tickers():
    fin = open("py/tickers.txt", 'r')
    tickers = []
    fin.readline()
    for line in fin.readlines():
        tickers.append(line[:line.index(",")])
    return tickers


def get_date(submission):
    time = submission.created
    print(submission.created)
    return datetime.datetime.fromtimestamp(time)

def date_to_day(date):
    return date[8:10]


def main_function(sc):
    print("starting the function now")
    #initializes data


    # sets up access to reddit
    reddit = praw.Reddit(
         client_id="l3pEhSgqHalm7g",
         client_secret="FL5BhDDlJXqciRIBckjJTIzDLTCDXw",
         user_agent="web scraper by u/qk_stock_scraper v0.1"
     )
    print("time is " + str(time.time()))
    # gets our tickers
    tickers = get_tickers()
    filtered_words = ["CEO", "FOR", "ID", "TA", "ALL", "AI", "EV", "YOLO", "FREE", "PUMP", "RH", "DD", "EOD", "IPO", "ATH", "HUGE", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P",
                      "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

    # gets the last post that was handled
    fin = open("py/prev.txt", "r+")

    prevDateStr = fin.readline()
    if prevDateStr == "":
        prevDateStr = "1608940800"
    prevDate = float(prevDateStr)
    fin.truncate(0)
    fin.close()

    # sets up variable to hold the timestamp of the first post we look at
    lastDateTS = prevDate
    sublist = ['wallstreetbets', 'stocks', 'investing']
    for subname in sublist:
        # gets the subreddit
        sub = reddit.subreddit(subname)

        # iterates through the 100 newest posts or until we reach a post we've already scanned
        for submission in sub.new(limit=1000):
            # breaks if we have seen this post before
            if float(submission.created) <= prevDate:
                print("breaking now")
                break

            # sets the first post we read as the previous post, so we know where to stop next time
            if lastDateTS == prevDate:
                print("just set the new date")
                lastDateTS = float(submission.created)


            #gets the sentiment of the body
            title_sent = get_sent(submission.selftext)

            # iterates through the title
            for word in submission.title.split():
                # handle if theres a dollar sign
                if word.startswith("$"):
                    word = word[1:]

                tickerset = set({})
                # TODO: Add a more advanced way to filter tickers, get rid of the noise
                if word in tickers and word not in filtered_words:
                    #gets the date as just a day
                    day = date.today()

                    #creats the unique id for each day
                    id = str(day) + word

                    tickerset.add(word)
                
            #gets the sentiment of the body
            body_sent = get_sent(submission.selftext)

            # iterates through the body of the post
            for word in submission.selftext.split():
                # handle if theres a dollar sign
                if word.startswith("$"):
                    word = word[1:]

                if word in tickers and word not in filtered_words:
                    #gets the date as yyyy-mm-dd for the id
                    day = date.today()
                    id = str(day) + word

                    # adds it to the set to add to db later
                    tickerset.add(word)

                    # adds the new ticker to the DB
                    # mycursor.execute("INSERT INTO mentions_nyse (id, mentions, sentiment, ticker, date, source) VALUES ('" + id + "', 1, " + body_sent + ", '" + word + "', '" + str(day) + "', '" + subname + "') ON CONFLICT (id) DO UPDATE SET mentions = mentions_nyse.mentions + 1,  sentiment = mentions_nyse.sentiment + " + body_sent)
                    # mydb.commit()

            # adds the new tickers to the DB
            for ticker in tickerset:
                mycursor.execute("INSERT INTO mentions_nyse (id, mentions, sentiment, ticker, date, source) VALUES ('" + id + "', 1, " + body_sent + ", '" + ticker + "', '" + str(day) + "', '" + subname + "') ON CONFLICT (id) DO UPDATE SET mentions = mentions_nyse.mentions + 1, sentiment = mentions_nyse.sentiment + " + body_sent)
                mydb.commit()

            
        print("Finished parsing " + subname)

    # writes the last post we looked at so we know when to stop
    fout = open("py/prev.txt", "w")
    fout.write(str(lastDateTS))
    fout.close

    # scheduler runs the next loop through
    print("stopping for 1 hour")
    s.enter(3600, 1, main_function, (sc,))


# sets up the database connector and cursor
mydb = psycopg2.connect(
    host="ec2-3-214-3-162.compute-1.amazonaws.com",
    database="d3vemptti50aoo",
    user="ruwwlubbxnwdsk",
    password="979a396bba68831aac97d498fca8ef91cef26c322def58c8e859ca219bbe956f")

mycursor = mydb.cursor()

init()
print("Model fully initialized...")

# sets up scheudler for the first run through
s = sched.scheduler(time.time, time.sleep)
s.enter(1, 1, main_function, (s,))
s.run()



