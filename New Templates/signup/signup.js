let body = document.querySelector("body");
let canvas = document.querySelector(".dots");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
let ctx = canvas.getContext('2d');

// ---- Config ----
const DOT_COUNT = 150;
const MAX_SPEED = 1.5;
const CONNECT_DISTANCE = 160;      // distance threshold for dot-to-dot lines
const MAX_CONNECTIONS_PER_DOT = 6; // soft cap to avoid O(n^2) overload
const MOUSE_CONNECT_DISTANCE = 200;

// ---- Dots ----
let dots = [];
for (let i = 0; i < DOT_COUNT; i++) {
    dots.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        size: Math.random() * 2 + 1,
        color: "#00f2ff",
        vx: (Math.random() - 0.5) * MAX_SPEED,
        vy: (Math.random() - 0.5) * MAX_SPEED
    });
}

// ---- Mouse ----
let mouse = { x: null, y: null };
body.addEventListener("mousemove", (e) => {
    mouse.x = e.pageX;
    mouse.y = e.pageY;
});
body.addEventListener("mouseout", () => {
    mouse.x = null;
    mouse.y = null;
});

// ---- Draw Dots ----
function drawCircles() {
    dots.forEach(dot => {
        ctx.fillStyle = dot.color;
        ctx.beginPath();
        ctx.arc(dot.x, dot.y, dot.size, 0, Math.PI * 2);
        ctx.fill();
    });
}

// ---- Update Positions ----
function updateDots() {
    dots.forEach(dot => {
        dot.x += dot.vx;
        dot.y += dot.vy;

        // bounce on edges
        if (dot.x < 0) { dot.x = 0; dot.vx *= -1; }
        if (dot.x > canvas.width) { dot.x = canvas.width; dot.vx *= -1; }
        if (dot.y < 0) { dot.y = 0; dot.vy *= -1; }
        if (dot.y > canvas.height) { dot.y = canvas.height; dot.vy *= -1; }
    });
}

// ---- Dot-to-Mouse Lines ----
function drawLinesToMouse() {
    if (mouse.x == null || mouse.y == null) return;
    for (let i = 0; i < dots.length; i++) {
        const dx = mouse.x - dots[i].x;
        const dy = mouse.y - dots[i].y;
        const dist = Math.hypot(dx, dy);
        if (dist < MOUSE_CONNECT_DISTANCE) {
            // fade with distance
            const alpha = 1 - dist / MOUSE_CONNECT_DISTANCE;
            ctx.strokeStyle = `rgba(0, 242, 255, ${alpha})`;
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(dots[i].x, dots[i].y);
            ctx.lineTo(mouse.x, mouse.y);
            ctx.stroke();
        }
    }
}

// ---- Dot-to-Dot Lines ----
function drawDotConnections() {
    // For performance, connect each pair only once: j starts at i+1
    for (let i = 0; i < dots.length; i++) {
        let connections = 0; // soft cap per dot
        for (let j = i + 1; j < dots.length; j++) {
            const dx = dots[j].x - dots[i].x;
            const dy = dots[j].y - dots[i].y;
            const dist = Math.hypot(dx, dy);
            if (dist <= CONNECT_DISTANCE) {
                // fade with distance
                const alpha = 1 - dist / CONNECT_DISTANCE;
                ctx.strokeStyle = `rgba(0, 242, 255, ${alpha})`;
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(dots[i].x, dots[i].y);
                ctx.lineTo(dots[j].x, dots[j].y);
                ctx.stroke();

                connections++;
                if (connections >= MAX_CONNECTIONS_PER_DOT) break;
            }
        }
    }
}

// ---- Animation ----
function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    updateDots();
    drawCircles();
    drawDotConnections(); // connect dots to one another
    drawLinesToMouse();   // connect dots to mouse
    requestAnimationFrame(animate);
}
animate();

// ---- Resize Handling ----
window.addEventListener("resize", () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});

