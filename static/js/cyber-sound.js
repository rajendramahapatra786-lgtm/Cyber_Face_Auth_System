// Cyber Sounds & Speech Synthesis
// Handles all audio feedback, text-to-speech, and sound effects

// Sound Management
const soundEffects = {
    granted: null,
    denied: null,
    scan: null,
    boot: null,
    typing: null,
    alert: null
};

let isMuted = false;
let audioContext = null;
let soundsLoaded = false;

// Initialize Web Audio API for synthetic sounds (fallback)
function initAudioContext() {
    try {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        return audioContext;
    } catch (e) {
        console.log('Web Audio API not supported');
        return null;
    }
}

// Generate synthetic beep sounds using Web Audio API
function generateBeep(type, duration = 0.3) {
    if (isMuted) return Promise.resolve();
    
    return new Promise((resolve) => {
        try {
            const context = initAudioContext();
            if (!context) {
                resolve();
                return;
            }
            
            const oscillator = context.createOscillator();
            const gainNode = context.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(context.destination);
            
            let frequency = 440;
            let volume = 0.3;
            
            switch(type) {
                case 'granted':
                    frequency = 880;  // High pitch
                    duration = 0.5;
                    volume = 0.4;
                    // Create ascending arpeggio
                    setTimeout(() => {
                        if (context.state === 'running') {
                            const osc2 = context.createOscillator();
                            const gain2 = context.createGain();
                            osc2.connect(gain2);
                            gain2.connect(context.destination);
                            osc2.frequency.value = 1100;
                            gain2.gain.value = 0.3;
                            osc2.start();
                            osc2.stop(context.currentTime + 0.2);
                        }
                    }, 100);
                    break;
                case 'denied':
                    frequency = 220;  // Low pitch
                    duration = 0.8;
                    volume = 0.35;
                    break;
                case 'scan':
                    frequency = 660;
                    duration = 0.2;
                    volume = 0.25;
                    // Sweep frequency
                    oscillator.frequency.value = 440;
                    oscillator.frequency.exponentialRampToValue(frequency, duration);
                    break;
                case 'boot':
                    frequency = 330;
                    duration = 1;
                    volume = 0.3;
                    // Rising tone
                    oscillator.frequency.value = 220;
                    oscillator.frequency.exponentialRampToValue(440, duration);
                    break;
                case 'typing':
                    frequency = 800 + Math.random() * 200;
                    duration = 0.05;
                    volume = 0.1;
                    break;
                case 'alert':
                    frequency = 550;
                    duration = 0.15;
                    volume = 0.4;
                    break;
                default:
                    frequency = 440;
            }
            
            oscillator.frequency.value = frequency;
            gainNode.gain.value = volume;
            
            // Resume audio context if suspended
            if (context.state === 'suspended') {
                context.resume();
            }
            
            oscillator.start();
            oscillator.stop(context.currentTime + duration);
            
            // Clean up
            setTimeout(() => {
                oscillator.disconnect();
                gainNode.disconnect();
                resolve();
            }, duration * 1000);
            
        } catch(e) {
            console.log('Web Audio error:', e);
            resolve();
        }
    });
}

// Play sound effect
async function playSound(soundName) {
    if (isMuted) return;
    
    // Try to load actual sound files first
    if (!soundsLoaded) {
        loadSoundFiles();
    }
    
    const sound = soundEffects[soundName];
    if (sound && sound.readyState >= 2) {
        // Use actual audio file if loaded
        sound.currentTime = 0;
        try {
            await sound.play();
            return;
        } catch(e) {
            // Fallback to generated sound
            console.log('Audio file playback failed, using generated sound');
        }
    }
    
    // Fallback to generated sound
    await generateBeep(soundName);
}

// Load actual sound files (optional - create or download these)
function loadSoundFiles() {
    const soundFiles = {
        granted: '/static/sounds/access-granted.mp3',
        denied: '/static/sounds/access-denied.mp3',
        scan: '/static/sounds/scanning.mp3',
        boot: '/static/sounds/system-boot.mp3',
        typing: '/static/sounds/typing.mp3',
        alert: '/static/sounds/alert.mp3'
    };
    
    for (const [name, path] of Object.entries(soundFiles)) {
        const audio = new Audio();
        audio.preload = 'auto';
        audio.src = path;
        soundEffects[name] = audio;
    }
    
    soundsLoaded = true;
}

// Text to Speech Function
function speak(text, options = {}) {
    if (isMuted) return Promise.resolve();
    
    return new Promise((resolve, reject) => {
        if (!('speechSynthesis' in window)) {
            console.log('Speech synthesis not supported');
            reject(new Error('Speech synthesis not supported'));
            return;
        }
        
        // Cancel any ongoing speech
        window.speechSynthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = options.rate || 0.9;
        utterance.pitch = options.pitch || 1.1;
        utterance.volume = options.volume || 1;
        utterance.lang = options.lang || 'en-US';
        
        // Select a voice (prefer female/cyber voice)
        const voices = window.speechSynthesis.getVoices();
        const preferredVoice = voices.find(voice => 
            voice.name.includes('Google UK') || 
            voice.name.includes('Samantha') ||
            voice.name.includes('Female')
        );
        if (preferredVoice) {
            utterance.voice = preferredVoice;
        }
        
        utterance.onend = () => {
            resolve();
        };
        
        utterance.onerror = (event) => {
            console.error('Speech error:', event);
            reject(event);
        };
        
        window.speechSynthesis.speak(utterance);
    });
}

