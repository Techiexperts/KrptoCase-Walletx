#font-consolas,lucidas
from tkinter import *
import mysql.connector,string
from tkinter.messagebox import showinfo,showerror,askyesno
from random import randint,uniform,shuffle
import matplotlib.pyplot as plt
import webbrowser,data

##########################################################################################

#for reading the cryptocurrency info. from 'crypto' file
def file_read(svalue):
    txt_list=[]
    file=open('crypto.txt','r',encoding='utf8')
    while True:
        txt=file.readline()
        #checking if line read is search value or not
        if txt==svalue+'\n':
            #if it is search value than preparing a info list of the search value
            while txt!='\n':
                #if readline is end of file than break
                if txt=='':
                    break
                #else if it is not'----' then add to list
                elif txt[0]!='-':
                    txt_list+=[txt]
                txt=file.readline()
        elif txt=='':
            break
        else:
            continue
    file.flush()
    file.close()
    return txt_list

##########################################################################################

#for sending bitcoin
def send():
    #connection establishment and fetching sender and receiver's details
    conn=mysql.connector.connect(user='root',host='localhost',passwd='Subinsk284@',database='crypto')
    cur=conn.cursor()
    cur.execute('use crypto')

    cur.execute('select Bitcoins from userlog where EmailAddress=(%s)',(emailadd.get(),))
    avalbal=cur.fetchone()
    cur.execute('select * from userlog where BitcoinAdd=(%s)',(sendto.get(),))
    receiver=cur.fetchone()

    try:
        if receiver!=None:
            if float(eval(bitcoin.get()+'+'+transfee.get()))<=float(avalbal[0]):
                #updating sender's bitcoin balance 
                up_bal=str(eval(avalbal[0]+'-'+str(eval(bitcoin.get()+'+'+transfee.get()))))
                cur.execute('update userlog set Bitcoins=(%s) where EmailAddress=(%s)',(up_bal,emailadd.get()))

                #updating receiver's bitcoin balance
                avalbal=receiver[3]
                up_bal=str(eval(avalbal+'+'+bitcoin.get()))
                cur.execute('update userlog set Bitcoins=(%s) where BitcoinAdd=(%s)',(up_bal,sendto.get()))
                cur.execute('update userlog set BitcoinAdd=NULL where BitcoinAdd=(%s)',(sendto.get(),))
            
                conn.commit()
                cur.close()
                conn.close()

                showinfo('Payment Processed!!','Bitcoins has been sent.')
            else:
                showerror('Insufficient Balance!!','There is not sufficient balance to complete the transaction.')
        else:
            showerror('Receiver Not Found!!','There is no receiver with %s address.'%(sendto.get()))
        
    except NameError:
        showerror('Error!','Please enter numeric value in amount and/or in transaction fee field.')
        
##########################################################################################

#for confirming send details
def sendcon():
    if sendto.get()!='' and bitcoin.get()!='' and transfee.get()!='':
        #clears the root. 
        l=root.winfo_children()
        for i in l:
            i.destroy()

        root.title('Send Bitcoins - KRYPTON WALLET')

        img=PhotoImage(file='edited.png')
        image_label=Label(root,image=img,width=1000,height=500)
        image_label.place(x=0,y=0)
        image_label.image=img
    
        Label(root,text='Review Details',font=('Consolas','32','bold'),bg='skyblue',fg='darkgreen').pack(pady=50)

        lab=['Sending To:','Amount Sending(BTC):','Transaction Fee(BTC):']
        var=[sendto,bitcoin,transfee]
        pad=200
        for i in range(0,3):
            Label(root,text=lab[i],font=('Consolas','15','bold'),anchor='w',width=21,bg='skyblue',fg='darkgreen').place(x=150,y=pad)
            Label(root,text=var[i].get(),font=('Consolas','15','bold'),anchor='w',width=40,bg='skyblue',fg='darkgreen').place(x=405,y=pad)
            pad+=50
            
        Button(root,text='Back',command=sendDetails,font=('Consolas','15','bold')).place(x=400,y=450)
        Button(root,text='Send',command=send,font=('Consolas','15','bold')).place(x=530,y=450)

        Label(root,text='**©Copyrights owned by Chaitanya Agarwal**',font=('Consolas','11','bold'),bg='skyblue',fg='darkgreen').pack(anchor='se',side='bottom')
        
    else:
        showerror('Empty Field(s)!!!','Please fill all the entries.')

##########################################################################################

#for taking input of send details
def sendDetails():
    #clears the root. 
    l=root.winfo_children()
    for i in l:
        i.destroy()

    #root resizing
    root.geometry('1000x500')
    root.maxsize(1000,500)
    root.minsize(1000,500)

    root.title('Send Bitcoins - KRYPTON WALLET')

    img=PhotoImage(file='edited.png')
    image_label=Label(root,image=img,width=1000,height=500)
    image_label.place(x=0,y=0)
    image_label.image=img

    Button(root,text='Back',command=mainWin,font=('Consolas','14','bold')).place(x=20,y=10)
    
    Label(root,text="Enter Receiver's Details",font=('Consolas','32','bold'),bg='skyblue',fg='darkgreen').pack(pady=10)

    #sending details
    lab=['Send To:','Amount(BTC):','Transaction Fee(BTC):']
    sendto.set('')
    bitcoin.set('')
    transfee.set('')
    var=[sendto,bitcoin,transfee]
    pad=200
    for i in range(0,3):
        Label(root,text=lab[i],font=('Consolas','15','bold'),anchor='w',width=21,bg='skyblue',fg='darkgreen').place(x=150,y=pad)
        Entry(root,textvariable=var[i],width=40,font=('lucida','15')).place(x=405,y=pad)
        pad+=50

    Button(root,text='Next',command=sendcon,font=('Consolas','15','bold')).place(x=460,y=450)

    Label(root,text='**©Copyrights owned by Chaitanya Agarwal**',font=('Consolas','11','bold'),bg='skyblue',fg='darkgreen').pack(anchor='se',side='bottom')

