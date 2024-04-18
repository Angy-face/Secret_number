from  termcolor import colored
import random
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan']

SERVICE_ACCOUNT_FILE = 'D:/PyProjects/Secret_number/secret.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
credential = None
credential = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
SPREAD_ID ='1LfYs-p1O_UfJiCcnddNQwT3rQqo5dm6tnjdbYpMIQoc'
service = build('sheets','v4',credentials=credential)
sheet =service.spreadsheets()
def finduser(toadd,csv):
    for i , _ in enumerate(csv['USER']):
        if(_==toadd[0][0]):
            range_toadd = "sheet1!A"+chr(i+50)+":B"
            print(colored(range_toadd,'green',attrs=['bold']))
            sheet.values().update(spreadsheetId=SPREAD_ID,range=range_toadd,valueInputOption="USER_ENTERED",
                            body={"values":toadd}).execute()
            return True
    return False
def add_to_leaderboard(USERNAME,time):
        csv=pd.read_csv(f'https://docs.google.com/spreadsheets/d/{SPREAD_ID}/export?format=csv')
        toadd=[[USERNAME,time]]
        if finduser(toadd,csv):
            print(colored(" Updated Your Score ", 'green', attrs=['bold']))
        else :
            sheet.values().append(spreadsheetId=SPREAD_ID,range='sheet1!A3:B',valueInputOption="USER_ENTERED",
                            body={"values":toadd}).execute()
            print(colored(" Added Your Username,Score ", 'green', attrs=['bold']))
    
def print_leaderboard():
    csv=pd.read_csv(f'https://docs.google.com/spreadsheets/d/{SPREAD_ID}/export?format=csv')
    csv_sorted = csv.sort_values(by=['GUESS'],ascending=True)
    for i, letter in enumerate(list("**** LEADERBOARD ****")):
        color = colors[i % len(colors)]
        print(colored(letter, color,attrs=['bold']), end='')
    print("")
    print(colored(csv_sorted, 'yellow', attrs=['bold']))

def main():
    print(colored(" I'm thinking of a number between 1 and 100. Try to guess it! \n *** Type H for hint but your guess will increase by 1 *** ",
                  'cyan',attrs=['bold']))
    print_leaderboard()
    username = input("Username : ")
    if username == "WONGPRANG":
        username = input(colored("Username : ",'red',attrs=['bold']))
    num = random.randint(1,100)
    time= 0
    while True:
        inp = input(" Guess the number! ( H/Hint E/Exit ): ")
        time+=1
        if inp == 'H':
            print(colored(" Think about cutting space where My number is", 'yellow', attrs=['bold']))
        elif inp =='E':
            print(colored(" Exited",'red',attrs=['bold']))
            break
        elif int(inp) == num :
            print(colored(" *** Congrat num is {} | Done in {} time *** ".format(num,time), 'green', attrs=['bold']))
            print(colored("PLAY AGAIN ? [y/n] :", 'yellow', attrs=['bold']),end='')
            inp = input("")
            add_to_leaderboard(username,time)  
            if inp ==  'y':
                main()
            elif inp == 'n':
                print(colored(" Exited",'red',attrs=['bold']))
            else:
                print(colored(" Enter y/n ".format(num,time), 'red', attrs=['bold']))
            break
        elif int(inp) < num :
            print(" More than {}".format(inp))
        elif int(inp) > num :
            print(" Less than {}".format(inp))
main()
