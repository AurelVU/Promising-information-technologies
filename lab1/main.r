lr1 <- read.csv2("data.csv")
View(lr1)

model <- lm(data = lr1, Y ~ X1 + X2 + X3 + X4)
print("Результаты регрессионного анализа")
print(summary(model))

print("Результаты регрессионного анализа со 
        статистически значимыми коэффициентами")
model <- lm(data = LR1, Y ~ X1 + X2 + X3)
print(summary(model))

# install.packages("lmtest")
library("lmtest")
print(gqtest(model, order.by = ~X3, data = LR1, fraction = 8))


print(dwtest(model))

# install.packages("car")
library(car)
print(durbinWatsonTest(model))