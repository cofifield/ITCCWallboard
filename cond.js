var loggedStates = document.getElementsByClassName("logged");
var talkingStates = document.getElementsByClassName("talk");
var waitingStates = document.getElementsByClassName("wait");
var abandonedStates = document.getElementsByClassName("abd");

// Logged in vs Talking Formatting
for(var i = 0; i < loggedStates.length; i++) {

    loggedInAgents = parseInt(loggedStates[i].innerHTML);
    talkingAgents = parseInt(talkingStates[i].innerHTML);


    if((talkingAgents / loggedInAgents) >= 0.75) {
        loggedStates[i].parentElement.className += " danger";
        continue;
    }

    if((talkingAgents / loggedInAgents) >= 0.5) {
        loggedStates[i].parentElement.className += " warning";
    }
}

// Waiting vs Logged in fromatting
for(var i = 0; i < waitingStates.length; i++) {
    loggedInAgents = parseInt(loggedStates[i].innerHTML);
    waitingCalls = parseInt(waitingStates[i].innerHTML);

    if((waitingCalls / loggedInAgents) > 0.5) {
        waitingStates[i].style.color = "red";
        continue;
    }

    if((waitingCalls / loggedInAgents) >= 0.25) {
        waitingStates[i].style.color = "#FAAC58";
    }

    if((waitingCalls / loggedInAgents) < 0.25) {
        waitingStates[i].style.color = "#3ADF00";
    }
}

// Abandonded fromatting
for(var i = 0; i < abandonedStates.length; i++) {
    abandoned = parseInt(abandonedStates[i].innerHTML);

    if(abandoned >= 10) {
        abandonedStates[i].style.color = "red";
        continue;
    }

    if(abandoned >= 5) {
        abandonedStates[i].style.color = "#FAAC58";
    }

    if(abandoned < 5) {
        abandonedStates[i].style.color = "#3ADF00";
    }
}

/* ##########################################################################
   ##########################################################################
*/

var agentStates = document.getElementsByClassName("as");
var reasonStates = document.getElementsByClassName("rd");
var tisStates = document.getElementsByClassName("tis");

// Reason Based Formatting
for(var i = 0; i < reasonStates.length; i++) {

    if((reasonStates[i].innerHTML == "Logon") || (reasonStates[i].innerHTML == "Office Tasks") || (reasonStates[i].innerHTML == "Meeting") 
        || (reasonStates[i].innerHTML == "ServiceNow Ticket") || (reasonStates[i].innerHTML == "Customer Walk-In") || (reasonStates[i].innerHTML == "Agent Off Hook")
        || (reasonStates[i].innerHTML == "Ring No Answer") || (reasonStates[i].innerHTML == "Work") || (reasonStates[i].innerHTML == "Lunch") || (reasonStates[i].innerHTML == "Break")) {
    	reasonStates[i].parentElement.className += " danger";
    }
}

// Time in State Formatting
for(var i = 0; i < tisStates.length; i++) {

	temp = tisStates[i].innerHTML.split(':');
	time = temp[0] + temp[1] + temp [2];
	time = parseInt(time);
    if((time > 3000) && (agentStates[i].innerHTML != "Ready")) {
    	tisStates[i].style.color = "red";
    }
}

// Agent Based Formatting
for(var i = 0; i < agentStates.length; i++) {

    if((agentStates[i].innerHTML == "Talking") || (agentStates[i].innerHTML == "Reserved")) {
    	agentStates[i].parentElement.className += " warning";
    }
}