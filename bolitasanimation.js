// Creamos un array para almacenar las bolitas
const bolitas = [];

// Creamos una función para crear una bolita
function crearBolita() {
    const bolita = document.createElement("div");
    bolita.className = "bolita";
    bolita.style.top = `${Math.random() * 100}%`;
    bolita.style.left = `${Math.random() * 100}%`;
    bolita.style.backgroundColor = `hsla(${Math.random() * 360}, 100%, 60%, 0.3)`;
    bolita.style.filter = `blur(10px)`;
    document.querySelector(".bolitas-container").appendChild(bolita);
    bolitas.push(bolita);

    // Agregamos una posición aleatoria inicial
    bolita.style.transform = `translateX(${Math.random() * 100}px) translateY(${Math.random() * 100}px)`;
}

// Creamos 10 bolitas iniciales
for (let i = 0; i < 10; i++) {
    crearBolita();
}

// Creamos una función para animar las bolitas
function animarBolitas() {
    bolitas.forEach((bolita) => {
        // Agregamos una velocidad mínima para cada bolita
        const velocidadX = 2; // velocidad mínima en el eje X
        const velocidadY = 2; // velocidad mínima en el eje Y

        // Agregamos una función para actualizar la posición de la bolita
        function actualizarPosicion() {
            bolita.style.transform = `translateX(${bolita.offsetLeft + velocidadX}px) translateY(${bolita.offsetTop + velocidadY}px)`;
            requestAnimationFrame(actualizarPosicion);
        }

        // Iniciamos la animación
        actualizarPosicion();
    });
}

// Iniciamos la animación
animarBolitas();

// Creamos un intervalo para crear nuevas bolitas cada 20 segundos
setInterval(() => {
    crearBolita();
}, 20000);

// Agregamos un estilo para las bolitas
document.querySelector(".bolitas-container").style.overflow = "hidden";
document.querySelector(".bolitas-container").style.height = "100vh";
document.querySelector(".bolitas-container").style.width = "100vw"; // aumentamos el tamaño del contenedor
document.querySelector(".bolitas-container").style.zIndex = "-1";
document.querySelector(".bolitas-container").style.pointerEvents = "none";
document.querySelector(".bolitas-container").style.position = "fixed";
document.querySelector(".bolitas-container").style.top = "0";
document.querySelector(".bolitas-container").style.left = "0";

// Agregamos un estilo para las bolitas individuales
bolitas.forEach((bolita) => {
    bolita.style.position = "absolute";
    bolita.style.borderRadius = "50%";
    bolita.style.width = "100px";
    bolita.style.height = "100px";
});