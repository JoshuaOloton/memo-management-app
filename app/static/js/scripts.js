// search bars for title, description and reciever
function myFunction() {
    // Declare variables
    var title_input, descr_input, source_input, title_filter, descr_filter, source_filter, table, tr, td1, td2, td3, i, j,txtValue1, txtValue2, txtValue3;

    // obtain input fields by className
    title_input = document.getElementsByClassName("search_title")[0];
    descr_input = document.getElementsByClassName("search_descr")[0];
    source_input = document.getElementsByClassName("search_source")[0];

    // obtain search queries from each field
    title_filter = title_input.value.toUpperCase();
    descr_filter = descr_input.value.toUpperCase();
    source_filter = source_input.value.toUpperCase();
    table = document.getElementsByClassName("myTable")[0];
    tr = table.getElementsByTagName("tr");

    if (!title_filter && !descr_filter && !source_filter) {
      for (j = 2; j < tr.length; j++) {
        tr[j].style.display = "none";
      }
    }
  
    // for (j = 0; j < tr.length; j++) {
    //   tr[j].style.display = "none";
    // }
    
    // Loop through all table rows, and hide those who don't match the search query
    for (i = 1; i < tr.length; i++) {
      td1 = tr[i].getElementsByTagName("td")[0]; // index 0 SEARCHES the ITEMS columns
      td2 = tr[i].getElementsByTagName("td")[2];
      td3 = tr[i].getElementsByTagName("td")[4];
      if (td1 && td2 && td3) {
        txtValue1 = td1.textContent || td1.innerText;
        txtValue2 = td2.textContent || td2.innerText;
        txtValue3 = td3.textContent || td3.innerText;
        if (txtValue1.toUpperCase().indexOf(title_filter) > -1 && txtValue2.toUpperCase().indexOf(descr_filter) > -1 && txtValue3.toUpperCase().indexOf(source_filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }
    }
  }

// display only 5 records per row in home report page
function testFunction() {
  // alert("Page is loaded");  
  var tables, tr;
  let limit = 6;  // 6th row and upwards 
  tables = document.getElementsByClassName("test");
  for (let i = 0; i < tables.length; i++) {
    tr = tables[i].getElementsByTagName("tr");
    for (let j = limit; j < tr.length; j++) {
      tr[j].style.display = "none";
      
    }
  }
}

function send() {
var table = document.getElementById("get");
url = table.baseURI;
window.location = url;
console.log(url);
}


const OFFICES = {
  user1: 'CITM',
  user2: 'Bursary',
  user3: 'Rectory',
  user4: 'Registry',
  user5: 'Registry',
  user6: 'Rectory',
  user7: 'Bursary',
  user8: 'CITM',
  user9: 'CITM',
  user10: 'Bursary',
  user11: 'Rectory',
  user12: 'Registry',
}
const OFFICE_NAMES = ['CITM', 'Bursary', 'Rectory', 'Registry']


function set_login_office() {
  var usernameValue, inputText, usernameField, recieverField, c, no_options;

  usernameField = document.getElementById("username");
  recieverField = document.getElementById("reciever");
  usernameValue = usernameField.value;

  if (usernameValue in OFFICES) {
    no_options = recieverField.options.length;
    if (no_options > 0) {
      // using no of options, iterate through the select input field removing each existing option
      for (let j = 0; j < no_options; j++) {
        recieverField.remove(0);
      }
    }
    c = document.createElement("option");
    c.text = OFFICES[usernameValue];
    c.value = OFFICES[usernameValue];
    recieverField.add(c, 0);
  } else {
      // if usernameField value dowsnt match required entries, clear out selectfield options. it must be blank
      if (recieverField.options.length > 0) {
        no_options = recieverField.options.length;
        // using no of options, iterate through the select input field removingeach option
        for (let j = 0; j < no_options; j++) {
          recieverField.remove(0);
        }
      }
  }
}


function set_register_office() {
  var usernameValue, inputText, usernameField, recieverField, c, no_options;

  usernameField = document.getElementById("username");
  recieverField = document.getElementById("reciever");
  usernameValue = usernameField.value;

  if (usernameValue in OFFICES) {
    if (recieverField.options.length > 0) {
      no_options = recieverField.options.length;
      // using no of options, iterate through the select input field removing each option
      for (let j = 0; j < no_options; j++) {
        recieverField.remove(0);
      }
    } 
    c = document.createElement("option");
    c.text = OFFICES[usernameValue];
    c.value = OFFICES[usernameValue];
    recieverField.options.add(c, 0);
  }
  else {
    // if usernameField value dowsnt match required entries, clear out selectfield options. it must be blank
    if (recieverField.options.length > 0) {
      no_options = recieverField.options.length;
      // using no of options, iterate through the select input field removingeach option
      for (let j = 0; j < no_options; j++) {
        recieverField.remove(0);
      }
    }
  }
}