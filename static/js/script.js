$(document).ready(function(){
	var isCETRegNo = /^1\d{2}1106\d{3}$/
	var isName = /^[a-zA-Z]+$/

	var profile = $("#profileSection")
	var detailsSection = $("#detailsSection")

	profile.hide()
	detailsSection.hide()

	function hideStuff () {
		console.log("Non CET Registration Number or Invalid Name")
		profile.fadeOut(500)
		detailsSection.fadeOut(500)
	}

	var userInput = $("input#userInput")
	input = document.getElementById("userInput")

	function autosuggest () {
		$.getJSON("/"+userInput.val(), function(data){
			var list = []
			$.each(data.students, function(index, value){
				// console.log(index, value.name)
				list.push(value.name)
			})
			console.log(list)
		})
	}

	userInput.change(function(e){
		e.preventDefault()
		var $this = $(this)
		var input = $this.val()

		if (isCETRegNo.test(input)) {
			console.log("Valid CET Registration Number, going for data retrieval")
			$.getJSON("/"+input, function(data){
				if(data == null){
					hideStuff()
				}


				profile.show(700)
				detailsSection.show(700)

				profile.find("#name").html(data.name)
				profile.find("#batch").html(data.batch)
				profile.find("#branch").html(data.branch)
				profile.find("#regno").html(data.regno)
				
				
				details = detailsSection.find("tbody")
				details.html("")

				var credits = 0
				var sumofproducts = 0

				data.semesters.forEach(function(element, index){
					// console.log(element)
					credits += element.credits
					sumofproducts += element.credits*element.sgpa
					details.append("<tr><td class='mdl-data-table__cell--non-numeric'><a href='"+element.path+"' target='new'>Semester "+element.sem+"</a></td><td>"+element.credits+"</td><td>"+element.sgpa+"</td></tr>")
				})
				var cgpa = sumofproducts/credits
				details.append("<tr id='cgpa'><td class='mdl-data-table__cell--non-numeric'><b>CGPA</b></td><td><b>"+credits+"</b></td><td><b>"+Math.round(cgpa*100)/100+"</b></td></tr>")
			})

		}
		else if (isName.test(input)) {
			autosuggest()
		}
		else {
			hideStuff()		
		}
	})
})