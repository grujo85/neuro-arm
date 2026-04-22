import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from flask import Flask, render_template

app = Flask(__name__)

# --- STABILNI 3D KOD ---
html_kod = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>NEURO-ARM STABLE</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <style>
        body { margin: 0; background: #050608; color: #00f2ff; font-family: monospace; display: flex; height: 100vh; overflow: hidden; }
        #ui { width: 260px; padding: 20px; background: rgba(10, 15, 25, 0.95); border-right: 1px solid #00f2ff; z-index: 100; }
        #container { flex-grow: 1; position: relative; background: #000; }
        .slider-box { margin-bottom: 25px; }
        input[type=range] { width: 100%; accent-color: #00f2ff; cursor: pointer; }
        .val { float: right; color: #fff; font-weight: bold; }
        h2 { font-size: 16px; text-shadow: 0 0 10px #00f2ff; margin-bottom: 30px; }
    </style>
</head>
<body>

<div id="ui">
    <h2>NEURO-ARM v2.0</h2>
    
    <div class="slider-box">
        <label>BAZA <span id="v1" class="val">0</span></label>
        <input type="range" id="j1" min="-180" max="180" value="0">
    </div>

    <div class="slider-box">
        <label>RAME <span id="v2" class="val">-45</span></label>
        <input type="range" id="j2" min="-90" max="45" value="-45">
    </div>

    <div class="slider-box">
        <label>LAKAT <span id="v3" class="val">90</span></label>
        <input type="range" id="j3" min="0" max="150" value="90">
    </div>

    <p style="font-size: 10px; color: #444; margin-top: 50px;">
        * Ako je ekran crn, proveri internet konekciju.
    </p>
</div>

<div id="container"></div>

<script>
    let scene, camera, renderer, base, arm1, arm2, controls;

    function init() {
        const container = document.getElementById('container');
        
        scene = new THREE.Scene();
        scene.background = new THREE.Color(0x050608);
        
        camera = new THREE.PerspectiveCamera(60, container.clientWidth/container.clientHeight, 0.1, 1000);
        camera.position.set(8, 6, 8);

        renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(renderer.domElement);

        controls = new THREE.OrbitControls(camera, renderer.domElement);
        scene.add(new THREE.GridHelper(20, 20, 0x00f2ff, 0x111111));

        scene.add(new THREE.AmbientLight(0xffffff, 0.6));
        const light = new THREE.PointLight(0xffffff, 1);
        light.position.set(5, 10, 5);
        scene.add(light);

        const material = new THREE.MeshStandardMaterial({ color: 0xeeeeee, metalness: 0.3, roughness: 0.5 });

        base = new THREE.Mesh(new THREE.CylinderGeometry(1.2, 1.5, 0.4, 6), material);
        scene.add(base);

        arm1 = new THREE.Group();
        base.add(arm1);
        const m1 = new THREE.Mesh(new THREE.BoxGeometry(0.5, 3, 0.5), material);
        m1.position.y = 1.5;
        arm1.add(m1);
        arm1.rotation.z = -0.8;

        arm2 = new THREE.Group();
        arm2.position.y = 3;
        arm1.add(arm2);
        const m2 = new THREE.Mesh(new THREE.BoxGeometry(0.4, 2.5, 0.4), material);
        m2.position.y = 1.25;
        arm2.add(m2);
        arm2.rotation.z = 1.57;

        window.addEventListener('resize', onWindowResize, false);
        animate();
    }

    function onWindowResize() {
        const container = document.getElementById('container');
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    }

    function animate() {
        requestAnimationFrame(animate);
        renderer.render(scene, camera);
    }

    document.querySelectorAll('input').forEach(input => {
        input.oninput = function() {
            const id = this.id;
            const val = this.value;
            document.getElementById('v' + id.slice(1)).innerText = val;

            if(id === 'j1') base.rotation.y = val * (Math.PI/180);
            if(id === 'j2') arm1.rotation.z = val * (Math.PI/180);
            if(id === 'j3') arm2.rotation.z = val * (Math.PI/180);
        };
    });

    init();
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Pokrećemo bez socketio za maksimalnu stabilnost
    app.run()
