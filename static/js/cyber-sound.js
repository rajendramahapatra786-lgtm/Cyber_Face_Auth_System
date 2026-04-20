// Simple Cyber Sound System (Typing Only)

const typingSound = new Audio('/static/sounds/typing.mp3');

// Play typing sound (single key press)
function playTypingSound() {
    typingSound.currentTime = 0;
    typingSound.play().catch(() => {});
}

// Export
window.cyberSounds = {
    playTypingSound
};

