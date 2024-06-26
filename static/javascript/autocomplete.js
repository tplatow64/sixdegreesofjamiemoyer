function autocomplete(inp, hidden_inp, id_name, arr) {
    /*the autocomplete function takes four arguments,
    the text field element, the hidden element and an array of possible autocompleted values:*/
    var currentFocus;
    var maxMatches = 25;
    /*execute a function when someone writes in the text field:*/
    inp.addEventListener("input", function(e) {
        var a, b, i, val = this.value;
        /*close any already open lists of autocompleted values*/
        val = val.replace("'", "&apos;");
        closeAllLists();
        if (!val) { return false;}
        currentFocus = -1;
        /*create a DIV element that will contain the items (values):*/
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        /*append the DIV element as a child of the autocomplete container:*/
        this.parentNode.appendChild(a);
        /*for each item in the array...*/
        var matchesFound = 0;
        for (i = 0; i < arr.length; i++) {
          /*check if the item starts with the same letters as the text field value:*/
          var regex = val.toUpperCase().replace(/\./g, '\\.')
          if (arr[i]['name'].toUpperCase().search(regex)>=0 && matchesFound < maxMatches) {
            /*pos = arr[i]['name'].toUpperCase().search(val.toUpperCase())  for bolding*/
            /*create a DIV element for each matching element:*/
            b = document.createElement("DIV");
            b.innerHTML = arr[i]['name']
            /*insert a input field that will hold the current array item's value:*/
            arr[i]['name'] = arr[i]['name'].replace("'", "&apos;");
            b.innerHTML += "<input type='hidden' value='" + arr[i]['name'] + "'>";
            b.innerHTML += "<input type='hidden' value='" + arr[i][id_name] + "'>";
            /*execute a function when someone clicks on the item value (DIV element):*/
            b.addEventListener("click", function(e) {
                /*insert the value for the autocomplete text field:*/
                /* alert(this.getElementsByTagName("input")[0].value);*/
                inp.value = this.getElementsByTagName("input")[0].value;
                hidden_inp.value = this.getElementsByTagName("input")[1].value;
                document.getElementById("submitButton").disabled=false;
                /*close the list of autocompleted values,
                (or any other open lists of autocompleted values:*/
                closeAllLists();
            });
            a.appendChild(b);
            matchesFound++;
          }else if(matchesFound >= maxMatches){
            break;
          }
        }
    });
    /*execute a function presses a key on the keyboard:*/
    inp.addEventListener("keydown", function(e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
          /*If the arrow DOWN key is pressed,
          increase the currentFocus variable:*/
          currentFocus++;
          /*and and make the current item more visible:*/
          addActive(x);
        } else if (e.keyCode == 38) { //up
          /*If the arrow UP key is pressed,
          decrease the currentFocus variable:*/
          currentFocus--;
          /*and and make the current item more visible:*/
          addActive(x);
        } else if (e.keyCode == 13) {
          /*If the ENTER key is pressed, prevent the form from being submitted,*/
          e.preventDefault();
          // if(a.children.length !== 1){ // more than 1 player in list
            
          // }else{ // only 1 player in list
          //   currentFocus = 0;
          //   if (x) x[currentFocus].click();
          //   document.getElementById("find_player").submit();
          // }
          
          
          if (currentFocus > -1) {
            /*and simulate a click on the "active" item:*/
            if (x) x[currentFocus].click();
          }
        }
    });
    function addActive(x) {
      /*a function to classify an item as "active":*/
      if (!x) return false;
      /*start by removing the "active" class on all items:*/
      removeActive(x);
      if (currentFocus >= x.length) currentFocus = 0;
      if (currentFocus < 0) currentFocus = (x.length - 1);
      /*add class "autocomplete-active":*/
      x[currentFocus].classList.add("autocomplete-active");
    }
    function removeActive(x) {
      /*a function to remove the "active" class from all autocomplete items:*/
      for (var i = 0; i < x.length; i++) {
        x[i].classList.remove("autocomplete-active");
      }
    }
    function closeAllLists(elmnt) {
      /*close all autocomplete lists in the document,
      except the one passed as an argument:*/
      var x = document.getElementsByClassName("autocomplete-items");
      for (var i = 0; i < x.length; i++) {
        if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function (e) {
      closeAllLists(e.target);
  });
  }