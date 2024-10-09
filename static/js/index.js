let fileURL = '';

document.getElementById('file').addEventListener('change', function() {
    const file = this.files[0];
    const fileName = file.name;

    // Exibir o nome do arquivo
    document.getElementById('file-name').textContent = `Histórico Escolar: ${fileName}`;

    // Se o arquivo for um PDF, exibir a pré-visualização
    if (file.type === 'application/pdf') {
        fileURL = URL.createObjectURL(file);
        const preview = document.getElementById('file-preview');
        preview.src = fileURL;
        preview.style.display = 'block'; // Exibe o iframe de pré-visualização

        // Mostrar o botão de visualizar histórico
        document.getElementById('view-historico').style.display = 'inline-block';
    }
});

function viewHistorico() {
    // Abre o PDF em uma nova aba
    window.open(fileURL, '_blank');
}