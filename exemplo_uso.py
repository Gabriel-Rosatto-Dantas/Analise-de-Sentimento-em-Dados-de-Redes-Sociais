"""
Exemplo de uso do sistema de análise de sentimento
"""
import sys
import os

# Adiciona o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import SentimentAnalysisPipeline

def exemplo_basico():
    """Exemplo básico usando dados de exemplo"""
    print("🚀 Exemplo Básico - Análise com Dados de Exemplo")
    print("="*60)
    
    # Cria pipeline para análise da Nike
    pipeline = SentimentAnalysisPipeline(brand_name="Nike")
    
    # Executa análise completa com dados de exemplo
    results = pipeline.run_complete_analysis(
        query="Nike",
        use_sample=True,  # Usa dados de exemplo
        max_results=50
    )
    
    if results['success']:
        print("\n✅ Análise concluída com sucesso!")
        print(f"📊 Total de comentários: {results['summary']['total_texts']}")
        print(f"📈 Sentimento dominante: {max(results['summary']['sentiment_percentages'], key=results['summary']['sentiment_percentages'].get)}")
        print(f"📄 Relatório: {results['report_file']}")
    else:
        print(f"❌ Erro: {results['error']}")

def exemplo_multiplas_marcas():
    """Exemplo analisando múltiplas marcas"""
    print("\n🚀 Exemplo Múltiplas Marcas")
    print("="*60)
    
    marcas = ["iPhone", "Samsung", "McDonald's"]
    
    for marca in marcas:
        print(f"\n📱 Analisando: {marca}")
        pipeline = SentimentAnalysisPipeline(brand_name=marca)
        
        results = pipeline.run_complete_analysis(
            query=marca,
            use_sample=True,
            max_results=30
        )
        
        if results['success']:
            summary = results['summary']
            dominant = max(summary['sentiment_percentages'], key=summary['sentiment_percentages'].get)
            print(f"   ✅ {marca}: {summary['total_texts']} comentários, sentimento dominante: {dominant}")
        else:
            print(f"   ❌ {marca}: Erro na análise")

def exemplo_personalizado():
    """Exemplo com configurações personalizadas"""
    print("\n🚀 Exemplo Personalizado")
    print("="*60)
    
    # Cria pipeline personalizado
    pipeline = SentimentAnalysisPipeline(brand_name="Minha Empresa")
    
    # Executa análise
    results = pipeline.run_complete_analysis(
        query="minha empresa produto",
        use_sample=True,
        max_results=100
    )
    
    if results['success']:
        # Mostra estatísticas detalhadas
        summary = results['summary']
        print(f"\n📊 Estatísticas Detalhadas:")
        print(f"   Total de textos: {summary['total_texts']}")
        print(f"   Polaridade média: {summary['polarity_stats']['mean']:.3f}")
        print(f"   Subjetividade média: {summary['subjectivity_stats']['mean']:.3f}")
        
        print(f"\n📈 Distribuição de Sentimentos:")
        for sentiment, percentage in summary['sentiment_percentages'].items():
            count = summary['sentiment_counts'][sentiment]
            print(f"   {sentiment.title()}: {percentage:.1f}% ({count} comentários)")
        
        print(f"\n📄 Arquivos gerados:")
        print(f"   Relatório: {results['report_file']}")
        for chart in results['chart_files']:
            print(f"   Gráfico: {chart}")

def exemplo_com_api_twitter():
    """Exemplo usando API real do Twitter (requer token)"""
    print("\n🚀 Exemplo com API do Twitter")
    print("="*60)
    
    # Verifica se há token configurado
    token = os.getenv('TWITTER_BEARER_TOKEN')
    
    if not token:
        print("⚠️ Token da API do Twitter não configurado.")
        print("   Configure a variável TWITTER_BEARER_TOKEN ou use dados de exemplo.")
        return
    
    pipeline = SentimentAnalysisPipeline(brand_name="Twitter Real")
    
    results = pipeline.run_complete_analysis(
        query="Python programação",
        use_sample=False,  # Usa API real
        bearer_token=token,
        max_results=50
    )
    
    if results['success']:
        print("✅ Análise com dados reais do Twitter concluída!")
        print(f"📊 {results['summary']['total_texts']} tweets analisados")
    else:
        print(f"❌ Erro na coleta do Twitter: {results['error']}")
        print("   Usando dados de exemplo como fallback...")
        
        # Fallback para dados de exemplo
        results = pipeline.run_complete_analysis(
            query="Python programação",
            use_sample=True,
            max_results=50
        )
        
        if results['success']:
            print("✅ Análise com dados de exemplo concluída!")

def main():
    """Função principal com menu de exemplos"""
    print("📊 Sistema de Análise de Sentimento em Redes Sociais")
    print("="*60)
    print("Escolha um exemplo para executar:")
    print("1. Exemplo Básico")
    print("2. Múltiplas Marcas")
    print("3. Configuração Personalizada")
    print("4. API do Twitter (requer token)")
    print("5. Executar Todos")
    
    try:
        escolha = input("\nDigite sua escolha (1-5): ").strip()
        
        if escolha == "1":
            exemplo_basico()
        elif escolha == "2":
            exemplo_multiplas_marcas()
        elif escolha == "3":
            exemplo_personalizado()
        elif escolha == "4":
            exemplo_com_api_twitter()
        elif escolha == "5":
            exemplo_basico()
            exemplo_multiplas_marcas()
            exemplo_personalizado()
            exemplo_com_api_twitter()
        else:
            print("❌ Escolha inválida!")
            
    except KeyboardInterrupt:
        print("\n\n👋 Execução interrompida pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro durante execução: {str(e)}")
    
    print("\n🎉 Exemplos concluídos! Verifique a pasta 'output' para os resultados.")

if __name__ == "__main__":
    main()
