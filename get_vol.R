# 计算日波动率
# author: 屠心怡

library(fGarch)
library(quantmod)
data <- read.csv("D:/desktop/data.csv", header = TRUE)
dim(data)
names(data)
detach(package:quantmod)


bank<-data.frame(data[,'bank'])
defense<-data.frame(data[,'defense'])
food<-data.frame(data[,'food'])


# (5) 建立GARCH类模型
#GARCH.model_1 <- garchFit(~garch(1,1), data=bank, trace=FALSE)                    # GARCH(1,1)-N模型
#GARCH.model_2 <- garchFit(~garch(2,1), data=bank, trace=FALSE)                    # GARCH(1,2)-N模型


#GARCH.model_3 <- garchFit(~garch(1,1), data=bank, cond.dist='std', trace=FALSE)   # GARCH(1,1)-t模型
#GARCH.model_4 <- garchFit(~garch(1,1), data=bank, cond.dist='sstd', trace=FALSE)  # GARCH(1,1)-st模型
#GARCH.model_5 <- garchFit(~garch(1,1), data=bank, cond.dist='ged', trace=FALSE)   # GARCH(1,1)-GED模型
#GARCH.model_6 <- garchFit(~garch(1,1), data=bank, cond.dist='sged', trace=FALSE)  # GARCH(1,1)-SGED模型


#GARCH.model_3 <- garchFit(~garch(1,1), data=defense, cond.dist='std', trace=FALSE)   # GARCH(1,1)-t模型
#GARCH.model_4 <- garchFit(~garch(1,1), data=defense, cond.dist='sstd', trace=FALSE)  # GARCH(1,1)-st模型
#GARCH.model_5 <- garchFit(~garch(1,1), data=defense, cond.dist='ged', trace=FALSE)   # GARCH(1,1)-GED模型
#GARCH.model_6 <- garchFit(~garch(1,1), data=defense, cond.dist='sged', trace=FALSE)  # GARCH(1,1)-SGED模型


GARCH.model_3 <- garchFit(~garch(1,1), data=food, cond.dist='std', trace=FALSE)   # GARCH(1,1)-t模型
GARCH.model_4 <- garchFit(~garch(1,1), data=food, cond.dist='sstd', trace=FALSE)  # GARCH(1,1)-st模型
GARCH.model_5 <- garchFit(~garch(1,1), data=food, cond.dist='ged', trace=FALSE)   # GARCH(1,1)-GED模型
GARCH.model_6 <- garchFit(~garch(1,1), data=food, cond.dist='sged', trace=FALSE)  # GARCH(1,1)-SGED模型


#summary(GARCH.model_1)


#plot(GARCH.model_1)


# (6) 提取GARCH类模型信息


#vol_1 <- fBasics::volatility(GARCH.model_1)
#vol_2 <- fBasics::volatility(GARCH.model_2)
vol_3 <- fBasics::volatility(GARCH.model_3)
vol_4 <- fBasics::volatility(GARCH.model_4)
vol_5 <- fBasics::volatility(GARCH.model_5)
vol_6 <- fBasics::volatility(GARCH.model_6)


# 提取GARCH(1,1)-N模型得到的波动率估计
#sres_1 <- residuals(GARCH.model_1, standardize=TRUE)          # 提取GARCH(1,1)-N模型得到的标准化残差
#vol_1.ts <- ts(vol_1, frequency=12, start=c(1990, 1))
#sres_1.ts <- ts(sres_1, frequency=12, start=c(1990, 1))
#par(mfcol=c(2,1))
#plot(vol_1.ts, xlab='年', ylab='波动率')
#plot(sres_1.ts, xlab='年', ylab='标准化残差')
write.table(vol_3,"D:/desktop/vol_ten.csv",row.names=TRUE,col.names=TRUE,sep=",")
write.table(vol_4,"D:/desktop/vol_ten2.csv",row.names=TRUE,col.names=TRUE,sep=",")
write.table(vol_5,"D:/desktop/vol_ten3.csv",row.names=TRUE,col.names=TRUE,sep=",")
write.table(vol_6,"D:/desktop/vol_ten4.csv",row.names=TRUE,col.names=TRUE,
