
  let subject_select = document.getElementById("subject");
  let argument_select = document.getElementById("coverage");

  subject_select.onchange = function () {

      fetch('arguments').then(function (response) {

          response.json().then(function (data) {
              let optionHTML = '';

              if(data[subject_select.value] !== undefined){
                for(let argument of data[subject_select.value]){
                    optionHTML += '<option value="' + argument + '">' + argument + '</option>>';
                }
              }else{
                optionHTML += '<option value=""></option>'
              }

              argument_select.innerHTML = optionHTML;
          })

      });

  }

