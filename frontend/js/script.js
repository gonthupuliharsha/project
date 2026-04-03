var map = L.map('map').setView([17.6868,83.2185],12);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
maxZoom:19
}).addTo(map);

function loadFacilities(){

fetch("http://127.0.0.1:5000/facilities")

.then(res=>res.json())

.then(data=>{

data.forEach(place=>{

if(place.latitude && place.longitude){

L.marker([place.latitude,place.longitude])
.addTo(map)
.bindPopup(place.name)

}

})

})

}