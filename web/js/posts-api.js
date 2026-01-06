// Posts page API integration
document.addEventListener('DOMContentLoaded', async () => {
    try {
        await loadPosts();
        initializeCategories();
        initializeSearch();
        initializeNewsletter();
    } catch (error) {
        console.error('Error loading posts:', error);
        showErrorMessage();
    }
});

let allPosts = [];
let currentCategory = 'all';

async function loadPosts() {
    try {
        allPosts = await window.fedelabsAPI.getPosts('published');
        displayPosts(allPosts);
        updateCategoryCounts();
    } catch (error) {
        console.error('Error loading posts:', error);
        throw error;
    }
}

function displayPosts(posts) {
    const postsList = document.querySelector('.posts-list');
    const postsHTML = posts.map(post => createPostCard(post)).join('');
    
    // Insert before load more button
    const loadMore = document.querySelector('.load-more');
    postsList.innerHTML = postsHTML + loadMore.outerHTML;
}

function createPostCard(post) {
    const publishDate = new Date(post.published_at).toLocaleDateString('es-ES', {
        day: 'numeric',
        month: 'short',
        year: 'numeric'
    });
    
    return `
        <article class="post-card" data-category="${post.type.toLowerCase()}">
            <div class="post-header">
                <time datetime="${post.published_at}" class="post-date">${publishDate}</time>
                <h3 class="post-title">
                    <a href="/post-detail.html?slug=${post.slug}">${post.title}</a>
                </h3>
            </div>
            <p class="post-excerpt">
                ${post.content.substring(0, 150)}...
            </p>
            <div class="post-meta">
                <span class="post-category">${post.type}</span>
                <span class="post-read-time">${calculateReadTime(post.content)} min read</span>
            </div>
        </article>
    `;
}

function initializeCategories() {
    const categoryLinks = document.querySelectorAll('.category-link');
    
    categoryLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Remove active from all
            categoryLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            
            const category = link.dataset.category;
            filterByCategory(category);
        });
    });
}

function filterByCategory(category) {
    currentCategory = category;
    
    let filtered = allPosts;
    if (category !== 'all') {
        filtered = allPosts.filter(post => post.type.toLowerCase() === category);
    }
    
    displayPosts(filtered);
    updatePostCount(filtered.length);
}

function updateCategoryCounts() {
    const categories = ['arquitectura', 'performance', 'databases', 'python', 'testing'];
    
    categories.forEach(category => {
        const count = allPosts.filter(post => 
            post.type.toLowerCase() === category
        ).length;
        
        const link = document.querySelector(`[data-category="${category}"] .count`);
        if (link) {
            link.textContent = count;
        }
    });
    
    // Update "Todos" count
    const allLink = document.querySelector('[data-category="all"] .count');
    if (allLink) {
        allLink.textContent = allPosts.length;
    }
}

function updatePostCount(count) {
    const subtitle = document.querySelector('.page-subtitle');
    if (count === allPosts.length) {
        subtitle.textContent = `${count} posts publicados`;
    } else {
        subtitle.textContent = `${count} posts encontrados`;
    }
}

function initializeSearch() {
    const searchInput = document.querySelector('.search-input');
    const searchBtn = document.querySelector('.search-btn');
    
    if (searchInput && searchBtn) {
        const performSearch = () => {
            const searchTerm = searchInput.value.toLowerCase();
            
            if (searchTerm === '') {
                displayPosts(currentCategory === 'all' ? allPosts : 
                    allPosts.filter(post => post.type.toLowerCase() === currentCategory));
            } else {
                const filtered = allPosts.filter(post => 
                    post.title.toLowerCase().includes(searchTerm) ||
                    post.content.toLowerCase().includes(searchTerm)
                );
                displayPosts(filtered);
                updatePostCount(filtered.length);
            }
        };
        
        searchInput.addEventListener('input', debounce(performSearch, 300));
        searchBtn.addEventListener('click', performSearch);
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') performSearch();
        });
    }
}

function initializeNewsletter() {
    const form = document.querySelector('.newsletter-form');
    
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const email = form.querySelector('input[type="email"]').value;
            const button = form.querySelector('button');
            const originalText = button.textContent;
            
            // Show loading state
            button.textContent = 'Suscribiendo...';
            button.disabled = true;
            
            try {
                // Simulate API call
                await new Promise(resolve => setTimeout(resolve, 1000));
                
                // Show success message
                button.textContent = '✓ Suscrito';
                button.classList.add('success');
                
                // Reset form
                form.reset();
                
                // Reset button after 3 seconds
                setTimeout(() => {
                    button.textContent = originalText;
                    button.disabled = false;
                    button.classList.remove('success');
                }, 3000);
                
            } catch (error) {
                button.textContent = 'Error. Intenta de nuevo';
                button.disabled = false;
                
                setTimeout(() => {
                    button.textContent = originalText;
                }, 3000);
            }
        });
    }
}

// Load more functionality
document.addEventListener('DOMContentLoaded', () => {
    const loadMoreBtn = document.getElementById('loadMoreBtn');
    
    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', async () => {
            loadMoreBtn.textContent = 'Cargando...';
            loadMoreBtn.disabled = true;
            
            try {
                // Simulate loading more posts
                await new Promise(resolve => setTimeout(resolve, 1000));
                
                // In real app, this would load from API
                // For now, just show a message
                loadMoreBtn.textContent = 'No hay más posts';
                loadMoreBtn.classList.add('disabled');
                
            } catch (error) {
                loadMoreBtn.textContent = 'Error. Recarga la página';
                loadMoreBtn.disabled = false;
            }
        });
    }
});

// Utility functions
function calculateReadTime(content) {
    const wordsPerMinute = 200;
    const words = content.split(' ').length;
    return Math.max(1, Math.ceil(words / wordsPerMinute));
}

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

function showErrorMessage() {
    const postsList = document.querySelector('.posts-list');
    postsList.innerHTML = `
        <div class="error-message">
            <h3>No se pudieron cargar los posts</h3>
            <p>Por favor, intenta recargar la página.</p>
            <button onclick="location.reload()" class="btn btn-primary">Recargar</button>
        </div>
    `;
    
    const style = document.createElement('style');
    style.textContent = `
        .error-message {
            text-align: center;
            padding: var(--spacing-xl);
            background: var(--surface);
            border-radius: 8px;
            border: 1px solid var(--border);
        }
    `;
    document.head.appendChild(style);
}

// Add newsletter success styles
const newsletterStyles = document.createElement('style');
newsletterStyles.textContent = `
    .newsletter-form button.success {
        background: #10b981 !important;
    }
    
    .load-more.disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
`;
document.head.appendChild(newsletterStyles);
