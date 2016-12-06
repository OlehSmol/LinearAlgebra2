console.log("all.js is running");

//
// --------------------------------global variables ------------------------------
//
var selectedProjectTabId = "project-1";
//
// -------------------------------------------------------------------------------
//


function onProjectTabClicked() {
    var id = this.id;
    document.getElementById(selectedProjectTabId).className = "";
    document.getElementById(id).className = "selected";
    document.getElementById(selectedProjectTabId+"-container").className = "nonvisible";
    document.getElementById(id + "-container").className = "";
    selectedProjectTabId = id;
}



function readMatrixValue(id) {
    "use strict";
    var table = document.getElementById(id),
        matrix = new Array(table.children.length); //table.children[0].children.length);

    for (var i = 0; i < table.children.length; i++) {
        var tr = table.children[i],
            row = new Array(tr.children.length + 1);
        for (var j = 0; j < tr.children.length; j++) {
            var td = tr.children[j],
                val = td.children[0].value;
            if (val === "" || Number(val) === NaN) {
                val = Number(td.children[0].placeholder);
            } else {
                val = Number(td.children[0].value)
            }
            row[j] = val;
        }
        matrix[i] = row;
    }
    return matrix;

}

function removeMatrix(id) {
    "use strict";
    document.getElementById('input-container').removeChild(document.getElementById(id));
}

function clearContent(id) {
    "use strict";
    document.getElementById(id).innerHTML = '';
}

function generateMatrixTable(m, n, id) {
    "use strict";
    var table = document.createElement('table');
    table.id = id;
    table.className = 'matrix';

    for (var i = 0; i < Number(m); i++) {
        var tr = document.createElement('tr');
        for (var j = 0; j < Number(n); j++) {
            var td = document.createElement('td');
            var input = document.createElement('input');
            input.placeholder = '1';
            td.appendChild(input);
            tr.appendChild(td);
        }
        table.appendChild(tr)
    }

    document.getElementById('input-container').appendChild(table);
}

function checkMatrixSize() {
    var m_selector = document.getElementById('m-size');
    var n_selector = document.getElementById('n-size');

    var m = m_selector.options[m_selector.selectedIndex].value;
    var n = n_selector.options[n_selector.selectedIndex].value;

    return [m, n];
}

function generateJSONmessage() {
    "use strict";
    var matrix = readMatrixValue('user-matrix'),
        bVector = readMatrixValue('b-vector');
    for (var i = 0; i < matrix.length; i++) {
        matrix[i][matrix[i].length - 1] = bVector[i][0];
    }

    return JSON.stringify({
        matrix
    });
}


function onChangeMatrixSizeHandler() {
    var size = checkMatrixSize();
    removeMatrix('user-matrix');
    removeMatrix('b-vector');
    clearContent('solution-description');
    generateMatrixTable(size[0], size[1], 'user-matrix');
    generateMatrixTable(size[0], 1, 'b-vector');
}

//
// -------------------------------- Project 2 code ------------------------------
//
function onResendCheckBoxClick(){
    if(document.getElementById('resendCheckBox').checked){
        document.getElementById('resendCheckBoxBtn').className = 'btn btn-prime btn-checkbox checked';
    }else{
        document.getElementById('resendCheckBoxBtn').className = 'btn btn-prime-outline btn-checkbox';
    }
}


//
// --------------------------------displayResponse ------------------------------
//
function createResponseMatrix(m) {
    var matrix = document.createElement('div');
    matrix.className = 'matrix';
    var matrixContainer = document.createElement('div');
    matrixContainer.className = 'matrix-container';

    for (var i = 0; i < m.length; i++) {
        var row = document.createElement('div');
        row.className = 'matrix-row';
        for (var j = 0; j < m[i].length; j++) {
            var col = document.createElement('div');
            col.className = 'matrix-column';
            col.innerHTML = m[i][j];
            row.appendChild(col);
        }
        matrixContainer.appendChild(row);
    }
    matrix.appendChild(matrixContainer);
    return matrix;
}

