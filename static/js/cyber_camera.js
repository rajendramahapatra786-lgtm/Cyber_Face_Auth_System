// Cyber Camera & Face Recognition JavaScript
// Handles webcam access, face capture, and API communication

const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const scanBtn = document.getElementById('scanBtn');
const resetBtn = document.getElementById('resetBtn');
const statusMessage = document.getElementById('statusMessage');
const statusLed = document.getElementById('statusLed');

let stream = null;
let isProcessing = false;
let glitchInterval = null;

// Initialize Camera
async function initCamera() {
    try {
        updateStatus('INITIALIZING CAMERA MODULE...', '#ffff00');
        
        stream = await navigator.mediaDevices.getUserMedia({ 
            video: { 
                width: { ideal: 640 },
                height: { ideal: 480 },
                facingMode: 'user'
            } 
        });
        
        video.srcObject = stream;
        
        // Wait for video to be ready
        await new Promise((resolve) => {
            video.onloadedmetadata = () => {
                resolve();
            };
        });
        
        updateStatus('CAMERA ACTIVE. AWAITING FACIAL DATA...', '#00ffff');
        if (statusLed) statusLed.style.background = '#00ff00';
        
        // Start cyber effects
        startCyberEffects();
        
        // Auto-detect after 2 seconds
        setTimeout(() => {
            updateStatus('SYSTEM READY. POSITION YOUR FACE IN FRAME.', '#00ffff');
        }, 2000);
        
    } catch (err) {
        console.error('Camera error:', err);
        
        if (err.name === 'NotAllowedError') {
            updateStatus('ERROR: CAMERA ACCESS DENIED BY USER', '#ff0000');
        } else if (err.name === 'NotFoundError') {
            updateStatus('ERROR: NO CAMERA DEVICE FOUND', '#ff0000');
        } else {
            updateStatus('ERROR: UNABLE TO ACCESS CAMERA', '#ff0000');
        }
        
        if (statusLed) statusLed.style.background = '#ff0000';
        
        // Disable scan button if no camera
        if (scanBtn) scanBtn.disabled = true;
    }
}
// Capture 5 images from webcam
async function registerFace() {
    let frames = [];

    for (let i = 0; i < 5; i++) {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0);

        const imageData = canvas.toDataURL('image/jpeg', 0.8);
        frames.push(imageData);

        // small delay between captures
        await new Promise(r => setTimeout(r, 300));
    }

    const username = prompt("Enter your name:");

    const response = await fetch('/api/face/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: username,
            images: frames
        })
    });

    const result = await response.json();
    alert(result.message);
}



// Start Cyber Effects (glitch and scan animations)
function startCyberEffects() {
    const cameraFrame = document.querySelector('.camera-frame');
    
    if (!cameraFrame) return;
    
    // Random glitch effect
    glitchInterval = setInterval(() => {
        if (Math.random() > 0.85) { // 15% chance
            const glitchOverlay = document.createElement('div');
            glitchOverlay.style.cssText = `
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, 
                    transparent 0%,
                    rgba(0, 255, 255, 0.3) 50%,
                    transparent 100%);
                animation: glitchFlash 0.3s ease-out;
                pointer-events: none;
                z-index: 10;
            `;
            cameraFrame.appendChild(glitchOverlay);
            
            setTimeout(() => {
                glitchOverlay.remove();
            }, 300);
        }
    }, 3000);
}

// Update Status Message with typing effect
function updateStatus(message, color = '#00ffff') {
    if (!statusMessage) return;
    
    statusMessage.textContent = message;
    statusMessage.style.color = color;
    
    // Add glitch effect to status
    statusMessage.style.animation = 'none';
    setTimeout(() => {
        statusMessage.style.animation = 'glitch 0.3s ease';
    }, 10);
}

