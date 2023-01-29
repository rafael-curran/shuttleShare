function addCancelButtons() {
    let cancelbuttons = document.querySelectorAll('#cancelbutton');
    cancelbuttons.forEach(element => element.addEventListener('click', function (event) {
        let rideId = event.target.value;
        let canceldata = new FormData();
        canceldata.append("rideId", rideId);
        fetch(('/cancel'), {
            "method": "POST",
            "body": canceldata,
        })
            .then(response => {
                if (response.redirected) {
                    window.location = response.url;
                } else {
                    console.log(response);
                }
            });


    }));
}
function getTrips() {
    let html = '';
    fetch(('/mytrips'), {
        "method": "POST"
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            console.log(typeof(data));
            for (row in data) {
                riders = data[row].riders;
                let riderhtml = '';
                for(rider in riders){
                    riderhtml += `<li class="list-group-item-dark">${riders[rider]}</li>`;
                }
                console.log(data[row]);
                console.log(typeof(data[row]));
                html += ` <tr>
              <th scope="row">${data[row].current.toString() + "/" + data[row].cap.toString()}</th>
              <td>${data[row].startloc}</td>
              <td>${data[row].departtime}</td>
              <td>${data[row].endloc}</td>
              <td><ol class="list-group list-group-numbered">${riderhtml}<ol></td>
              <td><button class="btn btn-danger" type="button" id="cancelbutton" value="${data[row].rideid}">Cancel</button></td>
            </tr>`;
            }
            document.querySelector('tbody').innerHTML = html;
            addCancelButtons();


            })}

getTrips();