// Cyber-style voice messages
function speakCyberMessage(messageType) {
    const messages = {
        welcome: "Welcome to the cyber security system",
        granted: "Access granted. Identity verified.",
        denied: "Access denied. Unauthorized user detected.",
        scan: "Initiating facial recognition scan",
        error: "System error. Please try again",
        logout: "Session terminated. Goodbye."
    };
    
    const text = messages[messageType];
    if (text) {
        speak(text, { rate: 0.85, pitch: 1.2 });
    }
}

// Play typing sound effect for terminal
let typingInterval = null;

function startTypingSound() {
    if (isMuted) return;
    
    if (typingInterval) clearInterval(typingInterval);
    typingInterval = setInterval(() => {
        playSound('typing');
    }, 100);
}

function stopTypingSound() {
    if (typingInterval) {
        clearInterval(typingInterval);
        typingInterval = null;
    }
}

// Create and add mute button to UI
function addMuteButton() {
    const buttonGroup = document.querySelector('.button-group');
    if (!buttonGroup) return;
    
    const muteBtn = document.createElement('button');
    muteBtn.id = 'muteBtn';
    muteBtn.className = 'cyber-btn cyber-btn-secondary';
    muteBtn.innerHTML = '<span class="btn-text">🔊 MUTE</span>';
    muteBtn.style.marginLeft = '10px';
    
    muteBtn.addEventListener('click', toggleMute);
    buttonGroup.appendChild(muteBtn);
}

// Toggle mute/unmute all sounds
function toggleMute() {
    isMuted = !isMuted;
    const muteBtn = document.getElementById('muteBtn');
    
    if (muteBtn) {
        if (isMuted) {
            muteBtn.innerHTML = '<span class="btn-text">🔇 UNMUTE</span>';
            // Cancel any ongoing speech
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
            }
        } else {
            muteBtn.innerHTML = '<span class="btn-text">🔊 MUTE</span>';
            // Play a test sound to confirm unmute
            playSound('boot');
        }
    }
    
    // Store preference
    localStorage.setItem('cyber_muted', isMuted);
}

// Load mute preference
function loadMutePreference() {
    const saved = localStorage.getItem('cyber_muted');
    if (saved === 'true') {
        isMuted = true;
        const muteBtn = document.getElementById('muteBtn');
        if (muteBtn) {
            muteBtn.innerHTML = '<span class="btn-text">🔇 UNMUTE</span>';
        }
    }
}

// Play system boot sound on page load
function playBootSequence() {
    playSound('boot').then(() => {
        setTimeout(() => {
            playSound('scan');
        }, 500);
    });
    
    // Optional: speak welcome message after boot
    setTimeout(() => {
        if (!isMuted) {
            speakCyberMessage('welcome');
        }
    }, 1500);
}

// Create simple sound visualizer (optional)
function createSoundVisualizer() {
    const statusPanel = document.querySelector('.status-panel');
    if (!statusPanel) return;
    
    const visualizer = document.createElement('div');
    visualizer.id = 'soundVisualizer';
    visualizer.style.cssText = `
        display: flex;
        gap: 3px;
        margin-left: 10px;
        align-items: center;
    `;
    
    for (let i = 0; i < 5; i++) {
        const bar = document.createElement('div');
        bar.className = 'viz-bar';
        bar.style.cssText = `
            width: 3px;
            height: 10px;
            background: #00ffff;
            transition: height 0.05s ease;
        `;
        visualizer.appendChild(bar);
    }
    
    statusPanel.appendChild(visualizer);
    
    // Animate visualizer when sound plays
    return {
        animate: (intensity = 0.5) => {
            const bars = document.querySelectorAll('.viz-bar');
            bars.forEach((bar, index) => {
                const height = 5 + (Math.random() * 20 * intensity);
                bar.style.height = `${height}px`;
                setTimeout(() => {
                    bar.style.height = '10px';
                }, 100);
            });
        }
    };
}

// Export functions for use in other scripts
window.cyberSounds = {
    playSound,
    speak,
    toggleMute,
    isMuted: () => isMuted,
    startTypingSound,
    stopTypingSound,
    speakCyberMessage
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Add mute button after a short delay
    setTimeout(() => {
        addMuteButton();
        loadMutePreference();
        
        // Create visualizer (optional)
        const visualizer = createSoundVisualizer();
        if (visualizer) {
            // Override playSound to animate visualizer
            const originalPlaySound = playSound;
            window.playSound = async function(soundName) {
                await originalPlaySound(soundName);
                visualizer.animate(0.7);
            };
        }
    }, 1000);
    
    // Preload voices
    if ('speechSynthesis' in window) {
        window.speechSynthesis.getVoices();
    }
});

// Clean up on page unload
window.addEventListener('beforeunload', () => {
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
    }
    if (typingInterval) {
        clearInterval(typingInterval);
    }
});