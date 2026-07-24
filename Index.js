// --- PART A: THREE.JS BACKGROUND SCENE GENERATION ---
geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

const material = new THREE.PointsMaterial({
    color: 0xffffff,
    size: 0.02,
    transparent: true,
    opacity: 0.8
});

const starParticles = new THREE.Points(geometry, material);
scene.add(starParticles);
camera.position.z = 3;

function animate3DScene() {
    requestAnimationFrame(animate3DScene);
    starParticles.rotation.y += 0.002;
    starParticles.rotation.x += 0.001;
    renderer.render(scene, camera);
}
animate3DScene();

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// --- PART B: DYNAMIC MOUSE TILT PARALLAX (3D HOVER COMPONENT) ---
const card = document.getElementById('interactiveCard');
if (card) {
    document.addEventListener('mousemove', (e) => {
        let xAxis = (window.innerWidth / 2 - e.pageX) / 20;
        let yAxis = (window.innerHeight / 2 - e.pageY) / 20;
        // Fixed syntax: changed quotes to backticks for string interpolation
        card.style.transform = `rotateY(${-xAxis}deg) rotateX(${yAxis}deg)`;
    });

    document.addEventListener('mouseleave', () => {
        card.style.transform = 'rotateY(0deg) rotateX(0deg)';
        card.style.transition = 'transform 0.5s ease';
    });

    document.addEventListener('mouseenter', () => {
        card.style.transition = 'none';
    });
}

// --- PART C: ASYNC FLASK ENDPOINT TRANSMISSION LAYER ---
let currentStep = 1;

function switchStep(stepNumber) {
    if (stepNumber === currentStep) return;
    currentStep = stepNumber;
    
    const slider = document.getElementById('tabSlider');
    const btn1 = document.getElementById('btnTab1');
    const btn2 = document.getElementById('btnTab2');
    const panel1 = document.getElementById('stepPanel1');
    const panel2 = document.getElementById('stepPanel2');
    const btnText = document.getElementById('btnText');
    
    if (stepNumber === 1) {
        if (slider) slider.style.transform = 'translateX(0%)';
        if (btn1) { btn1.classList.add('active'); btn1.style.color = '#fff'; }
        if (btn2) { btn2.classList.remove('active'); btn2.style.color = ''; }
        if (panel2) panel2.classList.remove('active');
        
        setTimeout(() => {
            if (panel1) panel1.classList.add('active');
        }, 150);
        
        if (btnText) btnText.innerText = "Connect to Core";
    } else {
        if (slider) slider.style.transform = 'translateX(100%)';
        if (btn2) { btn2.classList.add('active'); btn2.style.color = '#fff'; }
        if (btn1) { btn1.classList.remove('active'); btn1.style.color = ''; }
        if (panel1) panel1.classList.remove('active');
        
        setTimeout(() => {
            if (panel2) panel2.classList.add('active');
        }, 150);
        
        if (btnText) btnText.innerText = "Authorize Core Node";
    }
}

async function handlePrimaryAction() {
    if (currentStep === 1) {
        const fullNameEl = document.getElementById('fullName');
        const nidaIdEl = document.getElementById('nidaId');
        const routerEl = document.getElementById('router');
        const msisdnEl = document.getElementById('msisdn');
        
        const payload = {
            fullName: fullNameEl ? fullNameEl.value : "",
            nidaId: nidaIdEl ? nidaIdEl.value : "",
            router: routerEl ? routerEl.value : "",
            msisdn: msisdnEl ? msisdnEl.value : ""
        };
        
        switchStep(2);
        
        try {
            const response = await fetch('/submit-identity', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            
            const data = await response.json();
            
            if (data.status === "success") {
                const vaultStatusEl = document.getElementById('vaultStatus');
                const backendKeyEl = document.getElementById('backendKey');
                if (vaultStatusEl) vaultStatusEl.value = "🟢 Core Synced Successfully";
                if (backendKeyEl) backendKeyEl.value = data.mock_key || "NODE-KEY-SECURE";
            } else {
                alert(data.message || "An error occurred during submission.");
                switchStep(1);
            }
        } catch (e) {
            alert("3D Node Connection Interrupt.");
            switchStep(1);
        }
    } else {
        alert("🔒 3D Encrypted Payload Dispatched!");
    }
}

// Bind handler directly to structural interaction buttons
const actionBtn = document.getElementById('actionButton');
if (actionBtn) {
    actionBtn.addEventListener('click', handlePrimaryAction);
}
