const uploadButton = document.getElementById('upload-button');
const sendButton = document.getElementById('send-button');
const fileInput = document.getElementById('file-input');
const messageInput = document.getElementById('message-input');
const chatMessages = document.getElementById('chat-messages');

// Agrega un contenedor div para los mensajes del chat
const chatContainer = document.createElement('div');
chatContainer.className = 'chat-container';
chatMessages.appendChild(chatContainer);

uploadButton.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (e) => {
    const file = fileInput.files[0];
    const fileType = file.type;
    const allowedTypes = ['application/msword', 'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];

    if (allowedTypes.includes(fileType)) {
        const fileName = file.name;
        const message = messageInput.value;
        if (message.trim() !== '') {
            messageInput.value = `${message}\nArchivo: ${fileName}`;
        } else {
            alert('Por favor, escriba un mensaje antes de subir un archivo');
            fileInput.value = '';
        }
    } else {
        alert('Solo se aceptan archivos Word (.docx) y PDF');
        fileInput.value = '';
    }
});

sendButton.addEventListener('click', () => {
    const file = fileInput.files[0];
    if (!file) {
        alert('Por favor, seleccione un archivo antes de enviar');
        return;
    }
    const message = messageInput.value;

    // Crea un nuevo elemento li para el mensaje del usuario y el archivo subido
    const messageLi = document.createElement('li');
    messageLi.className = 'user-message'; // Agrega la clase CSS para la burbuja de texto del usuario

    // Agrega el mensaje del usuario
    const userMessageSpan = document.createElement('span');
    userMessageSpan.textContent = message;
    messageLi.appendChild(userMessageSpan);

    // Agrega el elemento li al contenedor de mensajes del chat
    chatContainer.appendChild(messageLi);

    // Envía el archivo seleccionado
    const formData = new FormData();
    formData.append('file', file);
    formData.append('message', message);

    fetch('http://127.0.0.1:8000/analysis/upload/', {
        method: 'POST',
        mode: 'cors',
        body: formData,
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Data received:', data);
        if (data.error) {
            console.error('Error:', data.error);

        } else if (data.analysis_result) {
            // Crea un nuevo elemento li para el mensaje del usuario y el archivo subido
            const messageLi = document.createElement('li');
            messageLi.className = 'ia-message'; // Agrega la clase CSS para la burbuja de texto del usuario

            // Agrega el mensaje de la ia
            const iaMessageSpan = document.createElement('span');
            iaMessageSpan.textContent = data.analysis_result; // Asigna el resultado de la análisis aquí
            messageLi.appendChild(iaMessageSpan);

            // Agrega el elemento li al contenedor de mensajes del chat
            chatContainer.appendChild(messageLi);
        } else {
            console.log('La respuesta no tiene la propiedad analysis_result');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        if (error instanceof Error && error.message.includes('HTTP error')) {
            console.error('HTTP error:', error.message);
        }
    })

    // Limpia el textarea y el input de tipo file
    messageInput.value = '';
    fileInput.value = '';
});