function displayResponse(response) {
    "use strict";
    var fillWord = "inconsistent";
    response = JSON.parse(response);
    if (response['consistency']) {
        fillWord = "consistent";
    }
    var message = "The system Ax = b is <span class='bold wrapped'>" + fillWord + "</span> ";
    var p = document.createElement('p');
    p.innerHTML = message;
    document.getElementById('solution-description').appendChild(p);

    p = document.createElement('p');
    p.innerHTML = "A linear system is consistent if and only if its coefficient matrix has the same rank as does its augmented matrix (the coefficient matrix with an extra column added, that column being the column vector of constants). To check it we find reduced echelon form of matrix by performing gaussian elimination.";
    document.getElementById('solution-description').appendChild(p);

    for (var i = 0; i < response['steps'].length; i++) {
        var DOMmatrix = createResponseMatrix(response['steps'][i]);
        var desc = document.getElementById('solution-description');
        desc.appendChild(DOMmatrix);

        if (i != response['steps'].length - 1) {
            var eqSign = document.createElement('div');
            eqSign.className = 'equal-sign';
            eqSign.innerHTML = ' ~ ';
            desc.appendChild(eqSign);
        }
    }

}

//
// --------------------------------XMLHttpRequest------------------------------
//

function makeXMLrequest(method, URI, onloadHandler, onerrorHandler, message) {
    "use strict";
    var xhr = new XMLHttpRequest();
    xhr.open(method, URI, true);

    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onload = function () {
        onloadHandler(xhr.response);
    };
    xhr.onerror = function () {
        onerrorHandler(xhr.status + ': ' + xhr.statusText);
    };
    xhr.send(message);
}

//
// --------------------------------window.onload------------------------------
//
window.onload = function () {
    "use strict";

    // left tab menu listener 
    document.getElementById('project-1').onclick = onProjectTabClicked;
    document.getElementById('project-2').onclick = onProjectTabClicked;
    document.getElementById('project-3').onclick = onProjectTabClicked;
    
    // resendCheckBox listener
    document.getElementById('resendCheckBox').onclick = onResendCheckBoxClick;

    // create and add two tables in main-section
    generateMatrixTable(2, 2, 'user-matrix');
    generateMatrixTable(2, 1, 'b-vector');

    // #m-size selector onchange handler
    document.getElementById('m-size').onchange = onChangeMatrixSizeHandler;

    // #n-size selector onchange handler
    document.getElementById('n-size').onchange = onChangeMatrixSizeHandler;


    // #submit button onclick handler
    document.getElementById('submit').onclick = function () {
        this.innerHTML = "Processing...";
        this.disabled = true;

        clearContent('solution-description');

        var myJSONString = generateJSONmessage();
        console.log(myJSONString);

        var onloadMethod = function (response) {
            document.getElementById('submit').innerHTML = "Push me again, I like it";
            document.getElementById('submit').disabled = false;
            console.log(response);
            displayResponse(response);
        };

        var onerrorMethod = function (responseMessage) {
            document.getElementById('submit').innerHTML = "Error, try again";
            document.getElementById('submit').disabled = false;
            console.log(responseMessage);
        };
        //        makeXMLrequest('POST', 'http://127.0.0.1:5000/linearalgebra/api/v1.0/consistent', onloadMethod, onerrorMethod, myJSONString);
        makeXMLrequest('POST', 'https://mnitd.pythonanywhere.com/linearalgebra/api/v1.0/consistent', onloadMethod, onerrorMethod, myJSONString);
    };
};

//
// --------------------------------window.onscroll------------------------------
//
window.onscroll = function () {
    "use strict";
    var headerHeight = 90,
        scrolled = window.pageYOffset || document.documentElement.scrollTop;

    if (scrolled >= headerHeight) {
        document.getElementById("aside-menu").className = "aside-menu fixed";
    } else {
        document.getElementById("aside-menu").className = "aside-menu";
    }
}