library(ggplot2)
data(diamonds)
str(diamonds)

###
# Create a histogram of diamond prices.
# Facet the histogram by diamond color
# and use cut to color the histogram bars.
ggplot(data = diamonds, aes(x = price)) + 
  geom_histogram(aes(color = cut)) +
  facet_wrap(~color) +
  scale_fill_brewer(type = 'qual')
  
###
# Create a scatterplot of diamond price vs.
# table and color the points by the cut of
# the diamond.
ggplot(data=diamonds, aes(x=table, y=price)) +
  geom_point(aes(color=cut)) + 
  scale_color_brewer(type = 'qual')

###
# Create a scatterplot of diamond price vs.
# volume (x * y * z) and color the points by
# the clarity of diamonds. Use scale on the y-axis
# to take the log10 of price. You should also
# omit the top 1% of diamond volumes from the plot.
diamonds$vol = diamonds$x * diamonds$y * diamonds$z
ggplot(data=diamonds, aes(x=price, y=vol)) +
  geom_point(aes(color=clarity)) +
  scale_color_brewer(type = 'div') +
  ylim(0, quantile(diamonds$vol, 0.99)) 

###
# Your task is to create a new variable called 'prop_initiated'
# in the Pseudo-Facebook data set. The variable should contain
# the proportion of friendships that the user initiated.
setwd('/home/anton/sandbox/datascience/p4-lessons/')
pf <- read.csv("pseudo_facebook.tsv", sep="\t")
pf$prop_initiated = pf$friendships_initiated / pf$friend_count

###
# Create a line graph of the median proportion of
# friendships initiated ('prop_initiated') vs.
# tenure and color the line segment by
# year_joined.bucket.
pf$year_joined = floor(2014 - pf$tenure/365)
pf$year_joined.bucket = cut(pf$year_joined, breaks=c(2004,2009,2011,2012,2014))
ggplot(data=pf, aes(x=tenure, y=prop_initiated)) +
  geom_line(aes(color=year_joined.bucket), stat='summary', fun.y = median) +
  geom_smooth()

###
# Create a scatter plot of the price/carat ratio
# of diamonds. The variable x should be
# assigned to cut. The points should be colored
# by diamond color, and the plot should be
# faceted by clarity.
ggplot(data=diamonds, aes(x=cut, y=price/carat)) +
  geom_jitter(aes(color=color)) +
  facet_wrap(~clarity) +
  scale_color_brewer(type = 'div')