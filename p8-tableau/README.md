# The Tweets of Donald Trump: A Tableau Story

Submitted 2018-05-18 by Anton Rubisov.

### Links
[Initial Version](https://public.tableau.com/profile/anton.rubisov#!/vizhome/TrumpTweets_34/Story1)  
[Final Version](https://public.tableau.com/profile/anton.rubisov#!/vizhome/TrumpTweets-Final/Story1)

### Summary

The underlying dataset for this story is the collection of tweets by `@theRealDonald` between
May 2009 and June 2017, found on Reddit at https://www.reddit.com/r/datasets/comments/6f9862/all_publicly_available_tweets_from_donald_trumps/.
I did some preprocessing to format timestamps and clean the tweet text of special characters, and ran
sentiment analysis remaining tweet content using a Python library called `textblob`. The resulting
Tableau story shows the evolution of Trump's tweeting habits, sentiment, and content of his tweets
across three epochs: before he announced his candidacy, during his electoral race, and after his
election as President of the United States.

### Design

I was inspired by some of the designs I had seen on Tableau Public for similar tweet analysis projects -
namely, the clock-style visualisation at [4] and the jittered points representing all tweets at [6].
I took it as a personal challenge to reproduce those visualisations without downloading their workbooks, and
countless hours were dedicated to those two tasks.

The scatter plot of tweets, favorites, and retweets was the first visual I produced, and largely dictated
the remainder of the analysis I did. I noticed a few very identifiable changes in behaviour - such as when
the number of favourites and retweets rapidly ascends, and likewise when Trump's own tweet volume
rapidly decreases - and was unsurprised to find that these coincided with his nomination to the
presidential election, and his subsequent win. These well defined eras were the inspiration for the analysis
that followed.

The final block of the story, the word cloud, was the most interesting visualisation I created. It was my
first time making use of both shape and colour to highlight the same variable (word count frequency) - in
all other plots I've ever made, including years of graduate school and years in the working world -  I've
never used two aesthetics to draw attention to a single variable. This shift away from purely academic
communication to something more visually-focused is a welcome change for me!

The main design change I made after soliciting feedback was the introduction of the histogram on the second
block, which was formerly two clock faces for AM and PM time. The single, linear axis is cleaner to read
and doesn't have an odd discontinuity at noon.

### Feedback

I showed this visualization to my work colleague Calvin Jepson. It was his first time
seeing Tableau, so he wasn't immediately familiar with the story format, the hover over
features, etc, and took him a little bit of stumbling to understand what was happening.

His primary feedback was around the visualisation of time-of-tweet as two clocks - he
felt it was an unintuitive presentation, and the discontinuity at noon was unacceptable for him.
He strongly suggested I either change to a single, 24-hour clock, or even better, to a histogram -
it was this latter suggestion that I implemented.

Calvin thought the time-of-tweet visalisation was the most telling as far as discerning
changes in behaviour. There is a notable difference in the cardinality of tweets, as well
as sentiment differences with considerably more vitriol in the election campaign era. At
the same time, Calvin was most enthused about the word cloud visualization, and spent the
longest on that sheet, taking the time to read the various words and form his own hypotheses.
Calvin suggested emphasizing the word cloud by moving it to the top of the page, on which I
gladly took his feedback. More broadly, it's clear that more NLP is the natural direction
to take a story focusing on tweet analysis.

### Resources

[1] https://www.reddit.com/r/datasets/comments/6f9862/all_publicly_available_tweets_from_donald_trumps/

[2] https://dev.to/rodolfoferro/sentiment-analysis-on-trumpss-tweets-using-python-

[3] https://www.thedataschool.co.uk/mina-ozgen/make-clock-chart/

[4] https://public.tableau.com/profile/matt.c6325#!/vizhome/TrumpTweets2016/TrumoTweets2016

[5] https://community.tableau.com/docs/DOC-9627

[6] https://public.tableau.com/profile/poojagandhi#!/vizhome/TrumpTweets_6/TrumpTweets
