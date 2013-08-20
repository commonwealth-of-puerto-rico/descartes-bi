
function fillDashMenu(iList, dashMenuParent){ 

	var mList = $(dashMenuParent).append('<ul class="dashMenuList"/>').find('ul',dashMenuParent);

	$(iList).each(function(index, element) {
		try{
						
			var gbItem = $(mList).append("<li class='dmItem'/>").find('.dmItem:last');
			if(this.title)
				$(gbItem).text(this.title);	
								
			if(this.icon)
				$(gbItem).attr("style","background-image:url("+ this.icon + ")");	
							
			if( this.hyperlink ){
				$(gbItem).append('<a/>');
				$('a',gbItem).attr("href",this.hyperlink);
			}
		}					
		catch(err){
			console.log(err.description);
		}
	});
}