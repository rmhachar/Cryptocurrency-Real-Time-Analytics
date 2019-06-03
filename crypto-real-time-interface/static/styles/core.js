function topFiveSpreads(){
	response = getTopFive()
	topFiveSpreads = response['largest_five_spreads']
	topFivePairs = response['largest_five_pairs']
	appendTopFive(topFiveSpreads, topFivePairs)
}

 function getTopFive(){

	var settings = {
		async: false,
		url: "/receiver",
		method: "GET",
		headers: {
			"Content-Type": "application/json"
		}
	}

	$.ajax(settings).done(function (response) {
		responseParsed = JSON.parse(response)
	})

	return responseParsed	
}

function appendTopFive(topFiveSpreads, topFivePairs) {
	for (var i = 0; i < topFiveSpreads.length; i++) {
		appendRow(topFiveSpreads, topFivePairs, i)
	}
}

function appendRow(topFiveSpreads, topFivePairs, i) {
	console.log(topFiveSpreads[i])
	$(document.getElementById(`highest-spread-${(i+1)}`)).append(`
		<div><p>${topFivePairs[i]} - ${topFiveSpreads[i].toFixed(3)}</p></div>
	`)
}