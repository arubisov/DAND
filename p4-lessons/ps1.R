library(ggplot2)
data(diamonds)
summary(diamonds)
str(diamonds)

ggplot(data = diamonds, aes(x = price)) + 
  geom_histogram(binwidth = 50, fill = '#5760AB') + 
  facet_wrap(~cut)

qplot(data = diamonds, x = price/carat) +
  facet_wrap(~cut, scales='free_y') +
  scale_x_log10()

by(diamonds$price, diamonds$cut, summary, digits=6)

summary(subset(diamonds, color == 'J')$price) 


ggplot(aes(x = carat), data = diamonds) + 
  geom_freqpoly(binwidth=0.05)

sum(diamonds$carat == 2)