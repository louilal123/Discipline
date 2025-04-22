
// JavaScript to handle the scroll event and add the backdrop filter
const navbar = document.getElementById('navbar');
const heroSection = document.getElementById('hero');

window.addEventListener('scroll', () => {
  const heroHeight = heroSection.offsetHeight;
  if (window.scrollY > heroHeight) {
    navbar.classList.add('backdrop-blur-md', 'bg-opacity-50');
  } else {
    navbar.classList.remove('backdrop-blur-md', 'bg-opacity-0');
  }
});

  // Theme toggle functionality
  const themeToggle = document.getElementById('theme-toggle');
  const mobileThemeToggle = document.getElementById('mobile-theme-toggle');
  const themeIcon = document.getElementById('theme-icon');
  
  // Check for saved user preference or use system preference
  const userTheme = localStorage.getItem('theme');
  const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches;
  
  // Initial theme check
  const themeCheck = () => {
      if (userTheme === 'dark' || (!userTheme && systemTheme)) {
          document.documentElement.classList.add('dark');
          themeIcon.setAttribute('stroke', 'currentColor');
          themeIcon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path>';
      } else {
          document.documentElement.classList.remove('dark');
          themeIcon.setAttribute('stroke', 'currentColor');
          themeIcon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path>';
      }
  };
  
  // Manual theme switch
  const themeSwitch = () => {
      if (document.documentElement.classList.contains('dark')) {
          document.documentElement.classList.remove('dark');
          localStorage.setItem('theme', 'light');
          themeIcon.setAttribute('stroke', 'currentColor');
          themeIcon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path>';
      } else {
          document.documentElement.classList.add('dark');
          localStorage.setItem('theme', 'dark');
          themeIcon.setAttribute('stroke', 'currentColor');
          themeIcon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path>';
      }
  };
  
  // Add event listeners
  if (themeToggle) {
      themeToggle.addEventListener('click', themeSwitch);
  }
  
  if (mobileThemeToggle) {
      mobileThemeToggle.addEventListener('click', themeSwitch);
  }
  
  // Invoke theme check on initial load
  themeCheck();
    // Mobile menu toggle
    document.getElementById('mobile-menu-button').addEventListener('click', function() {
      const menu = document.getElementById('mobile-menu');
      menu.classList.toggle('hidden');
  });

  // Filter buttons
  document.querySelectorAll('.filter-button').forEach(button => {
      button.addEventListener('click', function() {
          document.querySelectorAll('.filter-button').forEach(btn => {
              btn.classList.remove('active');
          });
          this.classList.add('active');
      });
  });

  // Initialize Three.js background
  function initThreeBackground() {
      const container = document.getElementById('hero-canvas');
      const width = container.clientWidth;
      const height = container.clientHeight;

      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
      camera.position.z = 5;

      const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
      renderer.setSize(width, height);
      container.appendChild(renderer.domElement);

      // Create particles
      const particlesGeometry = new THREE.BufferGeometry();
      const particlesCount = 1500;
      const posArray = new Float32Array(particlesCount * 3);

      for (let i = 0; i < particlesCount * 3; i++) {
          posArray[i] = (Math.random() - 0.5) * 15;
      }

      particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));

      // Materials
      const particlesMaterial = new THREE.PointsMaterial({
          size: 0.02,
          color: 0x6366f1,
          transparent: true,
          opacity: 0.8
      });

      // Mesh
      const particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
      scene.add(particlesMesh);

      // Animation
      function animate() {
          requestAnimationFrame(animate);
          particlesMesh.rotation.x += 0.0005;
          particlesMesh.rotation.y += 0.0005;
          renderer.render(scene, camera);
      }

      animate();

      // Handle window resize
      window.addEventListener('resize', () => {
          const newWidth = container.clientWidth;
          const newHeight = container.clientHeight;
          
          camera.aspect = newWidth / newHeight;
          camera.updateProjectionMatrix();
          renderer.setSize(newWidth, newHeight);
      });
  }