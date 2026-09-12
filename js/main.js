/**
 * FU-GLIDE | Modern Motion, 3D WebGL & Interaction Engine
 * Features:
 *  - Three.js Interactive 3D Hero Stage (Abstract Geometry, Nodes, Mouse Parallax)
 *  - Sitewide Ambient 3D Particle Atmosphere
 *  - Physics-based 3D Card Perspective Tilt & Dynamic Specular Shine
 *  - GSAP & ScrollTrigger Staggered 3D Scroll Reveals
 *  - Page-Hero Animated Staggered Typography
 *  - Glass Header Scroll Blur & Mobile Drawer Navigation
 */

document.addEventListener('DOMContentLoaded', async () => {
  await initHeader();
  initFooter();
  init3DCardTilt();
  initScrollAnimations();
  initHeroTypography();
  initAmbientBackground();
  initThreeJSHero();
  initBackToTop();
  initHeroRotator();
  initHeroLeadForm();
  initServiceImageLightbox();
});

/* ==========================================================================
   1. Standardized Navigation & Mobile Drawer
   ========================================================================== */
function initNavigation() {
  const navToggle = document.querySelector('.nav-toggle');
  const navLinks = document.querySelector('.nav-links');
  const dropdowns = document.querySelectorAll('.dropdown');

  if (navToggle && navLinks && !navToggle.dataset.initialized) {
    navToggle.dataset.initialized = 'true';
    navToggle.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpen = navLinks.classList.toggle('is-open');
      navToggle.classList.toggle('is-active', isOpen);
      navToggle.setAttribute('aria-expanded', String(isOpen));
    });

    // Close mobile drawer when clicking outside
    document.addEventListener('click', (e) => {
      if (navLinks.classList.contains('is-open') && !navLinks.contains(e.target) && !navToggle.contains(e.target)) {
        navLinks.classList.remove('is-open');
        navToggle.classList.remove('is-active');
        navToggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // Handle dropdown toggle on click for all devices
  dropdowns.forEach((dropdown) => {
    const toggleBtn = dropdown.querySelector('.dropdown-toggle');
    if (toggleBtn && !toggleBtn.dataset.initialized) {
      toggleBtn.dataset.initialized = 'true';
      toggleBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();

        const isCurrentlyExpanded = dropdown.classList.contains('is-expanded') || dropdown.classList.contains('is-open');

        // Close all other dropdowns
        dropdowns.forEach(other => {
          if (other !== dropdown) {
            other.classList.remove('is-expanded', 'is-open');
            const otherBtn = other.querySelector('.dropdown-toggle');
            if (otherBtn) otherBtn.setAttribute('aria-expanded', 'false');
          }
        });

        // Toggle this dropdown
        dropdown.classList.toggle('is-expanded', !isCurrentlyExpanded);
        dropdown.classList.toggle('is-open', !isCurrentlyExpanded);
        toggleBtn.setAttribute('aria-expanded', String(!isCurrentlyExpanded));
      });
    }
  });

  // Close dropdowns when clicking anywhere outside
  if (!document.body.dataset.dropdownListenerAttached) {
    document.body.dataset.dropdownListenerAttached = 'true';
    document.addEventListener('click', (e) => {
      dropdowns.forEach(dropdown => {
        if (!dropdown.contains(e.target)) {
          dropdown.classList.remove('is-expanded', 'is-open');
          const toggleBtn = dropdown.querySelector('.dropdown-toggle');
          if (toggleBtn) toggleBtn.setAttribute('aria-expanded', 'false');
        }
      });
    });
  }
}

/* ==========================================================================
   2. Sticky Glass Header Scroll Effect
   ========================================================================== */
function initStickyHeader() {
  const header = document.querySelector('.site-header');
  if (!header) return;

  const handleScroll = () => {
    if (window.scrollY > 30) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  };

  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll();
}

// Expose globally for components and loaders
window.initNavigation = initNavigation;
window.initStickyHeader = initStickyHeader;

