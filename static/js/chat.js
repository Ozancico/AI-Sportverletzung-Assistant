// AI-Sportverletzung-Assistant Chat JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chatForm');
    const messageInput = document.getElementById('messageInput');
    const chatMessages = document.getElementById('chatMessages');
    const sendButton = document.getElementById('sendButton');
    const typingIndicator = document.getElementById('typingIndicator');
    const quickQuestions = document.querySelectorAll('.quick-question');

    // Event Listener für das Chat-Formular
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const message = messageInput.value.trim();
        if (message) {
            sendMessage(message);
            messageInput.value = '';
        }
    });

    // Event Listener für Schnellfragen
    quickQuestions.forEach(button => {
        button.addEventListener('click', function() {
            const question = this.getAttribute('data-question');
            messageInput.value = question;
            sendMessage(question);
        });
    });

    // Enter-Taste für Senden
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event('submit'));
        }
    });

    // Auto-Focus auf Input
    messageInput.focus();

    // Nachricht senden
    async function sendMessage(message) {
        // Benutzernachricht anzeigen
        addMessage(message, 'user');
        
        // UI für "AI denkt nach" anzeigen
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
                // AI-Antwort anzeigen
                hideTypingIndicator();
                addMessage(data.answer, 'assistant');
            } else {
                // Fehler anzeigen
                hideTypingIndicator();
                addMessage('Entschuldigung, es gab einen Fehler. Bitte versuchen Sie es erneut.', 'assistant');
                console.error('Error:', data.error);
            }
        } catch (error) {
            // Netzwerkfehler
            hideTypingIndicator();
            addMessage('Verbindungsfehler. Bitte überprüfen Sie Ihre Internetverbindung und versuchen Sie es erneut.', 'assistant');
            console.error('Network error:', error);
        } finally {
            enableInput();
        }
    }

    // Nachricht zum Chat hinzufügen
    function addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        if (sender === 'assistant') {
            messageContent.innerHTML = `<i class="fas fa-robot"></i><span>${formatMessage(content)}</span>`;
        } else {
            messageContent.textContent = content;
        }
        
        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);
        
        // Zum Ende scrollen
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Nachricht formatieren (Zeilenumbrüche, etc.)
    function formatMessage(content) {
        return content
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>');
    }

    // Typing Indicator anzeigen
    function showTypingIndicator() {
        typingIndicator.style.display = 'block';
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Typing Indicator verstecken
    function hideTypingIndicator() {
        typingIndicator.style.display = 'none';
    }

    // Input deaktivieren
    function disableInput() {
        messageInput.disabled = true;
        sendButton.disabled = true;
        sendButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    }

    // Input aktivieren
    function enableInput() {
        messageInput.disabled = false;
        sendButton.disabled = false;
        sendButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
        messageInput.focus();
    }

    // Auto-Resize für Textarea (falls später verwendet)
    function autoResize(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = textarea.scrollHeight + 'px';
    }

    // Smooth Scrolling
    function smoothScrollToBottom() {
        chatMessages.scrollTo({
            top: chatMessages.scrollHeight,
            behavior: 'smooth'
        });
    }

    // Keyboard Shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K für neuen Chat
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            messageInput.focus();
        }
        
        // Escape um Input zu leeren
        if (e.key === 'Escape') {
            messageInput.value = '';
            messageInput.focus();
        }
    });

    // Chat-Historie laden (falls vorhanden)
    loadChatHistory();

    async function loadChatHistory() {
        try {
            const response = await fetch('/api/health');
            if (response.ok) {
                console.log('Verbindung zum Server erfolgreich');
            }
        } catch (error) {
            console.error('Server-Verbindung fehlgeschlagen:', error);
        }
    }

    // Utility-Funktionen
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

    // Error Handling
    window.addEventListener('error', function(e) {
        console.error('JavaScript Error:', e.error);
    });

    // Service Worker Registration (für zukünftige PWA-Features)
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', function() {
            // Service Worker kann hier registriert werden
            console.log('Service Worker Support verfügbar');
        });
    }
});