// Show Access Granted Animation
async function showAccessGranted(name) {
    return new Promise((resolve) => {
        const overlay = document.createElement('div');
        overlay.className = 'loading-overlay';
        overlay.innerHTML = `
            <div style="text-align: center; animation: fadeIn 0.5s ease;">
                <h1 style="color: #00ff00; font-size: 3rem; margin-bottom: 1rem; text-shadow: 0 0 20px #00ff00;">
                    🔓 ACCESS GRANTED
                </h1>
                <div style="color: #00ffff; margin-bottom: 1rem; font-size: 1.2rem;">
                    IDENTITY: ${name.toUpperCase()}
                </div>
                <div style="color: #ff00ff; margin-bottom: 1rem; font-size: 0.9rem;">
                    CONFIDENCE: 99.97%
                </div>
                <div class="loading-bar">
                    <div class="loading-progress"></div>
                </div>
                <div style="color: #00ffff; margin-top: 1rem;" id="loadingStatus">
                    DECRYPTING SECURE CHANNEL...
                </div>
            </div>
        `;
        document.body.appendChild(overlay);
        
        // Animated status messages
        const statusMessages = [
            'VERIFYING CREDENTIALS...',
            'CROSS-REFERENCING DATABASE...',
            'MATCH FOUND: 99.97%',
            'BYPASSING FIREWALL...',
            'ESTABLISHING SECURE CONNECTION...',
            'GRANTING ACCESS...'
        ];
        
        let index = 0;
        const statusInterval = setInterval(() => {
            const statusDiv = document.getElementById('loadingStatus');
            if (statusDiv && index < statusMessages.length) {
                statusDiv.textContent = statusMessages[index];
                index++;
            } else if (index >= statusMessages.length) {
                clearInterval(statusInterval);
            }
        }, 400);
        
        setTimeout(() => {
            clearInterval(statusInterval);
            overlay.style.animation = 'fadeOut 0.5s ease';
            setTimeout(() => {
                overlay.remove();
                resolve();
            }, 500);
        }, 3000);
    });
}

// Show Access Denied Animation
async function showAccessDenied() {
    return new Promise((resolve) => {
        const overlay = document.createElement('div');
        overlay.className = 'loading-overlay';
        overlay.style.background = 'rgba(0, 0, 0, 0.95)';
        overlay.innerHTML = `
            <div style="text-align: center; animation: fadeIn 0.5s ease;">
                <h1 style="color: #ff0000; font-size: 3rem; margin-bottom: 1rem; text-shadow: 0 0 20px #ff0000;">
                    ⛔ ACCESS DENIED
                </h1>
                <div style="color: #ff6600; margin-bottom: 1rem;">
                    FACIAL RECOGNITION FAILED
                </div>
                <div class="loading-bar">
                    <div style="width: 100%; height: 100%; background: #ff0000;"></div>
                </div>
                <div style="color: #ff0000; margin-top: 1rem;">
                    UNAUTHORIZED ACCESS ATTEMPT LOGGED
                </div>
            </div>
        `;
        document.body.appendChild(overlay);
        
        // Flash red effect on body
        document.body.style.backgroundColor = 'rgba(255, 0, 0, 0.3)';
        
        setTimeout(() => {
            document.body.style.backgroundColor = '';
            overlay.style.animation = 'fadeOut 0.5s ease';
            setTimeout(() => {
                overlay.remove();
                resolve();
            }, 500);
        }, 2000);
    });
}

