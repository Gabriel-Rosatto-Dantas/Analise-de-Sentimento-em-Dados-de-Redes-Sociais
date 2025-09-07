"""
Demonstração rápida do sistema de análise de sentimento
"""
import sys
import os

# Adiciona o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import SentimentAnalysisPipeline

def demo_rapida():
    """Demonstração rápida com dados de exemplo"""
    print("🚀 DEMONSTRAÇÃO RÁPIDA - Análise de Sentimento")
    print("="*60)
    
    # Análise da Nike
    print("\n📱 Analisando comentários sobre Nike...")
    pipeline_nike = SentimentAnalysisPipeline(brand_name="Nike")
    
    results_nike = pipeline_nike.run_complete_analysis(
        query="Nike",
        use_sample=True,
        max_results=10
    )
    
    if results_nike['success']:
        summary = results_nike['summary']
        print(f"✅ Nike: {summary['total_texts']} comentários analisados")
        print(f"   Sentimento dominante: {max(summary['sentiment_percentages'], key=summary['sentiment_percentages'].get).title()}")
        print(f"   Polaridade média: {summary['polarity_stats']['mean']:.2f}")
    
    # Análise do iPhone
    print("\n📱 Analisando comentários sobre iPhone...")
    pipeline_iphone = SentimentAnalysisPipeline(brand_name="iPhone")
    
    results_iphone = pipeline_iphone.run_complete_analysis(
        query="iPhone",
        use_sample=True,
        max_results=10
    )
    
    if results_iphone['success']:
        summary = results_iphone['summary']
        print(f"✅ iPhone: {summary['total_texts']} comentários analisados")
        print(f"   Sentimento dominante: {max(summary['sentiment_percentages'], key=summary['sentiment_percentages'].get).title()}")
        print(f"   Polaridade média: {summary['polarity_stats']['mean']:.2f}")
    
    # Análise do McDonald's
    print("\n🍔 Analisando comentários sobre McDonald's...")
    pipeline_mcd = SentimentAnalysisPipeline(brand_name="McDonald's")
    
    results_mcd = pipeline_mcd.run_complete_analysis(
        query="McDonald's",
        use_sample=True,
        max_results=10
    )
    
    if results_mcd['success']:
        summary = results_mcd['summary']
        print(f"✅ McDonald's: {summary['total_texts']} comentários analisados")
        print(f"   Sentimento dominante: {max(summary['sentiment_percentages'], key=summary['sentiment_percentages'].get).title()}")
        print(f"   Polaridade média: {summary['polarity_stats']['mean']:.2f}")
    
    print("\n" + "="*60)
    print("🎉 DEMONSTRAÇÃO CONCLUÍDA!")
    print("📁 Verifique a pasta 'output' para todos os relatórios e gráficos")
    print("📄 Abra os arquivos .html no navegador para ver os relatórios completos")
    print("="*60)

if __name__ == "__main__":
    demo_rapida()
