var aderr=document.getElementById('aderr')
var iderr=document.getElementById('iderr')
var codeerr=document.getElementById('codeerr')
function check(text,kind){
	if(text.value!='')return;
	// alert('不为空')
	if(kind=='area'){
		aderr.innerHTML='建议字段不可为空！'
		return;
	}
	if(kind=='text'){
		iderr.innerHTML='邮箱必填！--由于服务器原因，仅支持QQ邮箱'
		return;
	}
	codeerr.innerHTML='授权码必填！'
}
function checkSubmit(){
	var advice=document.getElementsByName("advice")[0]
	var id=document.getElementsByName('id')[0]
	var code=document.getElementsByName('adcode')[0]
	if(advice.value==''||id.value==''||code.value==''){
		alert("不可有字段为空！")
		return false
	}
	return true
}