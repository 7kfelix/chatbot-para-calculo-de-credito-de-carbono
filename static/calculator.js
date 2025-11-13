document.addEventListener('DOMContentLoaded', function() {
    console.log('📊 Carregando página de relatório...');
    
    const reportDataElement = document.getElementById('report-data');
    
    if (reportDataElement) {
        try {
            const reportData = JSON.parse(reportDataElement.textContent);
            console.log('✅ Dados do relatório carregados:', reportData);
            
            // Renderizar gráfico
            renderChart(reportData);
            
            // Formatar e exibir relatório narrativo
            formatNarrativeReport(reportData.narrative_report);
            
            // Atualizar cards de resumo
            updateReportCards(reportData);
            
        } catch (error) {
            console.error('❌ Erro ao carregar dados do relatório:', error);
            document.getElementById('narrative-report').innerHTML = 
                '<p style="color: var(--accent-red);">Erro ao carregar relatório. Por favor, recarregue a página.</p>';
        }
    } else {
        console.error('❌ Elemento report-data não encontrado');
    }
});

function formatNarrativeReport(text) {
    const narrativeDiv = document.getElementById('narrative-report');
    if (!narrativeDiv || !text) {
        console.error('❌ Elemento ou texto não encontrado');
        return;
    }
    
    console.log('📝 Formatando relatório narrativo...');
    
    // Converter Markdown para HTML
    let formatted = text
        // Links: [texto](url) ou [Link: url](url)
        .replace(/\[Link:\s*([^\]]+)\]\(([^)]+)\)/gi, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>')
        .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>')
        
        // Headers (fazer antes de bold)
        .replace(/^#### (.+)$/gm, '<h4>$1</h4>')
        .replace(/^### (.+)$/gm, '<h3>$1</h3>')
        .replace(/^## (.+)$/gm, '<h2>$1</h2>')
        
        // **Bold**
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        
        // *Italic*
        .replace(/\*(.+?)\*/g, '<em>$1</em>')
        
        // Listas numeradas: 1. Item
        .replace(/^\d+\.\s+(.+)$/gm, '<li class="numbered-item">$1</li>')
        
        // Listas com bullet: - Item ou * Item
        .replace(/^[\*\-]\s+(.+)$/gm, '<li class="bullet-item">$1</li>')
        
        // Quebras de linha duplas = separador de parágrafo
        .split('\n\n')
        .map(block => {
            block = block.trim();
            if (!block) return '';
            
            // Se já é tag HTML, retorna como está
            if (block.startsWith('<h') || block.startsWith('<div')) {
                return block;
            }
            
            // Se contém <li>, envelopar em <ul> ou <ol>
            if (block.includes('<li class="numbered-item">')) {
                return '<ol>' + block + '</ol>';
            }
            if (block.includes('<li class="bullet-item">')) {
                return '<ul>' + block + '</ul>';
            }
            
            // Se já tem tags <p>, <h>, etc, retorna
            if (block.includes('<p>') || block.includes('<h')) {
                return block;
            }
            
            // Caso contrário, wrap em <p>
            return '<p>' + block + '</p>';
        })
        .join('\n');
    
    // Limpar tags vazias
    formatted = formatted
        .replace(/<(ol|ul)>\s*<\/\1>/g, '')
        .replace(/<p>\s*<\/p>/g, '');
    
    // Processar quebras de linha simples dentro de parágrafos
    formatted = formatted.replace(/([^>])\n([^<])/g, '$1<br>$2');
    
    narrativeDiv.innerHTML = formatted;
    console.log('✅ Relatório formatado com sucesso');
}

function renderChart(reportData) {
    const ctx = document.getElementById('footprint-chart');
    if (!ctx) {
        console.error('❌ Canvas footprint-chart não encontrado');
        return;
    }
    
    try {
        console.log('📊 Renderizando gráfico...');
        
        const chartDetails = reportData.data_for_dashboard.details_kg_co2e;
        const totalEmissions = reportData.data_for_dashboard.total_kg_co2e;
        
        const labels = {
            'transporte': 'Transporte',
            'energia_eletrica': 'Energia Elétrica',
            'gas_cozinha': 'Gás de Cozinha'
        };
        
        const chartLabels = Object.keys(chartDetails).map(key => labels[key] || key);
        const chartValues = Object.values(chartDetails);
        
        // Destruir gráfico anterior se existir
        if (window.footprintChart) {
            window.footprintChart.destroy();
        }
        
        // Criar novo gráfico
        window.footprintChart = new Chart(ctx.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: chartLabels,
                datasets: [{
                    data: chartValues,
                    backgroundColor: ['#7e57c2', '#19c37d', '#fbc02d'],
                    borderColor: '#2a2b32',
                    borderWidth: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { 
                        position: 'top',
                        labels: { 
                            color: '#ececf1',
                            font: { size: 14, weight: '600' },
                            padding: 15,
                            usePointStyle: true
                        } 
                    },
                    title: { 
                        display: true, 
                        text: `Total: ${totalEmissions.toFixed(2)} kg CO2e`, 
                        color: '#ececf1',
                        font: { size: 18, weight: 'bold' },
                        padding: { top: 10, bottom: 20 }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        padding: 12,
                        titleColor: '#ececf1',
                        bodyColor: '#ececf1',
                        borderColor: '#7e57c2',
                        borderWidth: 1,
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed || 0;
                                const percentage = ((value / totalEmissions) * 100).toFixed(1);
                                return `${label}: ${value.toFixed(2)} kg CO2e (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
        
        console.log('✅ Gráfico renderizado com sucesso');
    } catch (error) {
        console.error('❌ Erro ao renderizar gráfico:', error);
    }
}

function updateReportCards(reportData) {
    try {
        const data = reportData.data_for_dashboard;
        const total = data.total_kg_co2e;
        const annual = total * 12;
        const trees = Math.round(annual / 22);
        const costMin = (annual / 1000) * 40;
        const costMax = (annual / 1000) * 60;
        
        // Atualizar cards
        const totalMonthly = document.getElementById('total-monthly');
        if (totalMonthly) {
            totalMonthly.textContent = total.toFixed(2) + ' kg CO2e';
        }
        
        const treesYearly = document.getElementById('trees-yearly');
        if (treesYearly) {
            treesYearly.textContent = trees + ' árvores';
        }
        
        const annualCost = document.getElementById('annual-cost');
        if (annualCost) {
            annualCost.textContent = `R$ ${costMin.toFixed(2)} - R$ ${costMax.toFixed(2)}`;
        }
        
        console.log('✅ Cards de resumo atualizados');
    } catch (error) {
        console.error('❌ Erro ao atualizar cards:', error);
    }
}

// Funções de UI (dropdown, sidebar)
function toggleDropdown() {
    const dropdown = document.getElementById('dropdown-menu');
    if (dropdown) {
        dropdown.classList.toggle('show');
    }
}

function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.sidebar-overlay');
    if (sidebar && overlay) {
        sidebar.classList.toggle('show');
        overlay.classList.toggle('show');
    }
}

function closeSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.sidebar-overlay');
    if (sidebar && overlay) {
        sidebar.classList.remove('show');
        overlay.classList.remove('show');
    }
}

// Fechar dropdown ao clicar fora
document.addEventListener('click', function(event) {
    const dropdown = document.getElementById('dropdown-menu');
    const userAvatar = document.querySelector('.user-avatar');
    
    if (dropdown && userAvatar && !dropdown.contains(event.target) && !userAvatar.contains(event.target)) {
        dropdown.classList.remove('show');
    }
});
