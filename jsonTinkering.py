import datetime

def main():
    f = open(str(datetime.datetime.today().strftime("%S_%M_%H_%d_%m_%y"))+".log","x")
    f.close()

if (__name__ == "__main__"):
    main()