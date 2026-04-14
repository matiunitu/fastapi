class UserProfile extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }

    connectedCallback() {
        this.render();
    }

    render() {
        const name = this.getAttribute('name') || 'Usuario Invitado';
        const role = this.getAttribute('role') || 'ROl Desconocido';
        const email = this.getAttribute('email') || 'no-email@example.com';

        this.shadowRoot.innerHTML = `
            <style>
                :host {
                    display: inline-block;
                }
                .profile-card {
                    display: flex;
                    align-items: center;
                    padding: 12px;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    gap: 16px;
                }
                .avatar {
                    width: 48px;
                    height: 48px;
                    background: #3b82f6;
                    color: white;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.25rem;
                    font-weight: bold;
                }
                .info {
                    display: flex;
                    flex-direction: column;
                }
                .name {
                    font-weight: 600;
                    color: #111827;
                    font-size: 0.95rem;
                }
                .role {
                    font-size: 0.75rem;
                    color: #6b7280;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                    margin-top: 2px;
                }
            </style>
            <div class="profile-card">
                <div class="avatar">${name.charAt(0).toUpperCase()}</div>
                <div class="info">
                    <span class="name">${name}</span>
                    <span class="role">${role}</span>
                </div>
            </div>
        `;
    }
}

customElements.define('user-profile', UserProfile);
