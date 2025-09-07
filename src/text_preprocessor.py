"""
Módulo para pré-processamento de texto
"""
import re
import string
import pandas as pd
from typing import List, Optional
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import RSLPStemmer

# Download necessário do NLTK (executar apenas uma vez)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class TextPreprocessor:
    """Classe para pré-processamento de texto"""
    
    def __init__(self, language: str = 'portuguese'):
        """
        Inicializa o pré-processador
        
        Args:
            language (str): Idioma para stopwords e stemming
        """
        self.language = language
        self.stemmer = RSLPStemmer()
        
        # Carrega stopwords
        try:
            self.stop_words = set(stopwords.words(language))
        except:
            # Fallback para inglês se português não estiver disponível
            self.stop_words = set(stopwords.words('english'))
            print("⚠️ Usando stopwords em inglês como fallback")
    
    def clean_text(self, text: str) -> str:
        """
        Limpa o texto removendo caracteres especiais e normalizando
        
        Args:
            text (str): Texto original
            
        Returns:
            str: Texto limpo
        """
        if pd.isna(text) or not isinstance(text, str):
            return ""
        
        # Converte para minúsculas
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove menções (@username)
        text = re.sub(r'@\w+', '', text)
        
        # Remove hashtags (#hashtag)
        text = re.sub(r'#\w+', '', text)
        
        # Remove caracteres especiais, mantendo apenas letras, números e espaços
        text = re.sub(r'[^a-zA-ZÀ-ÿ0-9\s]', '', text)
        
        # Remove números isolados
        text = re.sub(r'\b\d+\b', '', text)
        
        # Remove espaços extras
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def remove_stopwords(self, text: str) -> str:
        """
        Remove stopwords do texto
        
        Args:
            text (str): Texto limpo
            
        Returns:
            str: Texto sem stopwords
        """
        if not text:
            return ""
        
        tokens = word_tokenize(text, language=self.language)
        filtered_tokens = [word for word in tokens if word not in self.stop_words]
        
        return ' '.join(filtered_tokens)
    
    def stem_text(self, text: str) -> str:
        """
        Aplica stemming no texto
        
        Args:
            text (str): Texto sem stopwords
            
        Returns:
            str: Texto com stemming aplicado
        """
        if not text:
            return ""
        
        tokens = word_tokenize(text, language=self.language)
        stemmed_tokens = [self.stemmer.stem(word) for word in tokens]
        
        return ' '.join(stemmed_tokens)
    
    def preprocess_text(self, text: str, 
                       remove_stopwords: bool = True,
                       apply_stemming: bool = False) -> str:
        """
        Aplica todo o pipeline de pré-processamento
        
        Args:
            text (str): Texto original
            remove_stopwords (bool): Se deve remover stopwords
            apply_stemming (bool): Se deve aplicar stemming
            
        Returns:
            str: Texto pré-processado
        """
        # Limpa o texto
        cleaned_text = self.clean_text(text)
        
        # Remove stopwords se solicitado
        if remove_stopwords:
            cleaned_text = self.remove_stopwords(cleaned_text)
        
        # Aplica stemming se solicitado
        if apply_stemming:
            cleaned_text = self.stem_text(cleaned_text)
        
        return cleaned_text
    
    def preprocess_dataframe(self, df: pd.DataFrame, 
                           text_column: str = 'text',
                           remove_stopwords: bool = True,
                           apply_stemming: bool = False) -> pd.DataFrame:
        """
        Pré-processa uma coluna de texto em um DataFrame
        
        Args:
            df (pd.DataFrame): DataFrame com os dados
            text_column (str): Nome da coluna com o texto
            remove_stopwords (bool): Se deve remover stopwords
            apply_stemming (bool): Se deve aplicar stemming
            
        Returns:
            pd.DataFrame: DataFrame com texto pré-processado
        """
        df_processed = df.copy()
        
        # Cria nova coluna com texto pré-processado
        df_processed['processed_text'] = df_processed[text_column].apply(
            lambda x: self.preprocess_text(x, remove_stopwords, apply_stemming)
        )
        
        # Remove linhas com texto vazio após pré-processamento
        df_processed = df_processed[df_processed['processed_text'].str.len() > 0]
        
        print(f"✅ Texto pré-processado para {len(df_processed)} registros")
        
        return df_processed