##########################################################################################

#for generating receiving address for the user
def receive():
    rand_list=[]
    for i in string.ascii_lowercase:
        rand_list+=i
    for i in string.digits:
        rand_list+=i
    for i in string.ascii_uppercase:
        rand_list+=i
    address=['1']
    for i in range(0,30):
        shuffle(rand_list)
        address[0]+=rand_list[i]
    print(address[0])
    
    showinfo('Your Address','Your bitcoin address is \n%s'%(address[0]))

    #connection establishment and updating bitcoin address
    conn=mysql.connector.connect(user='root',host='localhost',passwd='Subinsk284@',database='crypto')
    cur=conn.cursor()
    cur.execute('use crypto')
    cur.execute('update userlog set BitcoinAdd=(%s) where EmailAddress=(%s)',(address[0],emailadd.get()))
    conn.commit()
    cur.close()
    conn.close()
    
##########################################################################################

#for selling bitcoins
def sell():
    webbrowser.open('www.paypal.com')
    sellDetails()
       
##########################################################################################

#for confirming selling details
def sellcon():
    try:
        #connection establishment and checking bitcoins detail
        conn=mysql.connector.connect(user='root',host='localhost',passwd='Subinsk284@',database='crypto')
        cur=conn.cursor()
        cur.execute('use crypto')
        cur.execute('select Bitcoins from userlog where EmailAddress=(%s)',(emailadd.get(),))
        fetchdata=cur.fetchone()

        if bitcoin.get()!='':
            if float(fetchdata[0])>=float(bitcoin.get()):
                #clears the root. 
                l=root.winfo_children()
                for i in l:
                    i.destroy()

                #root resizing
                root.geometry('1000x500')
                root.maxsize(1000,500)
                root.minsize(1000,500)

                img=PhotoImage(file='edited.png')
                image_label=Label(root,image=img,width=1000,height=500)
                image_label.place(x=0,y=0)
                image_label.image=img

                Label(root,text='Review Details',font=('Consolas','32','bold'),bg='skyblue',fg='darkgreen').pack(pady=10)

                #displaying no. of bitcoins being sold and amount in USD
                Label(root,text='Bitcoins you are selling:',anchor='w',width=25,font=('Consolas','16','bold'),bg='skyblue',fg='darkgreen').place(x=200,y=200)
                Label(root,text=bitcoin.get()+' BTC',font=('Consolas','16','bold'),anchor='w',width=15,bg='skyblue',fg='darkgreen').place(x=550,y=200)

                cur.execute('select Price from cryptodata where SNo=1')
                fetchdata=cur.fetchone()

                bittousd=eval('%s*%s'%(bitcoin.get(),fetchdata[0].lstrip('$')))
                Label(root,text='USD you will receive:',anchor='w',width=25,font=('Consolas','16','bold'),bg='skyblue',fg='darkgreen').place(x=200,y=300)
                Label(root,text='$ %d'%bittousd,font=('Consolas','16','bold'),anchor='w',width=15,bg='skyblue',fg='darkgreen').place(x=550,y=300)
                
                cur.close()
                conn.close()
                
                Button(root,text='Back',command=sellDetails,font=('Consolas','15','bold')).place(x=400,y=450)
                Button(root,text='Sell',command=sell,font=('Consolas','15','bold')).place(x=530,y=450)

                Label(root,text='**©Copyrights owned by Chaitanya Agarwal**',font=('Consolas','11','bold'),bg='skyblue',fg='darkgreen').pack(anchor='se',side='bottom')
                
            else:
                showerror('Insufficient Balance!','There is not sufficient balance to complete the transaction.')
        else:
            showerror('Empty Fields!!','Please fill all the entries.')
    except ValueError:
        showerror('Error!','Please enter numeric values in bitcoins field.')

##########################################################################################

#for taking input of selling details
def sellDetails():
    #clears the root. 
    l=root.winfo_children()
    for i in l:
        i.destroy()

    #root resizing
    root.geometry('1000x500')
    root.maxsize(1000,500)
    root.minsize(1000,500)
    
    root.title('Sell Your Bitcoins - KRYPTON WALLET')

    img=PhotoImage(file='edited.png')
    image_label=Label(root,image=img,width=1000,height=500)
    image_label.place(x=0,y=0)
    image_label.image=img

    Button(root,text="Back",command=mainWin,font=('Consolas','14','bold')).place(x=20,y=10)
    
    Label(root,text='Sell Your Bitcoins',font=('Consolas','32','bold'),bg='skyblue',fg='darkgreen').pack(pady=10)

    bitcoin.set('')
    Label(root,text='How many (BTC)?',font=('Consolas','16','bold'),bg='skyblue',fg='darkgreen').place(x=250,y=200)
    Entry(root,textvariable=bitcoin,width=20,font='lucida 15').place(x=500,y=200)

    Button(root,text='Next',command=sellcon,font=('Consolas','14','bold')).place(x=460,y=450)

    Label(root,text='**©Copyrights owned by Chaitanya Agarwal**',font=('Consolas','11','bold'),bg='skyblue',fg='darkgreen').pack(anchor='se',side='bottom')

##########################################################################################

#for buying bitcoins
def buy():
    webbrowser.open('www.paypal.com')
    buyDetails()

##########################################################################################

