from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import tkinter
from PIL import  Image, ImageTk
from calendar import Calendar 
from tkcalendar import Calendar, DateEntry
from tkinter.scrolledtext import ScrolledText
import mysql.connector
import PySimpleGUI as sg
sg.__version__
'4.60.1'
import score 
import subprocess
import os
import datetime
import sys

MYSQL_USER = 'root'
MYSQL_HOST = '127.0.0.1'
MYSQL_DATABASE = 'yuta'
SQL_SELECT_ALL ="SELECT  baseball.id,ymd,team1,team2,score1,score2 FROM baseball"
SQL_SELECT_WHERE= SQL_SELECT_ALL + " WHERE id =%s "
SQL_SELECT_WHERE2= SQL_SELECT_ALL + " WHERE ymd =%s "
SQL_SELECT_WHERE3= SQL_SELECT_ALL + " WHERE team1 =%s"
SQL_SELECT_WHERE4= SQL_SELECT_ALL + " WHERE team2 =%s"
SQL_SELECT_WHERE5= SQL_SELECT_ALL +"WHERE team1 =%s AND team2 =%s"
        


class Message_ExitView(tk.Frame):
    def __init__(self,root):     
              
        super().__init__(root)
        self.root = root
        self.root.title("閲覧メニュー:TOP")
        self.root.geometry("800x800")
        # フレームの作成
        self.Frame_main = tk.Frame(self.root, bg="#b0c4de")
        self.Frame_main.place(x=0, y=0, width=800, height=800)
        
        
        #入力値を保持
        self.select_kbn = tk.StringVar()
        self.select_id = tk.StringVar()
        self.select_ymd = tk.StringVar()
        self.select_team1= tk.StringVar()
        self.select_team2 = tk.StringVar()
        
        
        # 検索フォーム
        self.tx_String_search_data = tk.Entry(self.Frame_main,textvariable=self.select_id)
        self.tx_String_search_data.place(x=300, y=160)
        self.tx_String_search_data2= tk.Entry(self.Frame_main, textvariable=self.select_ymd)
        self.tx_String_search_data2.place(x=300, y=190)
        self.tx_String_search_data3 = tk.Entry(self.Frame_main, textvariable=self.select_team1)
        self.tx_String_search_data3.place(x=300, y=220)
        self.tx_String_search_data4 = tk.Entry(self.Frame_main, textvariable=self.select_team2)
        self.tx_String_search_data4.place(x=300, y=250)
        # 表の作成
        self.tree=ttk.Treeview(self.Frame_main,selectmode="browse")
        self.tree.place(x=150,y=300,width=500,height=300)
        self.tree.bind("<<TreeviewSelect>>", self.select_record)
        # self.back=self.tree.bind("<<TreeviewSelect>>", self.select_record)
        self.tree["columns"]=(1,2,3,4,5,6)
        self.tree["show"] = "headings"
        self.tree.column(1,width=40)
        self.tree.column(2,width=100)
        self. tree.column(3,width=100)
        self.tree.column(4,width=30)
        self.tree.column(5,width=30)
        self. tree.column(6,width=100)
        self.tree.heading(1,text="id")
        self.tree.heading(2,text="日付")
        self.tree.heading(3,text="先攻")
        self.tree.heading(4,text="得点")
        self.tree.heading(5,text="得点")
        self.tree.heading(6,text="後攻")
        
        style = ttk.Style()
        # TreeViewの全部に対して、フォントサイズの変更
        style.configure("Treeview",font=("",12))
        # TreeViewのHeading部分に対して、フォントサイズの変更と太字の設定
        style.configure("Treeview.Heading",font=("",14,"bold"))
        
        # sqlと接続
        DB = mysql.connector.connect(host='127.0.0.1',user='root',database='yuta')
        cur = DB.cursor()
        sql="SELECT baseball.id,ymd,team1,team2,score1,score2 from baseball"
       
        cur.execute(sql)
        results = cur.fetchall()  
        # cur.fetchall()を使用してクエリの結果を取得
        for dt in results:
            # print(dt)
            self.tree.insert("","end",iid=dt[0],values=(dt[0],dt[1],dt[2],dt[4],dt[5],dt[3],))
            
    
                
            
         # 記録ボタン    
        self.report = tk.Button(self.Frame_main,text="スコアを記録する",bg="#FFFFFF",command=self.execute_py)
        self.report.place(x=10,y=20)
        self.report.bind("<Return>",self.execute_py )    
        
        #検索ボタン
        self.btn_search_all = tk.Button(self.Frame_main, text="検索", bg="#FFFFFF",command=self.btn_select_click)
        self.btn_search_all.place(x=450, y=160)
        #検索(All)ボタン
        self.btn_search_all2 = tk.Button(self.Frame_main, text="全て記録を表示する", bg="#FFFFFF",command=lambda:self.btn_All_click(1))
        self.btn_search_all2.place(x=500, y=160)
        self.btn_search_all2.bind("<Return>",self.btn_All_click)
        
        
        lbl =tk.Label(self.Frame_main,text="id",bg="#b0c4de").place(x=225,y=160)
        lbl =tk.Label(self.Frame_main,text=" 日付",bg="#b0c4de").place(x=215,y=190)
        lbl =tk.Label(self.Frame_main,text="チーム名 先攻",bg="#b0c4de").place(x=200,y=220)
        lbl =tk.Label(self.Frame_main,text="チーム名 後攻",bg="#b0c4de").place(x=200,y=250)
       #検索(All)ボタン処理           
    def btn_All_click(self,event):
        #データベース接続
           
           self.tree.delete(*self.tree.get_children())
           DB = mysql.connector.connect(host='127.0.0.1',user='root',database='yuta')
           cur = DB.cursor()
           sql="SELECT baseball.id,ymd,team1,team2,score1,score2 from baseball"
           print("3")
           cur.execute(sql)
           results = cur.fetchall()  
        # cur.fetchall()を使用してクエリの結果を取得
           for dt in results:
            # print(dt)
            self.tree.insert("","end",iid=dt[0],values=(dt[0],dt[1],dt[2],dt[4],dt[5],dt[3]))
            
        
    def connector_mysql(self):
    # 接続情報の初期化
        

        try:
        # mysqlに接続
            DB = mysql.connector.connect(
            user=MYSQL_USER
            ,  host=MYSQL_HOST
            , database=MYSQL_DATABASE)
        
        except Exception as e:
        # 例外エラーはコンソールへ出力
             print(e)
             return None
        return DB
    
    def select_table(self,):
        
    # 検索結果初期化
        rows = None
        # Mysql接続処理
        connector = self.connector_mysql()
        # Mysql接続失敗処理
        if connector is None:
           messagebox.showinfo("DB接続エラー", "データベース接続に失敗しました。")
           return
    
        try:
        # カーソル作成：出力形式は辞書型
            cursor = connector.cursor()
        
        # プルダウン[ID]：WHERE句つきで検索
            if self.tx_String_search_data.get():
                 
            # 入力値を取得
                 param = self.select_id.get()
                 self.select_id.set('')
            # select 実行
                 cursor.execute(SQL_SELECT_WHERE,(param,))
        
            elif self.tx_String_search_data2.get():
              
            # 入力値を取得
                 param5 = self.select_ymd.get()
                 self.select_ymd.set('')
            # select 実行
                 cursor.execute(SQL_SELECT_WHERE2,(param5,))       
               
            elif self.tx_String_search_data3.get():
                  param1 = str(self.select_team1.get()) 
                  self.select_team1.set('')
                  cursor.execute(SQL_SELECT_WHERE3,(param1,))
                  
            elif self.tx_String_search_data4.get():
                 param2 = str(self.select_team2.get())
                 self.select_team2.set('')
                # select 実行
                 cursor.execute(SQL_SELECT_WHERE4,(param2,)) 
                 
            elif self.tx_String_search_data3.get() and  self.tx_String_search_data4.get():
                param3=   str(self.select_team1.get())   
                param4 =str(self.select_team2.get()) 
                self.select_team1.set('')
                self.select_team2.set('')
                cursor.execute(SQL_SELECT_WHERE5,(param3,param4))        
        # 全件取得
            rows = cursor.fetchall()  

        # カーソルクローズ
            cursor.close
    
        except Exception as e:
        # 例外エラーはコンソールへ出力
              print(e)
    
        finally:
           return rows
       
    def btn_select_click(self):
    # treeviwの初期化
        self.tree.delete(*self.tree.get_children())

    # Mysql接続処理
        connector = self.connector_mysql()
    
    # Mysql接続失敗処理
        if connector == None:
           messagebox.showinfo("DB接続エラー", "データベース接続に失敗しました。")
              
           return
    
    # 検索処理
        row_data = self.select_table()
    
    # 検索失敗処理    
        if row_data == None:
            messagebox.showinfo("検索エラー", "SELECTに失敗しました。")
            DB = mysql.connector.connect(host='127.0.0.1',user='root',database='yuta')
            cur = DB.cursor()
            sql="SELECT baseball.id,ymd,team1,team2,score1,score2 from baseball"
            print("3")
            cur.execute(sql)
            results = cur.fetchall()  
        # cur.fetchall()を使用してクエリの結果を取得
            for dt in results:
            # print(dt)
             self.tree.insert("","end",iid=dt[0],values=(dt[0],dt[1],dt[2],dt[4],dt[5],dt[3]))
            return

    # 検索結果出力
        if len(row_data) == 0:
            messagebox.showinfo("検索結果", "検索結果：0件です")
        else:
           for dt in row_data:
            self.tree.insert(
                "","end",iid=dt[0],values=(dt[0],dt[1],dt[2],dt[4],dt[5],dt[3])) 
            
            
    #treeviewbind処理        
            
                               
    #記録処理    
    def execute_py(self,):
        
        class Message_EntryView(tk.Frame):                
          def __init__(self,root):           
               super().__init__(root)
               self.root = root
        self.root.title("投稿ページ:TOP")
        self.root.geometry("800x800")
        self.itemName = ""
        self.flgs = 0 
        self.member2 = []
        
        # 記録するボタンを押したときのフレーム
        self.Frame_login = tk.Frame(self.root, bg="#cbd1d1")
        self.Frame_login.place(x=0, y=0, width=600, height=600)
        
        self.mainframe = tk.Frame(self.Frame_login, width=600,height=10,  bg="#c42f12").place(x=0,y=280)
        self.mainframe = tk.Frame(self.Frame_login,bg="#cbd1d1")
        self.mainframe.place(x=0,y=0)
        # 試合日の登録
          # カレンダーのスタイル 
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('my.DateEntry',
                        fieldbackground='white',
                        background='dark green',
                        foreground='black',
                        arrowcolor='white')

        self.ymd_entry = DateEntry(self.Frame_login,style='my.DateEntry')
        self.ymd_entry.place(x=60, y=10)
        #self.date_entry.place(x=60, y=40,width=90)

        self.datetime = tk.Label(self.Frame_login,text='試合日',foreground='#17171a',background='#FFFFFF').place(x=10, y=10)
        
        # チーム名　先行表示
        lbl =tk.Label(self.Frame_login,text="チーム名 先攻", font=("MSゴシック", "10", "bold"),foreground='#17171a',background='#FFFFFF').place(x=142,y=90)
        
        # チーム名　後攻表示
        lbl=tk.Label(self.Frame_login,text="チーム名 後攻", font=("MSゴシック", "10", "bold"),foreground='#17171a',background='#FFFFFF').place(x=402,y=90)
        
        
        # チーム名1
        self.team1_entry =tk.Entry(self.Frame_login,font=("MS ゴシック", "10", "bold"))
        self.team1_entry.place(x=110, y=110,width=150,height=28)
        
           
        # チーム名2
        self.team2_entry=tk.Entry(self.Frame_login,font=("MS ゴシック", "10", "bold"))
        self.team2_entry.place(x=370, y=110,width=150,height=28)
        
        lbl =tk.Label(self.Frame_login,text="―", font=("MSゴシック", "20", "bold"),foreground='#17171a').place(x=300,y=178)
        
        # 先攻の点数入力
        self.score1_entry=tk.Entry(self.Frame_login,font=("MSゴシック", "30", "bold"))
        self.score1_entry.place(x=140, y=170,width=80,height=60)
        
        #後攻の点数入力
        self.score2_entry=tk.Entry(self.Frame_login,font=("MSゴシック", "30", "bold"))
        self.score2_entry.place(x=410, y=170,width=80,height=60)
        
        
        # 投稿欄
        lbl = tk.Label(self.Frame_login,text='コメント欄',foreground='#17171a').place(x=5,y=290) 
        #テキストボックス（複数行）の生成
        self.text_text = ScrolledText(self.Frame_login, font=("游ゴシック", 10), height=15, width=70)
        self.text_text.place(x=40,y=320)
        
       
     # 保存ボタンの作成
        self.submit = tk.Button(self.Frame_login, command=lambda:self.btn_click(1),text="保存する",bg="#FFFFFF")
        self.submit.place(x=500,y=0)
        self.submit.bind("<Return>", self.btn_click)
        
        #  戻るボタン 
        self.change=tk.Button(self.Frame_login,command=lambda:[self.btn_change(1),self.btn_raise(1)] ,text="戻る",bg="#FFFFFF") 
        self.change.place(x=400,y=0)
        self.change.bind("<Return>",self.btn_change)
        self.change.bind("<Return>",self.btn_raise)
        
         
        # 保存ボタンの内容
    def btn_click(self,event): 
        print ('ボタン')
        
        
        if  self.score1_entry.get()==''  or self.score2_entry.get()==''or str(self.team1_entry.get())=='' or str(self.team2_entry.get())=='' : 
          messagebox.showerror('確認', 'スコア又はチーム名が入力されていません。')
          
          
        else:
           try:
                # Connect to the MySQL database
                DB = mysql.connector.connect(host='127.0.0.1',user='root',database='yuta')
                cursor = DB.cursor()
                print("2")
                
                # Get the entered score and team name
                ymd= self.ymd_entry.get_date() 
                score1 = int(self.score1_entry.get())
                score2 = int(self.score2_entry.get())
                team1 = self.team1_entry.get()
                team2 = self.team2_entry.get()
                text=self.text_text.get("1.0", "end-1c")
                
                self.score1_entry.delete(0, tk.END)
                self.score2_entry.delete(0, tk.END)
                self.team1_entry.delete(0, tk.END)
                self.team2_entry.delete(0, tk.END)
                self.text_text.delete("1.0", tk.END)
                print("3")
                # Prepare the SQL query to insert the data into the database
                insert_scores = "INSERT INTO baseball (ymd,score1, score2, team1, team2,text) VALUES (%s,%s, %s, %s, %s,%s)"
                values=(ymd,score1, score2, team1, team2,text)


                # Execute the query
                cursor.execute(insert_scores, values)
                DB.commit()

                # Close the cursor and database connection
                cursor.close()
                DB.close()

                messagebox.showinfo('確認', 'スコアとチーム名が保存されました。')
                
                
          
           except mysql.connector.Error as error:
                messagebox.showerror('エラー', 'データベースエラー: {}'.format(error))     
   
        
        
    def btn_change(self,event):
            
         self.Frame_login.destroy()
         
        
        
        
    def btn_raise(self,event):    
        #
        self.Frame_main.tkraise()  
        #記録一旦削除
        
    #treeviewbind処理    
    def select_record(self,event):     
        class Treeview_Exit(tk.Frame):
              def __init__(self,root):      
               super().__init__(root)       
               self.root = root
        self.root.title("閲覧メニュー")
        self.root.geometry("800x800")
        # フレームの作成
        self.Frame_main2 = tk.Frame(self.root, bg="#b0c4de")
        self.Frame_main2.place(x=0, y=0, width=800, height=800) 
                 
         #戻るボタン
        self.button=tk.Button(self.Frame_main2,command=lambda:[self.btn_change2(1)] ,text="戻る",bg="#FFFFFF")
        self.button.place(x=400,y=0)
        self.button.bind("<Return>",self.btn_change2)
        
        
        #treeviewからデータ取得
        self.record_id = self.tree.focus()
        self.record_values = self.tree.item(self.record_id, 'values')
        self.mainframe = tk.Frame(self.Frame_main2, width=600,height=10,  bg="#c42f12").place(x=0,y=280)
        
         #日付入力
        self.date_entry=tk.Entry(self.Frame_main2,)
        self.date_entry.place(x=60, y=40,width=90)
        self.date_entry.insert(tkinter.END,self.record_values[1])
        lbl =tk.Label(self.Frame_main2,text="―", font=("MSゴシック", "20", "bold"),foreground='#17171a',background='#FFFFFF').place(x=280,y=178)
        
        self.datetime = tk.Label(self.Frame_main2,text='試合日',foreground='#17171a',background='#FFFFFF').place(x=10, y=40)
        
        # チーム名　先行表示
        lbl =tk.Label(self.Frame_main2,text="先攻", font=("MSゴシック", "10", "bold"),foreground='#17171a',background='#FFFFFF').place(x=50,y=150)
        
        # チーム名　後攻表示
        lbl=tk.Label(self.Frame_main2,text="後攻", font=("MSゴシック", "10", "bold"),foreground='#17171a',background='#FFFFFF').place(x=490,y=150)
        
        #選考チームの得点表示
        print("self.record_values:", self.record_values)
        self.score1_label=tk.Label(self.Frame_main2,text=self.record_values[4],font=("MSゴシック", "25", "bold"),foreground='#17171a',background='#FFFFFF')
        self.score1_label.place(x=160, y=170,width=80,height=60)
        
        # 後攻チームの得点表示
        self.score2_label=tk.Label(self.Frame_main2,text=self.record_values[3],font=("MSゴシック", "25", "bold"),foreground='#17171a',background='#FFFFFF')
        self.score2_label.place(x=350, y=170,width=80,height=60)
        
        # チーム名1
        self.team1_label =tk.Label(self.Frame_main2,text=self.record_values[2],font=("MS ゴシック", "10", "bold"),foreground='#17171a',background='#FFFFFF')
        self.team1_label.place(x=10, y=190,width=120,height=28)
          
        # チーム名2
        self.team2_label=tk.Label(self.Frame_main2,text=self.record_values[5],font=("MS ゴシック", "10", "bold"),foreground='#17171a',background='#FFFFFF')
        self.team2_label.place(x=450, y=190,width=120,height=28)
        
        #テキスト
        self.text_text = tk.Message(self.Frame_main2,text="",font=("MS ゴシック", "10", "bold"),anchor=tkinter.NW,aspect=700,foreground='#17171a',background='#FFFFFF')
        self.text_text.place(x=40,y=320, height=300, width=500)
        
        
         # sqlと接続
        
        DB = mysql.connector.connect(host='127.0.0.1',user='root',database='yuta')
        cur = DB.cursor()
        sql2="SELECT baseball.text FROM baseball WHERE id= %s "
        param= self.record_values[0]
        param_tuple = (param,)
        print(param)
        cur.execute(sql2,param_tuple)
        self.text = cur.fetchall()  
        # cur.fetchall()を使用してクエリの結果を取得
        for dt in self.text:
            # print(dt)
            self.text_text["text"]=dt[0]
        
    def btn_change2(self,event):
       
        print(55) 
        self.tree.delete(*self.tree.get_children())
        DB = mysql.connector.connect(host='127.0.0.1',user='root',database='yuta')
        cur = DB.cursor()
        sql="SELECT baseball.id,ymd,team1,team2,score1,score2 from baseball"
        print("2")
        cur.execute(sql)
        results = cur.fetchall()  
          # cur.fetchall()を使用してクエリの結果を取得
        for dt in results:
            # print(dt)
            self.tree.insert("","end",iid=dt[0],values=(dt[0],dt[1],dt[2],dt[4],dt[5],dt[3]))
           
        self.Frame_main2.destroy()
        
def message_entry():
            root = tk.Tk()
            app = Message_ExitView(root)
            app.mainloop()
    
if __name__ == "__main__":
        message_entry()
        
