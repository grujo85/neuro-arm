# -*- coding: utf-8 -*-
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from flask import Flask, render_template

app = Flask(__name__)

html_kod = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>NEURO-ARM PRO v1.0</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <style>
        :root { --neon: #00f2ff; --bg: #0a0b10; }
        body { margin: 0; background: var(--bg); color: var(--neon); font-family: sans-serif; display: flex; height: 100vh; overflow: hidden; }
        #ui { width: 300px; padding: 25px; background: rgba(15, 17, 26, 0.95); border-right: 2px solid var(--neon); z-index: 100; box-shadow: 10px 0 20px rgba(0,0,0,0.5); }
        #container { flex-grow: 1; position: relative; }
        .slider-box { margin-bottom: 30px; }
        label { display: block; margin-bottom: 10px; letter-spacing: 1px; font-size: 12px; font-weight: bold; }
        input[type=range] { width: 100%; cursor: pointer; -webkit-appearance: none; background: #222; height: 4px; border-radius: 2px; }
        input[type=range]::-webkit-slider-thumb { -webkit-appearance: none; height: 18px; width: 18px; border-radius: 50%; background: var(--neon); box-shadow: 0 0 10px var(--neon); }
        .val { float: right; color: #fff; background: #222; padding: 2px 8px; border-radius: 4px; font-size: 11px; }
        h2 { font-size: 20px; text-transform: uppercase; margin-bottom: 40px; border-bottom: 1px solid #333; padding-bottom: 10px; }
    </style>
</head>
<body>

<div id="ui">
    <h2>NEURO-ARM <span style="color:#fff">V3.0</span></h2>
    
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
</div>

<div id="container"></div>

<script>
    let scene, camera, renderer, controls;
    let base, shoulder, elbow, forearm;

    function init() {
        const container = document.getElementById('container');
        scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0a0b10);
        
        camera = new THREE.PerspectiveCamera(50, container.clientWidth/container.clientHeight, 0.1, 1000);
        camera.position.set(10, 8, 12);

        renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(renderer.domElement);

        controls = new THREE.OrbitControls(camera, renderer.domElement);
        
        scene.add(new THREE.AmbientLight(0x404040, 1.5));
        const light = new THREE.PointLight(0x00f2ff, 2, 50);
        light.position.set(5, 10, 5);
        scene.add(light);

        scene.add(new THREE.GridHelper(30, 30, 0x00f2ff, 0x1a1a1a));

        const metalMat = new THREE.MeshStandardMaterial({ color: 0x333333, metalness: 0.8, roughness: 0.2 });
        const glowMat = new THREE.MeshBasicMaterial({ color: 0x00f2ff });

        // Model
        base = new THREE.Group();
        scene.add(base);
        base.add(new THREE.Mesh(new THREE.CylinderGeometry(1.5, 1.8, 0.5, 32), metalMat));

        shoulder = new THREE.Group();
        shoulder.position.y = 0.5;
        base.add(shoulder);
        shoulder.add(new THREE.Mesh(new THREE.SphereGeometry(0.6, 32, 32), metalMat));

        const arm1 = new THREE.Group();
        shoulder.add(arm1);
        const p1 = new THREE.Mesh(new THREE.BoxGeometry(0.6, 4, 0.6), metalMat);
        p1.position.y = 2;
        arm1.add(p1);

        elbow = new THREE.Group();
        elbow.position.y = 4;
        arm1.add(elbow);
        const p2 = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.5, 0.8, 16), metalMat);
        p2.rotation.z = Math.PI/2;
        elbow.add(p2);

        forearm = new THREE.Group();
        elbow.add(forearm);
        const p3 = new THREE.Mesh(new THREE.BoxGeometry(0.4, 3, 0.4), metalMat);
        p3.position.y = 1.5;
        forearm.add(p3);

        const neon = new THREE.Mesh(new THREE.BoxGeometry(0.1, 2, 0.42), glowMat);
        neon.position.set(0.26, 1.5, 0);
        forearm.add(neon);

        // Početna poza
        arm1.rotation.z = -0.8;
        forearm.rotation.z = 1.5;

        animate();
    }

    function animate() {
        requestAnimationFrame(animate);
        renderer.render(scene, camera);
    }

    document.querySelectorAll('input').forEach(input => {
        input.oninput = function() {
            const val = parseFloat(this.value);
            document.getElementById('v' + this.id.slice(1)).innerText = val;
            const rad = val * (Math.PI/180);
            if(this.id === 'j1') base.rotation.y = rad;
            if(this.id === 'j2') shoulder.children[1].rotation.z = rad;
            if(this.id === 'j3') forearm.rotation.z = rad;
        };
    });

    init();
</script>
</body>
</html>
"""

@app.route('/')
def index():
    # Flask će sam potražiti 'index.html' unutar 'templates' foldera
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
