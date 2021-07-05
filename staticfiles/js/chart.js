function loadJson(selector) {
	return JSON.parse(document.querySelector(selector).getAttribute('data-json'));
	}
	
window.onload = function () {
  var jsonData = loadJson('#jsonData');

  var data = jsonData.map((item) => item.value);
  var labels = jsonData.map((item) => item.date);

  console.log(data);
  console.log(labels);

  var config = {
	type: 'line',
	data: {
	  labels: labels,
	  datasets: [
		{
		  label: 'A random dataset',
		  backgroundColor: 'black',
		  borderColor: 'lightblue',
		  data: data,
		  fill: false
		}
	  ]
	},
	options: {
	  responsive: true
	}
  };

  var ctx = document.getElementById('chart').getContext('2d');
  window.myLine = new Chart(ctx, config);
};
	