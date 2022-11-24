function handleFile(event) {
	if (!event.target.files.length) return;

	const fileSize = event.target.files[0].size / 1024 / 1024; // MB
	if (fileSize > 1) {
		event.target.value = null;
		window.alert('This file is too large. Images more than 1MB are not allowed.');
		return;
	}

	const ext = event.target.value.split('.').pop().toLowerCase();

	if (!['jpg', 'jpeg'].includes(ext)) {
		event.target.value = null;
		window.alert('Only jpeg/jpg files are allowed.');
	}
}

document.getElementById('image-file-detectron').addEventListener('change', handleFile);
document.getElementById('image-file-yolo').addEventListener('change', handleFile);
