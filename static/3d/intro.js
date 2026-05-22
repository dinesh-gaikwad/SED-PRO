  
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';
import { OrbitControls } from 'https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/controls/OrbitControls.js';

class IntroAnimation {
    constructor(containerId){
        this.container = document.getElementById(containerId);
        if(!this.container){
            console.error('Container not found:', containerId);
            return;
        }
        this.init();
        this.animate();
        window.addEventListener('resize', this.onWindowResize.bind(this));
    }

    init(){
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x0f172a);
        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.camera.position.set(0, 0, 15);
        this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.container.appendChild(this.renderer.domElement);
        this.controls = new OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        this.controls.enableZoom = false;
        this.controls.autoRotate = true;
        this.controls.autoRotateSpeed = 1.5;
        this.createLights();
        this.createFloatingObjects();
        this.createParticles();
    }

    createLights(){
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
        this.scene.add(ambientLight);
        const pointLight1 = new THREE.PointLight(0x6366f1, 2, 50);
        pointLight1.position.set(5, 5, 5);
        this.scene.add(pointLight1);
        const pointLight2 = new THREE.PointLight(0x8b5cf6, 2, 50);
        pointLight2.position.set(-5, -5, 5);
        this.scene.add(pointLight2);
        const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
        directionalLight.position.set(0, 10, 10);
        this.scene.add(directionalLight);
    }

    createFloatingObjects(){
        this.objects = new THREE.Group();
        const geometries = [
            new THREE.BoxGeometry(1, 1, 1),
            new THREE.SphereGeometry(0.7, 32, 32),
            new THREE.TetrahedronGeometry(0.8),
            new THREE.OctahedronGeometry(0.8),
            new THREE.IcosahedronGeometry(0.7)
        ];
        const colors = [0x6366f1, 0x8b5cf6, 0x10b981, 0xf59e0b, 0xec4899];
        for(let i = 0; i < 20; i++){
            const geometry = geometries[Math.floor(Math.random() * geometries.length)];
            const material = new THREE.MeshPhongMaterial({
                color: colors[Math.floor(Math.random() * colors.length)],
                shininess: 100,
                specular: 0xffffff
            });
            const mesh = new THREE.Mesh(geometry, material);
            mesh.position.x = (Math.random() - 0.5) * 30;
            mesh.position.y = (Math.random() - 0.5) * 30;
            mesh.position.z = (Math.random() - 0.5) * 30;
            mesh.rotation.x = Math.random() * Math.PI * 2;
            mesh.rotation.y = Math.random() * Math.PI * 2;
            mesh.userData = {
                rotationSpeed: {
                    x: (Math.random() - 0.5) * 0.02,
                    y: (Math.random() - 0.5) * 0.02,
                    z: (Math.random() - 0.5) * 0.02
                },
                floatSpeed: Math.random() * 0.02 + 0.01,
                floatOffset: Math.random() * Math.PI * 2
            };
            this.objects.add(mesh);
        }
        this.scene.add(this.objects);
    }

    createParticles(){
        const particleCount = 500;
        const geometry = new THREE.BufferGeometry();
        const positions = new Float32Array(particleCount * 3);
        const colors = new Float32Array(particleCount * 3);
        const color = new THREE.Color();
        for(let i = 0; i < particleCount; i++){
            const i3 = i * 3;
            positions[i3] = (Math.random() - 0.5) * 50;
            positions[i3 + 1] = (Math.random() - 0.5) * 50;
            positions[i3 + 2] = (Math.random() - 0.5) * 50;
            color.setHSL(Math.random() * 0.3 + 0.6, 0.7, 0.5);
            colors[i3] = color.r;
            colors[i3 + 1] = color.g;
            colors[i3 + 2] = color.b;
        }
        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
        const material = new THREE.PointsMaterial({
            size: 0.1,
            vertexColors: true,
            transparent: true,
            opacity: 0.8
        });
        this.particles = new THREE.Points(geometry, material);
        this.scene.add(this.particles);
    }

    animate(){
        requestAnimationFrame(this.animate.bind(this));
        const time = Date.now() * 0.001;
        this.objects.children.forEach((obj, index) => {
            obj.rotation.x += obj.userData.rotationSpeed.x;
            obj.rotation.y += obj.userData.rotationSpeed.y;
            obj.rotation.z += obj.userData.rotationSpeed.z;
            obj.position.y += Math.sin(time * obj.userData.floatSpeed + obj.userData.floatOffset) * 0.01;
        });
        const positions = this.particles.geometry.attributes.position.array;
        for(let i = 0; i < positions.length; i += 3){
            positions[i + 1] += Math.sin(time + positions[i]) * 0.001;
        }
        this.particles.geometry.attributes.position.needsUpdate = true;
        this.controls.update();
        this.renderer.render(this.scene, this.camera);
    }

    onWindowResize(){
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
    }

    destroy(){
        window.removeEventListener('resize', this.onWindowResize.bind(this));
        this.container.removeChild(this.renderer.domElement);
    }
}

document.addEventListener('DOMContentLoaded', function(){
    const introContainer = document.getElementById('intro-3d');
    if(introContainer){
        new IntroAnimation('intro-3d');
    }
});

export default IntroAnimation;