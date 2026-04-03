let map = null;
let markers = [];
let clickMarker = null;

function initMap(lat=17.72, lng=83.30){

if(!map){

map = L.map('map').setView([lat,lng],12);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
maxZoom:19
}).addTo(map);

map.on("click", function(e){

let lat=e.latlng.lat;
let lng=e.latlng.lng;

document.getElementById("lat").value=lat.toFixed(6);
document.getElementById("lng").value=lng.toFixed(6);

if(clickMarker) map.removeLayer(clickMarker);

clickMarker=L.marker([lat,lng]).addTo(map).bindPopup("Selected").openPopup();
});
}
}

function analyze(){

let lat=parseFloat(document.getElementById("lat").value);
let lng=parseFloat(document.getElementById("lng").value);
let facility=document.getElementById("facility").value;

document.getElementById("result").innerHTML="Analyzing...";

fetch("http://127.0.0.1:5000/analyze",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
latitude:lat,
longitude:lng,
facility:facility
})
})
.then(res=>res.json())
.then(data=>{

markers.forEach(m=>map.removeLayer(m));
markers=[];

let html=`
<b>Status:</b> ${data.status}<br>
<b>Population:</b> ${data.population}<br>
<b>Reason:</b> ${data.reason}<br><br>
`;

if(data.existing_facilities.length>0){
html+="<b>Nearby Facilities:</b><br>";
data.existing_facilities.forEach(f=>{
html+=`${f.name} (${f.distance} km)<br>`;
});
}

if(data.suggestions.length>0){
html+="<br><b>Suggested Areas:</b><br>";
data.suggestions.forEach(s=>{
html+=`Lat:${s.lat}, Lng:${s.lon}<br>`;
});
}

document.getElementById("result").innerHTML=html;

})
.catch(()=>{
document.getElementById("result").innerHTML="Server error";
});
}