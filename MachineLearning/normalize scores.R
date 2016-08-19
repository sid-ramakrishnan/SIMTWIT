rm(list = ls(all = T))

dataread = read.table("/home/shravan/Downloads/sample_features.csv",header = F,sep = ",")
dataread2 = dataread
len = length(dataread)
for(x in 1 : length(dataread[,1]))
{
  
  dataread[x,] = dataread[x,] / sum(dataread[x,])
}

write.table(dataread,file = "~/Desktop/TrainNorm.csv",row.names = F,col.names = F,sep = ",",append = F)

