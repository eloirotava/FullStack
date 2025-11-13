document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('load-api');
  const output = document.getElementById('api-output');

  if (!btn || !output) return;

  btn.addEventListener('click', async () => {
    try {
      const resp = await fetch('/api/tasks');
      if (!resp.ok) {
        throw new Error('Erro ao chamar /api/tasks');
      }
      const data = await resp.json();
      output.textContent = JSON.stringify(data, null, 2);
      output.classList.remove('d-none');
    } catch (err) {
      output.textContent = 'Erro: ' + err.message;
      output.classList.remove('d-none');
    }
  });
});
