function login(){

let email=document.getElementById("email").value
let password=document.getElementById("password").value

fetch("http://127.0.0.1:5000/login",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({

email:email,
password:password

})

})

.then(res=>res.json())

.then(data=>{

if(data.message==="Login successful"){

alert("Login Successful")

window.location.href="dashboard.html"

}
else{

document.getElementById("message").innerText=data.message

}

})

.catch(error=>{

console.log(error)

})

}