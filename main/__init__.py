
'''
Logga in ska vi ej ha 

 
I första versionen kanske den ska innehålla följande, varav alla kommer vara med i final version på något sätt: 
- schemavy: dag 
- uppgifter: kommande uppgifter för två olika kurser, innehållande namn på uppg, startdatum och deadline och 
- uppgifter: dagens to do 
- statistik 

FUNKTIONER 
huvud 
se beckoschema 
se uppgifter 
se statitsik 
hantera kuser - lägg till ta bort / ändra info  
hantera uppgifter - lägg till ta bort ändra info 
skapa en lista för varje ny användare med deras nya namn och inkludera det som databasen ska använda 
'''

'''namn GLOBAL VARIABEL? SÅLÄNGE'''

def main():
    namn = input("Hej vad heter du? ")
    print(f"Välkommen {namn} till BeWisePlanners verktyg för studieplanering!")

    print("Vad vill du göra? Ange siffran för menyvalet du vill besöka")

    print("1) Se veckoschema schema över kommande uppgifter")
    print("2) Se alla uppgifter")
    print("3) Se statistik över dina studier")
    print("4) Hantera befintliga kurser")
    print("5) Lägg till nya kurser")
    print("6) Hantera befintliga uppgifter")
    print("7) Lägg till nya uppgifter")
   
    
    menyval = input("Ditt val: ")
   
    while True:
        
        if menyval == "1":
            pass 
        elif menyval == "2":
            pass 
        elif menyval == "3":
            pass 
        elif menyval == "4":
            pass 
        elif menyval == "5":
            pass
        else: 
            print("Menyvalet existerar inte, se lista och testa igen!")
            break 

def view_weekly_planning():
    

def view_all_assignments():
    print("ALLA DINA UPPGIFTER")
    print("*"x40)

    print("Vad vill du se? Ange")
    print("1) Visa alla avklarade och ej avklarade uppgifter oberoende av kurs")
    print("2) Filtrera efter kurs")
    print("3) Filtrera efter avklarade")
    print("4) Filtrera efter ej avklarade")


def manage_existing_courses():

    print("Här kan du hantera dina befintliga kurser och lägga till nya")
    changed_course = input("Vilken kurs vill du redigera?" )

    print


    #VI SÖKER I DATABASEN OCH ÅTERKOMMER MED EXISTERANDE KURS  OCH DESS INFO OM DEN FFINNS OCH ERBJUDER MÖJLIGHET ATT SPARA NY OM DET FINNS 



    return 
    
