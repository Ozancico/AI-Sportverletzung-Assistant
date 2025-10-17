// AI-Sportverletzung-Assistant Chat JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chatForm');
    const messageInput = document.getElementById('messageInput');
    const chatMessages = document.getElementById('chatMessages');
    const sendButton = document.getElementById('sendButton');
    const typingIndicator = document.getElementById('typingIndicator');
    const quickQuestions = document.querySelectorAll('.quick-question');
    const themeToggle = document.getElementById('themeToggle');
    const accentOptions = document.querySelectorAll('.accent-option');

    // Event listener for chat form
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const message = messageInput.value.trim();
        if (message) {
            sendMessage(message);
            messageInput.value = '';
        }
    });

    // Event listener for quick questions
    quickQuestions.forEach(button => {
        button.addEventListener('click', function() {
            const question = this.getAttribute('data-question');
            messageInput.value = question;
            sendMessage(question);
        });
    });

    // Enter key for sending
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event('submit'));
        }
    });

    // Auto-focus on input
    messageInput.focus();

    // Theme initialisieren und Toggle-Button verbinden
    initTheme();
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const isDark = document.body.classList.toggle('dark');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
            themeToggle.innerHTML = isDark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
        });
    }

    // Accent color Auswahl
    accentOptions.forEach(opt => {
        opt.addEventListener('click', function(e) {
            e.preventDefault();
            const color = this.getAttribute('data-accent');
            setAccent(color);
        });
    });

    // Send message
    async function sendMessage(message) {
        // Display user message
        addMessage(message, 'user');
        
        // Show "AI is thinking" UI
        showTypingIndicator();
        disableInput();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: message })
            });

            const data = await response.json();

            if (response.ok) {
                // Display AI response
                hideTypingIndicator();
                addMessage(data.answer, 'assistant');
            } else {
                // Display error
                hideTypingIndicator();
                addMessage('Entschuldigung, es gab einen Fehler. Bitte versuchen Sie es erneut.', 'assistant');
                console.error('Error:', data.error);
            }
        } catch (error) {
            // Network error
            hideTypingIndicator();
            addMessage('Verbindungsfehler. Bitte überprüfen Sie Ihre Internetverbindung und versuchen Sie es erneut.', 'assistant');
            console.error('Network error:', error);
        } finally {
            enableInput();
        }
    }

    // Add message to chat
    function addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        if (sender === 'assistant') {
            messageContent.innerHTML = `<div class="avatar avatar-assistant"><i class="fas fa-robot"></i></div><span class="msg-text">${formatMessage(content)}</span>`;
        } else {
            const avatar = document.createElement('div');
            avatar.className = 'avatar avatar-user';
            avatar.innerHTML = '<i class="fas fa-user"></i>';
            const textSpan = document.createElement('span');
            textSpan.className = 'msg-text';
            textSpan.textContent = content;
            messageContent.appendChild(avatar);
            messageContent.appendChild(textSpan);
        }

        // Meta-Bereich (Timestamp + Copy)
        const meta = buildMessageMeta(messageContent);
        messageContent.appendChild(meta);
        
        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function buildMessageMeta(container) {
        const meta = document.createElement('div');
        meta.className = 'message-meta';
        const ts = document.createElement('span');
        ts.className = 'timestamp';
        ts.textContent = new Date().toLocaleString('de-DE', { hour: '2-digit', minute: '2-digit' });

        const copyBtn = document.createElement('button');
        copyBtn.className = 'btn btn-light btn-sm copy-btn';
        copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
        copyBtn.title = 'Kopieren';
        copyBtn.addEventListener('click', function() { handleCopy(container, copyBtn); });

        meta.appendChild(ts);
        meta.appendChild(copyBtn);
        return meta;
    }

    function handleCopy(container, btn) {
        const textNode = container.querySelector('.msg-text');
        const text = textNode ? textNode.innerText : container.innerText;
        navigator.clipboard.writeText(text).then(() => {
            btn.innerHTML = '<i class="fas fa-check"></i>';
            setTimeout(() => (btn.innerHTML = '<i class=\"fas fa-copy\"></i>'), 1200);
        }).catch(err => console.error('Copy failed', err));
    }

    // Format message (line breaks, etc.)
    function formatMessage(content) {
        return content
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>');
    }

    // Show typing indicator
    function showTypingIndicator() {
        typingIndicator.style.display = 'block';
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Hide typing indicator
    function hideTypingIndicator() {
        typingIndicator.style.display = 'none';
    }

    // Disable input
    function disableInput() {
        messageInput.disabled = true;
        sendButton.disabled = true;
        sendButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    }

    // Enable input
    function enableInput() {
        messageInput.disabled = false;
        sendButton.disabled = false;
        sendButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
        messageInput.focus();
    }

    // Auto-resize for textarea (if used later)
    function autoResize(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = textarea.scrollHeight + 'px';
    }

    // Smooth scrolling
    function smoothScrollToBottom() {
        chatMessages.scrollTo({
            top: chatMessages.scrollHeight,
            behavior: 'smooth'
        });
    }

    // Delegierte Klick-Behandlung für statische Copy-Buttons (z. B. Willkommensnachricht)
    chatMessages.addEventListener('click', function(e) {
        const target = e.target.closest('.copy-btn');
        if (!target) return;
        const container = e.target.closest('.message-content');
        if (container) {
            handleCopy(container, target);
        }
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K for new chat
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            messageInput.focus();
        }
        
        // Escape to clear input
        if (e.key === 'Escape') {
            messageInput.value = '';
            messageInput.focus();
        }
    });

    // Load chat history (if available)
    loadChatHistory();

    async function loadChatHistory() {
        try {
            const response = await fetch('/api/health');
            if (response.ok) {
                console.log('Server connection successful');
            }
        } catch (error) {
            console.error('Server connection failed:', error);
        }
    }

    // Utility functions
    function formatTimestamp(timestamp) {
        const date = new Date(timestamp);
        return date.toLocaleString('de-DE', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    // Error handling
    window.addEventListener('error', function(e) {
        console.error('JavaScript Error:', e.error);
    });

    // Service Worker Registration (for future PWA features)
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', function() {
            // Service Worker can be registered here
            console.log('Service Worker support available');
        });
    }

    function initTheme() {
        const saved = localStorage.getItem('theme');
        const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
        const useDark = saved ? saved === 'dark' : prefersDark;
        if (useDark) {
            document.body.classList.add('dark');
        }
        if (themeToggle) {
            themeToggle.innerHTML = document.body.classList.contains('dark') ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
        }
        const savedAccent = localStorage.getItem('accent');
        if (savedAccent) setAccent(savedAccent);
    }

    function setAccent(color) {
        document.body.style.setProperty('--accent-color', color);
        document.body.setAttribute('data-accent', '1');
        localStorage.setItem('accent', color);
    }
});
