const API_BASE = "http://127.0.0.1:8000/api";
let meuGrafico = null;

// Formatar valores para o padrão monetário brasileiro (BRL)
function formatarMoeda(valor) {
  const numero = Number(valor) || 0;
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(numero);
}

// 1. Carregar KPIs da API
async function carregarKPIs() {
  try {
    const res = await fetch(`${API_BASE}/kpis`);
    const data = await res.json();
    
    document.getElementById('kpi-faturamento').innerText = formatarMoeda(data.receita_total);
    document.getElementById('kpi-qtd').innerText = data.total_vendas ?? 0;
    document.getElementById('kpi-ticket').innerText = formatarMoeda(data.ticket_medio);
  } catch (err) {
    console.error("Erro ao carregar KPIs:", err);
  }
}

// 2. Carregar Gráfico Chart.js
async function carregarGrafico() {
  try {
    const res = await fetch(`${API_BASE}/grafico-categorias`);
    const json = await res.json();

    const labels = json.labels || [];
    const valores = json.data || [];

    const canvasElement = document.getElementById('graficoCategorias');
    if (!canvasElement) {
      console.error("Elemento canvas 'graficoCategorias' não foi encontrado no HTML!");
      return;
    }

    const ctx = canvasElement.getContext('2d');
    
    if (meuGrafico) meuGrafico.destroy();

    meuGrafico = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Faturamento (R$)',
          data: valores,
          backgroundColor: ['#3498db', '#2ecc71', '#e74c3c'],
          borderRadius: 6
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false }
        }
      }
    });
  } catch (err) {
    console.error("Erro ao carregar gráfico:", err);
  }
}

// 3. Carregar Tabela com Filtro por Categoria
async function carregarTabela() {
  try {
    
    const selectElement = document.getElementById('select-categoria') || document.getElementById('filtroCategoria');
    const cat = selectElement ? selectElement.value : 'Todas';
    
    console.log("Categoria selecionada para o filtro:", cat); 
    
    let url = `${API_BASE}/tabela-vendas?limit=20`;
    
    if (cat && cat !== 'Todas' && cat !== '') {
      url += `&categoria=${encodeURIComponent(cat)}`;
    }

    const res = await fetch(url);
    const data = await res.json();

    const listaVendas = Array.isArray(data) ? data : (data.vendas || []);

    const tbody = document.getElementById('tabela-corpo');
    if (!tbody) return;
    
    tbody.innerHTML = '';

    if (listaVendas.length === 0) {
      tbody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: #7f8c8d; padding: 15px;">Nenhuma venda encontrada para esta categoria.</td></tr>`;
      return;
    }

    listaVendas.forEach(venda => {
      let dataFormatada = '-';
      const rawDate = venda.data_venda || venda.data_vendas;
      if (rawDate) {
        const partes = rawDate.split('T')[0].split('-');
        if (partes.length === 3) {
          dataFormatada = `${partes[2]}/${partes[1]}/${partes[0]}`;
        } else {
          dataFormatada = new Date(rawDate).toLocaleDateString('pt-BR');
        }
      }

      const row = `
        <tr>
          <td>#${venda.id}</td>
          <td>${venda.cliente}</td>
          <td>${venda.categoria}</td>
          <td>${formatarMoeda(venda.valor)}</td>
          <td>${dataFormatada}</td>
        </tr>
      `;
      tbody.innerHTML += row;
    });
  } catch (err) {
    console.error("Erro ao carregar tabela:", err);
  }
}

// Configura o evento de mudança no select assim que a página carregar
document.addEventListener('DOMContentLoaded', () => {
  const selectElement = document.getElementById('select-categoria') || document.getElementById('filtroCategoria');
  if (selectElement) {
    selectElement.addEventListener('change', () => {
      carregarTabela();
    });
  }
});

// Executar funções assim que a página carregar
window.onload = () => {
  carregarKPIs();
  carregarGrafico();
  carregarTabela();
};