const field = document.querySelector(".field");
const canvas = document.getElementById("field-canvas");

if (field && canvas) {
  const ctx = canvas.getContext("2d");
  const dots = [];
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let pointer = null;
  let running = false;
  let visible = true;

  function viewSize() {
    const rect = field.getBoundingClientRect();
    const footer = field.querySelector(".footer");
    const height = Math.max(1, rect.height - (footer ? footer.offsetHeight : 0));
    return { width: rect.width, height };
  }

  function size() {
    const { width, height } = viewSize();
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.style.height = height + "px";
    canvas.width = Math.max(1, Math.floor(width * dpr));
    canvas.height = Math.max(1, Math.floor(height * dpr));
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    dots.length = 0;
    const gap = width < 640 ? 24 : 28;
    for (let y = gap / 2; y < height; y += gap) {
      for (let x = gap / 2; x < width; x += gap) {
        dots.push({ ox: x, oy: y, x, y });
      }
    }
    draw(false);
  }

  function pointFromEvent(event) {
    const rect = field.getBoundingClientRect();
    pointer = {
      x: event.clientX - rect.left,
      y: event.clientY - rect.top,
    };
  }

  function draw(animate) {
    const width = canvas.clientWidth;
    const height = canvas.clientHeight;
    ctx.clearRect(0, 0, width, height);

    let moving = false;
    ctx.fillStyle = "#3a3a3a";
    for (const dot of dots) {
      let targetX = dot.ox;
      let targetY = dot.oy;
      if (pointer && !reduceMotion) {
        const dx = dot.ox - pointer.x;
        const dy = dot.oy - pointer.y;
        const distance = Math.hypot(dx, dy) || 1;
        const radius = 150;
        if (distance < radius) {
          const influence = 1 - distance / radius;
          const push = influence * influence * 36;
          targetX += (dx / distance) * push;
          targetY += (dy / distance) * push;
        }
      }
      if (animate) {
        dot.x += (targetX - dot.x) * 0.2;
        dot.y += (targetY - dot.y) * 0.2;
        if (Math.abs(dot.x - targetX) > 0.2 || Math.abs(dot.y - targetY) > 0.2) moving = true;
      } else {
        dot.x = targetX;
        dot.y = targetY;
      }
      ctx.beginPath();
      ctx.arc(dot.x, dot.y, 1.6, 0, Math.PI * 2);
      ctx.fill();
    }
    return moving;
  }

  function frame() {
    const stillMoving = draw(true);
    if ((pointer || stillMoving) && visible) {
      requestAnimationFrame(frame);
    } else {
      running = false;
    }
  }

  function start() {
    if (running || reduceMotion) return;
    running = true;
    requestAnimationFrame(frame);
  }

  field.addEventListener("pointermove", (event) => {
    pointFromEvent(event);
    start();
  });
  field.addEventListener("pointerdown", (event) => {
    pointFromEvent(event);
    start();
  });
  field.addEventListener("pointerleave", () => {
    pointer = null;
    start();
  });

  const observer = new IntersectionObserver(([entry]) => {
    visible = entry.isIntersecting;
    if (visible) start();
  });
  observer.observe(field);

  window.addEventListener("resize", size);
  size();
}
