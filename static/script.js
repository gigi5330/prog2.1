//Daten einlesen und speichern
var budget = document.getElementById("budget").innerHTML;
var budgetRemaining = document.getElementById("budget-remaining").innerHTML;
var robotMessage = document.getElementById("robot-message");

//Budget-Verbleib berechnen
if (budgetRemaining >= 0.9 * budget) {
    robotMessage.innerHTML = "Wow, Sie haben noch mehr als 90% Ihres Budgets übrig. Gut gemacht!";
} else if (budgetRemaining >= 0.5 * budget) {
    robotMessage.innerHTML = "Sie haben mehr als die Hälfte Ihres Budgets übrig. Weiter so!";
} else if (budgetRemaining >= 0) {
    robotMessage.innerHTML = "Achten Sie darauf, Ihre Ausgaben im Auge zu behalten. Sie haben nur noch " + budgetRemaining + " übrig.";
} else {
    robotMessage.innerHTML = "Vorsicht! Sie haben Ihr Budget überschritten. Kontrollieren Sie Ihre Ausgaben.";
}
