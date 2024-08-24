const uploadButton = document.getElementById('upload-button');
const fileInput = document.getElementById('file-input');
const sendButton = document.getElementById('send-button');
const textarea = document.getElementById('message-input');

uploadButton.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (e) => {
    const file = fileInput.files[0];
    const fileType = file.type;
    const allowedTypes = ['application/msword', 'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];

    if (allowedTypes.includes(fileType)) {
        const fileName = file.name;
        textarea.value = `Archivo seleccionado: ${fileName}`;
    } else {
    alert('Solo se aceptan archivos Word (.docx) y PDF');
    fileInput.value = '';
    }
});

sendButton.addEventListener('click', () => {
    const file = fileInput.files[0];
  // Aquí envías el archivo seleccionado
    console.log(file);
  // Limpia el textarea y el input de tipo file
    textarea.value = '';
    fileInput.value = '';
});