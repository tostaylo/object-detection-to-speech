const video = document.querySelector('#video');
const takePhotoEl = document.querySelector('#takePhoto');

function startVideo() {
	window.navigator.mediaDevices
		.getUserMedia({ video: true })
		.then((stream) => {
			video.srcObject = stream;
			video.onloadedmetadata = (e) => {
				video.play();
			};
		})
		.catch(() => {
			alert('You have to give the browser the permission to run webcam and mic ;( ');
		});
}

async function getImageDataUrl() {
	const canvas = document.querySelector('#canvas');
	canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
	const imgDataUrl = canvas.toDataURL('image/jpeg');

	return imgDataUrl;
}

function sayPrediction(prediction) {
	const synth = window.speechSynthesis;
	const utterance = new SpeechSynthesisUtterance(prediction);
	synth.speak(utterance);
}

async function takePhotoAndSayPrediction() {
	const imgDataUrl = await getImageDataUrl();

	const predictionResponse = await fetch('/webcam', {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
		},
		body: JSON.stringify(imgDataUrl),
	});

	const prediction = await predictionResponse.json();

	sayPrediction(prediction);
}

startVideo();

takePhotoEl.addEventListener('click', takePhotoAndSayPrediction);
