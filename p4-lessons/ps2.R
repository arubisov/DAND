library(ggplot2)
data(diamonds)
summary(diamonds)
str(diamonds)

###

ggplot(data = diamonds, aes(x = x, y = price)) + 
  geom_point()

with(diamonds, cor.test(x, price))
with(diamonds, cor.test(y, price))
with(diamonds, cor.test(z, price))

ggplot(data = diamonds, aes(x = depth, y = price)) + 
  geom_point(alpha = 0.01) +
  scale_x_continuous(breaks = seq(0,80,2))

with(diamonds, cor.test(depth, price))

ggplot(data = diamonds, aes(x = carat, y = price)) + geom_point()
  xlim(0, quantile(diamonds$carat, 0.99)) +
  ylim(0, quantile(diamonds$price, 0.99)) 

diamonds$vol = diamonds$x * diamonds$y * diamonds$z

ggplot(data = subset(diamonds, vol > 0 & vol < 800),
       aes(x = vol, y = price)) + 
  geom_point(alpha = 0.01) +
  geom_smooth(method = 'lm', color = 'red')

### 

diamondsByClarity = diamonds %>%
  group_by(clarity) %>%
  summarise(mean_price = mean(price),
            median_price = median(price),
            min_price = min(price),
            max_price = max(price),
            n = n()) %>%
  arrange(clarity)

###

diamonds_by_clarity <- group_by(diamonds, clarity)
diamonds_mp_by_clarity <- summarise(diamonds_by_clarity, mean_price = mean(price))

diamonds_by_color <- group_by(diamonds, color)
diamonds_mp_by_color <- summarise(diamonds_by_color, mean_price = mean(price))

b1 <- ggplot(data = diamonds_mp_by_clarity, aes(x = clarity, y = mean_price)) + geom_bar(stat = "identity")
b2 <- ggplot(data = diamonds_mp_by_color, aes(x = color, y = mean_price)) + geom_bar(stat = "identity")
grid.arrange(b1,b2, ncol=1)