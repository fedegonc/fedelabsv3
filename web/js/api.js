// API client for Fedelabs backend
class FedelabsAPI {
    constructor(baseURL = 'http://127.0.0.1:8000') {
        this.baseURL = baseURL;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            if (response.status === 204) {
                return null;
            }
            
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Projects
    async getProjects(status = 'published') {
        return this.request(`/projects?status=${status}`);
    }

    async getProjectBySlug(slug) {
        return this.request(`/projects/${slug}`);
    }

    // Posts
    async getPosts(status = 'published') {
        return this.request(`/posts?status=${status}`);
    }

    async getPostBySlug(slug) {
        return this.request(`/posts/${slug}`);
    }

    // Profile
    async getProfile() {
        return this.request('/profile');
    }

    // Health
    async getHealth() {
        return this.request('/health');
    }
}

// Create global instance
window.fedelabsAPI = new FedelabsAPI();

// Export for modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FedelabsAPI;
}
