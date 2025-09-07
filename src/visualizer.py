"""
Módulo para visualização dos resultados
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import warnings
warnings.filterwarnings('ignore')

# Configuração para português
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.style.use('seaborn-v0_8')

class SentimentVisualizer:
    """Classe para visualização dos resultados de análise de sentimento"""
    
    def __init__(self, figsize: tuple = (12, 8)):
        """
        Inicializa o visualizador
        
        Args:
            figsize (tuple): Tamanho padrão das figuras
        """
        self.figsize = figsize
        self.colors = {
            'positivo': '#2E8B57',  # Verde
            'negativo': '#DC143C',  # Vermelho
            'neutro': '#4682B4'     # Azul
        }
    
    def plot_sentiment_distribution(self, df: pd.DataFrame, 
                                   title: str = "Distribuição de Sentimentos") -> plt.Figure:
        """
        Cria gráfico de distribuição de sentimentos
        
        Args:
            df (pd.DataFrame): DataFrame com análise de sentimento
            title (str): Título do gráfico
            
        Returns:
            plt.Figure: Figura do matplotlib
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=self.figsize)
        
        # Gráfico de barras
        sentiment_counts = df['sentiment_class'].value_counts()
        colors = [self.colors.get(sentiment, '#808080') for sentiment in sentiment_counts.index]
        
        bars = ax1.bar(sentiment_counts.index, sentiment_counts.values, color=colors, alpha=0.7)
        ax1.set_title('Contagem de Sentimentos', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Número de Comentários')
        
        # Adiciona valores nas barras
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold')
        
        # Gráfico de pizza
        sentiment_percentages = df['sentiment_class'].value_counts(normalize=True) * 100
        colors_pie = [self.colors.get(sentiment, '#808080') for sentiment in sentiment_percentages.index]
        
        wedges, texts, autotexts = ax2.pie(sentiment_percentages.values, 
                                          labels=sentiment_percentages.index,
                                          colors=colors_pie,
                                          autopct='%1.1f%%',
                                          startangle=90)
        
        ax2.set_title('Percentual de Sentimentos', fontsize=14, fontweight='bold')
        
        # Melhora a aparência dos textos
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        plt.suptitle(title, fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        
        return fig
    
    def plot_polarity_distribution(self, df: pd.DataFrame,
                                  title: str = "Distribuição de Polaridade") -> plt.Figure:
        """
        Cria histograma da distribuição de polaridade
        
        Args:
            df (pd.DataFrame): DataFrame com análise de sentimento
            title (str): Título do gráfico
            
        Returns:
            plt.Figure: Figura do matplotlib
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Histograma com cores por sentimento
        for sentiment in df['sentiment_class'].unique():
            data = df[df['sentiment_class'] == sentiment]['polarity']
            ax.hist(data, alpha=0.6, label=sentiment, 
                   color=self.colors.get(sentiment, '#808080'), bins=20)
        
        ax.axvline(x=0, color='black', linestyle='--', alpha=0.5, label='Neutro')
        ax.set_xlabel('Polaridade (-1 = Negativo, +1 = Positivo)')
        ax.set_ylabel('Frequência')
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_subjectivity_distribution(self, df: pd.DataFrame,
                                     title: str = "Distribuição de Subjetividade") -> plt.Figure:
        """
        Cria histograma da distribuição de subjetividade
        
        Args:
            df (pd.DataFrame): DataFrame com análise de sentimento
            title (str): Título do gráfico
            
        Returns:
            plt.Figure: Figura do matplotlib
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Histograma com cores por sentimento
        for sentiment in df['sentiment_class'].unique():
            data = df[df['sentiment_class'] == sentiment]['subjectivity']
            ax.hist(data, alpha=0.6, label=sentiment, 
                   color=self.colors.get(sentiment, '#808080'), bins=20)
        
        ax.set_xlabel('Subjetividade (0 = Objetivo, 1 = Subjetivo)')
        ax.set_ylabel('Frequência')
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_sentiment_over_time(self, df: pd.DataFrame,
                                title: str = "Sentimento ao Longo do Tempo") -> plt.Figure:
        """
        Cria gráfico de sentimento ao longo do tempo
        
        Args:
            df (pd.DataFrame): DataFrame com análise de sentimento
            title (str): Título do gráfico
            
        Returns:
            plt.Figure: Figura do matplotlib
        """
        if 'created_at' not in df.columns:
            print("⚠️ Coluna 'created_at' não encontrada. Criando dados simulados.")
            # Cria dados simulados se não houver coluna de tempo
            df = df.copy()
            df['created_at'] = pd.date_range(start='2024-01-01', periods=len(df), freq='H')
        
        # Converte para datetime se necessário
        df['created_at'] = pd.to_datetime(df['created_at'])
        
        # Agrupa por dia e calcula média de polaridade
        daily_sentiment = df.groupby(df['created_at'].dt.date).agg({
            'polarity': 'mean',
            'sentiment_class': lambda x: x.value_counts().index[0] if len(x) > 0 else 'neutro'
        }).reset_index()
        
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Plota linha de polaridade
        ax.plot(daily_sentiment['created_at'], daily_sentiment['polarity'], 
               marker='o', linewidth=2, markersize=6, color='#2E8B57')
        
        # Adiciona linha de referência neutra
        ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        
        ax.set_xlabel('Data')
        ax.set_ylabel('Polaridade Média')
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Rotaciona labels do eixo x
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return fig
    
    def plot_word_cloud_sentiment(self, df: pd.DataFrame,
                                 title: str = "Palavras por Sentimento") -> plt.Figure:
        """
        Cria gráfico de palavras mais frequentes por sentimento
        
        Args:
            df (pd.DataFrame): DataFrame com análise de sentimento
            title (str): Título do gráfico
            
        Returns:
            plt.Figure: Figura do matplotlib
        """
        from collections import Counter
        
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        sentiments = ['positivo', 'negativo', 'neutro']
        
        for i, sentiment in enumerate(sentiments):
            if sentiment not in df['sentiment_class'].values:
                axes[i].text(0.5, 0.5, f'Sem dados para\n{sentiment}', 
                           ha='center', va='center', transform=axes[i].transAxes)
                axes[i].set_title(f'{sentiment.title()}', fontweight='bold')
                continue
            
            # Filtra textos do sentimento
            sentiment_texts = df[df['sentiment_class'] == sentiment]['processed_text']
            
            # Combina todos os textos
            all_text = ' '.join(sentiment_texts.astype(str))
            
            # Conta palavras
            words = all_text.split()
            word_counts = Counter(words)
            
            # Remove palavras muito curtas
            word_counts = {word: count for word, count in word_counts.items() 
                          if len(word) > 2 and count > 1}
            
            # Pega as 10 palavras mais frequentes
            top_words = dict(Counter(word_counts).most_common(10))
            
            if top_words:
                words_list = list(top_words.keys())
                counts_list = list(top_words.values())
                
                bars = axes[i].barh(words_list, counts_list, 
                                  color=self.colors.get(sentiment, '#808080'), alpha=0.7)
                
                # Adiciona valores nas barras
                for j, bar in enumerate(bars):
                    width = bar.get_width()
                    axes[i].text(width + 0.1, bar.get_y() + bar.get_height()/2.,
                               f'{int(width)}', ha='left', va='center', fontweight='bold')
            
            axes[i].set_title(f'{sentiment.title()}', fontweight='bold')
            axes[i].set_xlabel('Frequência')
        
        plt.suptitle(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        return fig
    
    def create_dashboard(self, df: pd.DataFrame, 
                       summary: Dict[str, any],
                       brand_name: str = "Marca") -> plt.Figure:
        """
        Cria dashboard completo com múltiplos gráficos
        
        Args:
            df (pd.DataFrame): DataFrame com análise de sentimento
            summary (Dict[str, any]): Resumo estatístico
            brand_name (str): Nome da marca analisada
            
        Returns:
            plt.Figure: Figura do matplotlib
        """
        fig = plt.figure(figsize=(20, 12))
        
        # Layout do dashboard
        gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)
        
        # 1. Distribuição de sentimentos (pizza)
        ax1 = fig.add_subplot(gs[0, 0])
        sentiment_percentages = df['sentiment_class'].value_counts(normalize=True) * 100
        colors_pie = [self.colors.get(sentiment, '#808080') for sentiment in sentiment_percentages.index]
        ax1.pie(sentiment_percentages.values, labels=sentiment_percentages.index,
               colors=colors_pie, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Distribuição de Sentimentos', fontweight='bold')
        
        # 2. Contagem de sentimentos (barras)
        ax2 = fig.add_subplot(gs[0, 1])
        sentiment_counts = df['sentiment_class'].value_counts()
        colors_bar = [self.colors.get(sentiment, '#808080') for sentiment in sentiment_counts.index]
        bars = ax2.bar(sentiment_counts.index, sentiment_counts.values, color=colors_bar, alpha=0.7)
        ax2.set_title('Contagem de Sentimentos', fontweight='bold')
        ax2.set_ylabel('Número de Comentários')
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold')
        
        # 3. Distribuição de polaridade
        ax3 = fig.add_subplot(gs[0, 2:])
        for sentiment in df['sentiment_class'].unique():
            data = df[df['sentiment_class'] == sentiment]['polarity']
            ax3.hist(data, alpha=0.6, label=sentiment, 
                    color=self.colors.get(sentiment, '#808080'), bins=20)
        ax3.axvline(x=0, color='black', linestyle='--', alpha=0.5)
        ax3.set_xlabel('Polaridade')
        ax3.set_ylabel('Frequência')
        ax3.set_title('Distribuição de Polaridade', fontweight='bold')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. Palavras mais frequentes por sentimento
        ax4 = fig.add_subplot(gs[1:, :])
        self._plot_word_frequency_by_sentiment(df, ax4)
        
        # Título principal
        fig.suptitle(f'Dashboard de Análise de Sentimento - {brand_name}', 
                    fontsize=20, fontweight='bold', y=0.98)
        
        return fig
    
    def _plot_word_frequency_by_sentiment(self, df: pd.DataFrame, ax):
        """Método auxiliar para plotar frequência de palavras por sentimento"""
        from collections import Counter
        
        sentiments = ['positivo', 'negativo', 'neutro']
        colors = [self.colors.get(sentiment, '#808080') for sentiment in sentiments]
        
        for i, sentiment in enumerate(sentiments):
            if sentiment not in df['sentiment_class'].values:
                continue
                
            sentiment_texts = df[df['sentiment_class'] == sentiment]['processed_text']
            all_text = ' '.join(sentiment_texts.astype(str))
            words = all_text.split()
            word_counts = Counter(words)
            word_counts = {word: count for word, count in word_counts.items() 
                          if len(word) > 2 and count > 1}
            top_words = dict(Counter(word_counts).most_common(5))
            
            if top_words:
                words_list = list(top_words.keys())
                counts_list = list(top_words.values())
                
                y_pos = np.arange(len(words_list))
                ax.barh(y_pos + i*0.3, counts_list, height=0.25, 
                       color=colors[i], alpha=0.7, label=sentiment)
                
                if i == 0:
                    ax.set_yticks(y_pos)
                    ax.set_yticklabels(words_list)
        
        ax.set_xlabel('Frequência')
        ax.set_title('Palavras Mais Frequentes por Sentimento', fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def save_plots(self, figures: List[plt.Figure], 
                  filenames: List[str], 
                  output_dir: str = "output"):
        """
        Salva figuras em arquivos
        
        Args:
            figures (List[plt.Figure]): Lista de figuras
            filenames (List[str]): Lista de nomes de arquivos
            output_dir (str): Diretório de saída
        """
        import os
        
        # Cria diretório se não existir
        os.makedirs(output_dir, exist_ok=True)
        
        for fig, filename in zip(figures, filenames):
            filepath = os.path.join(output_dir, filename)
            fig.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"📊 Gráfico salvo: {filepath}")
        
        plt.close('all')
