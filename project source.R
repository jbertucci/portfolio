library(arules)
library(rtweet)
library(twitteR)
library(ROAuth)
library(jsonlite)
library(streamR)
library(rjson)
library(tokenizers)
library(tidyverse)
library(plyr)
library(dplyr)
library(ggplot2)
library(syuzhet) #sentiment analysis package
library(stringr)
library(arulesViz)
library(tidytext)

library(magrittr)
library(rpart)
library(rattle)
library(rpart.plot)
library(RColorBrewer)
library(Cairo)
library(forcats)
library(dplyr)
library(e1071)
library(mlr)
library(caret)
library(naivebayes)
library(randomForest)

#loading data already cleaned by Antonio

ubercurpus<-read.csv("~//IST//707//Project//ubercurpus.csv", sep="")

#putting tweets into their own vector
tweets<-as.vector(ubercurpus$text)

sum(is.na(tweets))
#no na values

#getting emotional sentiment
tweet.emotion<-get_nrc_sentiment(as.vector(tweets))

length(which(tweet.emotion$positive > 0))

length(which(tweet.emotion$negative > 0))

#about half and half positive and negative.

#getting full sentiment values for each tweet using syuzhet

tweet.sent.value<-get_sentiment(as.vector(tweets))
most.positive<-tweets[tweet.sent.value == max(tweet.sent.value)]
most.positive
most.negative<-tweets[tweet.sent.value <= min(tweet.sent.value)]
most.negative

Sentimenttweets<-data.frame(tweets, tweet.sent.value)

Sentimenttweets$label<-0

Sentimenttweets$label[which(Sentimenttweets$tweet.sent.value>0)]<-1

Sentimenttweets$label[which(Sentimenttweets$tweet.sent.value<0)]<--1

uberdtm<-DocumentTermMatrix(ubercurpus)

Tokens<-tokenize_words(as.character(Sentimenttweets[,1]))

setwd("C:\\Users\\user\\Documents\\IST\\707\\Project\\Corpus")

ubercorpus<-Corpus(VectorSource(Sentimenttweets$tweets))

ntweets<-nrow(Sentimenttweets)

# ignore extremely rare words i.e. terms that appear in less then 1% of the documents
(minTermFreq <- ntweets * 0.0001)
# ignore overly common words i.e. terms that appear in more than 50% of the documents
(maxTermFreq <- ntweets * 1)

uberdtm<-DocumentTermMatrix(ubercorpus, control = list(bounds = list(global = c(minTermFreq, maxTermFreq))))
inspect(uberdtm)

uberdtm[-c(1:11), ]

inspect(uberdtm)

uberdf<-tidy(uberdtm)

head(uberdf)

(WordFreq <- colSums(as.matrix(uberdtm)))
ord <- order(WordFreq)
WordFreq[tail(ord)]
(Row_Sum_Per_doc <- rowSums((as.matrix(uberdtm))))

n<-nrow(as.matrix(uberdtm))

cut.point<-floor(n*.66)

train <- uberdtm[c(1:cut.point), ]
test <-uberdtm[c(6569:n),]

trainlabel<-Sentimenttweets$label[c(1:cut.point)]
testlabel<-Sentimenttweets$label[c(6569:n)]

traindf<-data.frame(trainlabel, as.matrix(train))

traindf$trainlabel<-as.factor(traindf$trainlabel)

testdf<-data.frame(as.matrix(test))

barplot(summary(traindf$trainlabel))
testlabel<-as.factor(testlabel)
barplot(summary(testlabel))

#naive bayes now that the data is sorted out

nbmodel1<-naiveBayes(trainlabel~., data=traindf)
nbprediction1<-predict(nbmodel1, testdf)
table(nbprediction1, testlabel)

#creating a decision tree
dtmodel1<-rpart(trainlabel~., data = traindf, method = "class")
dtprediction<-predict(dtmodel1, testdf, type = "class")

table(dtprediction, testlabel)

fancyRpartPlot(dtmodel1)

#running an SVM model
svmmodel1<-svm(trainlabel~., data=traindf, kernel = "polynomial", Cost = 10000)
svmprediction<-predict(svmmodel1, testdf)

table(svmprediction, testlabel)

#creating a randomforest model

rfmodel1<-randomForest(trainlabel~., data=traindf, trees=10)
rfprediction<-predict(rfmodel1, testdf)

table(rfprediction, testlabels)