// Capture and Verify Face
async function captureAndVerify() {
    if (isProcessing) {
        updateStatus('SYSTEM BUSY. PLEASE WAIT...', '#ffff00');
        return;
    }
    
    if (!video || !video.videoWidth || !video.videoHeight) {
        updateStatus('ERROR: CAMERA NOT READY', '#ff0000');
        return;
    }
    
    isProcessing = true;
    if (scanBtn) scanBtn.disabled = true;
    
    updateStatus('SCANNING NEURAL PATTERNS...', '#00ffff');
    if (statusLed) statusLed.style.background = '#ffff00';
    
    // Add visual feedback - brightness flash
    video.style.filter = 'brightness(1.5) contrast(1.2)';
    
    // Capture frame from video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Add scan line effect on capture
    context.strokeStyle = '#00ffff';
    context.lineWidth = 2;
    context.strokeRect(0, 0, canvas.width, canvas.height);
    
    // Get base64 image (JPEG format for smaller size)
    const imageData = canvas.toDataURL('image/jpeg', 0.8);
    
    // Send to backend
    try {
        const response = await fetch('/api/face/verify/', {
            method: 'POST',
            headers: {
                'Content-Type': application/json,
            },
            body: JSON.stringify({ image: imageData })
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            // Access Granted
            updateStatus(`ACCESS GRANTED. WELCOME, ${result.name.toUpperCase()}`, '#00ff00');
            if (statusLed) statusLed.style.background = '#00ff00';
            
            // Play success sound (if available)
            if (typeof playSound === 'function') {
                playSound('granted');
            }
            
            // Speak welcome message
            if (typeof speak === 'function') {
                speak(`Welcome ${result.name}. Access granted.`);
            }
            
            // Store username for dashboard
            localStorage.setItem('cyber_user', result.name);
            
            // Show success animation
            await showAccessGranted(result.name);
            
            // Redirect to dashboard
            window.location.href = '/dashboard/';
            
        } else {
            // Access Denied
            updateStatus('ACCESS DENIED. FACIAL RECOGNITION FAILED', '#ff0000');
            if (statusLed) statusLed.style.background = '#ff0000';
            
            // Play denied sound
            if (typeof playSound === 'function') {
                playSound('denied');
            }
            
            // Speak denial
            if (typeof speak === 'function') {
                speak('Access denied. Identity not recognized.');
            }
            
            // Show denied animation
            await showAccessDenied();
            
            // Reset status
            updateStatus('ACCESS DENIED. TRY AGAIN.', '#ff0000');
            setTimeout(() => {
                updateStatus('SYSTEM READY. AWAITING FACIAL SCAN...', '#00ffff');
                if (statusLed) statusLed.style.background = '#00ffff';
            }, 2000);
        }
        
    } catch (error) {
        console.error('API Error:', error);
        updateStatus('ERROR: COMMUNICATION FAILURE WITH SERVER', '#ff0000');
        if (statusLed) statusLed.style.background = '#ff0000';
        
        // Show error animation
        const overlay = document.createElement('div');
        overlay.className = 'loading-overlay';
        overlay.innerHTML = `
            <div style="text-align: center;">
                <h1 style="color: #ff0000;">⚠️ SYSTEM ERROR</h1>
                <div>Unable to communicate with server</div>
                <div style="margin-top: 20px;">Check if Django server is running</div>
            </div>
        `;
        document.body.appendChild(overlay);
        
        setTimeout(() => {
            overlay.remove();
        }, 2000);
        
    } finally {
        isProcessing = false;
        if (scanBtn) scanBtn.disabled = false;
        video.style.filter = '';
        
        // Reset LED after delay if still in fail state
        setTimeout(() => {
            if (statusLed && statusLed.style.background === '#ff0000') {
                statusLed.style.background = '#00ffff';
            }
        }, 3000);
    }
}

// Reset System
function resetSystem() {
    updateStatus('SYSTEM RESET. INITIALIZING PROTOCOLS...', '#ffff00');
    if (statusLed) statusLed.style.background = '#ffff00';
    
    // Clear any stored user data
    localStorage.removeItem('cyber_user');
    
    // Reset camera if needed
    if (stream) {
        const tracks = stream.getTracks();
        tracks.forEach(track => track.stop());
    }
    
    setTimeout(() => {
        // Reinitialize camera
        initCamera();
        updateStatus('SYSTEM READY. AWAITING FACIAL SCAN...', '#00ffff');
    }, 2000);
}

// Add glitch effect to camera feed (visual enhancement)
function addCameraGlitchEffect() {
    const cameraFrame = document.querySelector('.camera-frame');
    if (!cameraFrame) return;
    
    setInterval(() => {
        if (Math.random() > 0.9 && !isProcessing) {
            const glitch = document.createElement('div');
            glitch.style.cssText = `
                position: absolute;
                top: ${Math.random() * 100}%;
                left: 0;
                width: 100%;
                height: 2px;
                background: rgba(0, 255, 255, 0.8);
                animation: glitchFlash 0.2s ease-out;
                pointer-events: none;
                z-index: 15;
            `;
            cameraFrame.appendChild(glitch);
            setTimeout(() => glitch.remove(), 200);
        }
    }, 5000);
}

// Event Listeners
if (scanBtn) {
    scanBtn.addEventListener('click', captureAndVerify);
}

if (resetBtn) {
    resetBtn.addEventListener('click', resetSystem);
}

// Initialize on load
window.addEventListener('load', () => {
    initCamera();
    updateStatus('SYSTEM ONLINE. INITIALIZING NEURAL NETWORK...', '#00ffff');
    
    // Add CSS animations if not present
    const style = document.createElement('style');
    style.textContent = `
        @keyframes glitchFlash {
            0%, 100% { transform: translateX(0); opacity: 1; }
            50% { transform: translateX(5px); opacity: 0.5; }
        }
        
        @keyframes fadeOut {
            from { opacity: 1; }
            to { opacity: 0; visibility: hidden; }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
    `;
    document.head.appendChild(style);
    
    // Add camera glitch effects
    setTimeout(() => {
        addCameraGlitchEffect();
    }, 1000);
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
    if (glitchInterval) {
        clearInterval(glitchInterval);
    }
});