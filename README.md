# 📊 Análise de Sentimento em Dados de Redes Sociais

Um projeto completo para análise de sentimento em comentários de produtos ou marcas em redes sociais, especialmente Twitter. O sistema coleta dados, pré-processa texto, classifica comentários como 'positivo', 'negativo' ou 'neutro' e apresenta um resumo visual dos resultados.

## 🎯 Objetivo

Demonstrar como empresas podem monitorar a percepção pública e responder a crises de marca de forma proativa através da análise automatizada de sentimento em redes sociais.

## 🚀 Funcionalidades

- **Coleta de Dados**: Integração com API do Twitter para coleta automática de comentários
- **Pré-processamento**: Limpeza e normalização de texto em português
- **Análise de Sentimento**: Classificação usando TextBlob e NLTK com suporte a português
- **Visualizações**: Gráficos interativos e dashboard completo
- **Relatórios**: Geração automática de relatórios HTML com insights e recomendações
- **Dados de Exemplo**: Sistema funciona com dados simulados para demonstração

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **Pandas**: Manipulação de dados
- **NLTK**: Processamento de linguagem natural
- **TextBlob**: Análise de sentimento
- **Matplotlib/Seaborn**: Visualizações
- **Tweepy**: Integração com API do Twitter
- **HTML/CSS**: Relatórios interativos

## 📦 Instalação

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd analise-sentimento-redes-sociais
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\\Scripts\\activate  # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure a API do Twitter (Opcional)
Para usar dados reais do Twitter, você precisa de um token Bearer da API do Twitter:

1. Acesse [Twitter Developer Portal](https://developer.twitter.com/)
2. Crie uma aplicação e obtenha o Bearer Token
3. Configure a variável de ambiente:
```bash
export TWITTER_BEARER_TOKEN="seu_token_aqui"
```

## 🎮 Como Usar

### Uso Básico (Dados de Exemplo)
```bash
python main.py --brand "Nike" --query "Nike" --sample
```

### Uso com API do Twitter
```bash
python main.py --brand "iPhone" --query "iPhone" --token "seu_token" --max-results 200
```

### Parâmetros Disponíveis
- `--brand`: Nome da marca para análise
- `--query`: Termo de busca no Twitter
- `--sample`: Usar dados de exemplo (sem necessidade de API)
- `--token`: Token da API do Twitter
- `--max-results`: Número máximo de tweets para coletar

### Uso Programático
```python
from main import SentimentAnalysisPipeline

# Cria pipeline
pipeline = SentimentAnalysisPipeline(brand_name="Minha Marca")

# Executa análise completa
results = pipeline.run_complete_analysis(
    query="minha marca",
    use_sample=True,  # Usa dados de exemplo
    max_results=100
)

if results['success']:
    print(f"Análise concluída! Relatório em: {results['report_file']}")
```

## 📁 Estrutura do Projeto

```
analise-sentimento-redes-sociais/
├── src/
│   ├── __init__.py
│   ├── data_collector.py      # Coleta de dados do Twitter
│   ├── text_preprocessor.py   # Pré-processamento de texto
│   ├── sentiment_analyzer.py  # Análise de sentimento
│   ├── visualizer.py          # Criação de gráficos
│   └── report_generator.py    # Geração de relatórios
├── output/                    # Arquivos de saída
├── main.py                   # Script principal
├── config.py                 # Configurações
├── requirements.txt          # Dependências
└── README.md                # Este arquivo
```

## 📊 Saídas do Sistema

O sistema gera os seguintes arquivos na pasta `output/`:

### Dados
- `dados_brutos_[marca].csv`: Dados coletados do Twitter
- `dados_processados_[marca].csv`: Dados após pré-processamento
- `dados_analisados_[marca].csv`: Dados com análise de sentimento

### Visualizações
- `distribuicao_sentimentos_[marca].png`: Gráfico de distribuição
- `distribuicao_polaridade_[marca].png`: Histograma de polaridade
- `distribuicao_subjetividade_[marca].png`: Histograma de subjetividade
- `palavras_sentimento_[marca].png`: Palavras por sentimento
- `dashboard_[marca].png`: Dashboard completo

### Relatórios
- `relatorio_[marca].html`: Relatório HTML interativo
- `resumo_[marca].txt`: Resumo em texto simples

## 🔧 Configurações

Edite o arquivo `config.py` para personalizar:

- Palavras positivas/negativas em português
- Configurações de pré-processamento
- Cores dos gráficos
- Parâmetros de análise

## 📈 Exemplo de Resultado

O relatório HTML inclui:

- **Resumo Executivo**: Estatísticas principais
- **Distribuição de Sentimentos**: Percentuais e contagens
- **Visualizações**: Gráficos interativos
- **Insights**: Análises automáticas dos dados
- **Recomendações**: Sugestões baseadas nos resultados

## 🎯 Casos de Uso

### Monitoramento de Marca
- Acompanhar percepção pública em tempo real
- Identificar crises de marca rapidamente
- Medir impacto de campanhas publicitárias

### Análise de Produtos
- Avaliar feedback de lançamentos
- Comparar sentimentos entre produtos
- Identificar pontos de melhoria

### Gestão de Crise
- Detectar mudanças negativas na percepção
- Monitorar eficácia de respostas da empresa
- Acompanhar recuperação da imagem

## ⚠️ Limitações

- **API do Twitter**: Limitações de rate limit e custos
- **Idioma**: Otimizado para português brasileiro
- **Contexto**: Análise baseada em palavras-chave, não contexto completo
- **Ironia/Sarcasmo**: Pode não detectar corretamente

## 🔮 Melhorias Futuras

- [ ] Suporte a outras redes sociais (Instagram, Facebook)
- [ ] Análise de sentimento com modelos de deep learning
- [ ] Detecção de ironia e sarcasmo
- [ ] Análise temporal mais avançada
- [ ] Integração com APIs de IA (GPT, BERT)
- [ ] Dashboard web interativo
- [ ] Alertas automáticos por email

## 🤝 Contribuições

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para dúvidas ou problemas:

- Abra uma [issue](https://github.com/seu-usuario/analise-sentimento-redes-sociais/issues)
- Entre em contato: [gr.rosatto@gmail.com]

## 🙏 Agradecimentos

- Comunidade Python
- Desenvolvedores do NLTK e TextBlob
- Twitter Developer Platform
- Contribuidores do projeto

---

**Desenvolvido com ❤️ para análise de sentimento em redes sociais**
