library(ggplot2)
library(dplyr)
library(readr)
library(scales)

# 读取数据
data <- read.csv("C:\\Users\\61967\\Desktop\\GBD\\China\\BAPC预测\\WPP2022_Population\\结果\\Merged_Deaths_Data.csv")

# 创建示例数据
Female_ASR <- data.frame(
  year = data$Year,
  mean = data$PredictedDeaths_Female,
  lower = data$LowerCI_Female,
  upper = data$UpperCI_Female
)
Male_ASR <- data.frame(
  year = data$Year,
  mean = data$PredictedDeaths_Male,
  lower = data$LowerCI_Male,
  upper = data$UpperCI_Male
)
Male_Aproj <- data.frame(
  year = data$Year,
  mean = data$PredictedDeaths_Male,
  lower = data$LowerCI_Male,
  upper = data$UpperCI_Male
)
Female_Aproj <- data.frame(
  year = data$Year,
  mean = data$PredictedDeaths_Female,
  lower = data$LowerCI_Female,
  upper = data$UpperCI_Female
)

# 设置性别标签
Female_ASR$sex <- 'Female'
Male_ASR$sex <- 'Male'
Male_Aproj$sex <- 'Male'
Female_Aproj$sex <- 'Female'

# 合并数据
ASR <- rbind(Female_ASR, Male_ASR)
Num <- rbind(Male_Aproj, Female_Aproj)

# 自定义Nature风格主题
theme_nature <- theme(
  panel.background = element_blank(),
  panel.grid.major = element_blank(), # 去除主要网格线
  panel.grid.minor = element_blank(), # 去除次要网格线
  axis.line = element_line(color = "black"),
  axis.ticks = element_line(color = "black"),
  axis.text.x = element_text(vjust = 1, size = 8, color = 'black'), # 保持原字体
  axis.text.y = element_text(size = 8, color = 'black'), # 保持原字体
  axis.title.y = element_text(size = 10), # 保持原字体
  axis.title.x = element_text(size = 10), # 保持原字体
  title = element_text(size = 10, hjust = 0.5), # 保持原字体
  legend.position = c(0.05, 0.95), # 将图例放在左上角
  legend.justification = c(0, 1), # 调整图例位置
  legend.background = element_blank(),
  legend.key = element_blank(),
  legend.text = element_text(size = 8), # 保持原字体
  legend.title = element_text(size = 10) # 保持原字体
)

# 绘制图表
plot <- ggplot(Num, aes(x = year, y = mean)) +
  geom_col(aes(fill = sex), position = 'dodge', width = 0.8) +
  geom_errorbar(aes(ymin = lower, ymax = upper), position = position_dodge(width = 0.8), width = 0.7, cex = 0.5) +
  labs(title = NULL, x = 'Year', y = 'Number of Death Cases') +
  theme_nature +
  geom_ribbon(data = ASR, aes(x = year, ymin = lower, ymax = upper, fill = sex), alpha = 0.4) +
  geom_line(data = ASR, aes(x = year, y = mean, color = sex), size = 1) +
  scale_x_continuous(breaks = seq(1990, 2035, by = 10)) + # 添加X轴刻度，包括2035年
  scale_y_continuous(labels = comma) + # 将Y轴刻度标签格式化为千位分隔符
  scale_fill_manual(values = c("Female" = "#E69F00", "Male" = "#56B4E9")) +
  scale_color_manual(values = c("Female" = "#E69F00", "Male" = "#56B4E9"))

# 显示图表
print(plot)

