;(function($){

	$.app = {
		dateFormatSingle: 'ddd d MMMM[ yyyy]',
		dateTimeFormatSingle: 'ddd d MMMM[ yyyy][, H:mm]{[ - H:mm]}',
		dateTimeFormatMultiple: 'ddd d MMMM[ yyyy][, H:mm] - {ddd d MMMM[ yyyy]}[{, H:mm}]',
		monthNames: ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Septembre','Octobre','Novembre','Décembre'],
		monthNamesShort: ['Janv.','Févr.','Mars','Avr.','Mai','Juin','Juil.','Août','Sept.','Oct.','Nov.','Déc.'],
		dayNames: ['Dimanche','Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi'],
		dayNamesShort: ['Dim','Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'],
	};
	
})(jQuery);


$(document).ready(function() {

	var userId = $("#sess_data").attr("userid");
	var date = new Date();
	var d = date.getDate();
	var m = date.getMonth();
	var y = date.getFullYear();

	calendar = $("#calendar").fullCalendar({
		theme: true,
		header: {
			left: 'prev,next today',
			center: 'title',
			right: 'month,agendaWeek,agendaDay'
		},
		titleFormat: {
			month: 'MMMM yyyy',
			week: "d[ MMMM][ yyyy]{ - d MMMM yyyy}",
			day: 'dddd d MMMM yyyy'
		},
		columnFormat: {
			month: 'ddd',
			week: 'ddd d',
			day: ''
		},
		timeFormat: {
			'': 'H:mm',
			agenda: 'H:mm{ - H:mm}'
		},
		axisFormat: 'H:mm',
		firstDay: 1,
		monthNames: $.app.monthNames,
		monthNamesShort: $.app.monthNamesShort,
		dayNames: $.app.dayNames,
		dayNamesShort: $.app.dayNamesShort,
		buttonText: {
			today: 'aujourd\'hui',
			month: 'mois',
			week: 'semaine',
			day: 'jour'
		},
		allDayText: 'journ\351e',
		allDaySlot: false,
		slotMinutes: 60,
		defaultEventMinutes: 60,
		firstHour: 8,
		minTime: 8,
		maxTime: 18,
		editable: (rights.change_event || rights.delete_event) ? true : false,
		selectable: rights.add_event ? true : false,
		selectHelper: true,
		aspectRatio: 1.8,
		defaultView: getPreviousView(),
		select: function(startDate, endDate, allDay) {
		
			if(allDay) {
				calendar.fullCalendar('unselect');
				return;
			}

			init_time = {
				'start': {
					'hours'	: startDate.getHours(),
					'minutes'	: startDate.getMinutes(),
					'object'	: new Date(startDate.getFullYear(), startDate.getMonth(), startDate.getDate(), startDate.getHours(), startDate.getMinutes(), 0)
				},
				'end': {
					'hours'	: endDate.getHours(),
					'minutes'	: endDate.getMinutes(),
					'object'	: new Date(endDate.getFullYear(), endDate.getMonth(), endDate.getDate(), endDate.getHours(), endDate.getMinutes(), 0)
				},
				'allDay': allDay,
			}
			$("#new_event #start_date").datepicker('setDate', startDate);
			$("#new_event #end_date").datepicker('setDate', endDate);
			$("#new_event #start_time").val($.fullCalendar.formatDate(init_time.start.object, 'H:mm'));
			$("#new_event #end_time").val($.fullCalendar.formatDate(init_time.end.object, 'H:mm'));

			// Store time used by duration.
			oldTime = init_time.start.object;

			$("#new_event").dialog("open");
		},
		eventDrop: function(calEvent, dayDelta, minuteDelta, allDay, revertFunc, jsEvent) {
			postdata = 'csrfmiddlewaretoken='+csrf_token+'&event_id='+calEvent.id+'&start='+calEvent.start.getTime();

			if(calEvent.end !== null)
				postdata += '&end='+calEvent.end.getTime();

			$.ajax({
				type: 'POST',
				url: '/planner/dateupdate/',
				data: postdata,
				dataType: 'json',
				success: function(ret){
					if(ret.error)
					{
						revertFunc();
					}
				}
			});
		},
		eventResize: function(calEvent, dayDelta, minuteDelta, revertFunc, jsEvent) {
			postdata = 'csrfmiddlewaretoken='+csrf_token+'&event_id='+calEvent.id+'&start='+calEvent.start.getTime();

			if(calEvent.end !== null)
				postdata += '&end='+calEvent.end.getTime();

			$.ajax({
				type: 'POST',
				url: '/planner/dateupdate/',
				data: postdata,
				dataType: 'json',
				success: function(ret){
					if(ret.error)
					{
						revertFunc();
					}
				}
			});
		},
		eventAfterRender: function(calEvent, jsEvent, view) {
			var dtFormat = $.app.dateTimeFormatMultiple;
			if(calEvent.end != null) {
				if(	calEvent.start.getFullYear() == calEvent.end.getFullYear() &&
					calEvent.start.getMonth() == calEvent.end.getMonth() &&
					calEvent.start.getDate() == calEvent.end.getDate())
					dtFormat = $.app.dateTimeFormatSingle;
			}
				
			var tooltip_text = "Places disponibles : " + calEvent.slots_available + "/" + calEvent.slots_max + "<br />";
			$tooltip = $("<div>" + tooltip_text + "</div>");
			$tooltipActions = $("<div class='tooltip_actions'></div>");
			$tooltipActions.data("event_id", calEvent.id);
			$tooltipActions.data("event_desc", calEvent.title);
			$tooltipActions.data("event_date", $.fullCalendar.formatDates(
				calEvent.start,
				calEvent.end,
				dtFormat,
				options = {
					monthNames: $.app.monthNames,
					monthNamesShort: $.app.monthNamesShort,
					dayNames: $.app.dayNames,
					dayNamesShort: $.app.dayNamesShort
				}
			));
			
			var selfRegBtn = userRegBtn = deleteBtn = false;
			if(!rights.change_event && !rights.delete_event && !rights.add_event)
				selfRegBtn = $("<span class='selfRegBtn tooltip-actions'>S'inscrire</span>");
			if(rights.delete_event) {
				deleteBtn = $("<span class='deleteBtn tooltip-actions'>Supprimer</span>");
				userRegBtn = $("<span class='userRegBtn tooltip-actions'>Inscrire un client</span>");
			}
			
			if(selfRegBtn !== false)
				appendAction(selfRegBtn, $tooltipActions);
			if(userRegBtn !== false)
				appendAction(userRegBtn, $tooltipActions);
			if(deleteBtn !== false)
				appendAction(deleteBtn, $tooltipActions);
				
			$tooltipActions.appendTo($tooltip);
			
			jsEvent
				.removeData('qtip') 
				.qtip({
					content: {
						text: $tooltip,
						title: {
							text: calEvent.type_str
						}
					},
					position: {
						my: 'bottom center',
						at: 'top center',
						adjust: {
							screen: 'flip'
						},
						corner: {
							target: 'topRight',
							tooltip: 'bottomLeft'
						}
					},
					show: {
						event: 'click mouseenter',
						solo: true
					},
					hide: {
						delay: 800,
						event: 'mouseleave',
						fixed: true
					},
					style: {
						classes: 'ui-tooltip-shadow ui-tooltip-jtools'
					}
				});
			
		}
	});

	calendar.fullCalendar('addEventSource', '/planner/source/all/'+userId);

	$(".fc-button-month, .fc-button-basicWeek, .fc-button-basicDay, .fc-button-agendaWeek, .fc-button-agendaDay").click(function(){
		var curView = calendar.fullCalendar('getView').name;
		$.cookie('calPreviousView', curView, { path: '/', expires: 10 });
	});

	$(".tooltip-actions").live('click', function(){
		if($(this).hasClass('selfRegBtn')){
			$.ajax({
				type: 'POST',
				url: '/planner/self_reg/',
				data: {
					csrfmiddlewaretoken: csrf_token,
					event_id: $(this).parent().attr('event_id')
				},
				dataType: 'json',
				success: function(ret){
					
				}
			});
		}
		else if($(this).hasClass('userRegBtn')){
			
			var dataBank = $(this).parent();
			$("#user_reg_dialog #event_id").val(dataBank.data("event_id"));
			$("#user_reg_dialog #urd_event_desc").html(dataBank.data("event_desc"));
			$("#user_reg_dialog #urd_event_date").html(dataBank.data("event_date"));
			$(this).closest('.qtip').qtip('hide');
			$("#user_reg_dialog").dialog('open');
			
		}
	});

	$("#new_event").dialog({
		dialogClass: 'common-dialog',
		autoOpen: false,
		height: 'auto',
		width: 650,
		resizable: false,
		draggable: false,
		modal: true,
		show: "slide",
		showOpt: {direction: 'up'},
		buttons: {
			"Annuler": function(){
				$(this).dialog("close");
			},
			"Ajouter l'événement": function(){
				var eventType = $(this).find("#event_type").val();
				postdata = 'csrfmiddlewaretoken='+csrf_token+'&type='+eventType+'&start='+init_time.start.object.getTime();

				if(init_time.end.object !== null)
					postdata += '&end='+init_time.end.object.getTime();

				alert('start: ' + init_time.start.object + '\nend: ' + init_time.end.object);
				return;

				var $dialog = $(this);
				$.ajax({
					type: 'POST',
					url: '/planner/addevent/',
					data: postdata,
					dataType: 'json',
					success: function(ret){
						if(ret.error)
						{
							alert(ret.error_msg);
						}
						else
						{
							calendar.fullCalendar('refetchEvents');
							$dialog.dialog("close");
						}
					}
				});
			}
		},
		open: function(){
			$(this).next().find('button').addClass('common-button');
			fillAvailableVehicles();
		}
	});
	
	$("#user_reg_dialog").dialog({
		dialogClass: 'common-dialog',
		autoOpen: false,
		height: 'auto',
		width: 450,
		resizable: false,
		draggable: false,
		modal: true,
		show: "slide",
		showOpt: {direction: 'up'},
		buttons: {
			"Annuler": function(){
				$(this).dialog("close");
			},
			"Inscrire ce client": function(){
				
				var $dialog = $(this);
				var user_id = $dialog.find('#users_list').val();
				var event_id = $dialog.find('#event_id').val();
				
				$.ajax({
					type: 'POST',
					url: '/planner/user_reg/',
					data: {
						csrfmiddlewaretoken: csrf_token,
						user_id: user_id,
						event_id: event_id
					},
					dataType: 'json',
					success: function(ret){
						$dialog.dialog("close");
					}
				});
			}
		},
		open: function(){
			$(this).next().find('button').addClass('common-button');
		}
	});

	$("#new_event #event_type")
		.selectmenu({
			style: 'dropdown',
			transferClasses: true,
			width: "160px",
			menuWidth: "auto"
		})
		.change(function(){
			var selected = $(this).val();
			if(default_limits[selected] == undefined) {
				$("#new_event #max_slots_cont").hide();
			}
			else {
				$("#new_event #max_slots_cont").show();
				$("#new_event #max_slots").text(default_limits[selected]);
			}
			manageNewEventOptionalFields(selected);
		})
		.trigger("change");

	$("#new_event #start_date").datepicker({
		showAnim: '',
		onClose: function(date){
			var date = $(this).datepicker("getDate");
			init_time.start.object.setFullYear(date.getFullYear());
			init_time.start.object.setMonth(date.getMonth());
			init_time.start.object.setDate(date.getDate());
		}
	});

	$("#new_event #end_date").datepicker({
		showAnim: '',
		onClose: function(date){
			var date = $(this).datepicker("getDate");
			init_time.end.object.setFullYear(date.getFullYear());
			init_time.end.object.setMonth(date.getMonth());
			init_time.end.object.setDate(date.getDate());
		}
	});

	$("#new_event #start_time, #new_event #end_time").timePicker({
		show24Hours: true,
		step: 60,
		startTime: "08:00",
		endTime: "17:00"
	});

	var oldTime = null;
	
	$("#new_event #start_time").change(function() {
		start_time = $.timePicker("#new_event #start_time").getTime();
		end_time = $.timePicker("#new_event #end_time").getTime();

		if($("#new_event #end_time").val()){
			var comp_time = new Date(2001, 0, 0, oldTime.getHours(), oldTime.getMinutes(), oldTime.getSeconds());
			var duration = (end_time - comp_time);
			// Calculate and update the time in the second input.
			$.timePicker("#new_event #end_time").setTime(new Date(new Date(start_time.getTime() + duration)));
			oldTime = start_time;

			end_time = $.timePicker("#new_event #end_time").getTime();
			init_time.end.object.setHours(end_time.getHours());
			init_time.end.object.setMinutes(end_time.getMinutes());
		}
		init_time.start.object.setHours(start_time.getHours());
		init_time.start.object.setMinutes(start_time.getMinutes());
		if(manageVehicle())
			fillAvailableVehicles();
	});
	
	$("#new_event #end_time").change(function(){
		end_time = $.timePicker("#new_event #end_time").getTime();
		init_time.end.object.setHours(end_time.getHours());
		init_time.end.object.setMinutes(end_time.getMinutes());
		if(manageVehicle())
			fillAvailableVehicles();
	});

});

