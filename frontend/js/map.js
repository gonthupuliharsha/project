// ---------------- GLOBAL VARIABLES ----------------
let map;
let mapLoaded = false;
let markers = [];
let allData = [];

// ---------------- ICON FUNCTION ----------------
function getIcon(type){

let iconClass = "fa-location-dot";
let bgColor = "#3b82f6";

if(type === "hospital"){
    iconClass = "fa-stethoscope";
    bgColor = "#ef4444";
}
else if(type === "school"){
    iconClass = "fa-book";
    bgColor = "#22c55e";
}
else if(type === "restaurant"){
    iconClass = "fa-utensils";
    bgColor = "#f59e0b";
}
else if(type === "pharmacy"){
    iconClass = "fa-pills";
    bgColor = "#8b5cf6";
}
else if(type === "college"){
    iconClass = "fa-graduation-cap";
    bgColor = "#0ea5e9";
}
else if(type === "clinic"){
    iconClass = "fa-plus";
    bgColor = "#14b8a6";
}
else if(type === "pg"){
    iconClass = "fa-house";
    bgColor = "#64748b";
}

return L.divIcon({
html: `
<div style="
    background:${bgColor};
    width:36px;
    height:36px;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    color:white;
    font-size:16px;
    box-shadow:0 4px 12px rgba(0,0,0,0.3);
">
<i class="fa-solid ${iconClass}"></i>
</div>
`,
className: ""
});
}

// ---------------- FETCH DATA ----------------
fetch("http://127.0.0.1:5000/facilities")
.then(res => res.json())
.then(data => {

    allData = data;

    // Enable buttons
    document.querySelectorAll('.card').forEach(c=>{
        c.classList.remove('disabled');
    });

})
.catch(err => {
    console.error("Error fetching data:", err);
});



// ---------------- MAIN FUNCTION ----------------
function selectFacility(event, type){

if(allData.length === 0){
    console.log("Data still loading...");
    return;
}

// Highlight card
document.querySelectorAll('.card').forEach(c=>c.classList.remove('active'));
event.currentTarget.classList.add('active');

// Show map
document.getElementById("map").style.display = "block";

// Init map once
if(!mapLoaded){
map = L.map('map').setView([17.6868, 83.2185], 12);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
maxZoom:19
}).addTo(map);

mapLoaded = true;
}

// Clear markers
markers.forEach(m => map.removeLayer(m));
markers = [];

// ✅ Dynamic heading
let heading = type.charAt(0).toUpperCase() + type.slice(1) + "s";
let listHTML = `<h3>${heading}</h3>`;

let count = 0;

// Loop data
allData.forEach(place => {

let facilityType = (place.amenity || place.type || "").toLowerCase().trim();
let lat = parseFloat(place.lat || place.latitude);
let lng = parseFloat(place.lon || place.lng || place.longitude);

if(isNaN(lat) || isNaN(lng)) return;

if(facilityType === type){

count++;

// Marker
let marker = L.marker([lat,lng],{icon:getIcon(type)})
.addTo(map)
.bindPopup(`<b>${place.name}</b>`);

marker.on('mouseover', ()=>marker.openPopup());
marker.on('mouseout', ()=>marker.closePopup());

markers.push(marker);

// List item with loading text
let currentId = count;   // ✅ FIX

listHTML += `
<div class="item" onclick="focusMap(${lat},${lng})">
<b>${place.name}</b><br>
<a href="https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(place.name)}+${lat},${lng}" 
target="_blank" 
style="color:#2563eb; text-decoration:none;">
📍 View on Google Maps
</a>
</div>
`;
}

});

// No data
if(count === 0){
listHTML += `<p style="color:red;">No facilities found for this category</p>`;
}

// Update UI
document.getElementById("facilityList").innerHTML = listHTML;
}

// ---------------- ZOOM FUNCTION ----------------
function focusMap(lat,lng){
if(map){
    map.setView([lat,lng],16);
}
}