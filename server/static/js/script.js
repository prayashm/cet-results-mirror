$(document).ready(function(){
	var isCETRegNo = /^1\d{2}1106\d{3}$/
	var isNumber = /^\d{0,9}$/
	var isName = /^[a-zA-Z ]+$/

	var profile = $("#profileSection")
	var detailsSection = $("#detailsSection")

	profile.hide()
	detailsSection.hide()

	function hideStuff () {
		console.log("Non CET Registration Number or Invalid Name")
		profile.fadeOut(500)
		detailsSection.fadeOut(500)
	}

	var userInput = $(".typeahead")
	input = document.getElementById("userInput")
	
	var students = new Bloodhound({
		datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
		queryTokenizer: Bloodhound.tokenizers.whitespace,
		remote : {
			url: '/%QUERY',
			wildcard: '%QUERY',
			transform: function(response){
				data = response.students
				rv = []
				for(var i = 0; i < data.length; i++){
					rv.push({
						value: data[i].student_id,
						tokens: [data[i].name, data[i].student_id],
						name: data[i].name,
						batch: data[i].batch,
						branch: data[i].branch,
						student_id: data[i].student_id
					})
				}
				return rv
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

	function getDetails(student_id){
		$.getJSON("/"+student_id, function(data){
			if(data == null){
				hideStuff()
			}

			profile.show(700)
			detailsSection.show(700)

			profile.find("#name").html(data.name)
			profile.find("#batch").html(data.batch)
			profile.find("#branch").html(data.branch)
			profile.find("#student_id").html(data.student_id)

            console.log(data)

//			details = detailsSection.find("tbody")
//			details.html("")
//
//			var credits = 0
//			var sumofproducts = 0
//
//			data.semesters.forEach(function(element, index){
//				credits += element.credits
//				sumofproducts += element.credits*element.sgpa
//				details.append("<tr class='mdl-color--primary-dark semrow'><td class='mdl-data-table__cell--non-numeric'><a href='"+element.path+"' target='new'>Semester "+element.sem+" <i class='material-icons' id='open_icon'>open_in_new</i></a></td><td>"+element.credits+"</td><td>"+element.sgpa+"</td></tr>")
//				element.subjects.forEach(function(subject, index){
//					details.append("<tr><td class='mdl-data-table__cell--non-numeric'>"+subject.code+" - "+subject.name+"</td><td>"+subject.credits+"</td><td>"+subject.grade+"</td></tr>")
//				})
//			})

//			var cgpa = sumofproducts/credits
//			details.append("<tr id='cgpa' class='mdl-color--primary-dark semrow'><td class='mdl-data-table__cell--non-numeric'>CGPA</td><td>"+credits+"</td><td>"+Math.round(cgpa*100)/100+"</td></tr>")

			$("#hide").click(function(e){
				console.log("Gonna hide", data.student_id)
				$.getJSON("/hide/"+data.student_id, function(data){
					alert(data.message)
				})
			})
		})

}

function showResults (input) {
	if (isCETRegNo.test(input)) {
		console.log("Valid CET Registration Number, going for data retrieval")
		getDetails(input)
	}
	else {
		hideStuff()
	}
}

userInput.bind("typeahead:select", function(e, selection){
	showResults(selection.value)
	console.log("Selected", selection.name)
})

userInput.bind("keypress", function(e){
	var $this = $(this)
	var input = userInput.val()

	if(isNumber.test(input)){
		$('.notFound').addClass("hidden")
		console.log("Closing typeahead")
	}

	if (e.which == 13) {
		showResults(input)
	}
})

userInput.change(function(e){
	if (userInput.val() == '') {
		hideStuff()
	}
})

})