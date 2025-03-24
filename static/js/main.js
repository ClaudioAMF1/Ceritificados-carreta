// Carregar lista de estados ao iniciar
document.addEventListener('DOMContentLoaded', function() {
    carregarEstados();
});

// Função para carregar estados disponíveis
function carregarEstados() {
    fetch('/estados')
        .then(response => response.json())
        .then(data => {
            const selectEstado = document.getElementById('estado');
            
            if (data.estados && data.estados.length > 0) {
                data.estados.forEach(estado => {
                    const option = document.createElement('option');
                    option.value = estado;
                    option.textContent = estado;
                    selectEstado.appendChild(option);
                });
            }
        })
        .catch(error => {
            console.error('Erro ao carregar estados:', error);
        });
}

// Função para formatar o CPF enquanto o usuário digita
document.getElementById('cpf').addEventListener('input', function (e) {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length <= 11) {
        value = value.replace(/^(\d{3})(\d{3})(\d{3})(\d{2})$/, "$1.$2.$3-$4");
        value = value.replace(/^(\d{3})(\d{3})(\d{3})$/, "$1.$2.$3");
        value = value.replace(/^(\d{3})(\d{3})$/, "$1.$2");
        value = value.replace(/^(\d{3})$/, "$1");
    }
    e.target.value = value;
});

// Função para verificar se um curso já foi avaliado
function cursoJaAvaliado(cpf, curso) {
    const avaliacoes = JSON.parse(localStorage.getItem('cursosAvaliados') || '{}');
    return avaliacoes[cpf] && avaliacoes[cpf].includes(curso);
}

// Função para marcar um curso como avaliado
function marcarCursoComoAvaliado(cpf, curso) {
    const avaliacoes = JSON.parse(localStorage.getItem('cursosAvaliados') || '{}');
    
    if (!avaliacoes[cpf]) {
        avaliacoes[cpf] = [];
    }
    
    if (!avaliacoes[cpf].includes(curso)) {
        avaliacoes[cpf].push(curso);
        localStorage.setItem('cursosAvaliados', JSON.stringify(avaliacoes));
    }
}

// Função para configurar os botões de avaliação
function configurarBotoesAvaliacao() {
    document.querySelectorAll('.evaluation-btn').forEach(btn => {
        const cpf = btn.getAttribute('data-cpf');
        const curso = btn.getAttribute('data-curso');
        
        // Adicionar evento de clique para botões não avaliados
        btn.addEventListener('click', function(e) {
            // Permitir que o link se abra em nova aba
            setTimeout(function() {
                marcarCursoComoAvaliado(cpf, curso);
                
                // Substituir o botão por um span
                const buttonGroup = btn.parentElement;
                const textElement = document.createElement('span');
                textElement.className = 'course-evaluated';
                textElement.innerHTML = '<i class="fas fa-check-circle"></i> Curso avaliado!';
                
                // Remover o botão antigo e adicionar o novo span
                buttonGroup.removeChild(btn);
                buttonGroup.appendChild(textElement);
            }, 500);
        });
    });
}

function buscarCertificado() {
    const cpfInput = document.getElementById('cpf').value;
    const estado = document.getElementById('estado').value;
    const resultDiv = document.getElementById('result');
    const errorDiv = document.getElementById('error');
    const loader = document.getElementById('loader');
    const certificatesContainer = document.getElementById('certificates-container');
    
    // Limpar estados anteriores
    resultDiv.style.display = 'none';
    errorDiv.style.display = 'none';
    certificatesContainer.innerHTML = '';
    loader.style.display = 'block';
    
    // Validação simples
    const cpf = cpfInput.replace(/\D/g, '');
    if (!cpf) {
        errorDiv.textContent = 'Por favor, digite seu CPF';
        errorDiv.style.display = 'block';
        loader.style.display = 'none';
        return;
    }
    
    // Preparar dados para envio
    const dados = { cpf: cpf };
    if (estado) {
        dados.estado = estado;
    }
    
    // Fazer requisição para a API
    fetch('/certificado', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dados),
    })
    .then(response => response.json())
    .then(data => {
        loader.style.display = 'none';
        
        if (data.erro) {
            errorDiv.textContent = data.erro;
            errorDiv.style.display = 'block';
        } else {
            // Exibir informações do aluno
            const certificados = data.certificados;
            if (certificados && certificados.length > 0) {
                document.getElementById('nome').textContent = certificados[0].nome;
                document.getElementById('cpf-display').textContent = certificados[0].cpf;
                document.getElementById('certificate-count').textContent = certificados.length;
                
                // Exibir cada certificado
                certificados.forEach(cert => {
                    const downloadUrl = `/download-certificado/${encodeURIComponent(cert.cpf)}/${encodeURIComponent(cert.curso)}`;
                    const cursoAvaliado = cursoJaAvaliado(cert.cpf, cert.curso);
                    
                    const avaliacaoElement = cursoAvaliado ?
                        `<span class="course-evaluated">
                            <i class="fas fa-check-circle"></i> Curso avaliado!
                         </span>` :
                        `<a class="evaluation-btn" href="https://docs.google.com/forms/d/e/1FAIpQLScMa7x1JvlzTrC9e1_y99A754qzoLtUpim8wHlhqj3p1IF0PA/viewform?usp=sf_link" target="_blank" data-cpf="${cert.cpf}" data-curso="${cert.curso}">
                            <i class="fas fa-star"></i> Avaliar Curso
                         </a>`;
                    
                    const cardHtml = `
                        <div class="certificate-card">
                            <h3>${cert.curso}</h3>
                            <div class="certificate-meta">
                                ${cert.estado ? `<div class="info-row">
                                    <span class="info-label">Estado:</span> 
                                    <span>${cert.estado}</span>
                                </div>` : ''}
                                ${cert.escola ? `<div class="info-row">
                                    <span class="info-label">Escola:</span> 
                                    <span>${cert.escola}</span>
                                </div>` : ''}
                                ${cert.data_adesao ? `<div class="info-row">
                                    <span class="info-label">Data de Adesão:</span> 
                                    <span>${cert.data_adesao}</span>
                                </div>` : ''}
                            </div>
                            <div class="button-group">
                                <a class="download-btn" href="${downloadUrl}" target="_blank">
                                    <i class="fas fa-download"></i> Baixar Certificado
                                </a>
                                ${avaliacaoElement}
                            </div>
                        </div>
                    `;
                    certificatesContainer.innerHTML += cardHtml;
                });
                
                resultDiv.style.display = 'block';
                
                // Configurar os botões de avaliação após renderizar os certificados
                configurarBotoesAvaliacao();
            }
        }
    })
    .catch(error => {
        loader.style.display = 'none';
        errorDiv.textContent = 'Erro ao consultar o certificado. Tente novamente mais tarde.';
        errorDiv.style.display = 'block';
        console.error('Erro:', error);
    });
}