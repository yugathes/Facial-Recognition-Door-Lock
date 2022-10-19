print("Welcome to Face Recognition Door Lock")

def menu():
    print("Main Menu")
    print("1 : Enroll New Face")
    print("2 : Start Recognizer")
    print("3 : Delete Face")
    choice = int(input("Please Choice one option : "))
    return choice

c = menu()
if(c==1):
    print("Enroll")
if(c==2):
    print("Start")
if(c==3):
    print("Delete")