#for confirming bitcoins buying details
def buycon():
    try:
        if USD.get()!='':
            #connection establishment and checking bitcoins rate
            conn=mysql.connector.connect(user='root',host='localhost',passwd='Subinsk284@',database='crypto')
            cur=conn.cursor()
            cur.execute('use crypto')
            cur.execute('select Price from cryptodata where SNo=1')
            fetchdata=cur.fetchone()

            usdtobit=eval('%s/%s'%(USD.get(),fetchdata[0].lstrip('$')))
            
            #clears the root. 
            l=root.winfo_children()
            for i in l:
                i.destroy()

            #root resizing
            root.geometry('1000x500')
            root.maxsize(1000,500)
            root.minsize(1000,500)

            img=PhotoImage(file='edited.png')
            image_label=Label(root,image=img,width=1000,height=500)
            image_label.place(x=0,y=0)
            image_label.image=img

            Label(root,text='Review Details',font=('Consolas','32','bold'),bg='skyblue',fg='darkgreen').pack(pady=10)

            #displaying no. of bitcoins being bought and cost in USD
            Label(root,text='USD u are spending:',font=('Consolas','16','bold'),anchor='w',width=27,bg='skyblue',fg='darkgreen').place(x=200,y=200)
            Label(root,text='$ '+USD.get(),font=('Consolas','16','bold'),anchor='w',width=15,bg='skyblue',fg='darkgreen').place(x=550,y=200)

            Label(root,text='Bitcoins you will receive:',font=('Consolas','16','bold'),anchor='w',width=27,bg='skyblue',fg='darkgreen').place(x=200,y=300)
            Label(root,text='%.8f BTC'%usdtobit,font=('Consolas','16','bold'),anchor='w',width=15,bg='skyblue',fg='darkgreen').place(x=550,y=300)
                
            cur.close()
            conn.close()
                
            Button(root,text='Back',command=buyDetails,font=('Consolas','15','bold')).place(x=400,y=450)
            Button(root,text='Buy',command=buy,font=('Consolas','15','bold')).place(x=530,y=450)

            Label(root,text='**©Copyrights owned by Chaitanya Agarwal**',font=('Consolas','11','bold'),bg='skyblue',fg='darkgreen').pack(anchor='se',side='bottom')
            
        else:
            showerror('Empty Fields!!','Please fill all the entries.')
    except NameError:
        showerror('Error!','Please enter numeric values for USD.')
        
##########################################################################################

#for taking input of bitcoin buying details
def buyDetails():
    #clears the root. 
    l=root.winfo_children()
    for i in l:
        i.destroy()

    #root resizing
    root.geometry('1000x500')
    root.maxsize(1000,500)
    root.minsize(1000,500)
    
    root.title('Buy Bitcoins - KRYPTON WALLET')

    img=PhotoImage(file='edited.png')
    image_label=Label(root,image=img,width=1000,height=500)
    image_label.place(x=0,y=0)
    image_label.image=img

    Button(root,text="Back",command=mainWin,font=('Consolas','14','bold')).place(x=20,y=10)
    
    Label(root,text='Buy Bitcoins',font=('Consolas','32','bold'),bg='skyblue',fg='darkgreen').pack(pady=10)

    USD.set('')
    Label(root,text='How much USD do u want to spend?',font=('Consolas','16','bold'),bg='skyblue',fg='darkgreen').place(x=150,y=200)
    Entry(root,textvariable=USD,width=20,font='lucida 15').place(x=600,y=200)

    Button(root,text='Next',command=buycon,font=('Consolas','14','bold')).place(x=460,y=450)

    Label(root,text='**©Copyrights owned by Chaitanya Agarwal**',font=('Consolas','11','bold'),bg='skyblue',fg='darkgreen').pack(anchor='se',side='bottom')
    
##########################################################################################

#for displaying cryptocurrency info. from crypto file
def display_info(event):
    #getting text from file
    sval=event.widget.cget('text')
    txt_info=file_read(sval)
    
    #clears the root. 
    l=root.winfo_children()
    for i in l:
        i.destroy()

    #root resizing
    root.geometry('1300x700')
    root.maxsize(1300,700)
    root.minsize(1300,700)

    img=PhotoImage(file='edited1.png')
    image_label=Label(root,image=img,width=1300,height=700)
    image_label.place(x=0,y=0)
    image_label.image=img

    root.title('%s - KRYPTON WALLET'%sval)

    #placing widgets and displaying text
    Button(root,text="Back",command=mainWin,font=('Consolas','14','bold')).place(x=20,y=10)

    #search value as heading
    Label(root,text=txt_info[0].rstrip('\n'),font=('Consolas','32','bold'),bg='skyblue',fg='darkgreen').pack(pady=10)

    #changing info list of search value into string and then displaying it
    text=''
    i=1
    while i<len(txt_info):
        text+=txt_info[i]
        i+=1
    Message(root,text=text,font=('Consolas','14'),width=900,relief=RIDGE,borderwidth=6).pack(pady=10)

    Label(root,text='**©Copyrights owned by Chaitanya Agarwal**',font=('Consolas','11','bold'),bg='skyblue',fg='darkgreen').pack(anchor='se',side='bottom')

##########################################################################################

#for adding cryptocurrency to user's favourites list
def add_favourites(event):
    text=event.widget.cget('text')
    #retrieving the cryptocurrency to be added to favourites column
    i=text.split()
    favour=[i[1]]
            
    #connection establishment and updating user's favourites list
    conn=mysql.connector.connect(user='root',host='localhost',passwd='Subinsk284@',database='crypto')
    cur=conn.cursor()
    cur.execute('use crypto')
    
    #getting the whole data to be added in favourites column
    cur.execute('select favourites from userlog where EmailAddress=(%s)',(emailadd.get(),))
    fetchdata=cur.fetchone()
    
    if fetchdata[0]!=None: # check if favourite column have any favourites yet
        #if favourite column have any favourites
        fetchdata=fetchdata[0].split(',') # if there are favourites then split favourite string
        if favour[0] not in fetchdata:#check if the text of button pressed is in favourites column or not
            # if text of button pressed is not in favourites column
            for i in fetchdata: # adding fetchdata elements into favour one by one
                favour.append(i)
        else:
            # if text of button pressed is in favourites column
            favour=fetchdata
    favour=','.join(favour)

    #updates favourite column
    cur.execute('update userlog set Favourites=(%s) where EmailAddress=(%s)',(favour,emailadd.get()))
    conn.commit()
    cur.close()
    conn.close()

    showinfo('Added to Favourites','Successfully added to your favourites list.')

