//script.js

document.getElementById('emailForm').addEventListener('submit', async e => {
  e.preventDefault();
  const formData = new FormData(e.target);
  const resp = await fetch('/analyze', {method: 'POST', body: formData});
  const data = await resp.json();
  document.getElementById('resultado').innerHTML =
    `<p><b>Categoria:</b> ${data.categoria}</p><p><b>Resposta Sugerida:</b> ${data.resposta}</p>`;
});
