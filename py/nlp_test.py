from nltk.corpus import twitter_samples
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import FreqDist
from nltk import classify
from nltk import NaiveBayesClassifier
from nltk.tokenize import word_tokenize


import random
import re
import string
import nltk

def test():
    print("i'm inside nlp dude")



#print(tweet_tokens)

def lemmatize_sentence(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatized_sentence = []
    for word, tag in pos_tag(tokens):
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
    return lemmatized_sentence

def remove_noise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|' \
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)
        token = re.sub("(u/[A-Za-z0-9_]+)","", token)
        token = re.sub("(r/[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token

def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

def get_sent(text):
    custom_tokens = remove_noise(word_tokenize(text))
    sent = classifier.classify(dict([token, True] for token in custom_tokens))
    if (sent == 'Positive'):
        return "+ 1"
    return "- 1";

def init():
    #make sure that the right stuff is downloaded
    nltk.download('twitter_samples')
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')
    nltk.download('punkt')

    #get global variables ready
    global tweet_tokens, classifier, custom_tokens
    tweet_tokens = twitter_samples.tokenized('positive_tweets.json')[0]

    stop_words = stopwords.words('english')

    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []

    for tokens in positive_tweet_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    for tokens in negative_tweet_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    all_pos_words = get_all_words(positive_cleaned_tokens_list)
    freq_dist_pos = FreqDist(all_pos_words)

    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    positive_dataset = [(tweet_dict, "Positive")
                        for tweet_dict in positive_tokens_for_model]

    negative_dataset = [(tweet_dict, "Negative")
                        for tweet_dict in negative_tokens_for_model]

    dataset = positive_dataset + negative_dataset

    random.shuffle(dataset)

    train_data = dataset[:7000]
    test_data = dataset[7000:]

    print("Training started...")
    classifier = NaiveBayesClassifier.train(train_data)
    print("Model now trained...")

    # print("Accuracy is:", classify.accuracy(classifier, test_data))
    #
    # print(classifier.show_most_informative_features(10))

    custom_tweet = "I have spent a lot of time the past few months learning about technical analysis. I thought I would give it a try since I noticed an interesting trend the other day. I have been watching the 10-year treasury note yield, which can be seen as an indicator for investor confidence. Longer term treasury notes are seen as one of the safest options for investment. Basically an I.O.U. + interest from the US treasury. It is also an inverse indicator, meaning that higher yields indicate lower confidence. As price and demand for the treasury goes up, confidence and yield go down. And so I was watching the 10-year T note this week and saw it rose significantly, breaking its downward trend. I then noticed that spikes in the yield preceded market lows or troughs. My thoughts are institutional investors are liquidating their T-notes in anticipation of some sort of drawback/correction. Basically when equities can be bought at juicy discounted prices. So with this extra cash in hard, they take their profits at a market high, shake out the weak hands in the market and retest support levels to buy back in. Other things to note, that sort of back this up as well, are negative divergence in Relative Strength Index (RSI). And the 50 day moving average approaching the highs before the last correction mid-June. Which, to be honest, I'm not sure means anything, it's just a coincidence on how all this is lining up. Although the spike in yield was significant, it hasn't broken through a zone of indecision. This zone isn't a defined thing, it's just something to watch. If the price action continues to move into this zone, I would feel more and more confident about my sentiments towards a market correction. Even more so if it broke out of this zone. Things that don't support this idea: I'm a gay bear. Also, it could be that we just bounced off a level of support with the T-note, and that is just it - nothing to see here. So it may not have as much significance as I would like. Also a general trend since June of moving up, consolidating for a week or two, moving up and consolidating again before moving upwards once again. How big a correction? My guess is we want to, at the very least, test the most recent level of support at around 3280 - about a 90 pt drop. If that level of support is broken, i.e. daily close below 3280, watch out for a retest of the 3200 level - right around where the 50 day moving average is hanging out. Basically, the market is wanting to test the floor under it before it moves onto all time highs again. Crayon Drawings:  T-Note, Spy Overlay SPY support levels Position: SPY 336/332 Put Debit Spread + SPY 339/341 Call Credit Spread"
    custom_tokens = remove_noise(word_tokenize(custom_tweet))

    print(classifier.classify(dict([token, True] for token in custom_tokens)))