##########################################################################################

#for removing favourites of the user
def remove_favourites(event):
    text=event.widget.cget('text')
    #retrieving the cryptocurrency to be deleted from favourites column
    i=text.split()
    favour=i[1]
            
    #connection establishment and updating user's favourites list
    conn=mysql.connector.connect(user='root',host='localhost',passwd='Subinsk284@',database='crypto')
    cur=conn.cursor()
    cur.execute('use crypto')
    
    cur.execute('select favourites from userlog where EmailAddress=(%s)',(emailadd.get(),))
    fetchdata=cur.fetchone()

    if fetchdata[0]!=None: # check if favourite column have any favourites yet
        #if favourite column have any favourites
        fetchdata=fetchdata[0].split(',') # if there are favourites then split favourite string
        fetchdata.remove(favour)
    if fetchdata!=[]:
        fetchdata=','.join(fetchdata)
    else:
        fetchdata=None

    #updates favourite column
    cur.execute('update userlog set Favourites=(%s) where EmailAddress=(%s)',(fetchdata,emailadd.get()))
    conn.commit()
    cur.close()
    conn.close()

    showinfo('Removed from Favourites','Successfully removed %s from your favourites list.'%(favour))
    show_favourites()

##########################################################################################

#for displaying user's favourite
def show_favourites():
    #connection establishment and fetching users favourites list and its data from cryptodata table
    conn=mysql.connector.connect(user='root',host='localhost',passwd='Subinsk284@',database='crypto')
    cur=conn.cursor(buffered=True)
    cur.execute('use crypto')
    cur.execute('select favourites from userlog where emailaddress=(%s)',(emailadd.get(),))
    fetchdata=cur.fetchone()
    if fetchdata[0]!=None:
        fetchdata=fetchdata[0].split(',')

        cryptodata=[]
        for i in fetchdata:
            cur.execute('select * from cryptodata where Name=(%s)',(i,))
            cryptodata+=[cur.fetchone()]

        cur.close()
        conn.close()

        #clears the root. 
        l=root.winfo_children()
        for i in l:
            i.destroy()
            
        #root resizing
        root.geometry('1300x700+0+0')
        root.maxsize(1300,700)
        root.minsize(1300,700)

        root.title('Your Favourites - KRYPTON WALLET')

        img=PhotoImage(file='edited1.png')
        image_label=Label(root,image=img,width=1300,height=700)
        image_label.place(x=0,y=0)
        image_label.image=img
        
        Button(root,text='Back',command=mainWin,font=('Consolas','14','bold')).place(x=20,y=10)
                
        Label(root,text='Your Favourites',font=('Consolas','32','bold'),bg='skyblue',fg='darkgreen').place(x=500,y=10)

        '''''''''''''''''''''''''''''''''''''''''''''
                data table
        '''''''''''''''''''''''''''''''''''''''''''''

        ##################################
        for i in range(len(cryptodata)-1):
            smallndx=i
            for j in range(i+1,len(cryptodata)):
                if cryptodata[j][0]<cryptodata[smallndx][0]:
                    smallndx=j
            if smallndx!=i:
                cryptodata[smallndx],cryptodata[i]=cryptodata[i],cryptodata[smallndx]

        root.anchor(anchor='center')

        #label text list
        labtxt=['S.No.','Name','Market_Cap','Price','Volume','Circulating_Supply','Change_24h']
        labl=[]
        for i in range(7):
            if i==0 or i==1:
                Label(root,text=labtxt[i],font=('Consolas','14','bold','underline'),relief=SOLID).grid(row=0,column=i,ipady=3,ipadx=3,padx=1,sticky='nsew')
            else:
                labl.append(Label(root,text=labtxt[i],font=('Consolas','14','bold','underline'),relief=SOLID,cursor='hand2'))
                labl[-1].grid(row=0,column=i,ipady=3,ipadx=3,padx=1,sticky='nsew')
                labl[-1].bind('<Button-1>',show_graph)

        for i in range(1,len(cryptodata)+1):
            Label(root,text=i,font=('Consolas','14','bold'),relief=SUNKEN).grid(row=i,ipady=3,ipadx=3,pady=1,padx=1,sticky='nsew')

        #label list for creating labels binded to an event
        labellist=[]
        for i in range(1,len(cryptodata)+1):
            labellist.append(Label(root,text=cryptodata[i-1][1],font=('Consolas','14','underline','bold'),relief=SUNKEN,cursor='hand2'))
            labellist[-1].grid(row=i,column=1,ipady=3,ipadx=3,sticky='nsew',pady=1,padx=1)
            labellist[-1].bind("<Button-1>",display_info)

        #remaining fields of cryptodata table
        for i in range(1,len(cryptodata)+1):
            Label(root,text=cryptodata[i-1][2],font=('Consolas','14','bold'),relief=SUNKEN).grid(row=i,column=2,pady=1,padx=1,ipady=3,ipadx=3,sticky='nsew')
            Label(root,text=cryptodata[i-1][3],font=('Consolas','14','bold'),relief=SUNKEN).grid(row=i,column=3,padx=1,pady=1,ipady=3,ipadx=3,sticky='nsew')
            Label(root,text=cryptodata[i-1][4],font=('Consolas','14','bold'),relief=SUNKEN).grid(row=i,column=4,padx=1,pady=1,ipady=3,ipadx=3,sticky='nsew')
            Label(root,text=cryptodata[i-1][5],font=('Consolas','14','bold'),relief=SUNKEN).grid(row=i,column=5,padx=1,pady=1,ipady=3,ipadx=3,sticky='nsew')
            Label(root,text=cryptodata[i-1][6],font=('Consolas','14','bold'),relief=SUNKEN).grid(row=i,column=6,padx=1,pady=1,ipady=3,ipadx=3,sticky='nsew')

        #Delete from favourite button
        butlist=[]
        for i in range(1,len(cryptodata)+1):
            butlist.append(Button(root,text='Remove %s from favourites'%(cryptodata[i-1][1]),font=('OCR-A-Extended','14','bold')))
            butlist[-1].grid(row=i,column=7,pady=1,padx=7,ipady=3,ipadx=3,sticky='nsew')
            butlist[-1].bind('<Button-1>',remove_favourites)
        
        b=Button(root,text='Refresh',cursor='hand2',command=refresh,font=('Consolas','16','bold'))
        b.place(x=600,y=650)
        b.bind('<Button-1>',refresh)

        Label(root,text='**©Copyrights owned by Chaitanya Agarwal**',font=('Consolas','11','bold'),bg='skyblue',fg='darkgreen').place(x=957,y=680)

    else:
        showinfo('No favourites!','There are no favourites.')
        mainWin()

