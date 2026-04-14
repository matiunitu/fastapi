class FormInput extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }

    connectedCallback() {
        this.render();
        const input = this.shadowRoot.querySelector('input');
        input.addEventListener('input', (e) => {
            this.value = e.target.value;
            this.dispatchEvent(new CustomEvent('input-changed', {
                detail: { value: this.value }
            }));
        });
    }

    get value() {
        return this.getAttribute('value') || '';
    }

    set value(val) {
        this.setAttribute('value', val);
    }

    render() {
        const type = this.getAttribute('type') || 'text';
        const label = this.getAttribute('label') || 'Label';
        const placeholder = this.getAttribute('placeholder') || '';
        const name = this.getAttribute('name') || '';

        this.shadowRoot.innerHTML = `
            <style>
                :host {
                    display: block;
                    margin-bottom: 16px;
                }
                .input-group {
                    display: flex;
                    flex-direction: column;
                }
                label {
                    margin-bottom: 6px;
                    font-size: 0.875rem;
                    font-weight: 500;
                    color: #374151;
                }
                input {
                    padding: 10px 12px;
                    border: 1px solid #d1d5db;
                    border-radius: 6px;
                    font-size: 1rem;
                    transition: border-color 0.2s, box-shadow 0.2s;
                }
                input:focus {
                    outline: none;
                    border-color: #3b82f6;
                    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
                }
            </style>
            <div class="input-group">
                <label>${label}</label>
                <input type="${type}" name="${name}" placeholder="${placeholder}" value="${this.value}">
            </div>
        `;
    }
}

customElements.define('form-input', FormInput);
