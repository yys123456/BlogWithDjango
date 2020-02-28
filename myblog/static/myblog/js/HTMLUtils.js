 function HTMLdecode(str){
	  	var tmp=document.createElement('div')
	  	tmp.innerHTML=str
	  	var ret=tmp.innerText
	  	return ret
}