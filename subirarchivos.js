document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file-input-button');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chat-messages');

    let selectedFile = null;

    // Agrega un contenedor div para los mensajes del chat
    const chatContainer = document.createElement('div');
    chatContainer.className = 'chat-container';
    chatMessages.appendChild(chatContainer);

    fileInput.addEventListener('change', (e) => {
        const file = fileInput.files[0];
        const fileType = file.type;
        const allowedTypes = ['application/msword', 'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];

        if (allowedTypes.includes(fileType)) {
            selectedFile = file;
        } else {
            alert('Solo se aceptan archivos Word (.docx) y PDF');
            fileInput.value = '';
        }
    });

    sendButton.addEventListener('click', () => {
        if (selectedFile) {
            // Crea un nuevo elemento li para el archivo subido
            const messageLi = document.createElement('li');
            messageLi.className = 'user-message'; // Agrega la clase CSS para la burbuja de texto del usuario

            // Agrega el nombre del archivo subido
            const fileNameSpan = document.createElement('span');
            fileNameSpan.textContent = selectedFile.name; // Asigna el nombre del archivo aquí
            messageLi.appendChild(fileNameSpan);

            // Agrega el elemento li al contenedor de mensajes del chat
            chatContainer.appendChild(messageLi);

            // Envía el archivo seleccionado
            uploadFile(selectedFile);
            selectedFile = null;
        }
    });

    function uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        fetch('http://127.0.0.1:8000/analysis/upload/', {
            method: 'POST',
            mode: 'cors',
            body: formData,
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
        });

        // Limpia el input de tipo file
        fileInput.value = '';
    }
});