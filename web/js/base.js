// Base JavaScript functionality

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Header scroll effect
let lastScroll = 0;
const header = document.querySelector('.header');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll <= 0) {
        header.classList.remove('scroll-up');
        return;
    }
    
    if (currentScroll > lastScroll && !header.classList.contains('scroll-down')) {
        header.classList.remove('scroll-up');
        header.classList.add('scroll-down');
    } else if (currentScroll < lastScroll && header.classList.contains('scroll-down')) {
        header.classList.remove('scroll-down');
        header.classList.add('scroll-up');
    }
    lastScroll = currentScroll;
});

// Add scroll classes to header
const style = document.createElement('style');
style.textContent = `
    .header {
        transition: transform 0.3s ease;
    }
    .header.scroll-down {
        transform: translateY(-100%);
    }
    .header.scroll-up {
        transform: translateY(0);
    }
`;
document.head.appendChild(style);

// Mobile menu toggle (if needed in future)
function initMobileMenu() {
    const navLinks = document.querySelector('.nav-links');
    if (window.innerWidth < 768 && navLinks) {
        // Add mobile menu button if it doesn't exist
        if (!document.querySelector('.mobile-menu-toggle')) {
            const menuButton = document.createElement('button');
            menuButton.className = 'mobile-menu-toggle';
            menuButton.innerHTML = '☰';
            menuButton.setAttribute('aria-label', 'Toggle menu');
            
            const nav = document.querySelector('.nav');
            nav.appendChild(menuButton);
            
            menuButton.addEventListener('click', () => {
                navLinks.classList.toggle('active');
                menuButton.innerHTML = navLinks.classList.contains('active') ? '✕' : '☰';
            });
        }
    }
}

// Initialize on load and resize
window.addEventListener('load', initMobileMenu);
window.addEventListener('resize', initMobileMenu);

// Add mobile menu styles
const mobileStyle = document.createElement('style');
mobileStyle.textContent = `
    @media (max-width: 767px) {
        .nav-links {
            position: fixed;
            top: 64px;
            left: 0;
            right: 0;
            background: white;
            flex-direction: column;
            padding: var(--spacing-md);
            box-shadow: var(--shadow-lg);
            transform: translateY(-100vh);
            transition: transform 0.3s ease;
            z-index: 99;
        }
        
        .nav-links.active {
            transform: translateY(0);
        }
        
        .mobile-menu-toggle {
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            padding: var(--spacing-xs);
        }
    }
`;
document.head.appendChild(mobileStyle);

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Optimize scroll events
const optimizedScroll = debounce(() => {
    // Add any scroll-based optimizations here
}, 100);

window.addEventListener('scroll', optimizedScroll);

// External link handling
document.addEventListener('DOMContentLoaded', () => {
    // Add external link indicators
    document.querySelectorAll('a[href^="http"]').forEach(link => {
        if (!link.hasAttribute('target')) {
            link.setAttribute('target', '_blank');
            link.setAttribute('rel', 'noopener noreferrer');
        }
    });
    
    // Lazy load images when needed
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
});

// Console branding
console.log('%c Fedelabs ', 'background: #2563eb; color: white; font-weight: bold; padding: 5px 10px;');
