// Projects page API integration
document.addEventListener('DOMContentLoaded', async () => {
    try {
        await loadProjects();
        initializeFilters();
        initializePagination();
    } catch (error) {
        console.error('Error loading projects:', error);
        showErrorMessage();
    }
});

let allProjects = [];
let currentPage = 1;
const projectsPerPage = 6;

async function loadProjects() {
    try {
        allProjects = await window.fedelabsAPI.getProjects('published');
        displayProjects(allProjects);
        updateProjectCount();
        updatePagination();
    } catch (error) {
        console.error('Error loading projects:', error);
        throw error;
    }
}

function displayProjects(projects) {
    const projectsGrid = document.querySelector('.projects-grid');
    
    if (projects.length === 0) {
        projectsGrid.innerHTML = '<p class="no-projects">No se encontraron proyectos.</p>';
        return;
    }
    
    // Calculate pagination
    const startIndex = (currentPage - 1) * projectsPerPage;
    const endIndex = startIndex + projectsPerPage;
    const paginatedProjects = projects.slice(startIndex, endIndex);
    
    projectsGrid.innerHTML = paginatedProjects.map(project => `
        <div class="project-card" data-tech="${getMainTech(project.stack)}" data-year="${getYear(project.created_at)}">
            <h3>${project.title}</h3>
            <p>${project.description}</p>
            <div class="project-tech">
                ${project.stack.map(tech => `<span class="tech-badge">${tech}</span>`).join('')}
            </div>
            <div class="project-links">
                <a href="/project-detail.html?slug=${project.slug}" class="link">Ver detalle →</a>
                <div class="project-actions">
                    ${project.repo_url ? `<a href="${project.repo_url}" target="_blank" class="link">Repo</a>` : ''}
                    ${project.demo_url ? `<a href="${project.demo_url}" target="_blank" class="link">Demo</a>` : ''}
                </div>
            </div>
        </div>
    `).join('');
}

function initializeFilters() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            const filter = button.dataset.filter;
            filterProjects(filter);
        });
    });
}

function filterProjects(filter) {
    let filtered = allProjects;
    
    if (filter !== 'all') {
        filtered = allProjects.filter(project => {
            const mainTech = getMainTech(project.stack);
            const year = getYear(project.created_at);
            return mainTech === filter || year === filter;
        });
    }
    
    currentPage = 1; // Reset to first page
    displayProjects(filtered);
    updateProjectCount();
    updatePagination();
}

function initializePagination() {
    const paginationButtons = document.querySelectorAll('.pagination-btn');
    
    paginationButtons.forEach(button => {
        button.addEventListener('click', () => {
            if (button.disabled) return;
            
            if (button.textContent.includes('Anterior')) {
                if (currentPage > 1) currentPage--;
            } else if (button.textContent.includes('Siguiente')) {
                const maxPage = Math.ceil(allProjects.length / projectsPerPage);
                if (currentPage < maxPage) currentPage++;
            } else {
                currentPage = parseInt(button.textContent);
            }
            
            displayProjects(getCurrentFilteredProjects());
            updatePaginationButtons();
            
            // Scroll to top
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    });
}

function getCurrentFilteredProjects() {
    const activeFilter = document.querySelector('.filter-btn.active').dataset.filter;
    
    if (activeFilter === 'all') {
        return allProjects;
    }
    
    return allProjects.filter(project => {
        const mainTech = getMainTech(project.stack);
        const year = getYear(project.created_at);
        return mainTech === activeFilter || year === activeFilter;
    });
}

function updatePagination() {
    const filteredProjects = getCurrentFilteredProjects();
    const totalPages = Math.ceil(filteredProjects.length / projectsPerPage);
    
    // Update pagination buttons
    const paginationContainer = document.querySelector('.pagination');
    let paginationHTML = `
        <button class="pagination-btn" ${currentPage === 1 ? 'disabled' : ''}>← Anterior</button>
    `;
    
    for (let i = 1; i <= Math.min(totalPages, 4); i++) {
        paginationHTML += `
            <button class="pagination-btn ${i === currentPage ? 'active' : ''}">${i}</button>
        `;
    }
    
    if (totalPages > 4) {
        paginationHTML += `<span>...</span>`;
        paginationHTML += `<button class="pagination-btn">${totalPages}</button>`;
    }
    
    paginationHTML += `
        <button class="pagination-btn" ${currentPage === totalPages ? 'disabled' : ''}>Siguiente →</button>
    `;
    
    paginationContainer.innerHTML = paginationHTML;
    
    // Reinitialize pagination events
    initializePagination();
}

function updatePaginationButtons() {
    const paginationButtons = document.querySelectorAll('.pagination-btn');
    paginationButtons.forEach(button => {
        button.classList.remove('active');
        if (button.textContent == currentPage) {
            button.classList.add('active');
        }
    });
}

function updateProjectCount() {
    const filteredProjects = getCurrentFilteredProjects();
    const subtitle = document.querySelector('.page-subtitle');
    subtitle.textContent = `${filteredProjects.length} proyectos encontrados`;
}

function getMainTech(stack) {
    // Return the first tech as main category
    return stack[0]?.toLowerCase() || 'other';
}

function getYear(dateString) {
    return new Date(dateString).getFullYear().toString();
}

function showErrorMessage() {
    const projectsGrid = document.querySelector('.projects-grid');
    projectsGrid.innerHTML = `
        <div class="error-message">
            <h3>No se pudieron cargar los proyectos</h3>
            <p>Por favor, intenta recargar la página.</p>
            <button onclick="location.reload()" class="btn btn-primary">Recargar</button>
        </div>
    `;
    
    const style = document.createElement('style');
    style.textContent = `
        .error-message {
            grid-column: 1 / -1;
            text-align: center;
            padding: var(--spacing-xl);
        }
    `;
    document.head.appendChild(style);
}

// Search functionality
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.querySelector('.search-input');
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                const searchTerm = e.target.value.toLowerCase();
                
                if (searchTerm === '') {
                    displayProjects(getCurrentFilteredProjects());
                } else {
                    const filtered = allProjects.filter(project => 
                        project.title.toLowerCase().includes(searchTerm) ||
                        project.description.toLowerCase().includes(searchTerm) ||
                        project.stack.some(tech => tech.toLowerCase().includes(searchTerm))
                    );
                    displayProjects(filtered);
                    updateProjectCount();
                }
            }, 300);
        });
    }
});
