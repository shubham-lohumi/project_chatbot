class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button button'), // select the actual button
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }

        this.state = false;
        this.messages = [];
    }

    display() {
        const { openButton, chatBox, sendButton } = this.args;

        // Toggle chatbox on button click
        openButton.addEventListener('click', () => this.toggleState(chatBox));

        // Send message on send button click
        sendButton.addEventListener('click', () => this.onSendButton(chatBox));

        // Send message on Enter key
        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({ key }) => {
            if (key === "Enter") {
                this.onSendButton(chatBox);
            }
        });
    }

    toggleState(chatbox) {
        this.state = !this.state;
        chatbox.classList.toggle('chatbox--active', this.state);
    }

    onSendButton(chatbox) {
        const textField = chatbox.querySelector('input');
        const text1 = textField.value.trim();
        if (!text1) return;

        this.messages.push({ name: "User", message: text1 });
        textField.value = '';

        fetch('/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            headers: { 'Content-Type': 'application/json' }
        })
        .then(res => res.json())
        .then(data => {
            this.messages.push({ name: "Sam", message: data.answer });
            this.updateChatText(chatbox);
        })
        .catch(err => {
            console.error('Error:', err);
            this.messages.push({ name: "Sam", message: "Error connecting to server." });
            this.updateChatText(chatbox);
        });
    }

    updateChatText(chatbox) {
        let html = '';
        this.messages.slice().reverse().forEach(item => {
            if (item.name === "Sam") {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>';
            } else {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>';
            }
        });

        const chatMessage = chatbox.querySelector('.chatbox__messages'); // select the correct container
        chatMessage.innerHTML = html;
        chatMessage.scrollTop = chatMessage.scrollHeight;
    }
}


const chatbox = new Chatbox();
chatbox.display();
