"""
Módulo para geração de relatórios
"""
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Any
import os

class ReportGenerator:
    """Classe para geração de relatórios de análise de sentimento"""
    
    def __init__(self):
        """Inicializa o gerador de relatórios"""
        self.template = self._get_html_template()
    
    def _get_html_template(self) -> str:
        """Retorna template HTML para o relatório"""
        return """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Análise de Sentimento - {brand_name}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            border-bottom: 3px solid #2E8B57;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            color: #2E8B57;
            margin: 0;
            font-size: 2.5em;
        }}
        .header p {{
            color: #666;
            margin: 10px 0 0 0;
            font-size: 1.1em;
        }}
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .summary-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}
        .summary-card h3 {{
            margin: 0 0 10px 0;
            font-size: 2em;
        }}
        .summary-card p {{
            margin: 0;
            font-size: 1.1em;
        }}
        .sentiment-breakdown {{
            margin: 30px 0;
        }}
        .sentiment-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            border-left: 5px solid;
        }}
        .sentiment-positive {{
            background-color: #f0f9f0;
            border-left-color: #2E8B57;
        }}
        .sentiment-negative {{
            background-color: #fdf0f0;
            border-left-color: #DC143C;
        }}
        .sentiment-neutral {{
            background-color: #f0f4f9;
            border-left-color: #4682B4;
        }}
        .sentiment-label {{
            font-weight: bold;
            font-size: 1.2em;
        }}
        .sentiment-percentage {{
            font-size: 1.5em;
            font-weight: bold;
        }}
        .insights {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 30px 0;
        }}
        .insights h3 {{
            color: #2E8B57;
            margin-top: 0;
        }}
        .insights ul {{
            margin: 0;
            padding-left: 20px;
        }}
        .insights li {{
            margin: 10px 0;
        }}
        .recommendations {{
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            padding: 20px;
            border-radius: 10px;
            margin: 30px 0;
        }}
        .recommendations h3 {{
            color: #856404;
            margin-top: 0;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #666;
        }}
        .chart-container {{
            text-align: center;
            margin: 30px 0;
        }}
        .chart-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Relatório de Análise de Sentimento</h1>
            <p>{brand_name} - {report_date}</p>
        </div>
        
        <div class="summary-grid">
            <div class="summary-card">
                <h3>{total_texts}</h3>
                <p>Total de Comentários</p>
            </div>
            <div class="summary-card">
                <h3>{avg_polarity:.2f}</h3>
                <p>Polaridade Média</p>
            </div>
            <div class="summary-card">
                <h3>{avg_subjectivity:.2f}</h3>
                <p>Subjetividade Média</p>
            </div>
            <div class="summary-card">
                <h3>{dominant_sentiment}</h3>
                <p>Sentimento Dominante</p>
            </div>
        </div>
        
        <div class="sentiment-breakdown">
            <h2>📈 Distribuição de Sentimentos</h2>
            {sentiment_items}
        </div>
        
        <div class="chart-container">
            <h3>📊 Visualizações</h3>
            {chart_images}
        </div>
        
        <div class="insights">
            <h3>🔍 Principais Insights</h3>
            <ul>
                {insights_list}
            </ul>
        </div>
        
        <div class="recommendations">
            <h3>💡 Recomendações</h3>
            <ul>
                {recommendations_list}
            </ul>
        </div>
        
        <div class="footer">
            <p>Relatório gerado automaticamente em {report_date}</p>
            <p>Análise de Sentimento em Dados de Redes Sociais</p>
        </div>
    </div>
</body>
</html>
        """
    
    def generate_insights(self, summary: Dict[str, Any]) -> List[str]:
        """
        Gera insights baseados no resumo estatístico
        
        Args:
            summary (Dict[str, any]): Resumo estatístico
            
        Returns:
            List[str]: Lista de insights
        """
        insights = []
        
        # Análise da distribuição de sentimentos
        sentiment_percentages = summary['sentiment_percentages']
        total_texts = summary['total_texts']
        
        # Sentimento dominante
        dominant_sentiment = max(sentiment_percentages, key=sentiment_percentages.get)
        dominant_percentage = sentiment_percentages[dominant_sentiment]
        
        if dominant_percentage > 50:
            insights.append(f"O sentimento <strong>{dominant_sentiment}</strong> domina com {dominant_percentage:.1f}% dos comentários.")
        else:
            insights.append(f"A percepção está dividida, com nenhum sentimento dominando claramente.")
        
        # Análise de polaridade
        avg_polarity = summary['polarity_stats']['mean']
        if avg_polarity > 0.1:
            insights.append(f"A polaridade média positiva ({avg_polarity:.2f}) indica percepção geralmente favorável.")
        elif avg_polarity < -0.1:
            insights.append(f"A polaridade média negativa ({avg_polarity:.2f}) indica percepção geralmente desfavorável.")
        else:
            insights.append(f"A polaridade neutra ({avg_polarity:.2f}) indica percepção equilibrada.")
        
        # Análise de subjetividade
        avg_subjectivity = summary['subjectivity_stats']['mean']
        if avg_subjectivity > 0.6:
            insights.append(f"Alta subjetividade ({avg_subjectivity:.2f}) indica comentários emocionais e pessoais.")
        elif avg_subjectivity < 0.4:
            insights.append(f"Baixa subjetividade ({avg_subjectivity:.2f}) indica comentários mais objetivos e factuais.")
        else:
            insights.append(f"Subjetividade moderada ({avg_subjectivity:.2f}) indica mistura de comentários emocionais e objetivos.")
        
        # Análise de extremos
        if 'most_positive_text' in summary and summary['most_positive_text']:
            insights.append("Comentários muito positivos foram identificados, indicando pontos fortes da marca.")
        
        if 'most_negative_text' in summary and summary['most_negative_text']:
            insights.append("Comentários muito negativos foram identificados, indicando áreas de melhoria.")
        
        return insights
    
    def generate_recommendations(self, summary: Dict[str, Any]) -> List[str]:
        """
        Gera recomendações baseadas na análise
        
        Args:
            summary (Dict[str, any]): Resumo estatístico
            
        Returns:
            List[str]: Lista de recomendações
        """
        recommendations = []
        
        sentiment_percentages = summary['sentiment_percentages']
        avg_polarity = summary['polarity_stats']['mean']
        
        # Recomendações baseadas no sentimento dominante
        dominant_sentiment = max(sentiment_percentages, key=sentiment_percentages.get)
        dominant_percentage = sentiment_percentages[dominant_sentiment]
        
        if dominant_sentiment == 'negativo' and dominant_percentage > 40:
            recommendations.append("Implementar estratégias de comunicação de crise para melhorar a percepção.")
            recommendations.append("Investigar as principais causas dos comentários negativos.")
            recommendations.append("Desenvolver campanhas de engajamento positivo com clientes satisfeitos.")
        
        elif dominant_sentiment == 'positivo' and dominant_percentage > 50:
            recommendations.append("Capitalizar no sentimento positivo com campanhas de marketing.")
            recommendations.append("Amplificar os comentários positivos nas redes sociais.")
            recommendations.append("Usar o feedback positivo para melhorar produtos/serviços.")
        
        else:
            recommendations.append("Monitorar continuamente a percepção da marca.")
            recommendations.append("Desenvolver estratégias para converter sentimentos neutros em positivos.")
        
        # Recomendações gerais
        recommendations.append("Implementar monitoramento contínuo de sentimento em tempo real.")
        recommendations.append("Treinar equipe de atendimento ao cliente para responder adequadamente.")
        recommendations.append("Criar protocolos de resposta rápida para crises de marca.")
        
        return recommendations
    
    def generate_html_report(self, df: pd.DataFrame, 
                           summary: Dict[str, Any],
                           brand_name: str = "Marca",
                           chart_files: List[str] = None) -> str:
        """
        Gera relatório HTML completo
        
        Args:
            df (pd.DataFrame): DataFrame com análise de sentimento
            summary (Dict[str, any]): Resumo estatístico
            brand_name (str): Nome da marca
            chart_files (List[str]): Lista de arquivos de gráficos
            
        Returns:
            str: HTML do relatório
        """
        # Dados para o template
        report_date = datetime.now().strftime("%d/%m/%Y às %H:%M")
        total_texts = summary['total_texts']
        avg_polarity = summary['polarity_stats']['mean']
        avg_subjectivity = summary['subjectivity_stats']['mean']
        
        # Sentimento dominante
        sentiment_percentages = summary['sentiment_percentages']
        dominant_sentiment = max(sentiment_percentages, key=sentiment_percentages.get)
        
        # Items de sentimento
        sentiment_items = ""
        for sentiment, percentage in sentiment_percentages.items():
            count = summary['sentiment_counts'][sentiment]
            sentiment_class = f"sentiment-{sentiment}"
            sentiment_items += f"""
            <div class="{sentiment_class}">
                <span class="sentiment-label">{sentiment.title()}</span>
                <span class="sentiment-percentage">{percentage:.1f}% ({count} comentários)</span>
            </div>
            """
        
        # Imagens dos gráficos
        chart_images = ""
        if chart_files:
            for chart_file in chart_files:
                if os.path.exists(chart_file):
                    chart_images += f'<img src="{os.path.basename(chart_file)}" alt="Gráfico">'
        
        # Insights e recomendações
        insights = self.generate_insights(summary)
        recommendations = self.generate_recommendations(summary)
        
        insights_list = "".join([f"<li>{insight}</li>" for insight in insights])
        recommendations_list = "".join([f"<li>{recommendation}</li>" for recommendation in recommendations])
        
        # Substitui variáveis no template
        html_content = self.template.format(
            brand_name=brand_name,
            report_date=report_date,
            total_texts=total_texts,
            avg_polarity=avg_polarity,
            avg_subjectivity=avg_subjectivity,
            dominant_sentiment=dominant_sentiment.title(),
            sentiment_items=sentiment_items,
            chart_images=chart_images,
            insights_list=insights_list,
            recommendations_list=recommendations_list
        )
        
        return html_content
    
    def save_report(self, html_content: str, filename: str = None, output_dir: str = "output"):
        """
        Salva o relatório HTML
        
        Args:
            html_content (str): Conteúdo HTML do relatório
            filename (str): Nome do arquivo (opcional)
            output_dir (str): Diretório de saída
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"relatorio_sentimento_{timestamp}.html"
        
        # Cria diretório se não existir
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"📄 Relatório salvo: {filepath}")
        return filepath
    
    def generate_summary_text(self, summary: Dict[str, Any], brand_name: str = "Marca") -> str:
        """
        Gera resumo em texto simples
        
        Args:
            summary (Dict[str, any]): Resumo estatístico
            brand_name (str): Nome da marca
            
        Returns:
            str: Resumo em texto
        """
        sentiment_percentages = summary['sentiment_percentages']
        total_texts = summary['total_texts']
        avg_polarity = summary['polarity_stats']['mean']
        
        text = f"""
