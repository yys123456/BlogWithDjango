$('#input').focus(function(){
		display()
	}
)
 $('#input').blur(function(){
   		hide()
	}
)
function empty(){
	if($('#input').val()==''){
	    alert("恁要搜啥？(╯‵□′)╯︵┻━┻")
	    return false
	}else{
	    return true
	}
}

function display(){
	$('.bar').toggleClass('active');
}
function hide(){
	$('.active')[0].className='bar'
}