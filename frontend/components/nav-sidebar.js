class NavSidebar extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }

    connectedCallback() {
        this.render();
    }

    render() {
        const role = this.getAttribute('role') || 'USUARIO';
        
        // Example routes based on role (could be refined)
        let menuItems = `
            <li><a href="#" class="active"><i class="icon">🏠</i> Dashboard</a></li>
            <li><a href="#"><i class="icon">📝</i> Mis PQRS</a></li>
        `;
        
        if (role === 'ADMIN') {
            menuItems += `
                <li><a href="#"><i class="icon">⚙️</i> Gestión de Usuarios</a></li>
                <li><a href="#"><i class="icon">📊</i> Reportes</a></li>
            `;
        }

        this.shadowRoot.innerHTML = `
            <style>
                :host {
                    display: block;
                    width: 250px;
                    height: 100vh;
                    background: #1f2937;
                    color: white;
                }
                .sidebar {
                    display: flex;
                    flex-direction: column;
                    height: 100%;
                }
                .logo {
                    padding: 20px;
                    font-size: 1.5rem;
                    font-weight: bold;
                    border-bottom: 1px solid #374151;
                    text-align: center;
                }
                ul {
                    list-style: none;
                    padding: 0;
                    margin: 0;
                    flex: 1;
                }
                li {
                    border-bottom: 1px solid #374151;
                }
                a {
                    display: flex;
                    align-items: center;
                    padding: 16px 20px;
                    color: #d1d5db;
                    text-decoration: none;
                    transition: background 0.2s, color 0.2s;
                }
                a:hover, a.active {
                    background: #374151;
                    color: white;
                }
                .icon {
                    margin-right: 12px;
                }
                .footer {
                    padding: 20px;
                    border-top: 1px solid #374151;
                    text-align: center;
                    font-size: 0.875rem;
                    color: #9ca3af;
                }
            </style>
            <div class="sidebar">
                <div class="logo">PQRS System</div>
                <ul>
                    ${menuItems}
                </ul>
                <div class="footer">
                    &copy; 2026 Universidad
                </div>
            </div>
        `;
    }
}

customElements.define('nav-sidebar', NavSidebar);
