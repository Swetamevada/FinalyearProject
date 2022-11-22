$(function($){
	'use strict';

/*
|----------------------------------------------------------------------------
|  search form
|----------------------------------------------------------------------------
*/
var SerarchForm = document.getElementById('search-form');
if (SerarchForm !== null){
	function classReg( className ) {
	  return new RegExp("(^|\\s+)" + className + "(\\s+|$)");
	}
	// classList support for class management
	// altho to be fair, the api sucks because it won't accept multiple classes at once
	var classCheck, classAdding, classRemoving;

	if ( 'classList' in document.documentElement ) {
	  classCheck = function( elem, c ) {
	    return elem.classList.contains( c );
	  };
	  classAdding = function( elem, c ) {
	    elem.classList.add( c );
	  };
	  classRemoving = function( elem, c ) {
	    elem.classList.remove( c );
	  };
	}
	else {
	  classCheck = function( elem, c ) {
	    return classReg( c ).test( elem.className );
	  };
	  classAdding = function( elem, c ) {
	    if ( !classCheck( elem, c ) ) {
	      elem.className = elem.className + ' ' + c;
	    }
	  };
	  classRemoving = function( elem, c ) {
	    elem.className = elem.className.replace( classReg( c ), ' ' );
	  };
	}

	function toggleClass( elem, c ) {
	  var fn = classCheck( elem, c ) ? classRemoving : classAdding;
	  fn( elem, c );
	}

	var classie = {
	  // full names
	  classCheck: classCheck,
	  classAdding: classAdding,
	  classRemoving: classRemoving,
	  toggleClass: toggleClass,
	  // short names
	  has: classCheck,
	  add: classAdding,
	  remove: classRemoving,
	  toggle: toggleClass
	};

	// transport
	if ( typeof define === 'function' && define.amd ) {
	  // AMD
	  define( classie );
	} else {
	  // browser global
	  window.classie = classie;
	}
	// get vars
	var searchEl = document.querySelector("#input");
	var labelEl = document.querySelector("#label");

	// register clicks and toggle classes
	labelEl.addEventListener("click",function(){
		if (classie.has(searchEl,"focus")) {
			classie.remove(searchEl,"focus");
			classie.remove(labelEl,"active");
		} else {
			classie.add(searchEl,"focus");
			classie.add(labelEl,"active");
		}
	});

	// register clicks outisde search box, and toggle correct classes
	document.addEventListener("click",function(e){
		var clickedID = e.target.id;
		if (clickedID != "search-terms" && clickedID != "search-label") {
			if (classie.has(searchEl,"focus")) {
				classie.remove(searchEl,"focus");
				classie.remove(labelEl,"active");
			}
		}
	});
}

/*
|----------------------------------------------------------------------------
|  Revolution Slider
|----------------------------------------------------------------------------
*/ 
	var revapi;	
	revapi = jQuery("#rev_slider_1").revolution({
		sliderType:"standard",
	    sliderLayout:"auto",
	    fullScreenOffsetContainer:"#header",
		responsiveLevels:[4096,1400,992,768],
		delay:9000,
		navigation: {
			touch:{
				touchenabled:"on",
				swipe_threshold: 75,
				swipe_min_touches: 1,
				swipe_direction: "horizontal",
				drag_block_vertical: false
			},
			arrows:{
			    enable:false
			},
			bullets:{
				enable:true
			}			
		},			
		gridwidth:[1140,1140,720,320],
		gridheight:[700,700,500,500]		
	});

/*
|----------------------------------------------------------------------------
|   isotop gallery JS
|----------------------------------------------------------------------------
*/
	jQuery(window).on("load resize",function(e){
		var $container = $('.isotope'),
		colWidth = function () {
			var w = $container.width(), 
			columnNum = 1,
			columnWidth = 0;
		//Select what will be your porjects columns according to container widht
		if (w > 1040)     { columnNum  = 3; }  
		else if (w > 850) { columnNum  = 3; }  
		else if (w > 768) { columnNum  = 1; }  
		else if (w > 480) { columnNum  = 1; }
		else if (w > 300) { columnNum  = 1; }
		columnWidth = Math.floor(w/columnNum);

		//Default item width and height
		$container.find('.grid-item').each(function() {
			var $item = $(this), 
			width = columnWidth-0;
			$item.css({ width: width});
		}); 
		return columnWidth;
	},
	isotope = function () {
		$container.isotope({
			resizable: true,
			itemSelector: '.grid-item',
			masonry: {
				columnWidth: colWidth(),
				layoutMode: 'fitRows',
				gutterWidth: 10
			}
		});
	};
	isotope(); 

		// bind filter button click
		$('.isotope-filters').on( 'click', 'button', function() {
			var filterValue = $( this ).attr('data-filter');
			$container.isotope({ filter: filterValue });
		});

		$('.isotope-filters button').on('click',function(){
			$('.isotope-filters button').removeClass('active');
			$(this).addClass('active');
		});
	});

	jQuery(window).on("load resize",function(e){
		var $container = $('.isotope2'),
		colWidth = function () {
			var w = $container.width(), 
			columnNum = 1,
			columnWidth = 0;
		//Select what will be your porjects columns according to container widht
		if (w > 1040)     { columnNum  = 2; }  
		else if (w > 850) { columnNum  = 2; }  
		else if (w > 768) { columnNum  = 1; }  
		else if (w > 480) { columnNum  = 1; }
		else if (w > 300) { columnNum  = 1; }
		columnWidth = Math.floor(w/columnNum);

		//Default item width and height
		$container.find('.grid-item').each(function() {
			var $item = $(this), 
			width = columnWidth-0;
			$item.css({ width: width});
		}); 
		return columnWidth;
	},
	isotope = function () {
		$container.isotope({
			resizable: true,
			itemSelector: '.grid-item',
			masonry: {
				columnWidth: colWidth(),
				layoutMode: 'fitRows',
				gutterWidth: 10
			}
		});
	};
	isotope(); 

		// bind filter button click
		$('.isotope-filters').on( 'click', 'button', function() {
			var filterValue = $( this ).attr('data-filter');
			$container.isotope({ filter: filterValue });
		});

		$('.isotope-filters button').on('click',function(){
			$('.isotope-filters button').removeClass('active');
			$(this).addClass('active');
		});
	});

/*
|----------------------------------------------------------------------------
|   counter JS
|----------------------------------------------------------------------------
*/
    $('.counter').counterUp({
        delay: 10,
        time: 1000
    });

/*
|----------------------------------------------------------------------------
|   MAGNIFIC JS
|----------------------------------------------------------------------------
*/
	$('.image-large').magnificPopup({
		type: 'image',
		 gallery:{
		    enabled:true
		  }
	});
	
	$('.play-video').magnificPopup({
		type: 'iframe'
	});
	
	$.extend(true, $.magnificPopup.defaults, {
    iframe: {
        patterns: {
           youtube: {
              index: 'youtube.com/', 
              id: 'v=', 
              src: 'http://www.youtube.com/embed/%id%?autoplay=1' 
          }
        }
    }
	});
/*
|----------------------------------------------------------------------------
|   masonry JS
|----------------------------------------------------------------------------
*/
	$('.masonry').masonry({
	  // options...
	  itemSelector: '.m-item'
	});
	
/*
|----------------------------------------------------------------------------
|  	Ajax Contact Form
|----------------------------------------------------------------------------
*/
	function isValidEmail(emailAddress) {
	var pattern = new RegExp(/^(("[\w-\s]+")|([\w-]+(?:\.[\w-]+)*)|("[\w-\s]+")([\w-]+(?:\.[\w-]+)*))(@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$)|(@\[?((25[0-5]\.|2[0-4][0-9]\.|1[0-9]{2}\.|[0-9]{1,2}\.))((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\.){2}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\]?$)/i);

		return pattern.test(emailAddress);

	};
	$(".form-common").on('submit', function(e) {
		e.preventDefault();
		var data = {
			name: $("#name").val(),
			email: $("#email").val(),
			phone: $("#phone").val(),
			subject: $("#subject").val(),
			message: $("#message").val()
		};

		if (isValidEmail(data['email']) && (data['message'].length > 1) && (data['name'].length > 1) ) {
			$.ajax({
				type: "POST",
				url: "sendmail.php",
				data: data,
				success: function() {
					$('.form-common .input-success').delay(500).fadeIn(1000);
					$('.form-common .input-error').fadeOut(500);
				}
			});
		} else {
			$('.form-common .input-error').delay(500).fadeIn(1000);
			$('.form-common .input-success').fadeOut(500);
		}

		return false;
	});
	
}(jQuery));