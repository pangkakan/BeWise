
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
    namn = input("Hej! vad heter du? ")
    användaruppgifter = [namn]
    print(f"Välkommen {namn} till BeWisePlanners verktyg för studieplanering!")
    menu()
 
def menu():
    print("Vad vill du göra? Ange siffran för menyvalet du vill besöka")

    print("3) Lägg till nya kurser")
    print("2) Se dina kurser")
    print("2) Lägg till nya uppgifter inom valfri kurs")
    print("3) Se dina uppgifter")

    menyval = input("Ditt val: ")
   
    while True:
        if menyval == "1":
            add_courses()
        elif menyval == "2":
            view_courses()
        elif menyval == "3":
            add_assignments()
        elif menyval == "4":
            view_assignments()
        else:
            print("Menyvalet existerar inte, se lista och testa igen!")
            break 

def add_courses():
    print("LÄGG TILL KURSER")
 
    ny_kurs = input("Vad heter kursen du vill lägga till? ")
    #lägg till kursen i namn listan 
    aktiv_period = input("Hur länge pågår kursen? Ange antal veckor: ")
    #lägg till perioden i namn listan

    print("Vill du lägga till fler kurser")
    print("Ange 1 för att lägga till fler eller skriv valfri symbol för att komma tillbaka till huvudmenyn")
    kurs_fråga = input("Ditt val: ")

    while True:

     if kurs_fråga == "1":
       ny_kurs = input("Vad heter kursen du vill lägga till? ")
       #lägg till kursen i namn listan - TRY DVS CSV ÄR NOG LÄTTAST ? MINNS EJ HUR HÄMTA INOM DOKUMENTET OM EJ 
       aktiv_period = input("Hur länge pågår kursen? Ange antal veckor: ")
       #lägg till perioden i namn listan

     else: 
        menu() 

def view_courses():
   print("SE KURSER")
   #print alla kurser personen har 

   #vill du lägga till uppgifter till en viss kurs? 1) ja gå till uppgifter 2) nej meny 
 

def add_assignments():

    print("LÄGG TILL UPPGIFTER")
    #börja med att söka i listan efter kurser under personen och finns det ej hänvisa tillbaka till menyn eller låt dem välja lägga till kurser

    print("


    print("Här kan du hantera dina befintliga kurser och lägga till nya")
    changed_course = input("Vilken kurs vill du redigera?" )

    print


    #VI SÖKER I DATABASEN OCH ÅTERKOMMER MED EXISTERANDE KURS  OCH DESS INFO OM DEN FFINNS OCH ERBJUDER MÖJLIGHET ATT SPARA NY OM DET FINNS 



    return 
    
