async function setupCamera() {
    try {
        const video = document.getElementById('video');
        const stream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 } });
        video.srcObject = stream;
        return new Promise((resolve) => {
            video.onloadedmetadata = () => resolve(video);
        });
    } catch (error) {
        console.error('Error accessing the camera:', error);
        alert('Could not access the camera. Please check your permissions.');
    }
}

async function loadBlazeFaceModel() {
    try {
        return await blazeface.load();
    } catch (error) {
        console.error('Error loading BlazeFace model:', error);
        alert('Could not load the BlazeFace model. Please try again later.');
    }
}

async function detectFaces(model, video, canvas, avatarCanvas) {
    const context = canvas.getContext('2d');
    const avatarContext = avatarCanvas.getContext('2d');
    const avatarImage = new Image();
    avatarImage.src = 'image.png'; // Replace with your avatar image URL
    await avatarImage.decode(); // Ensure the image is loaded before drawing

    const detect = async () => {
        try {
            const predictions = await model.estimateFaces(video, false);

            context.clearRect(0, 0, canvas.width, canvas.height);
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            avatarContext.clearRect(0, 0, avatarCanvas.width, avatarCanvas.height);

            if (predictions.length > 0) {
                predictions.forEach((prediction) => {
                    const start = prediction.topLeft;
                    const end = prediction.bottomRight;
                    const size = [end[0] - start[0], end[1] - start[1]];

                    // Draw bounding box (for debugging purposes)
                    context.beginPath();
                    context.strokeStyle = 'red';
                    context.lineWidth = 2;
                    context.rect(start[0], start[1], size[0], size[1]);
                    context.stroke();

                    // Draw avatar image based on detected face position
                    avatarContext.drawImage(avatarImage, start[0], start[1], size[0], size[1]);
                });
            }
        } catch (error) {
            console.error('Error during face detection:', error);
        }

        requestAnimationFrame(detect);
    };

    detect();
}

(async function () {
    const video = await setupCamera();
    if (video) {
        video.play();

        const model = await loadBlazeFaceModel();
        if (model) {
            const canvas = document.getElementById('canvas');
            const avatarCanvas = document.getElementById('avatarCanvas');

            detectFaces(model, video, canvas, avatarCanvas);
        }
    }
})();
