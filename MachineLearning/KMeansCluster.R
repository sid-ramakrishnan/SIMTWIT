rm(list = ls(all = T))

path = "~/Desktop/NormalizedMatrix.csv"

k = 4

dataread = read.table(path,header = T,sep = ",")

noelements = length(dataread[,1])

nocols = length(dataread)
while(1)
{
rowsselect = sample(1:noelements,k)
centroids = dataread[rowsselect,2:nocols]  # Randomly init centroids
if(dim(unique(centroids))[1] == 4)
  break
}
#centroids = dataread[rowsselect,]  # Randomly init centroids


threshold = 0.0000001

associate = vector('numeric',noelements)

limits = 50

for(outerloop in 1 : limits)
{

for( x in 1 : length(dataread[,1]))
{
    #vector = dataread[x,(2:nocols)]
    vector = dataread[x,2:nocols]
    distindi = vector('numeric',k)
    for(z in 1 : k)
    {
      distindi[z] = norm((as.matrix(centroids[z,]) - as.matrix(vector)),"f")
    }
    associate[[x]] = match(min(distindi),distindi)
}

for(x in 1 : k)
{
  indices = which(associate %in% x)
  #vectors = dataread[indices,2:nocols]
  vectors = dataread[indices,2:nocols]
  coords = NULL
  for(y in 1 : (nocols-1))
  {
    coords = cbind(coords,mean(vectors[,y]))
  }
  centroids[x,] = coords
}

}