##########################################################################################

#for deleting user's account
def delete_account():
    ans=askyesno('Deleting your account','Should we delete your account?')

    if ans==True:
        #connection establishment and deleting user's account
        conn=mysql.connector.connect(user='root',host='localhost',passwd='Subinsk284@',database='crypto')
        cur=conn.cursor()
        cur.execute('use crypto')
        cur.execute('delete from userlog where emailaddress=%s',(emailadd.get(),))
        conn.commit()
        cur.close()
        conn.close()

        showinfo('Account Deleted!','Your account has been deleted.')
        #calling log layout func. to direct user to login page after deleting account
        loglayout()

##########################################################################################

#for showing graph of cryptodata table
def show_graph(event):
    txt=event.widget.cget('text')
    #connection establishment and fetching data for graph
    conn=mysql.connector.connect(user='root',host='localhost',passwd='Subinsk284@',database='crypto')
    cur=conn.cursor()
    cur.execute('use crypto')
    cur.execute('select %s from cryptodata'%(txt))
    fetchdata=cur.fetchall()
    cur.close()
    conn.close()

    #this block is to create a list of graph data
    labtxt=['Market_Cap','Price','Volume']
    tick_sym=[' BTC',' ETH',' XRP',' USDT',' BCH',' LTC',' EOS',' BNB',' BSV',' XLM']
    graphdata=[]
    for i in range(len(fetchdata)):
        if txt in labtxt:
            graphdata+=[float(fetchdata[i][0].lstrip('$'))]
        elif txt=='Circulating_Supply':
            graphdata+=[int(fetchdata[i][0].replace(tick_sym[i],''))]
        elif txt=='Change_24h':
            if ord(fetchdata[i][0][0])==45:
                graphdata.append(eval(fetchdata[i][0].rstrip('%')+'*-1'))
            else:
                graphdata+=[float(fetchdata[i][0].rstrip('%'))]

    crypto_list=['Bitcoin','Ethereum','XRP','Tether','Bitcoin Cash','Litecoin','EOS','Binance Coin','Bitcoin SV','Stellar']    
    plt.figure(figsize=(13,6))
    plt.gcf().canvas.set_window_title('%s graph'%txt)
    plt.plot(graphdata,color='magenta',marker='^',markerfacecolor='g',markersize=10,markeredgecolor='g')
    plt.xticks(range(len(graphdata)),crypto_list,fontsize=13)
    plt.grid(which='major',linestyle='-',linewidth='0.5',color='red')
    plt.grid(which='minor',linestyle=':',linewidth='0.5',color='blue')
    plt.minorticks_on()
    plt.title('Comparison of Cryptocurrencies on the Basis of %s'%txt,fontsize=16)
    plt.xlabel('Cryptocurrencies',fontsize=14)
    plt.ylabel('%s data'%txt,fontsize=14)
    plt.show()

##########################################################################################

#for refreshing cryptodata table
def refresh(event):
    #connection establishment and updating cryptodata table
    conn=mysql.connector.connect(user='root',host='localhost',passwd='Subinsk284@',database='crypto')
    cur=conn.cursor()
    cur.execute('use crypto')
    cur.execute('update cryptodata set Market_Cap=(%s),Price=(%s),Volume=(%s),\
Circulating_Supply=(%s),Change_24h=(%s) where SNo=1',('$'+str(randint(120000000000,140000000000)),'$'+str(round(uniform(6000,9000),2)),'$'+str(randint(18000000000,30000000000)),str(randint(18000000,19000000))+' BTC',str(round(uniform(-7,10),2))+'%'))
    cur.execute('update cryptodata set Market_Cap=(%s),Price=(%s),Volume=(%s),\
Circulating_Supply=(%s),Change_24h=(%s) where SNo=2',('$'+str(randint(15000000000,18000000000)),'$'+str(round(uniform(120,200),2)),'$'+str(randint(7000000000,8000000000)),str(randint(100000000,110000000))+' ETH',str(round(uniform(-5,5),2))+'%'))
    cur.execute('update cryptodata set Market_Cap=(%s),Price=(%s),Volume=(%s),\
Circulating_Supply=(%s),Change_24h=(%s) where SNo=3',('$'+str(randint(9000000000,10000000000)),'$'+str(round(uniform(0.232369,2),6)),'$'+str(randint(1300000000,1400000000)),str(randint(43000000000,44000000000))+' XRP',str(round(uniform(-3,3),2))+'%'))
    cur.execute('update cryptodata set Market_Cap=(%s),Price=(%s),Volume=(%s),\
Circulating_Supply=(%s),Change_24h=(%s) where SNo=4',('$'+str(randint(4000000000,5000000000)),'$'+str(round(uniform(1,3),2)),'$'+str(randint(20000000000,25000000000)),str(randint(4000000000,4300000000))+' USDT',str(round(uniform(-5,5),2))+'%'))
    cur.execute('update cryptodata set Market_Cap=(%s),Price=(%s),Volume=(%s),\
Circulating_Supply=(%s),Change_24h=(%s) where SNo=5',('$'+str(randint(3500000000,4500000000)),'$'+str(round(uniform(200,300),2)),'$'+str(randint(1000000000,2000000000)),str(randint(18000000,19000000))+' BCH',str(round(uniform(-2,2),2))+'%'))
    cur.execute('update cryptodata set Market_Cap=(%s),Price=(%s),Volume=(%s),\
Circulating_Supply=(%s),Change_24h=(%s) where SNo=6',('$'+str(randint(2500000000,3500000000)),'$'+str(round(uniform(40,50),2)),'$'+str(randint(2500000000,3000000000)),str(randint(62000000,64000000))+' LTC',str(round(uniform(-3,3),2))+'%'))
    cur.execute('update cryptodata set Market_Cap=(%s),Price=(%s),Volume=(%s),\
Circulating_Supply=(%s),Change_24h=(%s) where SNo=7',('$'+str(randint(2000000000,3000000000)),'$'+str(round(uniform(1,4),2)),'$'+str(randint(1000000000,2000000000)),str(randint(942113890,1942113890))+' EOS',str(round(uniform(-4,4),2))+'%'))
    cur.execute('update cryptodata set Market_Cap=(%s),Price=(%s),Volume=(%s),\
Circulating_Supply=(%s),Change_24h=(%s) where SNo=8',('$'+str(randint(2000000000,3000000000)),'$'+str(round(uniform(10,20),2)),'$'+str(randint(200000000,300000000)),str(randint(150000000,160000000))+' BNB',str(round(uniform(-2,2),2))+'%'))
    cur.execute('update cryptodata set Market_Cap=(%s),Price=(%s),Volume=(%s),\
Circulating_Supply=(%s),Change_24h=(%s) where SNo=9',('$'+str(randint(1500000000,2000000000)),'$'+str(round(uniform(100,200),2)),'$'+str(randint(400000000,800000000)),str(randint(18000000,19000000))+' BSV',str(round(uniform(-2,2),2))+'%'))
    cur.execute('update cryptodata set Market_Cap=(%s),Price=(%s),Volume=(%s),\
Circulating_Supply=(%s),Change_24h=(%s) where SNo=10',('$'+str(randint(1000000000,1300000000)),'$'+str(round(uniform(0.01,0.09),6)),'$'+str(randint(200000000,300000000)),str(randint(20000000000,21000000000))+' XLM',str(round(uniform(-3,2),2))+'%'))
    conn.commit()
    cur.close()
    conn.close()

    if event.widget.cget('cursor')=='hand1':
        showTable()
    else:
        show_favourites()

