
function showTab(tabId) {
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => {
        tab.classList.remove('active');
    });

    const activeTab = document.getElementById(tabId);
    activeTab.classList.add('active');
}

function openModal(codigo, nome, ementa, carga_horaria, requisitos, requisitos_pendentes) {
    document.getElementById('modal-title').innerText = `${codigo} - ${nome}`;
    document.getElementById('modal-ementa').innerText = `Ementa: ${ementa}`;
    document.getElementById('modal-carga-horaria').innerText = `Carga Horária: ${carga_horaria}h`;
    document.getElementById('modal-requisitos').innerText = `Requisitos: ${requisitos || 'Nenhum'}`;

    // Exibe o modal
    document.getElementById('modal').style.display = 'block';
}

function closeModal() {
    // Esconde o modal
    document.getElementById('modal').style.display = 'none';
}

// Fecha o modal ao clicar fora dele
window.onclick = function(event) {
    if (event.target === document.getElementById('modal')) {
        closeModal();
    }
}
