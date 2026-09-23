import * as THREE from './vendor/three/three.module.js';

/** Fixed camera: each pool center aligns with its HTML label at 1/6, 1/2, 5/6. */
export function createPoolScene(container, initialEligibility) {
  const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true, powerPreference: 'low-power' });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));
  renderer.setClearColor(0x10141c, 0);
  renderer.domElement.setAttribute('aria-hidden', 'true');
  container.append(renderer.domElement);

  const scene = new THREE.Scene();
  const camera = new THREE.OrthographicCamera(-4.8, 4.8, 2.4, -2.4, 0.1, 40);
  camera.position.set(0, 6, 10);
  camera.lookAt(0, 0, 0);
  scene.add(new THREE.AmbientLight(0xffffff, 2.4));
  const key = new THREE.DirectionalLight(0xffffff, 3);
  key.position.set(-4, 7, 5);
  scene.add(key);
  const geometry = new THREE.CylinderGeometry(0.8, 0.8, 0.16, 48);
  const ringGeometry = new THREE.TorusGeometry(0.8, 0.014, 8, 48);
  const logoGeometry = new THREE.PlaneGeometry(1.6, 1.6);
  const idle = new THREE.Color(0x3c485c);
  const active = new THREE.Color(0x3773ff);
  const values = initialEligibility.map(Number);
  let targets = [...values];
  const stacks = values.map((value, index) => {
    const group = new THREE.Group();
    group.position.x = (index - 1) * 3.2;
    const material = new THREE.MeshStandardMaterial({ color: idle.clone().lerp(active, value), roughness: 0.48, metalness: 0.18 });
    for (let i = 0; i < 3; i++) {
      const disc = new THREE.Mesh(geometry, material);
      disc.position.y = (i - 1) * 0.23;
      group.add(disc);
    }
    const ringMaterial = new THREE.MeshBasicMaterial({ color: 0x3773ff, transparent: true, opacity: value ? 0.8 : 0.15 });
    const ring = new THREE.Mesh(ringGeometry, ringMaterial);
    ring.rotation.x = Math.PI / 2;
    ring.position.y = 0.315;
    group.add(ring);
    const logoMaterial = new THREE.MeshBasicMaterial({
      transparent: true, depthWrite: false, toneMapped: false,
      opacity: value ? 1 : 0.8,
    });
    const logo = new THREE.Mesh(logoGeometry, logoMaterial);
    logo.rotation.x = -Math.PI / 2;
    logo.position.y = 0.327;
    if (index === 2) logo.scale.setScalar(0.46);
    logo.visible = false;
    group.add(logo);
    scene.add(group);
    return { material, ringMaterial, logoMaterial, logo };
  });

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  let visible = true;
  let frame = 0;
  let disposed = false;
  let previousTime = 0;
  const loader = new THREE.TextureLoader();
  const textures = ['flock', 'gemini'].map((name, assetIndex) => loader.load(
    new URL(`./assets/tokens/${name}.svg`, import.meta.url).href,
    (texture) => {
      if (disposed) { texture.dispose(); return; }
      texture.colorSpace = THREE.SRGBColorSpace;
      stacks.forEach((stack, index) => {
        if ((index === 2 ? 1 : 0) !== assetIndex) return;
        stack.logoMaterial.map = texture;
        stack.logoMaterial.needsUpdate = true;
        stack.logo.visible = true;
      });
      requestRender();
    },
    undefined,
    () => {
      // Keep the labeled static illustration if a logo cannot load.
      if (!disposed) dispose();
    },
  ));
  function render() {
    if (disposed) return;
    stacks.forEach((stack, i) => {
      stack.material.color.copy(idle).lerp(active, values[i]);
      stack.ringMaterial.opacity = 0.15 + 0.65 * values[i];
      stack.logoMaterial.opacity = 0.8 + 0.2 * values[i];
    });
    renderer.render(scene, camera);
  }
  function tick(time) {
    frame = 0;
    if (!visible || document.hidden || disposed) return;
    const dt = Math.min(time - previousTime || 16, 50);
    previousTime = time;
    let moving = false;
    values.forEach((value, i) => {
      values[i] = reduced.matches ? targets[i] : value + (targets[i] - value) * (1 - Math.exp(-dt / 65));
      if (Math.abs(values[i] - targets[i]) < 0.002) values[i] = targets[i];
      else moving = true;
    });
    render();
    if (moving) frame = requestAnimationFrame(tick);
  }
  function requestRender() {
    if (!frame && visible && !document.hidden && !disposed) {
      previousTime = 0;
      frame = requestAnimationFrame(tick);
    }
  }
  const resize = new ResizeObserver(() => {
    const { width, height } = container.getBoundingClientRect();
    if (!width || !height || disposed) return;
    renderer.setSize(width, height, false);
    camera.top = 4.8 * height / width;
    camera.bottom = -camera.top;
    camera.updateProjectionMatrix();
    requestRender();
  });
  const visibility = new IntersectionObserver((entries) => {
    visible = entries[0].isIntersecting;
    if (visible) requestRender();
    else { cancelAnimationFrame(frame); frame = 0; }
  });
  const onDocumentVisibility = () => {
    if (document.hidden) { cancelAnimationFrame(frame); frame = 0; }
    else requestRender();
  };
  const onContextLost = (event) => {
    event.preventDefault();
    container.dataset.ready = 'false';
    dispose();
  };
  const onPageHide = (event) => {
    if (!event.persisted) dispose();
    else { cancelAnimationFrame(frame); frame = 0; }
  };
  function dispose() {
    if (disposed) return;
    disposed = true;
    cancelAnimationFrame(frame);
    resize.disconnect();
    visibility.disconnect();
    reduced.removeEventListener('change', requestRender);
    document.removeEventListener('visibilitychange', onDocumentVisibility);
    window.removeEventListener('pagehide', onPageHide);
    window.removeEventListener('pageshow', requestRender);
    renderer.domElement.removeEventListener('webglcontextlost', onContextLost);
    geometry.dispose();
    ringGeometry.dispose();
    logoGeometry.dispose();
    textures.forEach((texture) => texture.dispose());
    stacks.forEach(({ material, ringMaterial, logoMaterial }) => {
      material.dispose(); ringMaterial.dispose(); logoMaterial.dispose();
    });
    renderer.dispose();
    renderer.domElement.remove();
    container.dataset.ready = 'false';
  }
  resize.observe(container);
  visibility.observe(container);
  reduced.addEventListener('change', requestRender);
  document.addEventListener('visibilitychange', onDocumentVisibility);
  renderer.domElement.addEventListener('webglcontextlost', onContextLost);
  window.addEventListener('pagehide', onPageHide);
  window.addEventListener('pageshow', requestRender);
  container.dataset.ready = 'true';
  requestRender();
  return {
    setEligibility(eligibility) { targets = eligibility.map(Number); requestRender(); },
    dispose
  };
}
