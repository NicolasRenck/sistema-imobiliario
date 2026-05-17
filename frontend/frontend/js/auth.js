document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('loginForm');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorEl = document.getElementById('loginError');
    const btn = form.querySelector('.login-btn');

    btn.textContent = 'Entrando...';
    btn.disabled = true;
    errorEl.textContent = '';

    try {
      const response = await fetch(`${API_URL}/token/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });

      if (response.ok) {
        const data = await response.json();
        setTokens(data.access, data.refresh);
        window.location.href = 'dashboard.html';
      } else {
        errorEl.textContent = 'Usuário ou senha incorretos.';
        btn.textContent = 'Entrar';
        btn.disabled = false;
      }
    } catch (err) {
      errorEl.textContent = 'Erro ao conectar com o servidor.';
      btn.textContent = 'Entrar';
      btn.disabled = false;
    }
  });
});

async function logout() {
  const refresh = getRefresh();
  const access = getToken();

  if (refresh && access) {
    await fetch(`${API_URL}/logout/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${access}`
      },
      body: JSON.stringify({ refresh })
    });
  }

  clearTokens();
  redirectToLogin();
}