import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from textblob import TextBlob
predict=TextBlob
#import csv
import matplotlib.pyplot as plt
import pandas as pd
import os
import sqlite3



Ui_MainWindow, QtBaseClass = uic.loadUiType("sentiappui.ui")

class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.analyzebutton1.clicked.connect(self.Calculateanalyze1)
        self.ui.connectdb.clicked.connect(self.connecttodb)
        self.ui.search_button.clicked.connect(self.search_function)
        
        #self.news1 = pd.read_csv("original_test_data.csv")
        
        
    def Calculateanalyze1(self):
        text = str(self.ui.textsentiment.toPlainText())
        done = predict(text)
        done_string  ="✓Senti Polarity        : "+str(done.sentiment.polarity)
        #done_string2 ="✓Senti Subjectivity : "+str(done.sentiment.subjectivity)
        if done.sentiment.polarity >= 0.2:
            sentiresult='Positive'
        elif done.sentiment.polarity < 0:
            sentiresult='Negative'
        else:
            sentiresult='Neutral'
        self.ui.textresult1.setText(done_string+"\n"+sentiresult)
        
        
        #LA FONCTION POUR SUPRIMER LES NON-ASCII LETTRES!
      
    def connecttodb(self):
        conn = sqlite3.connect('database1.db')
        cursorObj = conn.cursor()
        # cursorObj.execute('CREATE TABLE users (col1 text, col2 text)')
        
        # load the data into a Pandas DataFrame
        users = pd.read_csv('original_test_data.csv', usecols=[0], names=['col1'])
        # write the data to a 'qlite table
        #users.to_sql('table1', conn, if_exists='append', index = False)
        
        ex2= []
        for row in cursorObj.execute('SELECT col1 FROM table1' ):
            # print (row)
            
            tweet= dict()
            tweet['orig'] = str(row[0])
            done3 = predict(tweet['orig'])
                    
            if done3.sentiment.polarity >= 0.2:
                tweet['Sentiment']= 'Positive'
            elif done3.sentiment.polarity < 0:
                tweet['Sentiment']= 'Negative'
            else:
                tweet['Sentiment']= 'Neutral'
                    
            # tweets.append(tweet)
            
            ex2.append(tweet['Sentiment'])
            
        
        ex3= pd.DataFrame(ex2, columns=['col2'])
        self.result = pd.concat([users, ex3], axis=1, join='inner')
        # result.to_sql('table1', conn, if_exists='append', index = False)
        
   
    def search_function(self):
        
        neg = self.result[self.result['col2'] == 'Negative']
        pos = self.result[self.result['col2']== 'Positive']
        neu = self.result[self.result['col2'] == 'Neutral']
        negative = list(neg.col1)
        positive = list(pos.col1)
        neutral = list(neu.col1)
        negative = [str(element) for element in negative]
        positive = [str(element) for element in positive]
        neutral = [str(element) for element in neutral]
        negative_join_str= " ".join(negative)
        positive_join_str= " ".join(positive)
        neutral_join_str= " ".join(neutral)
        
        text2 = str(self.ui.word_search.toPlainText())
        word_to_count=text2
        #word_to_count= 'bad'
        # number of occurrence of 'p'
        print1= 'Occurrence of '+str(word_to_count) + ' in Negative dataset :', negative_join_str.lower().count(word_to_count)
        print2= 'Occurrence of '+str(word_to_count) + ' in Positive dataset :', positive_join_str.lower().count(word_to_count)
        print3= 'Occurrence of '+str(word_to_count) + ' in Neutral dataset :', neutral_join_str.lower().count(word_to_count)
        #============================================================================================================================
        done2 = predict(word_to_count)
        done_string2  ="✓ Senti Polarity: "+str(done2.sentiment.polarity)
        if done2.sentiment.polarity >= 0.2:
            sentiresult2='Positive'
        elif done2.sentiment.polarity < 0:
            sentiresult2='Negative'
        else:
            sentiresult2='Neutral'
        
        self.ui.result_search.setText(str(print1)+"\n"+str(print2)+"\n"+str(print3)+"\n"+"\n"+done_string2+"\n"+ "✓ "+sentiresult2)
        #print(done_string2+"\n"+'\033[1m' +sentiresult2+'\033[0m')
        
        
        tt= []
        tt.append(negative_join_str.count(word_to_count))
        tt.append(positive_join_str.count(word_to_count))
        tt.append(neutral_join_str.count(word_to_count))
        
        # x-coordinates of left sides of bars
        left = [1, 2, 3]
         
        # heights of bars
        #height = [10, 24, 36, 40]
        height = tt
         
        # labels for bars
        tick_label = ['Negative', 'Positive', 'Neutral']
         
        # plotting a bar chart
        plt.bar(left, height, tick_label = tick_label, width = 0.8, color = ['red', 'green', 'yellow'])
         
        # naming the x-axis
        plt.xlabel('x - axis')
        # naming the y-axis
        plt.ylabel('y - axis')
        # plot title
        plt.title('Graph Chart of word '+str(word_to_count.upper()))
        
        

        # function to show the plot
        plt.show()
        plt.subplots_adjust(top=0.774,bottom=0.265,left=0.1,right=0.71,hspace=0.2,wspace=0.2)
        plt.savefig('myplot2')
        pixmap2 = QPixmap('myplot2')
        #self.ui.label_5.clear()
        #self.ui.label_5.setPixmap(pixmap2)

        
        #os.remove("myplot.png")

       

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

#smc4python
    
#==============================================================================