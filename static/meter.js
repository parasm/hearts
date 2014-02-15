var canvas = document.getElementById('canvas'),
	context = canvas.getContext('2d'),
	value = 5,
	center_x = canvas.width / 2,
	center_y = canvas.height / 2;

function draw() {
	context.fillStyle = "rgb(192, 192, 192)";
	context.fillRect(0, 0, canvas.width, canvas.height);
	//context.clearRect(0, 0, canvas.width, canvas.height);
	var r = Math.floor(-value / 100 * 255);
	if(r < 0) {
		r = 0;
	}
	var g = Math.floor(value / 100 * 255);
	if(g < 0) {
		g = 0;
	}
	context.strokeStyle = "rgb(" + r + ", " + g + ", 0)";
	context.beginPath();
	context.moveTo(center_x, center_y);
	context.lineTo(center_x + (value / 100 * center_x), center_y);
	context.lineWidth = canvas.height;
	context.stroke();
}

draw();