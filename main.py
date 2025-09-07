"""
Análise de Sentimento em Dados de Redes Sociais
Projeto principal para monitoramento de percepção pública de marcas
"""
import os
import sys
import pandas as pd
from datetime import datetime
import argparse

# Adiciona o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_collector import TwitterDataCollector, collect_sample_data
from text_preprocessor import TextPreprocessor
from sentiment_analyzer import SentimentAnalyzer
from visualizer import SentimentVisualizer
from report_generator import ReportGenerator

class SentimentAnalysisPipeline:
    """Pipeline completo para análise de sentimento"""
    
    def __init__(self, brand_name: str = "Marca"):
        """
        Inicializa o pipeline
        
        Args:
            brand_name (str): Nome da marca para análise
        """
        self.brand_name = brand_name
        self.preprocessor = TextPreprocessor()
        self.analyzer = SentimentAnalyzer()
        self.visualizer = SentimentVisualizer()
        self.report_generator = ReportGenerator()
        
        # Cria diretório de saída
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def collect_data(self, query: str, use_sample: bool = True, 
                    bearer_token: str = None, max_results: int = 100) -> pd.DataFrame:
        """
        Coleta dados do Twitter ou usa dados de exemplo
        
        Args:
            query (str): Termo de busca
            use_sample (bool): Se deve usar dados de exemplo
            bearer_token (str): Token da API do Twitter
            max_results (int): Número máximo de resultados
            
        Returns:
            pd.DataFrame: DataFrame com os dados coletados
        """
        print(f"🔍 Coletando dados para: {query}")
        
        if use_sample or not bearer_token:
            print("📊 Usando dados de exemplo...")
            df = collect_sample_data()
        else:
            print("🐦 Coletando dados do Twitter...")
            collector = TwitterDataCollector(bearer_token)
            df = collector.search_tweets(query, max_results)
            
            if df.empty:
                print("⚠️ Nenhum dado coletado do Twitter. Usando dados de exemplo...")
                df = collect_sample_data()
        
        # Salva dados brutos
        raw_data_file = os.path.join(self.output_dir, f"dados_brutos_{self.brand_name.lower()}.csv")
        df.to_csv(raw_data_file, index=False, encoding='utf-8')
        print(f"💾 Dados brutos salvos: {raw_data_file}")
        
        return df
    
    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Pré-processa os dados de texto
        
        Args:
            df (pd.DataFrame): DataFrame com dados brutos
            
        Returns:
            pd.DataFrame: DataFrame pré-processado
        """
        print("🔧 Pré-processando texto...")
        
        df_processed = self.preprocessor.preprocess_dataframe(
            df, 
            text_column='text',
            remove_stopwords=True,
            apply_stemming=False
        )
        
        # Salva dados pré-processados
        processed_file = os.path.join(self.output_dir, f"dados_processados_{self.brand_name.lower()}.csv")
        df_processed.to_csv(processed_file, index=False, encoding='utf-8')
        print(f"💾 Dados processados salvos: {processed_file}")
        
        return df_processed
    
    def analyze_sentiment(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Analisa sentimento dos textos
        
        Args:
            df (pd.DataFrame): DataFrame pré-processado
            
        Returns:
            pd.DataFrame: DataFrame com análise de sentimento
        """
        print("🧠 Analisando sentimento...")
        
        df_analyzed = self.analyzer.analyze_dataframe(df, text_column='processed_text')
        
        # Salva dados com análise
        analyzed_file = os.path.join(self.output_dir, f"dados_analisados_{self.brand_name.lower()}.csv")
        df_analyzed.to_csv(analyzed_file, index=False, encoding='utf-8')
        print(f"💾 Dados analisados salvos: {analyzed_file}")
        
        return df_analyzed
    
    def create_visualizations(self, df: pd.DataFrame) -> list:
        """
        Cria visualizações dos resultados
        
        Args:
            df (pd.DataFrame): DataFrame com análise de sentimento
            
        Returns:
            list: Lista de arquivos de gráficos criados
        """
        print("📊 Criando visualizações...")
        
        figures = []
        filenames = []
        
        # 1. Distribuição de sentimentos
        fig1 = self.visualizer.plot_sentiment_distribution(
            df, f"Distribuição de Sentimentos - {self.brand_name}"
        )
        figures.append(fig1)
        filenames.append(f"distribuicao_sentimentos_{self.brand_name.lower()}.png")
        
        # 2. Distribuição de polaridade
        fig2 = self.visualizer.plot_polarity_distribution(
            df, f"Distribuição de Polaridade - {self.brand_name}"
        )
        figures.append(fig2)
        filenames.append(f"distribuicao_polaridade_{self.brand_name.lower()}.png")
        
        # 3. Distribuição de subjetividade
        fig3 = self.visualizer.plot_subjectivity_distribution(
            df, f"Distribuição de Subjetividade - {self.brand_name}"
        )
        figures.append(fig3)
        filenames.append(f"distribuicao_subjetividade_{self.brand_name.lower()}.png")
        
        # 4. Palavras por sentimento
        fig4 = self.visualizer.plot_word_cloud_sentiment(
            df, f"Palavras por Sentimento - {self.brand_name}"
        )
        figures.append(fig4)
        filenames.append(f"palavras_sentimento_{self.brand_name.lower()}.png")
        
        # 5. Dashboard completo
        summary = self.analyzer.get_sentiment_summary(df)
        fig5 = self.visualizer.create_dashboard(df, summary, self.brand_name)
        figures.append(fig5)
        filenames.append(f"dashboard_{self.brand_name.lower()}.png")
        
        # Salva todos os gráficos
        chart_files = []
        for fig, filename in zip(figures, filenames):
            filepath = os.path.join(self.output_dir, filename)
            fig.savefig(filepath, dpi=300, bbox_inches='tight')
            chart_files.append(filepath)
            print(f"📊 Gráfico salvo: {filepath}")
        
        return chart_files
    
    def generate_report(self, df: pd.DataFrame, chart_files: list) -> str:
        """
        Gera relatório final
        
        Args:
            df (pd.DataFrame): DataFrame com análise de sentimento
            chart_files (list): Lista de arquivos de gráficos
            
        Returns:
            str: Caminho do arquivo de relatório
        """
        print("📄 Gerando relatório...")
        
        # Gera resumo estatístico
        summary = self.analyzer.get_sentiment_summary(df)
        
        # Gera relatório HTML
        html_content = self.report_generator.generate_html_report(
            df, summary, self.brand_name, chart_files
        )
        
        # Salva relatório
        report_file = os.path.join(self.output_dir, f"relatorio_{self.brand_name.lower()}.html")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Gera também resumo em texto
        summary_text = self.report_generator.generate_summary_text(summary, self.brand_name)
        summary_file = os.path.join(self.output_dir, f"resumo_{self.brand_name.lower()}.txt")
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary_text)
        
        print(f"📄 Relatório HTML salvo: {report_file}")
        print(f"📄 Resumo em texto salvo: {summary_file}")
        
        return report_file
    
    def run_complete_analysis(self, query: str, use_sample: bool = True,
                            bearer_token: str = None, max_results: int = 100) -> dict:
        """
        Executa análise completa
        
        Args:
            query (str): Termo de busca
            use_sample (bool): Se deve usar dados de exemplo
            bearer_token (str): Token da API do Twitter
            max_results (int): Número máximo de resultados
            
        Returns:
            dict: Resultados da análise
        """
        print(f"🚀 Iniciando análise completa para: {self.brand_name}")
        print("="*60)
        
        start_time = datetime.now()
        
        try:
            # 1. Coleta de dados
            df_raw = self.collect_data(query, use_sample, bearer_token, max_results)
            
            # 2. Pré-processamento
            df_processed = self.preprocess_data(df_raw)
            
            # 3. Análise de sentimento
            df_analyzed = self.analyze_sentiment(df_processed)
            
            # 4. Visualizações
            chart_files = self.create_visualizations(df_analyzed)
            
            # 5. Relatório
            report_file = self.generate_report(df_analyzed, chart_files)
            
            # Resumo final
            summary = self.analyzer.get_sentiment_summary(df_analyzed)
            
            end_time = datetime.now()
            duration = end_time - start_time
            
            print("="*60)
            print("✅ ANÁLISE CONCLUÍDA COM SUCESSO!")
            print(f"⏱️ Tempo total: {duration.total_seconds():.2f} segundos")
            print(f"📊 Total de comentários analisados: {summary['total_texts']}")
            print(f"📈 Sentimento dominante: {max(summary['sentiment_percentages'], key=summary['sentiment_percentages'].get).title()}")
            print(f"📄 Relatório disponível em: {report_file}")
            print("="*60)
            
            return {
                'success': True,
                'data': df_analyzed,
                'summary': summary,
                'report_file': report_file,
                'chart_files': chart_files,
                'duration': duration
            }
            
        except Exception as e:
            print(f"❌ Erro durante a análise: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='Análise de Sentimento em Redes Sociais')
    parser.add_argument('--brand', type=str, default='Marca', help='Nome da marca para análise')
    parser.add_argument('--query', type=str, default='produto', help='Termo de busca')
    parser.add_argument('--sample', action='store_true', help='Usar dados de exemplo')
    parser.add_argument('--token', type=str, help='Token da API do Twitter')
    parser.add_argument('--max-results', type=int, default=100, help='Número máximo de resultados')
    
    args = parser.parse_args()
    
    # Cria pipeline
    pipeline = SentimentAnalysisPipeline(brand_name=args.brand)
    
    # Executa análise
    results = pipeline.run_complete_analysis(
        query=args.query,
        use_sample=args.sample,
        bearer_token=args.token,
        max_results=args.max_results
    )
    
    if results['success']:
        print("\n🎉 Análise concluída! Verifique os arquivos na pasta 'output'.")
    else:
        print(f"\n💥 Falha na análise: {results['error']}")

if __name__ == "__main__":
    main()
