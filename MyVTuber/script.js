async function setupWebcam() {
    const webcamElement = document.getElementById('webcam');
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    webcamElement.srcObject = stream;
    return new Promise((resolve) => {
        webcamElement.onloadedmetadata = () => {
            resolve(webcamElement);
        };
    });
}

async function loadPosenet() {
    const net = await posenet.load();
    return net;
}

function initThreeJS() {
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    // Basic avatar (a simple cube for demonstration)
    const geometry = new THREE.BoxGeometry();
    const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
    const avatar = new THREE.Mesh(geometry, material);
    scene.add(avatar);

    camera.position.z = 5;

    function animate() {
        requestAnimationFrame(animate);
        renderer.render(scene, camera);
    }
    animate();

    return { scene, camera, avatar };
}

async function main() {
    await setupWebcam();
    const net = await loadPosenet();
    const { scene, camera, avatar } = initThreeJS();

    const webcamElement = document.getElementById('webcam');

    async function detectPose() {
        const pose = await net.estimateSinglePose(webcamElement, {
            flipHorizontal: false
        });

        if (pose.keypoints) {
            const nose = pose.keypoints.find(point => point.part === 'nose');
            if (nose && nose.score > 0.5) {
                avatar.position.x = (nose.position.x / webcamElement.width) * 2 - 1;
                avatar.position.y = -(nose.position.y / webcamElement.height) * 2 + 1;
            }
        }

        requestAnimationFrame(detectPose);
    }

    detectPose();
}

main();
