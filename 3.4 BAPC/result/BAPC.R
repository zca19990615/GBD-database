library(reshape2)
library(data.table)
library(tidyverse)
library(dplyr)
library(Epi)
library(caTools)
library(fanplot)
library(colorspace)
library(BAPC)
library(Matrix)
library(foreach)
library(parallel)
library(INLA)
library(tidyr)

lung2021 <- read.csv("C:\\Users\\61967\\Desktop\\GBD\\China\\BAPC预测\\WPP2022_Population\\EC_predict.csv")
unique(lung2021$age)
ages <- c("25-29 years","30-34 years", "35-39 years", "40-44 years", "45-49 years", "50-54 years", "55-59 years",        
          "60-64 years", "65-69 years", "70-74 years", "75-79 years", "80-84 years", "85-89 years", 
          "90-94 years", "95+ years") 
lung2021<-lung2021 %>%  
  filter(age %in% ages &
           sex == 'Male' &
           metric == 'Number' &
           measure == 'DALYs (Disability-Adjusted Life Years)') %>% 
  select("age", "year", "val")  

lung2021_n<-dcast(data=lung2021,age + age ~ year) 
lung2021_n <- reshape2::dcast(data = lung2021, age + age ~ year, value.var = "val")
rownames(lung2021_n)<-c("25-29", "30-34", 
                        "35-39", "40-44", "45-49", "50-54", 
                        "55-59", "60-64", "65-69", "70-74", 
                        "75-79", "80-84", "85-89", "90-94","95+")  

##lung2021_n["0-14",] <- 0
lung2021_n<- lung2021_n[order(lung2021_n$age),]

#2019-2042???˿?????????
population <- fread('C:\\Users\\61967\\Desktop\\GBD\\China\\BAPC预测\\WPP2022_Population\\WPP2022_Population（改）.csv')
china_population <- population[Location == 'China',]
unique(china_population$AgeGrp)
china_population_1990_2021 <- china_population[Time %in% 1990:2050,
                                               .(Age = 1:15, AgeGrp, Time, PopMale = PopMale*1000)]
china_population_1990_2021_n <- dcast(data = china_population_1990_2021, Age +  AgeGrp ~ Time)
china_population_1990_2021_n <- dcast(data = china_population_1990_2021, Age +  AgeGrp ~ Time, value.var = "PopMale")

##china_population_1990_2021_n[15, 3:43] <- china_population_1990_2021_n[20, 3:43] + china_population_1990_2021_n[21, 3:43]

##china_population_1990_2021_n[1, 3:43] <- china_population_1990_2021_n[1, 3:43] +
## china_population_1990_2021_n[2, 3:43] + china_population_1990_2021_n[3, 3:43]

##china_population_1990_2021_n <- china_population_1990_2021_n[-c(2,3,20),]
rownames(china_population_1990_2021_n) <- c( "25-29", "30-34", 
                                             "35-39", "40-44", "45-49", "50-54", 
                                             "55-59", "60-64", "65-69", "70-74", 
                                             "75-79", "80-84", "85-89", "90-94","95+")


#??׼?˿?????
age_stand <- fread('C:\\Users\\61967\\Desktop\\GBD\\China\\BAPC预测\\WPP2022_Population\\age_stand.csv')
##wstand <- c(age_stand$`WHO World Standard (%)`[1:3] %>% as.numeric() %>% sum(), 
##  age_stand$`WHO World Standard (%)`[4:19] %>% as.numeric(),
##age_stand$`WHO World Standard (%)`[20:21] %>% as.numeric() %>% sum() - 0.035)/100



# 将第 6 到 20 个年龄组的比例转换为数值类型
wstand <- age_stand$`WHO World Standard (%)`[6:20] %>% as.numeric()

# 将最后一个元素减去 0.035
###wstand[length(wstand)] <- wstand[length(wstand)] - 0.035


sum(wstand)
print(wstand)












