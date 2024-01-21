#MODULE TO CHECK MYSQL CONNECTIVITY
import mysql.connector as m
global myConnection
myConnection=m.connect(host="localhost",user="root",passwd="helloworld124" )
if myConnection:
    print("\nCONGRATULATIONS ! MYSQL CONNECTION HAS BEEN ESTABLISHED !")
else:
    print("\nERROR ESTABLISHING MYSQL CONNECTION CHECK USERNAME AND PASSWORD !")



#MODULE TO CREATE DATABASE   
def create_db():
    cur=myConnection.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS BM")
    return myConnection
create_db()
 

#CREATING TABLE
myConnection=m.connect(host="localhost",user="root",passwd="helloworld124",database="BM")
def createtable():
    cur=myConnection.cursor()
    s="CREATE TABLE IF NOT EXISTS BANK(ACNO INTEGER PRIMARY KEY, NAME VARCHAR(50), BALANCE INTEGER, MOB CHAR(10) CHECK(LENGTH(MOB)=10))"
    t="CREATE TABLE IF NOT EXISTS TRANSACTIONS(ACNO INT, AMOUNT INT(6), TRANSACTION_TYPE VARCHAR(50), CURRENT DATE, TIME TIME, FOREIGN KEY (ACNO) REFERENCES BANK(ACNO))"
    cur.execute(s)
    cur.execute(t)
    myConnection.close()
createtable()


#MODULE TO USE DATABASE
def menu():
    myConnection=m.connect(host="localhost",user="root",passwd="helloworld124",database="BM")
    cur=myConnection.cursor()
    query="SELECT MAX(ACNO) FROM BANK"
    cur.execute(query)
    a=cur.fetchone()[0]
    if a==None: #In case no record is there
        ano=1001
    else:
        ano=a+1
    while True:
        print("x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x")
        print(" "*18,end='')
        print("BANK MANAGEMENT SYSTEM")
        print("x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x")
        print()
        choice=int(input("1--> OPEN ACCOUNT\n\n2--> CASH DEPOSIT\n\n3--> CASH WITHDRAWAL\n\n4--> ACCOUNT STATEMENT\n\n5--> TRANSACTION HISTORY\n\n6--> EXIT\n\nENTER YOUR CHOICE: "))

        #OPEN ACCOUNT
        if choice==1:
            name=input("Enter name of Account Holder: ")
            balance=int(input("Enter Opening Balance: "))
            mob=input("Enter registered Mobile number: ")
            s="INSERT INTO BANK VALUES({},'{}',{},'{}')".format(ano, name ,balance, mob)
            if len(str(mob))==10:
                cur.execute(s)
                print("Account opened successfully!")
            else:
                print("Check your mobile number...")
            myConnection.commit()
            print()
        

        #CASH DEPOSIT
        if choice==2:
            acno=int(input("Enter your Account Number: "))
            depo=int(input("Enter Amount to be Deposited: "))
            ttype="Deposit"
            s="INSERT INTO TRANSACTIONS VALUES({}, {}, '{}', curdate(), curtime())".format(acno, depo, ttype)
            t="UPDATE BANK SET BALANCE=BALANCE+{} WHERE ACNO={}".format(depo, acno)
            cur.execute(s)
            cur.execute(t)
            myConnection.commit()
            print("Rs.", depo, "has been deposited succesfully in account no.: ", acno)
            print()

        #CASH WITHDRAWAL
        if choice==3:
            acno=int(input("Enter your Account Number: "))
            withdr=int(input("Enter Amount to be Withdrawn: "))
            s="SELECT BALANCE FROM BANK WHERE ACNO={}".format(acno)
            cur.execute(s)
            bal=cur.fetchone()[0]
            if withdr<bal:
                ttype="Withdraw"
                t="INSERT INTO TRANSACTIONS VALUES({}, {}, '{}', curdate(), curtime())".format(acno, withdr, ttype)
                u="UPDATE BANK SET BALANCE=BALANCE-{} WHERE ACNO={}".format(withdr, acno)
                cur.execute(t)
                cur.execute(u)
                print("Rs.", withdr, "has been withdrawn succesfully from account no.: ", acno)
                myConnection.commit()
            else:
                print("Can't withdraw money. Insufficient Balance!")
                print()

        #ACCOUNT SUMMARY
        if choice==4:
            acno=int(input("Enter your Account Number: "))
            p="SELECT * FROM BANK WHERE ACNO={}".format(acno)
            cur.execute(p)
            data=cur.fetchone()
            if cur.rowcount>0:
                print()
                print("x"*57)
                print("Account Details are:")
                print("Account Number = ",data[0])
                print("Name of Account Holder = ",data[1])
                print("Account Balance = ",data[2])
                print("Registered Mobile Number = ",data[3])
                print("x"*57)
            else:
                print("Account Number Not Found...")
            print()

        #TRANSACTION DETAILS
        if choice==5:
            acno=int(input("Enter your Account Number: "))
            s="SELECT * FROM BANK WHERE ACNO={}".format(acno)
            cur.execute(s)
            if cur.fetchone() is None:
                print()
                print('Invalid Account number!!')
            else:
                p="SELECT B.ACNO, B.NAME, T.TRANSACTION_TYPE, T.AMOUNT, T.CURRENT, T.TIME FROM BANK B, TRANSACTIONS T WHERE T.ACNO={} AND B.ACNO={}".format(acno, acno)
                cur.execute(p)
                data=cur.fetchall()
                print("+-----------------------------------------------------------------------------+")
                print("|Account Number| Name     |Transaction Type| Amount | Date        | Time      |")
                print("+-----------------------------------------------------------------------------+")
                for i in data:
                    print("|",i[0]," "*(11-len(str(i[0]))),"|",i[1]," "*(7-len(i[1])),"|",i[2]," "*(13-len(i[2])),"|",i[3]," "*(5-len(str(i[3]))),"|",i[4]," "*(3-len(str(i[4]))),"|",i[5]," "*(8-len(str(i[5]))),"|")
                print("+-----------------------------------------------------------------------------+")
                print()

        #ELSE
        if choice==6:
            break

        #WRONG INPUT
        if choice not in [1,2,3,4,5,6]:
            print("Please Select from the given choices...")
            print()


