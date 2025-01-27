# Appunti di Swift 🐦

Questi sono i miei appunti di base su Swift.

---

## Indice

1. [Variabili e Costanti](#variabili-e-costanti)
2. [Tipi di Dati](#tipi-di-dati)
3. [Controllo di Flusso](#controllo-di-flusso)
4. [Operatori](#operatori)
5. [Funzioni](#funzioni)
6. [Esempi Avanzati](#esempi-avanzati)

---

## Variabili e Costanti

### Variabili
Le variabili possono essere modificate durante l'esecuzione del programma e si dichiarano con `var`.

```swift
var greeting = "Hello, playgroundo"
```

### Costanti
Le costanti, dichiarate con `let`, non possono essere modificate una volta assegnato un valore.

```swift
let costante = "una costante"
```

---

## Tipi di Dati

Swift supporta diversi tipi di dati, tutti fortemente tipizzati.

```swift
// String: testo semplice
let myFirstItem: String = "Questa è una stringa"

// Int: numero intero
let mySecondItem: Int = 7

// Double e CGFloat: numeri decimali
let myThirdItem: Double = 7.1
let myFourthItem: CGFloat = 7.2

// Bool: valori booleani
let myFifthItem: Bool = false
```

### Esempio con controllo del tipo

```swift
let a = 10       // Int
let b = 20.5     // Double

// Errore: tipi incompatibili
// let somma = a + b

// Conversione esplicita
let somma = Double(a) + b
```

---

## Controllo di Flusso

Swift include costrutti come `if-else` e `switch` per controllare il flusso del programma.

### If-Else

```swift
if myFifthItem {
    print("fifth item it's true")
} else {
    print("fifth item it's false")
}
```

### Con negazione

```swift
if !myFifthItem {
    print("Fifth item è falso")
} else {
    print("fifth item è vero")
}
```

---

## Operatori

Gli operatori permettono di effettuare operazioni matematiche e logiche sui dati.

### Operazioni matematiche

```swift
var like = 3
var commenti = 4
var views = 100

like = like + 3       // Aggiunge 3 a like
commenti = commenti * 5 // Moltiplica commenti per 5
views = views / 10     // Divide views per 10

print(like, commenti, views)
```

### Operatori logici

```swift
if like > commenti || commenti > views {
    print("Like è maggiore di commenti OPPURE i commenti sono maggiori delle views")
} else {
    print("Like è minore di commenti E views è minore di commenti")
}
```

---

## Funzioni

Le funzioni sono blocchi di codice riutilizzabili che possono opzionalmente restituire un valore.

### Esempio base

```swift
func myFirstFunction() {
    print("My First Function Called")
    mySecondFunction()
}

func mySecondFunction() {
    print("My Second Function Called")
    myThirdFunction()
}

func myThirdFunction() {
    print("My Third Function Called")
}

myFirstFunction()
```

### Funzioni con ritorno

```swift
func getUserName() -> String {
    let username: String = "Chruis"
    return username
}

let name: String = getUserName()
print(name)
```

---

## Esempi Avanzati

### Controllo dello stato utente

```swift
var userExist: Bool = false
var userIsDead: Bool = true

func checkUserStatus() -> Bool {
    if userExist && userIsDead {
        return false
    } else {
        return true
    }
}
```

---
