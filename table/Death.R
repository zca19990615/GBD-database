library(tidyverse)
library(dplyr)

setwd("C:\\Users\\61967\\Desktop\\GBD\\China\\表")
getwd()

data <- read.csv('EAPC.csv', header = TRUE)

EAPC <- data %>%
  filter(age == 'Age-standardized') %>%
  filter(metric == 'Rate') %>%
  filter(measure == 'DALYs (Disability-Adjusted Life Years)') %>%
  select(cause, year, val)

head(EAPC)

a <- EAPC %>% filter(cause == 'All causes')
head(a)

a$y <- log(a$val)
a <- a %>% filter(!is.na(y) & !is.nan(y) & is.finite(y))
head(a$y)

mod_simp_reg <- lm(y ~ year, data = a)

summary(mod_simp_reg)

summary(mod_simp_reg)[["coefficients"]]

summary(mod_simp_reg)[["coefficients"]][2, 1] ## 斜率

summary(mod_simp_reg)[["coefficients"]][2, 2] ## 斜率的标准误

(exp(summary(mod_simp_reg)[["coefficients"]][2, 1]) - 1) * 100

## 可信区间 mean +- 1.96 * se
(exp(summary(mod_simp_reg)[["coefficients"]][2, 1] -
       1.96 * summary(mod_simp_reg)[["coefficients"]][2, 2]) - 1) * 100

(exp(summary(mod_simp_reg)[["coefficients"]][2, 1] +
       1.96 * summary(mod_simp_reg)[["coefficients"]][2, 2]) - 1) * 100

EAPC <- data %>%
  filter(age == 'Age-standardized') %>%
  filter(metric == 'Rate') %>%
  filter(measure == 'DALYs (Disability-Adjusted Life Years)') %>%
  select(cause, year, val)

EAPC_cal <- data.frame(
  cause = unique(EAPC$cause),
  EAPC = rep(0, times = length(unique(EAPC$cause))),
  LCI = rep(0, times = length(unique(EAPC$cause))),
  UCI = rep(0, times = length(unique(EAPC$cause)))
)

for (i in 1:length(unique(EAPC$cause))) {
  cause_cal <- as.character(EAPC_cal[i, 1])
  a <- subset(EAPC, cause == cause_cal)
  a$y <- log(a$val)
  a <- a %>% filter(!is.na(y) & !is.nan(y) & is.finite(y))
  
  if (nrow(a) > 1) {  # 确保有足够的数据点进行回归分析
    mod_simp_reg <- lm(y ~ year, data = a)
    estimate <- (exp(summary(mod_simp_reg)[["coefficients"]][2, 1]) - 1) * 100
    low <- (exp(summary(mod_simp_reg)[["coefficients"]][2, 1] -
                  1.96 * summary(mod_simp_reg)[["coefficients"]][2, 2]) - 1) * 100
    high <- (exp(summary(mod_simp_reg)[["coefficients"]][2, 1] +
                   1.96 * summary(mod_simp_reg)[["coefficients"]][2, 2]) - 1) * 100
    EAPC_cal[i, 2] <- estimate
    EAPC_cal[i, 3] <- low
    EAPC_cal[i, 4] <- high
  } else {
    EAPC_cal[i, 2:4] <- NA  # 如果数据不足，填入NA
  }
}

EAPC_cal <- EAPC_cal %>%
  mutate(EAPC = round(EAPC, 2),
         LCI = round(LCI, 2),
         UCI = round(UCI, 2))

EAPC_cal <- EAPC_cal %>%
  mutate(EAPC_CI = paste(EAPC, LCI, sep = '\n(')) %>%
  mutate(EAPC_CI = paste(EAPC_CI, UCI, sep = ' to ')) %>%
  mutate(EAPC_CI = paste0(EAPC_CI, ')'))

head(EAPC_cal)

