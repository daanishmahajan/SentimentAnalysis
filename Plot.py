import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime,timedelta
import scipy.stats as stats
import numpy as np

file="/home/daanish/Desktop/Project/MachineLearning/Twitter/Testfiles/outf01.csv"
column_names=["SNo","Time","Location","Text","Label"]
timespan=1

class Plot:
    def __init__(self):
        df=pd.read_csv(file,names=column_names,header=None)
        df["Label"].replace("",np.nan,inplace=True)
        df.dropna(subset=["Label"],inplace=True)
        # print(df.head())
        # return
        self.draw_bar_time_label(df)
        self.draw_scatter_regressionline(df["Time"])

    def draw_bar_time_label(self,df):
        dates={}
        # df["Label"].astype("int64")
        for i in range(len(df["Time"])):
            datetime_obj=datetime.strptime(df["Time"][i],"%Y-%m-%d %H:%M:%S")
            label=df["Label"][i]
            date="{0}-{1}-{2}".format(datetime_obj.strftime("%Y"),datetime_obj.strftime("%m"),datetime_obj.strftime("%d"))
            if date in dates.keys():
                # print(date)
                if label in dates[date].keys():
                    dates[date][label]+=1
                else:
                    dates[date][label]=1
            else:
                dates[date]={label:1}
                # print(dates[date])

        date=[]
        x=[i for i in range(1,len(dates)+1)]
        y=[]
        for i in range(3):
            y.append([])
        ymax=0
        width=0.2
        for key in dates.keys():
            date.append(key)
            for i in range(3):
                if i in dates[key].keys():
                    y[i].append(dates[key][i])
                    ymax=max(ymax,dates[key][i])
                else:
                    y[i].append(0)

        # print(x)
        # return
        ax=plt.subplot(111)
        bar1=ax.bar(np.array(x)-width,y[0],width,color="r")
        bar2=ax.bar(np.array(x),y[1],width,color="g")
        bar3=ax.bar(np.array(x)+width,y[2],width,color="b")

        ax.set_xticks(x)
        ax.set_xticklabels(date,rotation=90)
        ax.legend((bar1[0],bar2[0],bar3[0]),("Negative","Neutral","Positive"))#colour

        ax.set_ylabel("Sentiment Frequency")
        ax.set_xlabel("Date")
        plt.title("Sentiment Scores for Different Days")
        plt.axis([0,x[len(x)-1]+5,0,ymax+50])
        plt.show()
        return

    def draw_scatter_regressionline(self,df,deg=10):
        y=[]
        obj1=datetime.strptime(df[0],"%Y-%m-%d %H:%M:%S")
        cnt=0
        for i in range(len(df)):
            obj0=datetime.strptime(df[i],"%Y-%m-%d %H:%M:%S")
            hours=self.get_hour(obj0,obj1)
            if(hours<=timespan):
                cnt+=1
            else:
                y.append(cnt)
                obj1,N=self.get_new(obj0,obj1)
                for j in range(N):
                    y.append(0)
                cnt=1
        y.append(cnt)
        print("Starting Time: ",df[0],"\nTweet Count: ",y)
        x=[i for i in range(1,len(y)+1)]

        plt.scatter(x,y)
        
        coeff=np.polyfit(x,y,deg=deg)
        print("Coefficients of regression curve: ",coeff)

        y=[]
        length=len(x)
        x=np.arange(1.0,length+0.5,0.1)
        ymax=0.0
        for i in range(0,len(x)):
            val=0
            length=len(coeff)
            xv=1
            for j in range(length):
                val+=xv*coeff[length-j-1]
                xv*=x[i]
            # print(val)
            ymax=max(val,ymax)
            y.append(val)

        plt.plot(x,y)

        pearson=stats.pearsonr(x,y)#r,p-value
        print("Pearson Correlation: ",pearson)
        spearman=stats.spearmanr(x,y)
        print("Spearman Correlation: ",spearman)
        kendall=stats.kendalltau(x,y)
        print("kendalltau Correlation: ",kendall)
        # plt.text(1,1,(pearson)+"\n"+spearman+"\n"+kendall,horizontalalignment="center",
        #     verticalalignment="center",transform="ax.transAxes")

        plt.xlabel("Timespan")
        plt.ylabel("Count of Tweets for every {0} hour interval".format(timespan))
        plt.title("Activity v/s Time")
        plt.axis([0,x[len(x)-1]+10,0,ymax+50])
        plt.show()
    
    def get_new(self,dt0,dt1):
        cnt=0
        while self.get_hour(dt0,dt1)>timespan:
            # dt1=dt1-datetime.strptime("2018-12-{0} {1}:0:0".format(dt1.strftime("%d"),timespan),"%Y-%m-%d %H:%M:%S")
            dt1=dt1-timedelta(hours=1)
            cnt+=1
        return dt1,cnt-1

    def get_hour(self,dt0,dt1):
        diff=dt1-dt0
        return diff.days*24+diff.seconds/3600.0

plot=Plot()


