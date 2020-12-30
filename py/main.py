# This is the main script of the stock scraper
import datetime
import time
import sched
import praw
import mysql.connector



# gets all the tickers from the tickers  file
def get_tickers():
    fin = open("tickers.txt", 'r')
    tickers = []
    fin.readline()
    for line in fin.readlines():
        tickers.append(line[:line.index(",")])
    return tickers

def get_date(submission):
    time = submission.created
    print(submission.created)
    return datetime.datetime.fromtimestamp(time)

def main_function(sc):
    print("starting the function now")
    # main part of the script
    reddit = praw.Reddit(
         client_id="l3pEhSgqHalm7g",
         client_secret="FL5BhDDlJXqciRIBckjJTIzDLTCDXw",
         user_agent="web scraper by u/qk_stock_scraper v0.1"
     )
    print("time is " + str(time.time()))
    #gets our tickers
    tickers = get_tickers()
    filtered_words = ["YOLO", "FREE", "PUMP", "RH", "EOD", "IPO", "ATH", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P",
                      "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

    # gets the last post that was handled
    fin = open("prev.txt", "r+")
    prevDateStr = fin.readline()
    if prevDateStr == "":
        prevDateStr = "1608940800"
    prevDate = float(prevDateStr)
    fin.truncate(0)
    fin.close()

    # sets up variable to hold the timestamp of the first post we look at
    lastDateTS = prevDate

    # iterates through the 10 newest posts
    wsb = reddit.subreddit("wallstreetbets")
    for submission in wsb.new(limit=100):

        #print("author", submission.author.name)

        # breaks if we have seen this post before
        if float(submission.created) <= prevDate:
            print("breaking now")
            break


        # sets the first post we read as the previous post, so we know where to stop next time
        if lastDateTS == prevDate:
            print("just set the new date")
            lastDateTS = float(submission.created)

        # sets up the set to store the new tickers
        new_tickers = set()

        # print("")
        # print("Title: ", submission.title)
        # print("Body: ", submission.selftext)

        # handle if theres a dollar sign
        for word in submission.title.split():
            if word.startswith("$"):
                word = word[1:]
            #TODO: Add a more advanced way to filter tickers, get rid of the noise
            if word in tickers and word not in filtered_words:
                new_tickers.add(word)
        for word in submission.selftext.split():
            if word in tickers:
                new_tickers.add(word)
        for word in new_tickers:
            print("Found: ", word)
            #inserts any tickers that get found into the mysql database
            #TODO: Add a way to convert the date we get from submission object to something human readable instead of
            #using now()
            mycursor.execute("insert into stock_testing values (default, '" + word + "', now())")
            mydb.commit()
            print("added")

    # writes the last post we looked at so we know when to stop
    fout = open("prev.txt", "w")
    fout.write(str(lastDateTS))
    fout.close

    print("stopping for 10 mins")
    s.enter(600, 1, main_function, (sc,))



#sets up the database connector and cursor
mydb = mysql.connector.connect(
  host="localhost",
  user="stock_scraper",
  password="quinnkump1",
  database="py_stock_scraper"
)
mycursor = mydb.cursor()

s = sched.scheduler(time.time, time.sleep)
s.enter(1, 1, main_function, (s,))
s.run()



