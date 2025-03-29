document.addEventListener('DOMContentLoaded', function () {
  new Vue({
    el: '#app',
    data() {
      return {
        nome: '',
        url: '',
        meses: '',
        resultadoOperadora: [],
        resultadoDespesas: [],
        scrapingResult: '',
        zipFile: null,
      };
    },
    methods: {
      buscarOperadora() {
        console.log('Chamando buscarOperadora...');
        axios
          .get(`http://localhost:5000/buscar_operadora?nome=${this.nome}`)
          .then((response) => {
            console.log('Resposta da API:', response.data);
            this.resultadoOperadora = response.data;
          })
          .catch((error) => console.error('Erro ao buscar operadora:', error));
      },

      buscarDespesas() {
        console.log('Chamando buscarDespesas...');
        axios
          .get(`http://localhost:5000/buscar_despesas?meses=${this.meses}`)
          .then((response) => {
            console.log('Resposta da API:', response.data);
            this.resultadoDespesas = response.data.map((item) => ({
              nomeOperadora: item[0],
              despesas: parseFloat(item[1]).toLocaleString('pt-BR', {
                style: 'currency',
                currency: 'BRL',
              }),
            }));
          })
          .catch((error) => console.error('Erro ao buscar despesas:', error));
      },
    },
  });
});
