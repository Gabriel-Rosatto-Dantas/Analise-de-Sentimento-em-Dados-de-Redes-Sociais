"""
Módulo para análise de sentimento
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from textblob import TextBlob
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download necessário do NLTK
try:
    nltk.data.find('vader_lexicon')
    VADER_AVAILABLE = True
except LookupError:
    try:
        nltk.download('vader_lexicon')
        VADER_AVAILABLE = True
    except:
        VADER_AVAILABLE = False
        print("⚠️ VADER não disponível, usando análise básica")

class SentimentAnalyzer:
    """Classe para análise de sentimento"""
    
    def __init__(self):
        """Inicializa o analisador de sentimento"""
        if VADER_AVAILABLE:
            self.vader_analyzer = SentimentIntensityAnalyzer()
        else:
            self.vader_analyzer = None
        
        # Palavras positivas e negativas em português para TextBlob
        self.positive_words = {
            'bom', 'boa', 'ótimo', 'ótima', 'excelente', 'fantástico', 'fantástica',
            'incrível', 'maravilhoso', 'maravilhosa', 'perfeito', 'perfeita',
            'adoro', 'amo', 'gosto', 'recomendo', 'satisfeito', 'satisfeita',
            'feliz', 'alegre', 'contente', 'impressionado', 'impressionada',
            'surpreendente', 'genial', 'brilhante', 'espetacular', 'magnífico',
            'delicioso', 'deliciosa', 'saboroso', 'saborosa', 'gostoso', 'gostosa'
        }
        
        self.negative_words = {
            'ruim', 'péssimo', 'péssima', 'horrível', 'terrível', 'odioso',
            'detesto', 'odeio', 'desgosto', 'desapontado', 'desapontada',
            'frustrado', 'frustrada', 'irritado', 'irritada', 'bravo', 'brava',
            'furioso', 'furiosa', 'chateado', 'chateada', 'triste', 'deprimido',
            'deprimida', 'angustiado', 'angustiada', 'preocupado', 'preocupada',
            'nervoso', 'nervosa', 'ansioso', 'ansiosa', 'medo', 'assustado',
            'assustada', 'decepcionado', 'decepcionada', 'chocado', 'chocada'
        }
    
    def analyze_with_textblob(self, text: str) -> Dict[str, float]:
        """
        Analisa sentimento usando TextBlob
        
        Args:
            text (str): Texto para análise
            
        Returns:
            Dict[str, float]: Dicionário com polaridade e subjetividade
        """
        if not text or pd.isna(text):
            return {'polarity': 0.0, 'subjectivity': 0.0}
        
        blob = TextBlob(text)
        
        # Calcula polaridade baseada em palavras conhecidas
        words = text.lower().split()
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)
        
        # Ajusta polaridade baseada em palavras em português
        if positive_count > negative_count:
            polarity = min(1.0, blob.polarity + 0.3)
        elif negative_count > positive_count:
            polarity = max(-1.0, blob.polarity - 0.3)
        else:
            polarity = blob.polarity
        
        return {
            'polarity': polarity,
            'subjectivity': blob.subjectivity
        }
    
    def analyze_with_vader(self, text: str) -> Dict[str, float]:
        """
        Analisa sentimento usando VADER
        
        Args:
            text (str): Texto para análise
            
        Returns:
            Dict[str, float]: Dicionário com scores do VADER
        """
        if not text or pd.isna(text):
            return {'compound': 0.0, 'pos': 0.0, 'neu': 1.0, 'neg': 0.0}
        
        if self.vader_analyzer is None:
            # Fallback se VADER não estiver disponível
            return {'compound': 0.0, 'pos': 0.0, 'neu': 1.0, 'neg': 0.0}
        
        scores = self.vader_analyzer.polarity_scores(text)
        return scores
    
    def classify_sentiment(self, polarity: float, threshold: float = 0.1) -> str:
        """
        Classifica sentimento baseado na polaridade
        
        Args:
            polarity (float): Valor da polaridade (-1 a 1)
            threshold (float): Limiar para classificação neutra
            
        Returns:
            str: 'positivo', 'negativo' ou 'neutro'
        """
        if polarity > threshold:
            return 'positivo'
        elif polarity < -threshold:
            return 'negativo'
        else:
            return 'neutro'
    
    def analyze_text(self, text: str) -> Dict[str, any]:
        """
        Analisa sentimento completo de um texto
        
        Args:
            text (str): Texto para análise
            
        Returns:
            Dict[str, any]: Resultado completo da análise
        """
        # Análise com TextBlob
        textblob_result = self.analyze_with_textblob(text)
        
        # Análise com VADER
        vader_result = self.analyze_with_vader(text)
        
        # Classificação final (usa TextBlob como principal)
        sentiment_class = self.classify_sentiment(textblob_result['polarity'])
        
        return {
            'text': text,
            'sentiment_class': sentiment_class,
            'polarity': textblob_result['polarity'],
            'subjectivity': textblob_result['subjectivity'],
            'vader_compound': vader_result['compound'],
            'vader_pos': vader_result['pos'],
            'vader_neu': vader_result['neu'],
            'vader_neg': vader_result['neg']
        }
    
    def analyze_dataframe(self, df: pd.DataFrame, 
                         text_column: str = 'processed_text') -> pd.DataFrame:
        """
        Analisa sentimento de um DataFrame inteiro
        
        Args:
            df (pd.DataFrame): DataFrame com textos
            text_column (str): Nome da coluna com texto
            
        Returns:
            pd.DataFrame: DataFrame com análise de sentimento
        """
        df_analyzed = df.copy()
        
        # Aplica análise de sentimento
        sentiment_results = []
        for text in df_analyzed[text_column]:
            result = self.analyze_text(text)
            sentiment_results.append(result)
        
        # Adiciona colunas de sentimento ao DataFrame
        sentiment_df = pd.DataFrame(sentiment_results)
        
        # Combina com DataFrame original
        df_analyzed = pd.concat([df_analyzed, sentiment_df.drop('text', axis=1)], axis=1)
        
        print(f"✅ Análise de sentimento concluída para {len(df_analyzed)} textos")
        
        return df_analyzed
    
    def get_sentiment_summary(self, df: pd.DataFrame) -> Dict[str, any]:
        """
        Gera resumo estatístico da análise de sentimento
        
        Args:
            df (pd.DataFrame): DataFrame com análise de sentimento
            
        Returns:
            Dict[str, any]: Resumo estatístico
        """
        if 'sentiment_class' not in df.columns:
            raise ValueError("DataFrame deve conter coluna 'sentiment_class'")
        
        # Contagem por classe
        sentiment_counts = df['sentiment_class'].value_counts()
        
        # Percentuais
        sentiment_percentages = df['sentiment_class'].value_counts(normalize=True) * 100
        
        # Estatísticas de polaridade
        polarity_stats = df['polarity'].describe()
        
        # Estatísticas de subjetividade
        subjectivity_stats = df['subjectivity'].describe()
        
        return {
            'total_texts': len(df),
            'sentiment_counts': sentiment_counts.to_dict(),
            'sentiment_percentages': sentiment_percentages.to_dict(),
            'polarity_stats': polarity_stats.to_dict(),
            'subjectivity_stats': subjectivity_stats.to_dict(),
            'most_positive_text': df.loc[df['polarity'].idxmax(), 'text'] if len(df) > 0 else None,
            'most_negative_text': df.loc[df['polarity'].idxmin(), 'text'] if len(df) > 0 else None
        }
