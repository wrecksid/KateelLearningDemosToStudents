// Emotional Support Assistant
// Builds knowledge graph from user inputs and provides empathetic responses

class EmotionalSupportAssistant {
    constructor() {
        this.knowledgeGraph = {
            users: [],
            emotions: [],
            connections: []
        };
        this.currentMood = null;
        this.conversationHistory = [];
        this.userId = 'user_' + Date.now();
        
        this.init();
    }

    init() {
        this.initSpeech();
        this.bindEvents();
        this.loadState();
    }

    initSpeech() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (SpeechRecognition) {
            this.recognition = new SpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-US';
        }
    }

    bindEvents() {
        document.getElementById('send-btn').addEventListener('click', () => this.sendMessage());
        document.getElementById('user-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
        document.getElementById('mic-btn').addEventListener('click', () => this.startVoiceInput());
        
        document.querySelectorAll('.mood-btn').forEach(btn => {
            btn.addEventListener('click', () => this.setMood(btn.dataset.mood));
        });
    }

    sendMessage() {
        const input = document.getElementById('user-input');
        const message = input.value.trim();
        if (!message) return;
        
        this.addMessage('user', message);
        input.value = '';
        
        // Process and respond
        setTimeout(() => this.processMessage(message), 500);
    }

    processMessage(message) {
        const emotion = this.detectEmotion(message);
        const response = this.generateEmpatheticResponse(message, emotion);
        
        this.updateKnowledgeGraph(message, emotion);
        this.addMessage('bot', response);
        this.speakResponse(response);
        this.askFollowUp(emotion);
    }

    detectEmotion(text) {
        const lower = text.toLowerCase();
        const emotions = {
            sad: ['sad', 'unhappy', 'depressed', 'cry', 'tears', 'hurt'],
            lonely: ['lonely', 'alone', 'isolated', 'alone', 'solitary'],
            anxious: ['anxious', 'worried', 'stress', 'nervous', 'panic'],
            happy: ['happy', 'good', 'great', 'wonderful', 'amazing'],
            angry: ['angry', 'mad', 'furious', 'upset']
        };
        
        for (const [emotion, keywords] of Object.entries(emotions)) {
            if (keywords.some(kw => lower.includes(kw))) {
                return emotion;
            }
        }
        return 'neutral';
    }

    generateEmpatheticResponse(message, emotion) {
        const responses = {
            sad: [
                "I'm here with you in this difficult time. It's okay to feel sad - these feelings are valid. Would you like to talk more about what's weighing on your heart?",
                "Your sadness matters. I may be an AI, but I genuinely care about your wellbeing. Can you share what's causing these feelings?",
                "I understand how heavy sadness can feel. Remember that this moment of pain doesn't define your entire story. You're not alone in this."
            ],
            lonely: [
                "I hear the loneliness in your words, and I want you to know that reaching out is a brave step. Connection is possible, even when it feels impossible right now.",
                "Loneliness can be overwhelming, but the fact that you're sharing this with me shows your strength. Let's explore what might help you feel more connected.",
                "Being alone isn't the same as being lonely. I'm here with you now - let's work together to find ways to ease this feeling."
            ],
            anxious: [
                "Anxiety can feel all-consuming, but it's just a feeling - not a reality. Let's breathe together and talk through what's causing worry.",
                "I can sense your anxiety, and I want you to know that feeling this way doesn't mean something is wrong with you. Would you like to explore what's on your mind?",
                "Anxiety speaks loudly, but your courage to face it is louder. Take a deep breath with me, and let's work through this together."
            ],
            happy: [
                "I'm so glad to hear some joy in your voice today! These moments of happiness are important - hold onto them.",
                "Your happiness brightens my day too. It's wonderful that you're experiencing some good feelings.",
                "That's wonderful news! I hope this positive energy carries forward. What's bringing you joy?"
            ],
            neutral: [
                "I'm here whenever you need to talk. There's no pressure, but I care about what you're experiencing.",
                "Thank you for sharing with me. Your feelings deserve to be heard and validated.",
                "I'm listening. Whatever you're feeling, it's okay to express it here."
            ]
        };
        
        const opts = responses[emotion] || responses.neutral;
        return opts[Math.floor(Math.random() * opts.length)];
    }

    updateKnowledgeGraph(message, emotion) {
        // Add user if not exists
        if (!this.knowledgeGraph.users.find(u => u.id === this.userId)) {
            this.knowledgeGraph.users.push({
                id: this.userId,
                name: 'You',
                emotions: []
            });
        }
        
        // Add emotion to user's history
        const user = this.knowledgeGraph.users.find(u => u.id === this.userId);
        user.emotions.push({
            emotion: emotion,
            timestamp: new Date().toISOString(),
            message: message
        });
        
        // Add emotion node if new
        if (!this.knowledgeGraph.emotions.find(e => e.id === emotion)) {
            this.knowledgeGraph.emotions.push({
                id: emotion,
                label: emotion.charAt(0).toUpperCase() + emotion.slice(1)
            });
        }
        
        // Add connection
        this.knowledgeGraph.connections.push({
            from: this.userId,
            to: emotion,
            timestamp: new Date().toISOString()
        });
        
        this.saveState();
        this.renderGraph();
    }

    askFollowUp(emotion) {
        const followUps = {
            sad: "What do you think triggered these feelings? Sometimes understanding our emotions helps us find the path forward.",
            lonely: "When do you feel most connected - with family, friends, or even pets? Identifying these moments can help us create more of them.",
            anxious: "What's the story you're telling yourself right now? Often anxiety comes from our imagination of worst-case scenarios.",
            happy: "What's bringing you joy today? Hold onto these moments.",
            neutral: "Is there anything specific on your mind you'd like to explore further?"
        };
        
        setTimeout(() => {
            const question = followUps[emotion] || followUps.neutral;
            this.addMessage('bot', question);
        }, 2000);
    }

    addMessage(sender, text) {
        const messagesEl = document.getElementById('chat-messages');
        const msgDiv = document.createElement('div');
        msgDiv.className = `msg ${sender}`;
        
        const avatar = sender === 'bot' ? '💙' : '👤';
        const msgClass = sender === 'bot' ? 'msg-content' : 'msg-content';
        
        msgDiv.innerHTML = `
            <div class="msg-avatar">${avatar}</div>
            <div class="${msgClass}">
                <p>${text}</p>
            </div>
        `;
        
        messagesEl.appendChild(msgDiv);
        messagesEl.scrollTop = messagesEl.scrollHeight;
    }

    setMood(mood) {
        this.currentMood = mood;
        const message = `I'm feeling ${mood} right now.`;
        this.addMessage('user', message);
        setTimeout(() => this.processMessage(message), 500);
    }

    renderGraph() {
        const el = document.getElementById('connection-graph');
        const user = this.knowledgeGraph.users.find(u => u.id === this.userId);
        
        if (!user || user.emotions.length === 0) {
            el.innerHTML = '<p class="hint">Your emotional journey will appear here...</p>';
            return;
        }
        
        let html = '<div style="margin-bottom: 10px;"><strong>Your Emotions:</strong></div>';
        user.emotions.slice(-5).forEach(e => {
            html += `<span class="connection-node">${e.emotion}</span>`;
        });
        
        el.innerHTML = html;
    }

    speakResponse(text) {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 0.9;
            utterance.pitch = 1.1;
            speechSynthesis.speak(utterance);
        }
    }

    startVoiceInput() {
        if (!this.recognition) {
            alert('Voice input not supported in this browser.');
            return;
        }
        
        this.recognition.start();
        this.recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            document.getElementById('user-input').value = transcript;
            this.sendMessage();
        };
    }

    saveState() {
        localStorage.setItem('emotionalSupportState', JSON.stringify({
            knowledgeGraph: this.knowledgeGraph,
            userId: this.userId
        }));
    }

    loadState() {
        const state = localStorage.getItem('emotionalSupportState');
        if (state) {
            const parsed = JSON.parse(state);
            this.knowledgeGraph = parsed.knowledgeGraph;
            this.userId = parsed.userId;
            this.renderGraph();
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new EmotionalSupportAssistant();
});