function manageNewEventOptionalFields(type)
{
	if(manageVehicle())
		$("#selected_cars").show();
	else
		$("#selected_cars").hide();
}

function manageVehicle()
{
	var type = $("#new_event #event_type").val();
	switch(type)
	{
		case "code":
		case "code_exam":
			return false;
			
		case "driving":
		case "plateau":
		case "driving_exam":
		case "initial_circuit":
		case "medium_circuit":
		case "improvement_circuit":
			return true;
	}
}

function fillAvailableVehicles()
{
	$.ajax({
		type: 'GET',
		url: '/planner/vehicles/',
		data: {
			csrfmiddlewaretoken: csrf_token,
			start_time: init_time.start.object.getTime(),
			end_time: init_time.end.object.getTime(),
		},
		dataType: 'json',
		success: function(ret){
			if(ret.vehicles){
				$("#selected_cars_slt").empty();
				var options = '';
				$.each(ret.vehicles, function(key, vehicle){
					options += '<option value="' + vehicle.id + '">' + vehicle.description + '</option>';
				});
				$("#selected_cars_slt").html(options);
				$("#selected_cars_slt").multiselect2side('destroy');
				$("#selected_cars_slt").multiselect2side({
					moveOptions: false,
					labelsx: 'Disponibles',
					labeldx: 'S&eacute;lectionn&eacute;s'
				});
			}
		}
	});
}

function getPreviousView()
{
	var previousView = $.cookie('calPreviousView');
	if(previousView === null)
		previousView = 'agendaWeek';

	return previousView;
}

function checkAddPossible()
{
	
}

function appendAction(action, elem)
{
	if(elem.html() == "")
		$(action).appendTo(elem);
	else {
		$("<span class='tooltip-actions-separator'> | </span>").appendTo(elem);
		$(action).appendTo(elem);
	}
}
