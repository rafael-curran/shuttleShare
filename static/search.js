function addJoinButtons() {
  let joinbuttons = document.querySelectorAll('#joinbutton');
  joinbuttons.forEach(element => element.addEventListener('click', function (event) {
    let rideid = event.target.value;
    let joindata = new FormData();
    joindata.append("rideid", rideid);
    fetch(('/join'), {
      "method": "POST",
      "body": joindata,
    })
      .then(response => {
        if (response.redirected) {
          window.location = response.url
        } else {
          console.log(response);
        }
      });

  }));
}

let searchForm = document.querySelector('#searchform');
searchForm.addEventListener('submit', function (event) {
  event.preventDefault();
  console.log('button clicked');
  let startloc = document.querySelector("#starting");
  let endloc = document.querySelector("#destination");
  let departime = document.querySelector("#departure-datetime");


  if (!document.querySelector("#searchform").checkValidity()) {
    event.preventDefault()
    event.stopPropagation()
    document.querySelector("#searchform").classList.add('was-validated')
    return;
  }


  let data = new FormData();
  let html = '';
  startloc = startloc.value.replace(/'/g, '');
  endloc = endloc.value.replace(/'/g, '');
  departime = departime.value;
  data.append("startloc", startloc)
  data.append("endloc", endloc)
  data.append("departime", departime)
  fetch(('/search'), {
    "method": "POST",
    "body": data,
  })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      const td = new Date();
      for (row of data) {
        const d = new Date(row.departtime);
        html += ` <tr>
                  <th scope="row">${row.current.toString() + "/" + row.cap.toString()}</th>
                  <td>${row.startloc}</td>
                  <td>${row.departtime}</td>
                  <td>${row.endloc}</td>
                  <td><button class="btn btn-success" type="button" id="joinbutton" value="${row.rideid}" ${row.current == row.cap || d < td ? "disabled" : ''}>Join</button></td>
                </tr>`;
      }
      if (!html) {
        html = `<div class="container-fluid"><p class="lead">No rides were found for these search conditions. If you are unable to find an existing ride, you are welcome to <a href="/create">Create a New Ride</a>. </p>
        </div>`
      }
      document.querySelector('tbody').innerHTML = html;
      addJoinButtons();
      event.preventDefault();
      return;
    });
});
