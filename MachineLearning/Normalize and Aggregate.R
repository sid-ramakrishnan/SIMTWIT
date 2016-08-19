rm(list = ls(all = T))


path = "/home/shravan/Downloads/real_features.csv"

dataread = read.table(path,header = T,sep = ",")

nocols = length(dataread)
norows = length(dataread[,1])

for(x in 1 : norows)
{
  sum = sum(as.numeric(dataread[x,2:nocols]))
  if(sum > 0)
  {
    dataread[x,2:nocols] = dataread[x,2:nocols]/sum
  }
}
listofusers = unique(as.character(dataread[,1]))

dataread2 = data.frame()

for(x in 1 : length(listofusers))
{
  dataread2[x,1] = listofusers[x]
  subset = dataread[dataread[,1] == listofusers[x],]
  nousers = length(dataread[,1])
  for(y in 2 : nocols)
  {
   dataread2[x,y] = mean(subset[,y])
  }
}
colnames(dataread2) = colnames(dataread)

write.table(dataread2,file = "~/Desktop/NormalizedMatrix.csv",sep=",",row.names =F,col.names = T,append = F)