#BAPCԤ??
#?˿?????????
china_ay <- t(china_population_1990_2021_n ) %>% as.data.frame()
china_ay <- china_ay[-c(1,2),]
china_ay <- apply(china_ay, c(1,2), as.integer) %>% as.data.frame() 
colnames(china_ay) <-  c("25-29", "30-34", 
                         "35-39", "40-44", "45-49", "50-54", 
                         "55-59", "60-64", "65-69", "70-74", 
                         "75-79", "80-84", "85-89", "90-94","95+") 

#????????????
lung_ay <- t(lung2021_n) %>% as.data.frame()
lung_ay <- lung_ay[-c(1,2),]
lung_ay <- apply(lung_ay, c(1,2), as.integer) %>% as.data.frame()


#????û?????????ݵ?????
lung_pro <- matrix(data = NA, nrow = 29, ncol = 15) %>% as.data.frame() 
rownames(lung_pro ) <- seq(2022,2050,1)
colnames(lung_pro ) <-  c( "25-29", "30-34", 
                           "35-39", "40-44", "45-49", "50-54", 
                           "55-59", "60-64", "65-69", "70-74", 
                           "75-79", "80-84", "85-89", "90-94","95+")
lung_ay<- rbind(lung_ay, lung_pro) 





#??ģԤ??
lung_APCL <- APCList(lung_ay,china_ay,gf = 5)
require(INLA)
bapc_result <- BAPC(lung_APCL, predict = list(npredict = 29, retro = T),
                    secondDiff =T, stdweight =wstand, verbose = TRUE)



plotBAPC(bapc_result, scale=10^5, type = 'ageStdRate',showdata = T,
         col.fan =terrain.colors)

plotBAPC(bapc_result, scale=10^5, type = 'ageStdRate',showdata = T)






# 检查 agestd.proj 插槽的结构
str(slot(bapc_result, "agestd.proj"))

# 提取预测结果
predictions <- as.data.frame(slot(bapc_result, "agestd.proj"))

# 设置列名
colnames(predictions) <- c("PredictedDeaths", "sd")
predictions$Year <- as.numeric(sub("X", "", rownames(predictions)))

# 打印预测结果以确认
print(predictions)

# 将预测结果转换为长格式以便绘图
predictions_long <- melt(predictions, id.vars = "Year", variable.name = "Type", value.name = "Value")

# 可视化预测结果
ggplot(predictions_long, aes(x = Year, y = Value, color = Type)) +
  geom_line() +
  labs(title = "Predicted Deaths by Age Group (2022-2050)", x = "Year", y = "Predicted Deaths") +
  theme_minimal() +
  theme(legend.position = "bottom")





# 设置列名
colnames(predictions) <- c("PredictedDeaths", "sd")
predictions$Year <- as.numeric(sub("X", "", rownames(predictions)))

# 计算置信区间
predictions$LowerCI <- predictions$PredictedDeaths - 1.96 * predictions$sd
predictions$UpperCI <- predictions$PredictedDeaths + 1.96 * predictions$sd

# 保存预测结果到 CSV 文件
write.csv(predictions, "predictions.csv", row.names = FALSE)

# 打印预测结果以确认
print(predictions)




# 保存预测结果到指定文件夹
output_path <- "C:\\Users\\61967\\Desktop\\GBD\\China\\BAPC预测\\WPP2022_Population\\predictions male.csv"
write.csv(predictions, output_path, row.names = FALSE)




























#??ȡ???ݲ?????
#δ?껯??????
age_rate <- agespec.rate(x = bapc_result) %>% as.data.frame()
age_rate_mean <- age_rate[,colnames(age_rate) %like% 'mean']
age_rate_mean $year <- rownames(age_rate_mean )
colnames(age_rate_mean) <-  c( "25-29", "30-34", 
                               "35-39", "40-44", "45-49", "50-54", 
                               "55-59", "60-64", "65-69", "70-74", 
                               "75-79", "80-84", "85-89", "90-94","95+","year")

agerate<-age_rate_mean %>% 
  pivot_longer(cols = !year, 
               names_to = "age",
               values_to = "rate")



#????ÿ????????????
sum_year <- apply(age_proj_mean, 1, sum) %>% as.data.frame()
colnames(sum_year) <- 'number'
sum_year$year <- rownames(sum_year)
