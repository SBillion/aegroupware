(function(c){c.fn.extend({defaultValue:function(i,e){if("placeholder"in this[0])return false;var f=i||{},j=c.extend({defaultValue:f.defaultValue||null},f);return this.each(function(){if($(this).data("defaultValued"))return false;var a=$(this),k=j.value||a.attr("placeholder"),g={input:a};a.data("defaultValued",true);var d=function(){var b;if(a.context.nodeName.toLowerCase()=="input")b=c("<input />").attr({type:"text"});else if(a.context.nodeName.toLowerCase()=="textarea")b=c("<textarea />");else throw"DefaultValue only works with input and textareas"; b.attr({value:k,"class":a.attr("class")+" empty",size:a.attr("size"),style:a.attr("style"),tabindex:a.attr("tabindex"),name:"defaultvalue-clone-"+((1+Math.random())*65536|0).toString(16).substring(1)});b.focus(function(){b.hide();a.show();setTimeout(function(){a.focus()},1)});return b}();g.clone=d;d.insertAfter(a);var h=function(){if(a.val().length<=0){d.show();a.hide()}else{d.hide();a.show().trigger("click")}};a.bind("blur",h);h();e&&e(g)})}})})(jQuery); 