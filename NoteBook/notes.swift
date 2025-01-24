let questaunacostante = 73 // una costante è tale quando il valore assegnatogli non cambia nel corso del programma
var questaunavariabile = 1 // una variabile è tale perchè nel corso del programma il valore può variare

// Proviamo a cambiare il valore della variabile
questaunavariabile = 10 // cambiamo il valore della variabile
// variabile è ora = 10

// Provando a cambiare il valore della costante (questo causerà un errore, perché le costanti non possono essere modificate)
// questaunacostante = 100 // Questa linea darà errore, poiché non possiamo modificare una costante

var environment = "development" // qua sta dicendo: "environment è development (al momento)"
let maximumNumberOfLoginAttempts: Int // non ha valore, verrà attribuito più avanti
// maximumNumberOfLoginAttempts has no value yet.


if environment == "development" { // se environment è development (come in questo caso)
    maximumNumberOfLoginAttempts = 100 // allora il numero massimo di tentativi sarà una costante = 100
} else { // sennò
    maximumNumberOfLoginAttempts = 10 // qualsiasi altro stato non uguale a development darà un max di 10 tentativi (costante)
}
// Now maximumNumberOfLoginAttempts has a value, and can be read.

var x = 0.0, y = 0.0, z = 0.0 // puoi attribuire più variabili su una stessa riga usando le virgole come separatori

var welcomeMessage: String // puoi scegliere il tipo di annotazione da attribuire a una variabile o costante, con i due punti
// in questo caso stai dicendo che la variabile welcomeMessage può essere solo una String

// ora puoi assegnare a questa variabile una qualsiasi stringa di testo
welcomeMessage = "Hello"

// puoi dare a più variabili sulla stessa riga un annotazione
// l'annotazione Double è per definire numeri con la virgola, che definirai in seguito
var red, green, blue: Double

// le costanti e le variabili possono avere qualsiasi nome unicode
let π = 3.14159
let 你好 = "你好世界"
let 🐶🐮 = "dogcow"


// puoi cambiare il valore di una variabile in qualsiasi momento
var friendlyWelcome = "Hello!"
friendlyWelcome = "Bonjour!"
// friendlyWelcome is now "Bonjour!"