/* ==========================================================================
   3. Interactive 3D Perspective Card Tilt with Specular Reflection
   ========================================================================== */
function init3DCardTilt() {
  // Check if touch device or reduced motion is preferred
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches || 'ontouchstart' in window) {
    return;
  }

  const tiltCards = document.querySelectorAll(
    '.stat-card, .partner-card, .feature-item, .team-card, .info-card, .portfolio-card, .hero-card .card-panel, .contact-panel, .form-shell'
  );

  tiltCards.forEach((card) => {
    let bounds;
    let isHovering = false;

    const onMouseEnter = () => {
      bounds = card.getBoundingClientRect();
      isHovering = true;
      card.style.transition = 'transform 0.1s ease-out, border-color 0.3s ease, box-shadow 0.3s ease';
    };

    const onMouseMove = (e) => {
      if (!isHovering) return;
      if (!bounds) bounds = card.getBoundingClientRect();

      const mouseX = e.clientX - bounds.left;
      const mouseY = e.clientY - bounds.top;

      // Set CSS variables for radial specular light sweep
      card.style.setProperty('--mouse-x', `${mouseX}px`);
      card.style.setProperty('--mouse-y', `${mouseY}px`);

      // Calculate tilt angles (-10deg to +10deg)
      const xPct = (mouseX / bounds.width - 0.5) * 2;
      const yPct = (mouseY / bounds.height - 0.5) * 2;

      const rotateX = -yPct * 7.5;
      const rotateY = xPct * 7.5;

      card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) scale3d(1.015, 1.015, 1.015)`;
    };

    const onMouseLeave = () => {
      isHovering = false;
      card.style.transition = 'transform 0.5s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.3s ease, box-shadow 0.3s ease';
      card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
    };

    card.addEventListener('mouseenter', onMouseEnter);
    card.addEventListener('mousemove', onMouseMove);
    card.addEventListener('mouseleave', onMouseLeave);
  });
}

/* ==========================================================================
   4. Staggered 3D Scroll Reveals (GSAP ScrollTrigger or IntersectionObserver)
   ========================================================================== */
function initScrollAnimations() {
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const revealElements = document.querySelectorAll('.reveal');

  if (prefersReduced) {
    revealElements.forEach((el) => el.classList.add('is-visible'));
    return;
  }

  // Use GSAP ScrollTrigger if loaded
  if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
    gsap.registerPlugin(ScrollTrigger);

    revealElements.forEach((element) => {
      gsap.fromTo(
        element,
        {
          opacity: 0,
          x: 35,
          transformPerspective: 800,
        },
        {
          opacity: 1,
          x: 0,
          duration: 0.95,
          ease: 'power3.out',
          scrollTrigger: {
            trigger: element,
            start: 'top 88%',
            toggleActions: 'play none none none',
            once: true,
          },
          onComplete: () => {
            element.classList.add('is-visible');
            element.style.transform = '';
          },
        }
      );
    });
  } else {
    // Robust Intersection Observer fallback
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
    );

    revealElements.forEach((el) => observer.observe(el));
  }
}

/* ==========================================================================
   5. Page-Hero Animated Staggered Typography
   ========================================================================== */
function initHeroTypography() {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const pageHeroH1 = document.querySelector('.page-hero h1, .hero h1');
  if (!pageHeroH1) return;

  if (typeof gsap !== 'undefined') {
    gsap.from(pageHeroH1, {
      opacity: 0,
      y: 35,
      filter: 'blur(8px)',
      duration: 0.95,
      ease: 'power3.out',
      delay: 0.2,
    });

    const eyebrow = document.querySelector('.hero .eyebrow, .page-hero .eyebrow');
    if (eyebrow) {
      gsap.from(eyebrow, {
        opacity: 0,
        scale: 0.85,
        y: 20,
        duration: 0.8,
        ease: 'back.out(1.7)',
      });
    }
  }
}

/* ==========================================================================
   6. Sitewide Ambient 3D Particle Canvas Atmosphere
   ========================================================================== */
function initAmbientBackground() {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  let canvas = document.getElementById('ambient-bg-canvas');
  if (!canvas) {
    canvas = document.createElement('canvas');
    canvas.id = 'ambient-bg-canvas';
    canvas.className = 'ambient-particles-canvas';
    document.body.prepend(canvas);
  }

  const ctx = canvas.getContext('2d');
  let width, height;
  let particles = [];
  let animId = null;

  const resize = () => {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  };

  window.addEventListener('resize', resize, { passive: true });
  resize();

  const particleCount = window.innerWidth < 768 ? 24 : 48;
  const colors = ['rgba(176, 108, 255, 0.45)', 'rgba(246, 184, 75, 0.35)', 'rgba(255, 255, 255, 0.25)'];

  for (let i = 0; i < particleCount; i++) {
    particles.push({
      x: Math.random() * width,
      y: Math.random() * height,
      radius: Math.random() * 2 + 0.8,
      color: colors[Math.floor(Math.random() * colors.length)],
      vx: (Math.random() - 0.5) * 0.4,
      vy: (Math.random() - 0.5) * 0.4,
      pulse: Math.random() * Math.PI,
    });
  }

  function render() {
    ctx.clearRect(0, 0, width, height);

    for (let i = 0; i < particles.length; i++) {
      const p = particles[i];
      p.x += p.vx;
      p.y += p.vy;
      p.pulse += 0.02;

      if (p.x < 0) p.x = width;
      if (p.x > width) p.x = 0;
      if (p.y < 0) p.y = height;
      if (p.y > height) p.y = 0;

      const alpha = 0.3 + 0.35 * Math.sin(p.pulse);
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius * (1 + 0.2 * Math.sin(p.pulse)), 0, Math.PI * 2);
      ctx.fillStyle = p.color;
      ctx.globalAlpha = Math.max(0.1, alpha);
      ctx.fill();
    }

    // Connect close particles with subtle energy lines
    ctx.globalAlpha = 0.08;
    ctx.strokeStyle = '#b06cff';
    ctx.lineWidth = 0.75;
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 120) {
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.stroke();
        }
      }
    }
    ctx.globalAlpha = 1;

    animId = requestAnimationFrame(render);
  }

  // Handle visibility optimization
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      if (animId) cancelAnimationFrame(animId);
    } else {
      animId = requestAnimationFrame(render);
    }
  });

  animId = requestAnimationFrame(render);
}

/* ==========================================================================
   7. Three.js Interactive 3D Hero Scene (Geometric Hub + Mouse Parallax)
   ========================================================================== */
function initThreeJSHero() {
  const canvas = document.getElementById('hero-canvas');
  if (!canvas || typeof THREE === 'undefined') return;

  const container = canvas.parentElement || canvas;
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Scene, Camera, Renderer
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.1, 1000);
  camera.position.z = 24;

  const renderer = new THREE.WebGLRenderer({
    canvas: canvas,
    alpha: true,
    antialias: window.devicePixelRatio < 2,
    powerPreference: 'high-performance',
  });

  renderer.setSize(container.clientWidth, container.clientHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

  // Lighting
  const ambientLight = new THREE.AmbientLight(0x1a243b, 1.8);
  scene.add(ambientLight);

  const violetLight = new THREE.PointLight(0xb06cff, 3.5, 60);
  violetLight.position.set(10, 12, 15);
  scene.add(violetLight);

  const goldLight = new THREE.PointLight(0xf6b84b, 3, 60);
  goldLight.position.set(-12, -8, 12);
  scene.add(goldLight);

  // Group for overall scene rotation & mouse parallax
  const mainGroup = new THREE.Group();
  scene.add(mainGroup);

  // 1. Central Hero Icosahedron Core (Software / Innovation)
  const coreGeo = new THREE.IcosahedronGeometry(4.8, 1);
  const coreMat = new THREE.MeshStandardMaterial({
    color: 0x121e38,
    wireframe: true,
    emissive: 0x7c3aed,
    emissiveIntensity: 0.45,
    roughness: 0.2,
    metalness: 0.8,
  });
  const coreMesh = new THREE.Mesh(coreGeo, coreMat);
  mainGroup.add(coreMesh);

  // Inner Glowing Crystal Solid
  const innerGeo = new THREE.OctahedronGeometry(2.4, 0);
  const innerMat = new THREE.MeshStandardMaterial({
    color: 0xf6b84b,
    emissive: 0xf6b84b,
    emissiveIntensity: 0.6,
    roughness: 0.1,
    metalness: 0.9,
  });
  const innerMesh = new THREE.Mesh(innerGeo, innerMat);
  mainGroup.add(innerMesh);

  // 2. Orbital Torus Ring 1 (Apps & Ecosystem)
  const torusGeo1 = new THREE.TorusGeometry(7.2, 0.08, 16, 100);
  const torusMat1 = new THREE.MeshStandardMaterial({
    color: 0xb06cff,
    emissive: 0xb06cff,
    emissiveIntensity: 0.7,
    roughness: 0.3,
  });
  const torus1 = new THREE.Mesh(torusGeo1, torusMat1);
  torus1.rotation.x = Math.PI / 3;
  torus1.rotation.y = Math.PI / 6;
  mainGroup.add(torus1);

  // Orbital Torus Ring 2 (Tutoring & Career Elevation)
  const torusGeo2 = new THREE.TorusGeometry(8.6, 0.06, 16, 100);
  const torusMat2 = new THREE.MeshStandardMaterial({
    color: 0xf6b84b,
    emissive: 0xf6b84b,
    emissiveIntensity: 0.8,
    roughness: 0.3,
  });
  const torus2 = new THREE.Mesh(torusGeo2, torusMat2);
  torus2.rotation.x = -Math.PI / 4;
  torus2.rotation.z = Math.PI / 3;
  mainGroup.add(torus2);

  // 3. Floating Satellite Polyhedra (Floating Modules)
  const satellites = [];
  const satelliteGeo = [
    new THREE.BoxGeometry(1.2, 1.2, 1.2),
    new THREE.TetrahedronGeometry(1.1),
    new THREE.OctahedronGeometry(1.0),
    new THREE.DodecahedronGeometry(0.9),
  ];

  for (let i = 0; i < 6; i++) {
    const geo = satelliteGeo[i % satelliteGeo.length];
    const isGold = i % 2 === 0;
    const mat = new THREE.MeshStandardMaterial({
      color: isGold ? 0xf6b84b : 0xb06cff,
      wireframe: true,
      emissive: isGold ? 0xf6b84b : 0xb06cff,
      emissiveIntensity: 0.5,
    });
    const mesh = new THREE.Mesh(geo, mat);
    const angle = (i / 6) * Math.PI * 2;
    const radius = 9.5 + Math.sin(i * 1.5) * 2;
    mesh.position.set(Math.cos(angle) * radius, Math.sin(angle) * (radius * 0.6), (Math.random() - 0.5) * 6);
    mesh.userData = {
      angle: angle,
      speed: 0.004 + i * 0.0015,
      radius: radius,
      rotSpeedX: (Math.random() - 0.5) * 0.02,
      rotSpeedY: (Math.random() - 0.5) * 0.02,
      yOffset: mesh.position.y,
    };
    satellites.push(mesh);
    mainGroup.add(mesh);
  }

  // 4. Background Starfield / Particle Cloud
  const particleGeo = new THREE.BufferGeometry();
  const particleCount = window.innerWidth < 768 ? 120 : 260;
  const posArray = new Float32Array(particleCount * 3);

  for (let i = 0; i < particleCount * 3; i += 3) {
    posArray[i] = (Math.random() - 0.5) * 60;
    posArray[i + 1] = (Math.random() - 0.5) * 40;
    posArray[i + 2] = (Math.random() - 0.5) * 30;
  }

  particleGeo.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
  const particleMat = new THREE.PointsMaterial({
    size: 0.18,
    color: 0xb06cff,
    transparent: true,
    opacity: 0.85,
    blending: THREE.AdditiveBlending,
  });
  const particleCloud = new THREE.Points(particleGeo, particleMat);
  mainGroup.add(particleCloud);

  // Mouse Tracking for Parallax
  let mouseX = 0;
  let mouseY = 0;
  let targetX = 0;
  let targetY = 0;

  const onPointerMove = (e) => {
    const halfW = window.innerWidth / 2;
    const halfH = window.innerHeight / 2;
    mouseX = (e.clientX - halfW) / halfW;
    mouseY = (e.clientY - halfH) / halfH;
  };

  window.addEventListener('mousemove', onPointerMove, { passive: true });

  // Handle Resize
  const onResize = () => {
    if (!container) return;
    const w = container.clientWidth;
    const h = container.clientHeight;
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  };
  window.addEventListener('resize', onResize, { passive: true });

  // Performance Guardrail: Intersection Observer to pause Three.js loop when scrolled off-screen
  let isVisible = true;
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      isVisible = entry.isIntersecting;
    });
  }, { threshold: 0.05 });
  observer.observe(container);

  // Animation Loop with Lerped Damping
  let clock = new THREE.Clock();
  let animFrameId = null;

  const animate = () => {
    animFrameId = requestAnimationFrame(animate);
    if (!isVisible || document.hidden || prefersReduced) return;

    const elapsedTime = clock.getElapsedTime();

    // Lerped Mouse Parallax
    targetX += (mouseX - targetX) * 0.05;
    targetY += (mouseY - targetY) * 0.05;

    mainGroup.rotation.y = targetX * 0.4 + elapsedTime * 0.08;
    mainGroup.rotation.x = -targetY * 0.35;

    // Rotate core & rings
    coreMesh.rotation.x = elapsedTime * 0.15;
    coreMesh.rotation.y = elapsedTime * 0.2;
    innerMesh.rotation.y = -elapsedTime * 0.35;
    innerMesh.rotation.z = elapsedTime * 0.25;

    torus1.rotation.z = elapsedTime * 0.25;
    torus2.rotation.y = -elapsedTime * 0.2;

    // Animate satellite nodes
    satellites.forEach((sat) => {
      sat.userData.angle += sat.userData.speed;
      sat.position.x = Math.cos(sat.userData.angle) * sat.userData.radius;
      sat.position.y = Math.sin(sat.userData.angle) * (sat.userData.radius * 0.6) + Math.sin(elapsedTime * 1.5 + sat.userData.angle) * 0.5;
      sat.rotation.x += sat.userData.rotSpeedX;
      sat.rotation.y += sat.userData.rotSpeedY;
    });

    // Pulse lights gently
    violetLight.intensity = 3.2 + Math.sin(elapsedTime * 2) * 0.8;
    goldLight.intensity = 2.8 + Math.cos(elapsedTime * 2) * 0.7;

    renderer.render(scene, camera);
  };

  animate();

  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      if (animFrameId) cancelAnimationFrame(animFrameId);
    } else {
      clock.start();
      animate();
    }
  });
}

/* ==========================================================================
   Back to Top Floating Action
   ========================================================================== */
function initBackToTop() {
  const backToTopBtn = document.getElementById('backToTop');
  if (!backToTopBtn) return;

  const handleScroll = () => {
    if (window.scrollY > 300) {
      backToTopBtn.classList.add('is-visible');
    } else {
      backToTopBtn.classList.remove('is-visible');
    }
  };

  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll();

  backToTopBtn.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });
}

/* ==========================================================================
   Hero Dynamic Text Rotator
   ========================================================================== */
function initHeroRotator() {
  const rotatorElement = document.getElementById('heroRotatorDynamic');
  if (!rotatorElement) return;

  const words = ['EXCELLENCE', 'EXPERTISE', 'SKILLS', 'SUCCESS'];
  let currentIndex = 0;

  setInterval(() => {
    rotatorElement.classList.add('rotate-out');

    setTimeout(() => {
      currentIndex = (currentIndex + 1) % words.length;
      rotatorElement.textContent = words[currentIndex];
      rotatorElement.classList.remove('rotate-out');
      rotatorElement.classList.add('rotate-in');

      setTimeout(() => {
        rotatorElement.classList.remove('rotate-in');
      }, 350);
    }, 350);
  }, 2600);
}

/* ==========================================================================
   Hero Lead Generation Form Submission
   ========================================================================== */
function initHeroLeadForm() {
  const form = document.getElementById('heroLeadForm');
  if (!form) return;

  const statusMsg = document.getElementById('heroFormStatus');
  const submitBtn = form.querySelector('.hero-btn-gold');
  const btnText = submitBtn ? submitBtn.querySelector('.hero-btn-text') : null;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = form.elements['name']?.value?.trim() || '';
    const email = form.elements['email']?.value?.trim() || '';
    const phone = form.elements['phone']?.value?.trim() || '';
    const course = form.elements['course']?.value || '';

    if (!name || !email || !phone || !course) {
      if (statusMsg) {
        statusMsg.textContent = 'Please fill out all fields.';
        statusMsg.className = 'hero-form-status error';
      }
      return;
    }

    if (btnText) btnText.textContent = 'Submitting...';
    if (submitBtn) submitBtn.disabled = true;

    try {
      if (window.db && typeof window.db.collection === 'function') {
        await window.db.collection('lead_submissions').add({
          name,
          email,
          phone,
          course,
          source: 'Hero Above-The-Fold Form',
          createdAt: new Date().toISOString()
        });
      }
    } catch (err) {
      console.warn('Firebase store lead note:', err);
    }

    setTimeout(() => {
      if (statusMsg) {
        statusMsg.textContent = '✓ Thank you! We will get in touch with you shortly.';
        statusMsg.className = 'hero-form-status success';
      }
      form.reset();
      if (btnText) btnText.textContent = 'Submit';
      if (submitBtn) submitBtn.disabled = false;

      setTimeout(() => {
        if (statusMsg) {
          statusMsg.textContent = '';
          statusMsg.className = 'hero-form-status';
        }
      }, 6000);
    }, 600);
  });
}

/* ==========================================================================
   Common Modular Header Loader
   ========================================================================== */
async function initHeader() {
  const placeholder = document.getElementById('header-placeholder');
  
  if (placeholder) {
    const relativeRoot = getRelativeSiteRoot();
    const candidatePaths = [
      `${relativeRoot}header.html`,
      '/header.html',
      'header.html',
      '../header.html',
      '../../header.html',
      './header.html'
    ];

    let headerHtml = '';
    for (const path of candidatePaths) {
      try {
        const response = await fetch(path);
        if (response.ok) {
          headerHtml = await response.text();
          break;
        }
      } catch (e) {
        // Try next candidate path
      }
    }

    if (headerHtml) {
      placeholder.outerHTML = headerHtml;
      normalizeLocalSitePaths();
    }
  }

  // Bind navigation listeners & sticky effects whether header was static or injected
  initNavigation();
  initStickyHeader();
  highlightActiveNav();

  // If URL has a hash anchor (e.g. #seo, #smo, #robotics, etc.), scroll smoothly after DOM paints
  if (window.location.hash) {
    setTimeout(() => {
      try {
        const target = document.querySelector(window.location.hash);
        if (target) {
          target.scrollIntoView({ behavior: 'smooth' });
        }
      } catch (e) {
        // Ignore invalid selectors
      }
    }, 200);
  }
}

function highlightActiveNav() {
  const currentPath = window.location.pathname.toLowerCase().replace(/^\//, '');
  const links = document.querySelectorAll('.nav-links a');
  
  links.forEach(link => {
    const href = link.getAttribute('href');
    if (!href) return;
    const cleanHref = href.toLowerCase().replace(/^\.\//, '').replace(/^\.\.\//, '').replace(/^\//, '');
    
    if (cleanHref && (currentPath === cleanHref || (cleanHref === 'index.html' && (currentPath === '' || currentPath === 'index.html')))) {
      link.classList.add('active');
    }
  });
}

/* ==========================================================================
   Common Modular Footer Loader
   ========================================================================== */
async function initFooter() {
  const placeholder = document.getElementById('footer-placeholder');
  if (placeholder) {
    const relativeRoot = getRelativeSiteRoot();
    const candidatePaths = [
      `${relativeRoot}footer.html`,
      '/footer.html',
      'footer.html',
      '../footer.html',
      '../../footer.html',
      './footer.html'
    ];

    let footerHtml = '';
    for (const path of candidatePaths) {
      try {
        const response = await fetch(path);
        if (response.ok) {
          footerHtml = await response.text();
          break;
        }
      } catch (e) {
        // Try next candidate path
      }
    }

    if (footerHtml) {
      placeholder.outerHTML = footerHtml;
      normalizeLocalSitePaths();
    }
  }

  // Auto-update copyright year across all footers (static or dynamically loaded)
  const yearEl = document.querySelector('.footer-bottom p');
  if (yearEl) {
    const currentYear = new Date().getFullYear().toString();
    if (!yearEl.innerHTML.includes(currentYear)) {
      yearEl.innerHTML = yearEl.innerHTML.replace(/\b20\d{2}\b/, currentYear);
    }
  }
}

function getRelativeSiteRoot() {
  const currentPath = window.location.pathname.toLowerCase();
  if (currentPath.includes('/course_details.html/')) return '../../';
  if (currentPath.includes('/pages/')) return '../';
  return '';
}

function normalizeLocalSitePaths() {
  const relativeRoot = getRelativeSiteRoot();
  document.querySelectorAll('a[href^="/"], img[src^="/"]').forEach((element) => {
    const attribute = element.hasAttribute('href') ? 'href' : 'src';
    const value = element.getAttribute(attribute);
    element.setAttribute(attribute, `${relativeRoot}${value.slice(1)}`);
  });
}

/* ==========================================================================
   Service Image Fullscreen Lightbox Preview
   ========================================================================== */
function initServiceImageLightbox() {
  const imageWraps = document.querySelectorAll('.service-card-image-wrap');
  if (!imageWraps.length) return;

  // Create modal container once if it doesn't exist
  let modal = document.querySelector('.service-lightbox-modal');
  if (!modal) {
    modal = document.createElement('div');
    modal.className = 'service-lightbox-modal';
    modal.setAttribute('role', 'dialog');
    modal.setAttribute('aria-modal', 'true');
    modal.setAttribute('aria-label', 'Full Service Image Preview');
    modal.innerHTML = `
      <div class="service-lightbox-dialog">
        <button type="button" class="service-lightbox-close" aria-label="Close Preview">&times;</button>
        <img class="service-lightbox-img" src="" alt="Service Full Image Preview" />
        <p class="service-lightbox-caption"></p>
      </div>
    `;
    document.body.appendChild(modal);

    const closeBtn = modal.querySelector('.service-lightbox-close');
    const closeModal = () => {
      modal.classList.remove('is-active');
      document.body.style.overflow = '';
    };

    closeBtn.addEventListener('click', closeModal);
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal();
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal.classList.contains('is-active')) {
        closeModal();
      }
    });
  }

  const modalImg = modal.querySelector('.service-lightbox-img');
  const modalCaption = modal.querySelector('.service-lightbox-caption');

  imageWraps.forEach((wrap) => {
    if (wrap.dataset.lightboxInitialized) return;
    wrap.dataset.lightboxInitialized = 'true';

    wrap.addEventListener('click', () => {
      const img = wrap.querySelector('.service-card-img');
      if (!img) return;

      modalImg.src = img.currentSrc || img.src;
      modalImg.alt = img.alt || 'Service Full Preview';
      modalCaption.textContent = img.alt || '';
      modal.classList.add('is-active');
      document.body.style.overflow = 'hidden';
    });
  });
}




