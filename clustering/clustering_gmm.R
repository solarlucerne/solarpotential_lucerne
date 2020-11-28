library(tidyverse)
library(mclust)


# Read data:
data <- read.csv("Data/buildings.csv", header = TRUE, sep = ",", encoding = "UTF-8")


# Clustering with features "TD_FLAECHE" AND "PV_ERTRAG"

# Choose columns used for clustering and subset:
columns <- c("TD_FLAECHE", "PV_ERTRAG", "DACHART", 
             "Gebäudekategorie", "Bauperiode", "X", "Y")

data.clustering <- data[columns]

# Normalize feature columns for "TD_FLAECHE" AND "PV_ERTRAG"
data.normalized <- data.clustering %>% mutate_each_(list(~scale(.) %>% as.vector), 
                                         vars = c("TD_FLAECHE"))
data.normalized <- data.clustering %>% mutate_each_(list(~scale(.) %>% as.vector), 
                                         vars = c("PV_ERTRAG"))

# Replace NAs with 0
data.normalized[is.na(data.normalized)] <- 0

# Fitting:
fit <- Mclust(data.normalized)

# Inspect the fit:
summary(fit)


# Plot information about the fit (take long to calculate and render!):

# 1. Plot density of the fit, all features:
# plot(fit, what = "density")

# 2. Plot the classification based on the features
# plot(fit, what = "classification")


# Inspect and plot the fit's BIC:
fit$BIC
summary(fit$BIC)
plot(fit, what = "BIC")


# Exctract the dimensions and add to the data fitted:
classifications <- data.normalized
classifications["Cluster"] <- fit$classification


# Plot the fit and the clusters:
ggplot(classifications,
       aes(x = X,
           y = Y,
           color = factor(Cluster))) +
  geom_point() +
  theme(axis.title.x = element_blank(),
        axis.text.x = element_blank(),
        axis.ticks.x = element_blank(),
        axis.title.y = element_blank(),
        axis.text.y = element_blank(),
        axis.ticks.y = element_blank()) +
  labs(title = "Clustering based on GMM")
