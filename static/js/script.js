$(document).ready(function () {
	var isCETRegNo = /^1\d{2}1106\d{3}$/
	var isNumber = /^\d{0,9}$/
	var isName = /^[a-zA-Z ]+$/

	var profile = $("#profileSection")
	var detailsSection = $("#detailsSection")

	$("#download-results").hide()

	profile.hide()
	detailsSection.hide()

	function hideStuff() {
		console.log("Non CET Registration Number or Invalid Name")
		input.bind()
		profile.fadeOut(500)
		detailsSection.fadeOut(500)
	}

	var userInput = $("#userInput")
	var students = new Bloodhound({
		datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
		queryTokenizer: Bloodhound.tokenizers.whitespace,
		remote: {
			url: '/%QUERY',
			wildcard: '%QUERY',
			transform: function (response) {
				data = response.students
				queriedStudentList = []
				for (var i = 0; i < data.length; i++) {
					queriedStudentList.push({
						value: data[i].regno,
						tokens: [data[i].name, data[i].regno],
						name: data[i].name,
						batch: data[i].batch,
						branch: data[i].branch,
						regno: data[i].regno
					})
				}
				return queriedStudentList
			}
		}
	})


	userInput.typeahead({
		hint: false,
		highlight: true
	},
		{
			name: 'students',
			limit: 10,
			display: 'value',
			source: students.ttAdapter(),
			templates: {
				notFound: Handlebars.compile('<div class="notFound">No student found with name: <strong>{{query}}</strong></div>'),
				suggestion: Handlebars.compile('<div>{{value}} - {{name}} - {{branch}} [{{batch}}]</div>')
			}
		})
	// beginning of advanced
	var advanced_tab = document.getElementById("advanced")

	$("#advanced").click(function (e) {
		$.getJSON("/advanced", function (data) {
			if ($('#branch_dropdown li').length == 0) {
				data.branch.forEach(function (element, index) {
					$("#branch_dropdown").append('<li style="text-align: center;"  class="mdl-menu__item selected" data-val="' + element.code + '">' + element.branch + '</li>')
					$(".selected").click(function(e){
						$(".mdl-layout__header-row").click()
					})
				})
			}Array
			if ($('#batch_dropdown li').length == 0) {
				data.batch.forEach(function (element, index) {
					$("#batch_dropdown").append('<li style="text-align: center;"  class="mdl-menu__item selected" data-val="' + element.year + '">' + element.year + '</li>')
					$(".selected").click(function(e){
						$(".mdl-layout__header-row").click()
					})
				})
			}
			if ($('#sem_dropdown li').length == 0) {
				$("#sem_dropdown").append('<li style="text-align: center;" class="mdl-menu__item selected" data-val="0">CGPA</li>')
				$(".selected").click(function(e){
					$(".mdl-layout__header-row").click()
				})
				data.semester.forEach(function (element, index) {
					$("#sem_dropdown").append('<li style="text-align: center;" class="mdl-menu__item selected" data-val="' + element.semester.slice(-1) + '">' + element.semester + '</li>')
					$(".selected").click(function(e){
						$(".mdl-layout__header-row").click()
					})
				})
			}
			getmdlSelect.init(".getmdl-select")
			componentHandler.upgradeDom()
			console.log(data)
		})
	})
	$("#view-results").click(function (e) {$("#advanced").click(function (e) {
		$.getJSON("/advanced", function (data) {
			if ($('#branch_dropdown li').length == 0) {
				data.branch.forEach(function (element, index) {
					$("#branch_dropdown").append('<li style="text-align: center;"  class="mdl-menu__item selected" data-val="' + element.code + '">' + element.branch + '</li>')
					$(".selected").click(function(e){
						$(".mdl-layout__header-row").click()
					})
				})
			}
			if ($('#batch_dropdown li').length == 0) {
				data.batch.forEach(function (element, index) {
					$("#batch_dropdown").append('<li style="text-align: center;"  class="mdl-menu__item selected" data-val="' + element.year + '">' + element.year + '</li>')
					$(".selected").click(function(e){
						$(".mdl-layout__header-row").click()
					})
				})
			}
			if ($('#sem_dropdown li').length == 0) {
				$("#sem_dropdown").append('<li style="text-align: center;" class="mdl-menu__item selected" data-val="0">CGPA</li>')
				$(".selected").click(function(e){
					$(".mdl-layout__header-row").click()
				})
				data.semester.forEach(function (element, index) {
					$("#sem_dropdown").append('<li style="text-align: center;" class="mdl-menu__item selected" data-val="' + element.semester.slice(-1) + '">' + element.semester + '</li>')
					$(".selected").click(function(e){
						$(".mdl-layout__header-row").click()
					})
				})
			}
			getmdlSelect.init(".getmdl-select")
			componentHandler.upgradeDom()
			console.log(data)
		})
	})
		var postdata = { branch: $('#branch_list').attr("data-val"), batch: $('#batch_list').attr("data-val"), semester: $('#sem_list').attr("data-val") }
		var downloadFileName = postdata.batch+"-"+postdata.branch+"-"+postdata.semester+".csv"
		console.log(postdata)
		$("#download-results").show()
		$.post("/advanced/results/", postdata, function (response) {
			// $("#bulkDetailsSection").append('<a href="raw/results.csv" download="'+downloadFileName+'"> Download </a>')
			details = $("#bulkDetailsSection").find("tbody")
			details.empty()

			details.append('<th class="mdl-cell--3-col">#</th><th class="mdl-data-table__cell--non-numeric mdl-cell--6-col">Name</th><th class="mdl-cell--3-col">Roll</th><th class="mdl-cell--3-col">SGPA</th>')
			console.log(response)
			var ctr = 1
			response.students.forEach(function (data, index) {
				if (ctr % 2)
					details.append("<tr><td>" + ctr + "</td><td class='mdl-data-table__cell--non-numeric'>" + data.name + "</td><td>" + data.student_id + "</td><td>" + data.sgpa + "</td></tr>")
				else
					details.append("<tr style='background-color: rgba(30, 115, 115, 0.19);'><td>" + ctr + "</td><td class='mdl-data-table__cell--non-numeric'>" + data.name + "</td><td>" + data.student_id + "</td><td>" + data.sgpa + "</td></tr>")
				ctr++;
			})
			for(var  i = 0; i < 10; i++)
				details.append("<tr><td> </td></tr>")
			details.append("<tr class='downloadrow'><td colspan='100%' style='text-align:center;'><a style='color:#ffffff' href='raw/results.csv' download='" + downloadFileName + "'> Download </a></td></tr>")
		}, 'json')
	})
	// end of advanced

	// beginning of internal
	$("#internal").click(function (e) {
		$.getJSON("/internal", function (data) {
			if ($('#i_branch_dropdown li').length == 0) {
				data.branch.forEach(function (element, index) {
					$("#i_branch_dropdown").append('<li style="text-align: center;"  class="mdl-menu__item selected" data-val="' + element.code + '">' + element.branch + '</li>')
					$(".selected").click(function(e){
						$(".mdl-layout__header-row").click()
					})
				})
			}
			if ($('#i_batch_dropdown li').length == 0) {
				data.batch.forEach(function (element, index) {
					$("#i_batch_dropdown").append('<li style="text-align: center;"  class="mdl-menu__item selected" data-val="' + element.year + '">' + element.year + '</li>')
					$(".selected").click(function(e){
						$(".mdl-layout__header-row").click()
					})
				})
			}
			if ($('#i_sem_dropdown li').length == 0) {
				data.semester.forEach(function (element, index) {
					$("#i_sem_dropdown").append('<li style="text-align: center;" class="mdl-menu__item selected" data-val="' + element.semester.slice(-1) + '">' + element.semester + '</li>')
					$(".selected").click(function(e){
						$(".mdl-layout__header-row").click()
					})
				})
			}
			getmdlSelect.init(".getmdl-select")
			componentHandler.upgradeDom()
			console.log(data)
		})
	})
	$("#generate_internal_form").click(function (e) {$("#internal").click(function (e) {
		$.getJSON("/internal", function (data) {
			if ($('#i_branch_dropdown li').length == 0) {
				data.branch.forEach(function (element, index) {
					$("#i_branch_dropdown").append('<li style="text-align: center;"  class="mdl-menu__item selected" data-val="' + element.code + '">' + element.branch + '</li>')
					$(".selected").click(function(e){
						$(".mdl-layout__header-row").click()
					})
				})
			}
			if ($('#i_batch_dropdown li').length == 0) {
				data.batch.forEach(function (element, index) {
					$("#i_batch_dropdown").append('<li style="text-align: center;"  class="mdl-menu__item selected" data-val="' + element.year + '">' + element.year + '</li>')
					$(".selected").click(function(e){
						$(".mdl-layout__header-row").click()
					})
				})
			}
			if ($('#i_sem_dropdown li').length == 0) {
				data.semester.forEach(function (element, index) {
					$("#i_sem_dropdown").append('<li style="text-align: center;" class="mdl-menu__item selected" data-val="' + element.semester.slice(-1) + '">' + element.semester + '</li>')
					$(".selected").click(function(e){
						$(".mdl-layout__header-row").click()
					})
				})
			}
			getmdlSelect.init(".getmdl-select")
			componentHandler.upgradeDom()
			console.log(data)
		})
	})
		var postdata = { branch: $('#i_branch_list').attr("data-val"), batch: $('#i_batch_list').attr("data-val"), semester: $('#i_sem_list').attr("data-val") }
		var downloadFileName = postdata.batch+"-"+postdata.branch+"-"+postdata.semester+".csv"
		console.log(postdata)
		$("#download-results").show()
		$.post("/internal/display/", postdata, function (response) {
			// $("#bulkDetailsSection").append('<a href="raw/results.csv" download="'+downloadFileName+'"> Download </a>')
			details = $("#i_bulkDetailsSection").find("tbody")
			details.empty()

			details.append('<th class="mdl-cell--3-col">#</th><th class="mdl-data-table__cell--non-numeric mdl-cell--6-col">Name</th><th class="mdl-cell--3-col">Roll</th><th class="mdl-cell--3-col">Marks</th>')
			console.log(response)
			var ctr = 1
			response.students.forEach(function (data, index) {
				if (ctr % 2)
					details.append("<tr><td>" + ctr + "</td><td class='mdl-data-table__cell--non-numeric'>" + data.name + "</td><td>" + data.student_id + "</td><td style='text-align: center;'><input class='mark-entry' id='"+ data.student_id +"'type='number'/></td></tr>")
				else
					details.append("<tr style='background-color: rgba(30, 115, 115, 0.19);'><td>" + ctr + "</td><td class='mdl-data-table__cell--non-numeric'>" + data.name + "</td><td>" + data.student_id + "</td><td style='text-align: center;'><input class='mark-entry' id='"+ data.student_id +"' type='number'/></td></tr>")
				ctr++;
			})
				$(".mark-entry").keyup(function(e){
					var z = e.currentTarget.id;
					var score = $("#"+z).val()
					if(0 <= score && score < 6){
						$("#"+z).css({ 'color': 'red'});
					}
					else if(score >= 6 && score < 11){
						$("#"+z).css({ 'color': 'blue'});
					}
					else{
						$("#"+z).css({ 'color': 'green'});
					}
				})
			for(var  i = 0; i < 10; i++)
				details.append("<tr><td> </td></tr>")
			details.append("<tr class='downloadrow'><td colspan='100%' style='text-align:center;'><a style='color:#ffffff' href='raw/results.csv' download='" + downloadFileName + "'> Download </a></td></tr>")
		}, 'json')
	})

	var subject_list = new Bloodhound({
		datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
		queryTokenizer: Bloodhound.tokenizers.whitespace,
		remote: {
			url: '/internal/subjects/',
			prepare: function (query, settings) {
				settings.type = "POST";
				settings.contentType = "application/json;";
        		settings.dataType = 'json',
				settings.data = JSON.stringify({ subject : query});
				return settings;
			},
			transform: function(response) {
				data = response.subject_list
				final_sub_list = []
				for(var i = 0; i < data.length; i++){
					final_sub_list.push({name : data[i].name, code: data[i].code})
				}
				return final_sub_list
			}
		}
	})

	$("#subjectInput").typeahead({
		hint: false,
		highlight: true
	},
	{
		name: 'subject_list',
		limit: 100,
		display: 'name',
		source: subject_list.ttAdapter(),
		templates: {
			notFound: Handlebars.compile('<div class="notFound">No subject found with name: <strong>{{query}}</strong></div>'),
			suggestion: Handlebars.compile('<div>{{name}} - {{code}}</div>')
		}
	})
	
	// $("#subjectInput").keyup(function(e){
	// 	var partial_subs = { subject : $("#subjectInput").val()}
	// 	// $.post("/internal/subjects/", partial_subs, function (response) {
	// 	// 	console.log(response)
	// 	// 	raw_subject_data = response
	// 	// })
	// })

	// end of internal

	function getDetails(regno) {
		$.getJSON("/" + regno, function (data) {
			if (data == null) {
				hideStuff()
			}

			profile.show(700)
			detailsSection.show(700)

			profile.find("#name").html(data.name)
			profile.find("#batch").html(data.batch)
			profile.find("#branch").html(data.branch)
			profile.find("#regno").html(data.regno)

			downloadFileName = data.regno + ".csv"
			console.log(data)

			details = detailsSection.find("tbody")
			details.html("")

			var credits = 0
			var sumofproducts = 0

			data.semesters.forEach(function (element, index) {
				credits += element.credits
				sumofproducts += element.credits * element.sgpa;
				details.append("<tr class='mdl-color--primary-dark semrow'><td colspan='100%' style='text-align:center;'><a style='color:#ffffff' href='" + element.path + "' target='new'>Semester " + element.sem.slice(-1) + " <i class='material-icons' id='open_icon'>open_in_new</i></a></td></tr>")
				details.append('<th class="mdl-data-table__cell--non-numeric mdl-cell--6-col">Subject</th><th class="mdl-cell--3-col">Credits</th><th class="mdl-cell--3-col">Grade</th>')

				var ctr = 1;
				element.subjects.forEach(function (subject, index) {
					if (ctr % 2)
						details.append("<tr><td class='mdl-data-table__cell--non-numeric'>" + subject.name + "</td><td>" + subject.credits + "</td><td>" + subject.grade + "</td></tr>")
					else
						details.append("<tr style='background-color: rgba(30, 115, 115, 0.19);'><td class='mdl-data-table__cell--non-numeric'>" + subject.name + "</td><td>" + subject.credits + "</td><td>" + subject.grade + "</td></tr>")
					ctr++;
				})
				details.append("<tr class='mdl-color--primary-dark semrow'><td class='mdl-data-table__cell--non-numeric' style='text-align:left'><div> Credits : Sgpa </div></td><td>" + element.credits + "</td><td colspan='98%'>" + element.sgpa + "</td></tr>")

			})

			var cgpa = sumofproducts / credits
			details.append("<tr id='cgpa' class='mdl-color--primary-dark semrow'><td class='mdl-data-table__cell--non-numeric'>CGPA</td><td>" + credits + "</td><td colspan='98%'>" + Math.round(cgpa * 100) / 100 + "</td></tr>")
			for(var  i = 0; i < 10; i++)
				details.append("<tr><td> </td></tr>")
			details.append("<tr class='downloadrow'><td colspan='100%' style='text-align:center;'><a style='color:#ffffff' href='raw/results.csv' download='" + downloadFileName + "'> Download </a></td></tr>")

			input.blur();
			var scroller = document.getElementById("profileSection");
			scroller.scrollIntoView();
			scroller.focus();
			scroller.blur();


			$("#hide").click(function (e) {
				console.log("Gonna hide", data.regno)
				$.getJSON("/hide/" + data.regno, function (data) {
					alert(data.message)
				})
			})

			$("#btn2").click(function (e) {
				$.getJSON("/hide_data/" + data.regno, function (button_text) {
					var hide_button = document.getElementById("hide")
					hide_button.innerText = button_text.visible_message
					console.log(button_text)
				})
			})


		})
	}



	function showResults(input) {
		if (isCETRegNo.test(input)) {
			console.log("Valid CET Registration Number, going for data retrieval")
			getDetails(input)
		}
		else {
			hideStuff()
		}
	}

	userInput.bind("typeahead:select", function (e, selection) {
		showResults(selection.value)
		console.log("Selected", selection.name)
	})

	userInput.bind("keypress", function (e) {
		var $this = $(this)
		var input = userInput.val()

		if (isNumber.test(input)) {
			$('.notFound').addClass("hidden")
			console.log("Closing typeahead")
		}

		if (e.which == 13) {
			showResults(input)
		}
	})

	userInput.change(function (e) {
		if (userInput.val() == '') {
			hideStuff()
		}
	})

})