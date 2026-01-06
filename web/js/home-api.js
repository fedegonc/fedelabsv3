// Home page API integration
document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Load recent projects
        await loadRecentProjects();
        
        // Load recent posts
        await loadRecentPosts();
        
        // Load profile for footer/about
        await loadProfileInfo();
    } catch (error) {
        console.error('Error loading home page data:', error);
        showErrorMessage();
    }
});

async function loadRecentProjects() {
    try {
        const projects = await window.fedelabsAPI.getProjects('published');
        const projectsGrid = document.querySelector('.projects-grid');
        
        if (projects && projects.length > 0) {
            // Take only first 3 for home
            const recentProjects = projects.slice(0, 3);
            
            projectsGrid.innerHTML = recentProjects.map(project => `
                <div class="project-card">
                    <h3>${project.title}</h3>
                    <p>${project.description}</p>
                    <div class="project-tech">
                        ${project.stack.map(tech => `<span class="tech-badge">${tech}</span>`).join('')}
                    </div>
                    <div class="project-links">
                        ${project.repo_url ? `<a href="${project.repo_url}" target="_blank" class="link">Repo</a>` : ''}
                        ${project.demo_url ? `<a href="${project.demo_url}" target="_blank" class="link">Demo</a>` : ''}
                    </div>
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading projects:', error);
        // Keep placeholder content
    }
}

async function loadRecentPosts() {
    try {
        const posts = await window.fedelabsAPI.getPosts('published');
        const postsGrid = document.querySelector('.posts-grid');
        
        if (posts && posts.length > 0) {
            // Take only first 3 for home
            const recentPosts = posts.slice(0, 3);
            
            postsGrid.innerHTML = recentPosts.map(post => `
                <article class="post-card" onclick="window.location.href='/post-detail.html?slug=${post.slug}'">
                    <h3>${post.title}</h3>
                    <p>${post.content.substring(0, 100)}...</p>
                    <div class="post-meta">
                        <span class="post-time">${calculateReadTime(post.content)} min read</span>
                        <span class="post-category">${post.type}</span>
                    </div>
                </article>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading posts:', error);
        // Keep placeholder content
    }
}

async function loadProfileInfo() {
    try {
        const profile = await window.fedelabsAPI.getProfile();
        
        if (profile) {
            // Update about section if needed
            const aboutText = document.querySelector('.about-text');
            if (aboutText && profile.bio) {
                aboutText.textContent = profile.bio;
            }
            
            // Update skills if needed
            updateSkillsFromProfile(profile);
        }
    } catch (error) {
        console.error('Error loading profile:', error);
        // Keep default content
    }
}

function updateSkillsFromProfile(profile) {
    // This could be expanded to load skills from profile
    // For now, keeping static skills
}

function calculateReadTime(content) {
    const wordsPerMinute = 200;
    const words = content.split(' ').length;
    return Math.ceil(words / wordsPerMinute);
}

function showErrorMessage() {
    // Show a subtle error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'api-error';
    errorDiv.innerHTML = `
        <p>No se pudieron cargar los datos. <a href="/projects.html">Ver proyectos</a></p>
    `;
    
    const style = document.createElement('style');
    style.textContent = `
        .api-error {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: var(--surface);
            border: 1px solid var(--border);
            padding: var(--spacing-md);
            border-radius: 6px;
            box-shadow: var(--shadow-lg);
            z-index: 1000;
            animation: slideIn 0.3s ease;
        }
        
        @keyframes slideIn {
            from { transform: translateX(100%); }
            to { transform: translateX(0); }
        }
    `;
    
    document.head.appendChild(style);
    document.body.appendChild(errorDiv);
    
    // Auto hide after 5 seconds
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}