##########################################################################################
        
#for showing table of top 10 cryptocurrencies
def showTable():
    #clears the root. 
    l=root.winfo_children()
    for i in l:
        i.destroy()
        
    #root resizing
    root.geometry('1300x700+0+0')
    root.maxsize(1300,700)
    root.minsize(1300,700)

    img=PhotoImage(file='edited1.png')
    image_label=Label(root,image=img,width=1300,height=700)
    image_label.place(x=0,y=0)
    image_label.image=img

    Button(root,text="Back",command=mainWin,font=('Consolas','14','bold')).place(x=20,y=10)

    '''''''''''''''''''''''''''
            data table
    '''''''''''''''''''''''''''
    
    root.anchor(anchor='center')

    #label text list
    labtxt=['S.No.','Name','Market_Cap','Price','Volume','Circulating_Supply','Change_24h']
    labl=[]
    for i in range(7):
        if i==0 or i==1:
            Label(root,text=labtxt[i],font=('Consolas','14','bold','underline'),relief=SOLID).grid(row=0,column=i,ipady=3,ipadx=3,padx=1,sticky='nsew')
        else:
            labl.append(Label(root,text=labtxt[i],font=('Consolas','14','bold','underline'),cursor='hand2',relief=SOLID))
            labl[-1].grid(row=0,column=i,ipady=3,ipadx=3,padx=1,sticky='nsew')
            labl[-1].bind('<Button-1>',show_graph)

    #connection establishment and displaying cryptodata table
    conn=mysql.connector.connect(user='root',host='localhost',passwd='Subinsk284@',database='crypto')
    cur=conn.cursor()
    cur.execute('use crypto')
    cur.execute('select * from cryptodata')
    fetchdata=cur.fetchall()
    cur.close()
    conn.close()
    
    for i in range(1,11):
        Label(root,text=i,font=('Consolas','14','bold'),relief=SUNKEN).grid(row=i,ipady=3,ipadx=3,pady=1,padx=1,sticky='nsew')

    #label list for creating labels binded to an event
    labellist=[]
    for i in range(1,11):
        labellist.append(Label(root,text=fetchdata[i-1][1],font=('Consolas','14','underline','bold'),cursor='hand2',relief=SUNKEN))
        labellist[-1].grid(row=i,column=1,ipady=3,ipadx=3,sticky='nsew',pady=1,padx=1)
        labellist[-1].bind("<Button-1>",display_info)

    #remaining fields of cryptodata table
    for i in range(1,11):
        Label(root,text=fetchdata[i-1][2],font=('Consolas','14','bold'),relief=SUNKEN).grid(row=i,column=2,padx=1,pady=1,ipady=3,ipadx=3,sticky='nsew')
        Label(root,text=fetchdata[i-1][3],font=('Consolas','14','bold'),relief=SUNKEN).grid(row=i,column=3,padx=1,pady=1,ipady=3,ipadx=3,sticky='nsew')
        Label(root,text=fetchdata[i-1][4],font=('Consolas','14','bold'),relief=SUNKEN).grid(row=i,column=4,padx=1,pady=1,ipady=3,ipadx=3,sticky='nsew')
        Label(root,text=fetchdata[i-1][5],font=('Consolas','14','bold'),relief=SUNKEN).grid(row=i,column=5,padx=1,pady=1,ipady=3,ipadx=3,sticky='nsew')
        Label(root,text=fetchdata[i-1][6],font=('Consolas','14','bold'),relief=SUNKEN).grid(row=i,column=6,padx=1,pady=1,ipady=3,ipadx=3,sticky='nsew')

    #Add to favourite button
    butlist=[]
    but_txtlist=['Bitcoin','Ethereum','XRP','Tether','Bitcoin_Cash','Litecoin','EOS','Binance_Coin','Bitcoin_SV','Stellar']
    for i in range(1,11):
        butlist.append(Button(root,text='Add %s to favourites'%(but_txtlist[i-1]),font=('OCR-A-Extended','14','bold')))
        butlist[-1].grid(row=i,column=7,padx=1,pady=1,ipady=3,ipadx=3,sticky='nsew')
        butlist[-1].bind('<Button-1>',add_favourites)
                    
    b=Button(root,text='Refresh',cursor='hand1',font=('Consolas','16','bold'))
    b.place(x=600,y=650)    
    b.bind('<Button-1>',refresh)

