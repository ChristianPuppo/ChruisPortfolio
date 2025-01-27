import Foundation

// Variabile, può essere cambiata nel corso del codice
var greeting = "Hello, playgroundo"

// Costante, nel corso del programma non può essere cambiata
let costante = "una costante"

// String, indica del semplice testo
let myFirstItem:String = "Questa è una stringa"

// Int, un numero intero (senza virgola)
let mySecondItem:Int = 7

// Double (o CGFLOAT) per numeri con virgola
let myThirdItem:Double = 7.1 // Double per Matematica
let myFourthItem:CGFloat = 7.2 // Float per UI UX

// Bool (Boolean), indica una costante o variabile vera o falsa.
let myFifthItem:Bool = false

// Statement if, in questo caso si sta chiedendo "Se myFifthItem è vero: Printa... sennò..."
if myFifthItem{
    print("fifth item it's true")
} else {
    print("fifth item it's false")
}

// Statement if, in questo caso si chiede "se fifthitem è falso: printa... sennò..."
if !myFifthItem{
    print("Fifth item è falso")
} else{
    print ("fifth item è vero")
}

// ora la variabile è impostata su ciao
var variabileModificabile:String = "Ciao"
// stampa ciao
print(variabileModificabile)

//ora non è più ciao
variabileModificabile = "non più ciao"
// stampa npn è più ciao
print(variabileModificabile)

var like = 3
var commenti = 4
var views = 100

like = like + 3 // stiamo addizionando var like + 3
commenti = commenti * 5 // stiamo moltiplicando comment per 6
views = views / 10 // stiamo dividendo views per 10

// ora abbiamo riprogrammato i valori di like commenti e views
print (like, commenti, views)

// ----------------------------------------------------------------------------- //

// Statement if, con operatore
if like > commenti {
    print("Like è Maggiore di Commenti")
} else {
    print("Commenti è Maggiore di Like")
}


// Statement if, con operatori e || che significa oppure
// si può usare anche && che significa AND
if like > commenti || commenti > views {
    print("Like è maggiore di commenti OPPURE i commenti sono maggiori delle views")
} else {
    print("Like è minore di commenti E views è minore di commenti")
}


// ----------------------------------------------------------------------------- //

// Qua abbiamo settato una funzione, Non stampa nulla finchè non la chiamiamo
func myFirstFunction() {
    print("My First Function Called")
    mySecondFunction() // abbiamo concatenato la seconda alla prima
}

// Seconda Funzione, possiamo concatenarla alla prima
func mySecondFunction() {
    print("My Second Function Called")
    myThirdFunction() // concatenato la terza alla seconda, che viene concatenata alla prima
}

// Terza Funzione, possiamo concatenarla alla seconda, che verrà concatenata alla prima
func myThirdFunction() {
    print("My Third Function Called")
}

// chiamiamo la funzione, farà l'azione dentro la funzione, ovverò chiamare prima funzione e poi la seconda con dentro la terza
myFirstFunction()


// altro esempio, la costante dentro la funzione è privata, non può essere accessa da fuori.
// per non printare il risultato della funzione possiamo chiedere di darci un return
// ovvero innanzitutto specificare cosa vogliamo in ritorno "-> String"
// poi aggiungere alla fine cosa deve ritornarci "return username"
func getUserName() -> String {
    let username:String = "Chruis"
    // print(username)
    return username
}

// in questa maniera facciamo sì che una variabile possa assumere il risultato della funzione
let name:String = getUserName()

// stampa la costante
print(name)

// ----------------------------------------------------------------------------- //

var userExist:Bool = false
var userIsDead:Bool = true

func checkUserStatus() -> Bool { // è il relativo di chiedere "Una funzione chiamata checkUserStatus() che dovrà ritornare un type Bool
    if userExist && userIsDead { // se userexist e userisdead è true ritorna falso
        return false
    } else { // sennò se solo uno dei due o entrambi e flaso ritorna true
        return true
    }
}