RELATÓRIO DE ANÁLISE DE SENTIMENTO - {brand_name.upper()}
{'='*50}

RESUMO EXECUTIVO:
- Total de comentários analisados: {total_texts}
- Polaridade média: {avg_polarity:.2f}
- Sentimento dominante: {max(sentiment_percentages, key=sentiment_percentages.get).title()}

DISTRIBUIÇÃO DE SENTIMENTOS:
"""
        
        for sentiment, percentage in sentiment_percentages.items():
            count = summary['sentiment_counts'][sentiment]
            text += f"- {sentiment.title()}: {percentage:.1f}% ({count} comentários)\n"
        
        text += f"""
ESTATÍSTICAS DE POLARIDADE:
- Média: {summary['polarity_stats']['mean']:.2f}
- Mediana: {summary['polarity_stats']['50%']:.2f}
- Desvio padrão: {summary['polarity_stats']['std']:.2f}
- Mínimo: {summary['polarity_stats']['min']:.2f}
- Máximo: {summary['polarity_stats']['max']:.2f}

ESTATÍSTICAS DE SUBJETIVIDADE:
- Média: {summary['subjectivity_stats']['mean']:.2f}
- Mediana: {summary['subjectivity_stats']['50%']:.2f}
- Desvio padrão: {summary['subjectivity_stats']['std']:.2f}

Relatório gerado em: {datetime.now().strftime("%d/%m/%Y às %H:%M")}
        """
        
        return text