##########################################################################################

#for logging into user's account   
def login():
    if emailadd.get()!='' and password.get()!='':
        #connection establishment and checking if user's account exist or not
        conn=mysql.connector.connect(user='root',host='localhost',passwd='Subinsk284@',database='crypto')
        cur=conn.cursor()
        cur.execute('use crypto')
        cur.execute('select * from userlog where emailaddress=(%s) and password=(%s)',(emailadd.get(),password.get()))
        fetchdata=cur.fetchone()
        cur.close()
        conn.close()
        if fetchdata!=None:
            mainWin()
        else:
            showinfo('Record does not exist','You have entered wrong email address and/or password.\n\
Enter correct email address and/or password. \nOr you may have not created an account.\nCreate a new account and try again.')
    else:
        showerror('Empty Fields','Please fill all the entries.')
        
##########################################################################################

#for signing up the user
def signup():
    if emailadd.get()!='' and password.get()!='' and conpass.get()!='' and name.get()!='':
        if len(password.get())>=5 and len(password.get())<=16:
            if password.get()==conpass.get(): 
                #connection establishment and creating table
                conn=mysql.connector.connect(user='root',host='localhost',passwd='Subinsk284@')
                cur=conn.cursor()
                cur.execute('create database if not exists crypto')
                cur.execute('use crypto')
                cur.execute('create table if not exists userlog(Name varchar(40) not null,EmailAddress varchar(50)\
                            primary key,Password varchar(20) not null,Bitcoins varchar(20) default "0",BitcoinAdd varchar(40) unique,favourites varchar(100))')
                #checking for data accuracy
                cur.execute('select emailaddress from userlog where EmailAddress=(%s)',(emailadd.get(),))
                fetchdata=cur.fetchone()
                if fetchdata==None:
                    if ('@' in emailadd.get()) and (' ' not in emailadd.get()) and (emailadd.get()[-1:-5:-1]=='moc.' or emailadd.get()[-1:-5:-1]=='gro.' or emailadd.get()[-1:-5:-1]=='ten.' or emailadd.get()[-1:-4:-1]=='ni.'):
                         #writing data in table
                         cur.execute('insert into userlog (Name,EmailAddress,Password) values(%s,%s,%s)',(name.get(),emailadd.get(),password.get()))
                         conn.commit()
                         cur.close()
                         conn.close()
                         showinfo('Sign UP successful!','You have successfully created your account!!!')
                    else:
                        showerror('Invalid Email Address!!','You have entered invalid email address.\
    \nEnter email address that contain "@" and extensions like ".com",".org",".in" and ".net"')
                else:
                     showerror('Account already exists!!','You have entered an email address that already exists.\
    \nEnter a different valid email address or log in if you have an account.')
            else:
                showerror('Password doesn\'t match!!','Password and confirm password field does not match.\
    \nEnter same password in both the fields.')
        else:
                 showerror('Password length error!!','You have entered a password that is too short or too long.\
    \nEnter password of 5-16 characters.')
    else:
        showerror('Empty fields!!','Please fill all the entries.')

##########################################################################################

#for displaying login page
def loglayout():
    #root resizing
    root.geometry('1000x500')
    root.maxsize(1000,500)
    root.minsize(1000,500)
    
    root.title('Log In - KRYPTON WALLET')
    
    #clears the root. 
    l=root.winfo_children()
    for i in l:
        i.destroy()

    img=PhotoImage(file='edited.png')
    image_label=Label(root,image=img,width=1000,height=500)
    image_label.place(x=0,y=0)
    image_label.image=img
    
    '''''''''''''''''''''''''''''''''''''''
                login page layout
    '''''''''''''''''''''''''''''''''''''''            
    emailadd.set('')
    password.set('')
    #login page layout
    Label(root,text='Log In',font=('Consolas','32','bold'),bg='skyblue',fg='darkgreen').pack(pady=30)

    #label text list
    lab=['Email Address:','Password:']

    #Entry widget variables
    var=[emailadd,password]

    #entry widget list
    entl=[]

    #placing label and entry widgets
    pad=170
    for i in range(len(lab)):
        Label(root,text=lab[i],bg='skyblue',font=('Consolas','17','bold'),fg='darkgreen',width=14,anchor='w').place(x=210,y=pad)
        entl.append(Entry(root,textvariable=var[i],width=30,font='lucida 15'))
        entl[i].place(x=460,y=pad)
        pad+=80
    entl[-1].config(show='*')    
    
    Button(root,text='Log In',padx=3,pady=5,command=login,font=('Consolas','16','bold')).place(y=350,x=460)

    l=Label(root,text='Wanna Create a new account??',fg='darkgreen',bg='skyblue',cursor='hand2',font=('Consolas','11'))
    l.place(y=440,x=400)
    l.bind("<Button-1>",signlayout)

    Label(root,text='**©Copyrights owned by Chaitanya Agarwal**',font=('Consolas','11','bold'),bg='skyblue',fg='darkgreen').pack(anchor='se',side='bottom')
    
##########################################################################################

