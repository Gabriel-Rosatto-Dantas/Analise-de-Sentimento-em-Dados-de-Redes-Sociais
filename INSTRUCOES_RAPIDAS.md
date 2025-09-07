# 🚀 Instruções Rápidas - Análise de Sentimento

## ⚡ Início Rápido

### 1. Instalação
```bash
pip install -r requirements.txt
python setup_nltk.py
```

### 2. Demonstração Rápida
```bash
python demo.py
```

### 3. Uso Básico
```bash
python main.py --brand "Sua Marca" --query "termo de busca" --sample
```

## 📊 Exemplos Práticos

### Análise de uma marca específica
```bash
python main.py --brand "Nike" --query "Nike" --sample
```

### Análise com API do Twitter (requer token)
```bash
python main.py --brand "iPhone" --query "iPhone" --token "seu_token" --max-results 100
```

### Análise programática
```python
from main import SentimentAnalysisPipeline

pipeline = SentimentAnalysisPipeline(brand_name="Minha Marca")
results = pipeline.run_complete_analysis(
    query="minha marca",
    use_sample=True,
    max_results=50
)
```

## 📁 Arquivos Gerados

Após executar uma análise, você encontrará na pasta `output/`:

- **dados_brutos_[marca].csv**: Dados coletados
- **dados_processados_[marca].csv**: Dados após limpeza
- **dados_analisados_[marca].csv**: Dados com análise de sentimento
- **relatorio_[marca].html**: Relatório HTML interativo
- **resumo_[marca].txt**: Resumo em texto
- **dashboard_[marca].png**: Dashboard visual
- **distribuicao_*.png**: Gráficos de distribuição

## 🎯 Casos de Uso

### Monitoramento de Marca
- Acompanhar percepção pública em tempo real
- Identificar crises de marca rapidamente
- Medir impacto de campanhas

### Análise de Produtos
- Avaliar feedback de lançamentos
- Comparar sentimentos entre produtos
- Identificar pontos de melhoria

### Gestão de Crise
- Detectar mudanças negativas na percepção
- Monitorar eficácia de respostas
- Acompanhar recuperação da imagem

## ⚙️ Configuração da API do Twitter

1. Acesse [Twitter Developer Portal](https://developer.twitter.com/)
2. Crie uma aplicação
3. Obtenha o Bearer Token
4. Configure a variável de ambiente:
   ```bash
   export TWITTER_BEARER_TOKEN="seu_token"
   ```

## 🔧 Personalização

Edite `config.py` para:
- Adicionar palavras positivas/negativas
- Configurar cores dos gráficos
- Ajustar parâmetros de análise

## 📞 Suporte

- Verifique os logs de erro no terminal
- Consulte o README.md completo
- Abra uma issue no repositório

---

**🎉 Pronto para usar! Execute `python demo.py` para começar.**