#MODULE FOR AUTHORISED USERS
myConnection=m.connect(host="localhost",user="root",passwd="helloworld124",database="BM")
cur=myConnection.cursor()
s="CREATE TABLE IF NOT EXISTS USER_TABLE(USERNAME VARCHAR(25) PRIMARY KEY, PASSWORD VARCHAR(25) NOT NULL)"
cur.execute(s)
while True:
    print('1.REGISTER')
    print('2.LOGIN')
    print('3.EXIT')
    n=int(input('ENTER YOUR CHOICE: '))
    if n== 1:
        name=input('ENTER A USERNAME: ')
        passwd=eval(input('ENTER A 4 DIGIT PASSWORD: '))
        if len(str(passwd))==4 and type(passwd)==int:
            t="INSERT INTO USER_TABLE VALUES('{}', '{}')".format(name,passwd)
            cur.execute(t)
            myConnection.commit()
            print('USER created succesfully...')
            print()
        else:
            print("Enter a 4 digit password only!")
    if n==2 :
        name=input('ENTER YOUR USERNAME: ')
        passwd=int(input('ENTER YOUR 4 DIGIT PASSWORD: '))
        
        print()
        t="SELECT * FROM USER_TABLE WHERE PASSWORD='{}' AND USERNAME='{}'".format(passwd,name)
        cur.execute(t)
        if len(str(passwd))==4 and type(passwd)==int:
            if cur.fetchone() is None:
                print("-------------------------------")
                print("Invalid Username or Password...")
                print("-------------------------------")
                print()
            else:
                menu()
        else:
            print("Invalid Username or Password...")
            print()
    if n==3:
        break
    else:
        print("Choose from the given choices...")

 
                                                

    







