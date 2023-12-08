// Script is from DrMagnus

console.log("Starting operation.");
var table;
table = document.getElementsByClassName("message new");
var hasNewApplicationMessages = table.length > 0;

setInterval(function() {
    hasNewApplicationMessages = false;
    var count = 0;
    for (var i = 0, row; row = table[i]; i++) {
        if (row.getElementsByTagName("td")[2].getElementsByClassName("subject")[0].textContent == "You received a membership application") {
            row.getElementsByTagName("td")[0].getElementsByTagName("input")[0].checked = true
            hasNewApplicationMessages = true;
            count++;
        }
    }
    if (hasNewApplicationMessages) {
        console.log("I found " + count.toString() + " application messages.");
        var start = new Date().getTime();
        var end = start;
        while (end < start + 500) {
            end = new Date().getTime();
        }
        document.getElementsByClassName("red btn btn-xs btn-danger")[0].click();
        document.getElementsByClassName("btn btn-default button button-remove-message")[0].click();

        table = document.getElementsByClassName("message new");
        console.log(table.length);
        console.log(hasNewApplicationMessages);
    } else {
        console.log("I found no new applications on this page!");
        console.log("Operation complete.");
    }
}, 3000)