#for displaying signup page
def signlayout(event):
    #root resizing
    root.geometry('1000x500')
    root.maxsize(1000,500)
    root.minsize(1000,500)
    
    root.title('Sign Up - KRYPTON WALLET')
    
    #clears the root.
    l=root.winfo_children()
    for i in l:
        i.destroy()
        
    '''''''''''''''''''''''''''''''''''''''
                signup page layout
    '''''''''''''''''''''''''''''''''''''''
    img=PhotoImage(file='edited.png')
    image_label=Label(root,image=img,width=1000,height=500)
    image_label.place(x=0,y=0)
    image_label.image=img
    
    Label(text='Sign Up',font=('Consolas','32','bold'),bg='skyblue',fg='darkgreen').pack(pady=10)
    #label text list
    lab=['Name:','Email Address:','Password:','Confirm Password:']
    #Entry widget variables
    emailadd.set('')
    password.set('')
    name.set('')
    conpass.set('')
    var=[name,emailadd,password,conpass]
    #entry widget list
    entl=[]

    #placing entry and label widgets
    pad=100
    for i in range(len(lab)):
        Label(root,text=lab[i],font=('Consolas','17','bold'),bg='skyblue',fg='darkgreen',width=17,anchor='w').place(x=75,y=pad)
        entl.append(Entry(root,textvariable=var[i],width=50,font=('lucida','15')))
        entl[i].place(x=355,y=pad+4)
        pad+=70
    entl[-1].config(show='*')
    entl[-2].config(show='*')

    Button(root,text='Sign Up',command=signup,font=('Consolas','17','bold')).place(x=435,y=pad)
    Button(root,text='Log In',command=loglayout,font=('Consolas','17','bold')).place(x=443,y=pad+60)

    Label(root,text='**©Copyrights owned by Chaitanya Agarwal**',font=('Consolas','11','bold'),bg='skyblue',fg='darkgreen').pack(anchor='se',side='bottom')
        
##########################################################################################

#for displaying main window i.e. first window after user logs in 
def mainWin():
    #clears the root. 
    l=root.winfo_children()
    for i in l:
        i.destroy()
        
    #root resizing
    root.geometry('1300x700+0+0')
    root.maxsize(1300,700)
    root.minsize(1300,700)

    img=PhotoImage(file='edited1.png')
    image_label=Label(root,image=img,width=1300,height=700)
    image_label.place(x=0,y=0)
    image_label.image=img
   
    #connection establishment and creating table
    conn=mysql.connector.connect(user='root',host='localhost',passwd='Subinsk284@',database='crypto')
    cur=conn.cursor()
    cur.execute('use crypto')
    cur.execute('select * from userlog where emailaddress=(%s) and password=(%s)',(emailadd.get(),password.get()))
    fetchdata=cur.fetchone()
    cur.close()
    conn.close()

    root.title('Welcome %s - KRYPTON WALLET'%fetchdata[0])
    
    #account login status and logout
    l=Label(root,text='Hi,%s'%(fetchdata[0]),bg='skyblue',fg='darkgreen',font=('Consolas','14'))
    l.place(x=20,y=10)
    
    Button(root,text='Log Out',command=loglayout,font=('Consolas','14','bold')).place(x=1200,y=10)

    label_l=['Balance(BTC):-','Balance(USD):-']
    pad=70
    for i in range(0,2):
        l=Label(root,text=label_l[i],font=('Consolas','14'),bg='skyblue',fg='darkgreen')
        l.place(x=1080,y=pad)
        pad+=30

    #connection establishment and fetching no. of bticoins and price from table
    conn=mysql.connector.connect(user='root',host='localhost',passwd='Subinsk284@',database='crypto')
    cur=conn.cursor()
    cur.execute('use crypto')
    cur.execute('select Bitcoins from userlog where emailaddress=(%s)',(emailadd.get(),))
    fetchdata=cur.fetchone()
    cur.execute('select Price from cryptodata where SNo=1')
    fetchprice=cur.fetchone()
    cur.close()
    conn.close()
    
    l=Label(root,text=fetchdata[0]+' BTC',font=('Consolas','14'),bg='skyblue',fg='darkgreen')
    l.place(x=1230,y=70)
    
    balance_eval=fetchprice[0][1::]+'*'+fetchdata[0]
    l=Label(root,text='$'+str(eval(balance_eval)),width=5,font=('Consolas','14'),bg='skyblue',fg='darkgreen')
    l.place(x=1230,y=100)

    Button(root,text='Top 10 cryptocurrencies',width=58,command=showTable,font=('Consolas','16','bold')).place(x=300,y=200)
    Button(root,text='Send Bitcoins',width=20,command=sendDetails,font=('Consolas','16','bold')).place(x=300,y=300)
    Button(root,text='Receive Bitcoins',width=20,command=receive,font=('Consolas','16','bold')).place(x=300,y=400)
    Button(root,text='Sell Bitcoins',width=20,command=sellDetails,font=('Consolas','16','bold')).place(x=300,y=500)
    Button(root,text='Buy Bitcoins',width=20,command=buyDetails,font=('Consolas','16','bold')).place(x=750,y=300)
    Button(root,text='Your Favourites',width=20,command=show_favourites,font=('Consolas','16','bold')).place(x=750,y=400)
    Button(root,text='Delete Your Account',width=20,command=delete_account,font=('Consolas','16','bold')).place(x=750,y=500)
    
    Label(root,text='**©Copyrights owned by Chaitanya Agarwal**',font=('Consolas','11','bold'),bg='skyblue',fg='darkgreen').place(x=957,y=680)

##########################################################################################
##########################################################################################


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                            MAIN PART
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

root=Tk()
root.wm_iconbitmap('logo.ico')
root.resizable(0,0)

#global variables
name=StringVar()
conpass=StringVar()
emailadd=StringVar()
password=StringVar()
sendto=StringVar()
bitcoin=StringVar()
transfee=StringVar()
USD=StringVar()

#using data.py's databaseCreator function to create cryptocurrency's database in mysql
try:
    data.databaseCreator()
except Exception as e:
    print(e)

#calling log in page function
loglayout()

root.mainloop()

##########################################################################################
##########################################################################################
