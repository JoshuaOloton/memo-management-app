// search bars for title, description and reciever
function myFunction() {
    // Declare variables
    var title_input, descr_input, source_input, title_filter, descr_filter, source_filter, table, tr, td1, td2, td3, i, txtValue1, txtValue2, txtValue3;

    title_input = document.getElementsByClassName("search_title")[0];
    descr_input = document.getElementsByClassName("search_descr")[0];
    source_input = document.getElementsByClassName("search_source")[0];

    title_filter = title_input.value.toUpperCase();
    descr_filter = descr_input.value.toUpperCase();
    source_filter = source_input.value.toUpperCase();
    table = document.getElementsByClassName("myTable")[0];
    tr = table.getElementsByTagName("tr");
  
    // Loop through all table rows, and hide those who don't match the search query
    for (i = 1; i < tr.length; i++) {
      td1 = tr[i].getElementsByTagName("td")[0]; // index 0 SEARCHES the ITEMS columns
      td2 = tr[i].getElementsByTagName("td")[1];
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

// search bar for items alone
function myFunc() {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementsByClassName("search_item")[0];
  filter = input.value.toUpperCase();
  table = document.getElementsByClassName("myTable")[0];
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 1; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0]; // index 0 SEARCHES the ITEMS columns
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
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