/*!
 * HeadFollow: la cabeza de marca 2894 sigue al puntero.
 *
 * Parallax 2.5D: un mapa de profundidad desplaza los píxeles del PNG original
 * según la posición del puntero. No se pinta nada nuevo; cada píxel visible
 * sale de la imagen original, y con el puntero centrado la imagen es idéntica.
 *
 * Uso (mejora progresiva: el <img> es el fallback y el texto alternativo):
 *   <div data-head-follow data-depth="assets/head-depth.png">
 *     <img src="assets/head.png" alt="2894_">
 *   </div>
 *   <script src="head-follow.js" defer></script>
 *
 * O por código: const h = HeadFollow.mount(el, { strength: 0.03 });
 *   h.setOptions({ smoothing: 6 }); h.destroy();
 */
(function () {
  "use strict";

  var DEFAULTS = {
    strength: 0.03, // desplazamiento máximo, en fracción del ancho de la imagen
    smoothing: 7, // frecuencia del muelle: más alto es más rápido
    pivot: 0.45, // profundidad que no se mueve (0 lejos, 1 cerca)
    idle: true, // leve respiración cuando el puntero está quieto
  };

  var VERT =
    "attribute vec2 p;varying vec2 uv;" +
    "void main(){uv=vec2(p.x*.5+.5,.5-p.y*.5);gl_Position=vec4(p,0.,1.);}";

  // Inversión por punto fijo del desplazamiento s + o·(h(s)−pivot) = uv.
  // Converge porque el mapa es suave y el desplazamiento pequeño.
  var FRAG =
    "precision highp float;varying vec2 uv;" +
    "uniform sampler2D img,dep;uniform vec2 o;uniform float pivot;" +
    "void main(){vec2 s=uv;" +
    "for(int i=0;i<6;i++){s=uv-o*(texture2D(dep,s).r-pivot);}" +
    "if(s.x<0.||s.y<0.||s.x>1.||s.y>1.){gl_FragColor=vec4(0.);return;}" +
    "gl_FragColor=texture2D(img,s);}";

  function loadImage(src) {
    return new Promise(function (resolve, reject) {
      var im = new Image();
      im.crossOrigin = "anonymous";
      im.onload = function () { resolve(im); };
      im.onerror = reject;
      im.src = src;
    });
  }

  function mount(el, opts) {
    var o = Object.assign({}, DEFAULTS, opts);
    var img = el.querySelector("img");
    var depthSrc = o.depth || el.getAttribute("data-depth");
    var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
    if (!img || !depthSrc || reduce.matches) return null;

    var canvas = document.createElement("canvas");
    canvas.setAttribute("aria-hidden", "true");
    // pointer-events:none para que el lienzo nunca reciba foco, selección ni arrastre.
    canvas.style.cssText = "position:absolute;inset:0;width:100%;height:100%;pointer-events:none;outline:none;";
    var gl2 = canvas.getContext("webgl2", { premultipliedAlpha: true, antialias: false });
    var gl = gl2 || canvas.getContext("webgl", { premultipliedAlpha: true, antialias: false });
    if (!gl) return null;

    var state = { x: 0, y: 0, vx: 0, vy: 0, tx: 0, ty: 0, lastMove: 0 };
    var raf = 0, visible = true, ready = false, destroyed = false, last = 0;

    function shader(type, src) {
      var s = gl.createShader(type);
      gl.shaderSource(s, src);
      gl.compileShader(s);
      return s;
    }
    var prog = gl.createProgram();
    gl.attachShader(prog, shader(gl.VERTEX_SHADER, VERT));
    gl.attachShader(prog, shader(gl.FRAGMENT_SHADER, FRAG));
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) return null;
    gl.useProgram(prog);

    gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    var loc = gl.getAttribLocation(prog, "p");
    gl.enableVertexAttribArray(loc);
    gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    var uO = gl.getUniformLocation(prog, "o");
    var uPivot = gl.getUniformLocation(prog, "pivot");

    function texture(unit, source, premultiply) {
      gl.activeTexture(gl.TEXTURE0 + unit);
      gl.bindTexture(gl.TEXTURE_2D, gl.createTexture());
      gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL, premultiply);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, source);
      // WebGL2 admite mipmaps en texturas de cualquier tamaño: nitidez sin aliasing al reducir.
      if (gl2) {
        gl.generateMipmap(gl.TEXTURE_2D);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);
      } else {
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
      }
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    }

    function resize() {
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      var w = Math.round(el.clientWidth * dpr), h = Math.round(el.clientHeight * dpr);
      if (canvas.width !== w || canvas.height !== h) {
        canvas.width = w;
        canvas.height = h;
        gl.viewport(0, 0, w, h);
      }
      wake();
    }

    function onPointer(e) {
      var r = el.getBoundingClientRect();
      var cx = r.left + r.width / 2, cy = r.top + r.height / 2;
      // Normaliza respecto a media ventana: el giro máximo llega en el borde de la pantalla.
      var nx = (e.clientX - cx) / (window.innerWidth / 2);
      var ny = (e.clientY - cy) / (window.innerHeight / 2);
      state.tx = Math.tanh(nx * 1.4);
      state.ty = Math.tanh(ny * 1.4);
      state.lastMove = performance.now();
      wake();
    }
    function onLeave(e) {
      if (e.relatedTarget) return;
      state.tx = 0;
      state.ty = 0;
      wake();
    }

    function frame(now) {
      raf = 0;
      var dt = Math.min((now - (last || now)) / 1000, 1 / 20);
      last = now;

      var tx = state.tx, ty = state.ty;
      var idleFor = (now - state.lastMove) / 1000;
      if (o.idle && idleFor > 2.5) {
        var k = Math.min((idleFor - 2.5) / 2, 1) * 0.08;
        tx += Math.sin(now / 2300) * k;
        ty += Math.sin(now / 3100) * k * 0.6;
      }

      // Muelle críticamente amortiguado: inercia sin rebote.
      var w = o.smoothing;
      state.vx += (w * w * (tx - state.x) - 2 * w * state.vx) * dt;
      state.vy += (w * w * (ty - state.y) - 2 * w * state.vy) * dt;
      state.x += state.vx * dt;
      state.y += state.vy * dt;

      var aspect = el.clientWidth / el.clientHeight;
      gl.uniform2f(uO, state.x * o.strength, state.y * o.strength * aspect);
      gl.uniform1f(uPivot, o.pivot);
      gl.clearColor(0, 0, 0, 0);
      gl.clear(gl.COLOR_BUFFER_BIT);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);

      var settled = Math.abs(tx - state.x) + Math.abs(ty - state.y) +
        Math.abs(state.vx) + Math.abs(state.vy) < 1e-4;
      if (!settled || o.idle) wake();
      else last = 0;
    }

    function wake() {
      if (!raf && ready && visible && !destroyed) raf = requestAnimationFrame(frame);
    }

    var io = new IntersectionObserver(function (entries) {
      visible = entries[0].isIntersecting && !document.hidden;
      if (!visible) last = 0;
      wake();
    });
    function onVisibility() {
      visible = !document.hidden;
      last = 0;
      wake();
    }
    var ro = new ResizeObserver(resize);

    Promise.all([
      img.complete && img.naturalWidth ? img : loadImage(img.currentSrc || img.src),
      loadImage(depthSrc),
    ]).then(function (images) {
      if (destroyed) return;
      texture(0, images[0], true);
      texture(1, images[1], false);
      gl.uniform1i(gl.getUniformLocation(prog, "img"), 0);
      gl.uniform1i(gl.getUniformLocation(prog, "dep"), 1);

      if (getComputedStyle(el).position === "static") el.style.position = "relative";
      // Sin el resaltado azul de selección (clic, doble clic), toque (móvil) ni arrastre nativo.
      el.style.userSelect = el.style.webkitUserSelect = "none";
      el.style.webkitTapHighlightColor = "transparent";
      img.draggable = false;
      el.appendChild(canvas);
      img.style.visibility = "hidden"; // conserva el layout y el alt
      ready = true;
      state.lastMove = performance.now();
      window.addEventListener("pointermove", onPointer, { passive: true });
      window.addEventListener("pointerdown", onPointer, { passive: true });
      document.addEventListener("pointerout", onLeave);
      document.addEventListener("visibilitychange", onVisibility);
      io.observe(el);
      ro.observe(el);
      resize();
    }).catch(function () { /* el <img> queda visible */ });

    return {
      setOptions: function (next) { Object.assign(o, next); wake(); },
      destroy: function () {
        destroyed = true;
        cancelAnimationFrame(raf);
        window.removeEventListener("pointermove", onPointer);
        window.removeEventListener("pointerdown", onPointer);
        document.removeEventListener("pointerout", onLeave);
        document.removeEventListener("visibilitychange", onVisibility);
        io.disconnect();
        ro.disconnect();
        canvas.remove();
        img.style.visibility = "";
        img.draggable = true;
        el.style.userSelect = el.style.webkitUserSelect = el.style.webkitTapHighlightColor = "";
      },
    };
  }

  window.HeadFollow = { mount: mount, defaults: DEFAULTS };

  function auto() {
    document.querySelectorAll("[data-head-follow]").forEach(function (el) {
      el.headFollow = mount(el);
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", auto);
  else auto();
})();
