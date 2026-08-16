let cartCount = 0;

// Model Looks Array for interactive vertical slider controls
const modelLooks = [
  { label: 'LOOK 01 • RADIANT NUDE GLOW' },
  { label: 'LOOK 02 • VELVET MATTE ELEGANCE' },
  { label: 'LOOK 03 • GOLDEN HOUR SHIMMER' },
  { label: 'LOOK 04 • SILK SATIN GLAMOUR' }
];

let currentLookIndex = 0;

// Cart & Toast System
function addToCart(productName) {
  cartCount++;
  const cartCountEl = document.getElementById('cartCount');
  if (cartCountEl) {
    cartCountEl.innerText = cartCount;
  }
  
  showToast(`✨ ${productName} added to your bag.`);
}

function showToast(message) {
  const container = document.getElementById('toast-container');
  if (!container) return;
  
  const toast = document.createElement('div');
  toast.className = 'toast';
  
  toast.innerHTML = `
    <span class="toast-success-icon">✓</span>
    <span class="toast-message">${message}</span>
  `;
  
  container.appendChild(toast);
  
  setTimeout(() => {
    toast.classList.add('fade-out');
    toast.addEventListener('animationend', () => {
      toast.remove();
    });
  }, 3500);
}

// Model Look Switcher Logic
function initModelControls() {
  const prevBtn = document.getElementById('prevLookBtn');
  const nextBtn = document.getElementById('nextLookBtn');
  const lookTag = document.getElementById('lookTag');
  const modelImg = document.getElementById('modelImage');

  function updateLook(direction) {
    if (direction === 'next') {
      currentLookIndex = (currentLookIndex + 1) % modelLooks.length;
    } else {
      currentLookIndex = (currentLookIndex - 1 + modelLooks.length) % modelLooks.length;
    }

    if (lookTag) {
      lookTag.innerText = modelLooks[currentLookIndex].label;
    }

    if (modelImg) {
      modelImg.style.opacity = '0.4';
      modelImg.style.transform = 'scale(0.96)';
      setTimeout(() => {
        modelImg.style.opacity = '1';
        modelImg.style.transform = 'scale(1)';
      }, 200);
    }
  }

  if (prevBtn) prevBtn.addEventListener('click', () => updateLook('prev'));
  if (nextBtn) nextBtn.addEventListener('click', () => updateLook('next'));
}

// 3D Tilt Effect on Product Cards
function initTiltEffect() {
  const cards = document.querySelectorAll('.product-card, .category-card');
  
  cards.forEach(card => {
    card.addEventListener('mousemove', e => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      const xPercent = (x / rect.width) - 0.5;
      const yPercent = (y / rect.height) - 0.5;
      
      const maxTilt = 8;
      const tiltX = -yPercent * maxTilt;
      const tiltY = xPercent * maxTilt;
      
      card.style.transform = `perspective(1000px) rotateX(${tiltX}deg) rotateY(${tiltY}deg) translateY(-6px)`;
    });
    
    card.addEventListener('mouseleave', () => {
      card.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px)`;
    });
  });
}

// DOM Initialization
document.addEventListener('DOMContentLoaded', () => {
  initModelControls();
  initTiltEffect();
});