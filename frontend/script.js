async function loadKeywords() {
    const resp = await fetch('/keywords');
    const data = await resp.json();
    // Preenche os campos de edição
    document.getElementById('produtivoKeywords').value = data.produtivo.join(", ");
    document.getElementById('improdutivoKeywords').value = data.improdutivo.join(", ");
    // Mostra na tela
    document.getElementById('showProdutivo').textContent = data.produtivo.join(", ") || "(nenhuma)";
    document.getElementById('showImprodutivo').textContent = data.improdutivo.join(", ") || "(nenhuma)";
}

document.getElementById('keywordsForm').addEventListener('submit', async e => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("produtivo", document.getElementById('produtivoKeywords').value);
    formData.append("improdutivo", document.getElementById('improdutivoKeywords').value);
    await fetch('/keywords', {method: 'POST', body: formData});
    alert("Palavras-chave atualizadas!");
    // Recarrega a exibição
    loadKeywords();
});

window.onload = loadKeywords;
