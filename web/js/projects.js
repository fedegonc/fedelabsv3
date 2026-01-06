// Projects page functionality

// Filter functionality
document.addEventListener('DOMContentLoaded', () => {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            const filter = button.dataset.filter;
            
            // Filter projects
            projectCards.forEach(card => {
                if (filter === 'all') {
                    card.classList.remove('hidden');
                } else {
                    const tech = card.dataset.tech;
                    const year = card.dataset.year;
                    
                    if (tech === filter || year === filter) {
                        card.classList.remove('hidden');
                    } else {
                        card.classList.add('hidden');
                    }
                }
            });
            
            // Update count
            updateProjectCount();
        });
    });
    
    function updateProjectCount() {
        const visibleCards = document.querySelectorAll('.project-card:not(.hidden)');
        const subtitle = document.querySelector('.page-subtitle');
        subtitle.textContent = `${visibleCards.length} proyectos encontrados`;
    }
});

// Pagination (simulated)
document.querySelectorAll('.pagination-btn').forEach(button => {
    button.addEventListener('click', () => {
        if (!button.disabled && !button.classList.contains('active')) {
            // Remove active from all
            document.querySelectorAll('.pagination-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Add active to clicked
            if (!button.textContent.includes('Anterior') && !button.textContent.includes('Siguiente')) {
                button.classList.add('active');
            }
            
            // Simulate page change
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    });
});

// Project card hover effect
document.querySelectorAll('.project-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.transform = 'translateY(-4px)';
    });
    
    card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0)';
    });
});

// Animate tech stats on scroll
const observerOptions = {
    threshold: 0.5,
    rootMargin: '0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const statFills = entry.target.querySelectorAll('.stat-fill');
            statFills.forEach(fill => {
                const width = fill.style.width;
                fill.style.width = '0';
                setTimeout(() => {
                    fill.style.width = width;
                }, 100);
            });
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe sidebar cards
document.querySelectorAll('.sidebar-card').forEach(card => {
    observer.observe(card);
});

// Search functionality (placeholder)
function initSearch() {
    // Add search input if needed
    const filterSection = document.querySelector('.filters .container');
    
    if (!document.querySelector('.search-input')) {
        const searchContainer = document.createElement('div');
        searchContainer.className = 'search-container';
        searchContainer.innerHTML = `
            <input type="text" class="search-input" placeholder="Buscar proyectos...">
            <button class="search-btn">🔍</button>
        `;
        
        filterSection.insertBefore(searchContainer, filterSection.firstChild);
        
        // Add search styles
        const searchStyles = document.createElement('style');
        searchStyles.textContent = `
            .search-container {
                display: flex;
                justify-content: center;
                margin-bottom: var(--spacing-md);
            }
            
            .search-input {
                padding: 0.5rem 1rem;
                border: 1px solid var(--border);
                border-radius: 9999px 0 0 9999px;
                outline: none;
                width: 300px;
                max-width: 100%;
            }
            
            .search-btn {
                padding: 0.5rem 1rem;
                background: var(--primary);
                color: white;
                border: none;
                border-radius: 0 9999px 9999px 0;
                cursor: pointer;
            }
            
            @media (max-width: 640px) {
                .search-input {
                    width: 200px;
                }
            }
        `;
        document.head.appendChild(searchStyles);
        
        // Search functionality
        const searchInput = document.querySelector('.search-input');
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase();
            const projectCards = document.querySelectorAll('.project-card');
            
            projectCards.forEach(card => {
                const title = card.querySelector('h3').textContent.toLowerCase();
                const description = card.querySelector('p').textContent.toLowerCase();
                
                if (title.includes(searchTerm) || description.includes(searchTerm)) {
                    card.classList.remove('hidden');
                } else {
                    card.classList.add('hidden');
                }
            });
            
            updateProjectCount();
        });
    }
}

// Initialize search on load
window.addEventListener('load', initSearch);
