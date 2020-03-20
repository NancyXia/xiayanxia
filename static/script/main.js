function detectBrowser(){  //检测浏览器
	    var browser=navigator.appName;
        alert(browser);
		if(browser=="Microsoft Internet Explorer"){			
			jQuery.messager.alert('不兼容IE内核','请您切换到<span style="color:red">极速模式</span>打开该网站，暂时不兼容IE内核。','info');
		}        
}