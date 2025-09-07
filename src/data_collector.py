"""
Módulo para coleta de dados do Twitter
"""
import tweepy
import pandas as pd
import time
from datetime import datetime, timedelta
import os
from typing import List, Dict, Optional

class TwitterDataCollector:
    """Classe para coletar dados do Twitter"""
    
    def __init__(self, bearer_token: str):
        """
        Inicializa o coletor de dados do Twitter
        
        Args:
            bearer_token (str): Token de acesso da API do Twitter
        """
        self.client = tweepy.Client(bearer_token=bearer_token)
        
    def search_tweets(self, 
                     query: str, 
                     max_results: int = 100,
                     days_back: int = 7) -> pd.DataFrame:
        """
        Busca tweets baseado em uma query
        
        Args:
            query (str): Termo de busca (ex: "Nike" ou "iPhone")
            max_results (int): Número máximo de tweets para coletar
            days_back (int): Número de dias para buscar no passado
            
        Returns:
            pd.DataFrame: DataFrame com os tweets coletados
        """
        try:
            # Calcula a data de início da busca
            start_time = datetime.now() - timedelta(days=days_back)
            
            tweets_data = []
            
            # Busca tweets
            tweets = tweepy.Paginator(
                self.client.search_recent_tweets,
                query=query,
                tweet_fields=['created_at', 'public_metrics', 'context_annotations', 'lang'],
                user_fields=['username', 'verified'],
                max_results=min(max_results, 100),  # Máximo por página
                start_time=start_time
            ).flatten(limit=max_results)
            
            for tweet in tweets:
                tweet_info = {
                    'id': tweet.id,
                    'text': tweet.text,
                    'created_at': tweet.created_at,
                    'author_id': tweet.author_id,
                    'retweet_count': tweet.public_metrics['retweet_count'],
                    'like_count': tweet.public_metrics['like_count'],
                    'reply_count': tweet.public_metrics['reply_count'],
                    'quote_count': tweet.public_metrics['quote_count'],
                    'lang': tweet.lang
                }
                tweets_data.append(tweet_info)
                
            df = pd.DataFrame(tweets_data)
            
            if not df.empty:
                print(f"✅ Coletados {len(df)} tweets para a query: '{query}'")
            else:
                print(f"⚠️ Nenhum tweet encontrado para a query: '{query}'")
                
            return df
            
        except Exception as e:
            print(f"❌ Erro ao coletar tweets: {str(e)}")
            return pd.DataFrame()
    
    def save_tweets(self, df: pd.DataFrame, filename: str):
        """
        Salva os tweets em um arquivo CSV
        
        Args:
            df (pd.DataFrame): DataFrame com os tweets
            filename (str): Nome do arquivo para salvar
        """
        if not df.empty:
            df.to_csv(filename, index=False, encoding='utf-8')
            print(f"💾 Tweets salvos em: {filename}")
        else:
            print("⚠️ Nenhum dado para salvar")

def collect_sample_data():
    """
    Função para coletar dados de exemplo (simulados)
    Usado quando não há acesso à API do Twitter
    """
    sample_tweets = [
        {
            'id': 1,
            'text': 'Adorei o novo iPhone! A câmera está incrível e a bateria dura muito mais.',
            'created_at': '2024-01-15 10:30:00',
            'author_id': 'user1',
            'retweet_count': 5,
            'like_count': 23,
            'reply_count': 2,
            'quote_count': 1,
            'lang': 'pt'
        },
        {
            'id': 2,
            'text': 'iPhone muito caro para o que oferece. Não vale o preço.',
            'created_at': '2024-01-15 11:45:00',
            'author_id': 'user2',
            'retweet_count': 2,
            'like_count': 8,
            'reply_count': 5,
            'quote_count': 0,
            'lang': 'pt'
        },
        {
            'id': 3,
            'text': 'Design do iPhone continua lindo, mas esperava mais inovações.',
            'created_at': '2024-01-15 12:15:00',
            'author_id': 'user3',
            'retweet_count': 1,
            'like_count': 12,
            'reply_count': 3,
            'quote_count': 0,
            'lang': 'pt'
        },
        {
            'id': 4,
            'text': 'Nike sempre inovando! Os novos tênis são perfeitos para corrida.',
            'created_at': '2024-01-15 13:20:00',
            'author_id': 'user4',
            'retweet_count': 8,
            'like_count': 45,
            'reply_count': 7,
            'quote_count': 2,
            'lang': 'pt'
        },
        {
            'id': 5,
            'text': 'Nike decepcionou com a qualidade dos materiais. Esperava melhor.',
            'created_at': '2024-01-15 14:10:00',
            'author_id': 'user5',
            'retweet_count': 3,
            'like_count': 15,
            'reply_count': 8,
            'quote_count': 1,
            'lang': 'pt'
        },
        {
            'id': 6,
            'text': 'Produto Nike ok, mas o atendimento ao cliente precisa melhorar.',
            'created_at': '2024-01-15 15:30:00',
            'author_id': 'user6',
            'retweet_count': 1,
            'like_count': 6,
            'reply_count': 4,
            'quote_count': 0,
            'lang': 'pt'
        },
        {
            'id': 7,
            'text': 'McDonald\'s lançou um novo hambúrguer e está delicioso!',
            'created_at': '2024-01-15 16:45:00',
            'author_id': 'user7',
            'retweet_count': 12,
            'like_count': 67,
            'reply_count': 15,
            'quote_count': 5,
            'lang': 'pt'
        },
        {
            'id': 8,
            'text': 'McDonald\'s muito caro para a qualidade da comida.',
            'created_at': '2024-01-15 17:20:00',
            'author_id': 'user8',
            'retweet_count': 4,
            'like_count': 22,
            'reply_count': 12,
            'quote_count': 2,
            'lang': 'pt'
        },
        {
            'id': 9,
            'text': 'McDonald\'s é prático, mas não é a melhor opção de comida.',
            'created_at': '2024-01-15 18:00:00',
            'author_id': 'user9',
            'retweet_count': 2,
            'like_count': 9,
            'reply_count': 6,
            'quote_count': 1,
            'lang': 'pt'
        },
        {
            'id': 10,
            'text': 'Netflix tem os melhores documentários! Recomendo muito.',
            'created_at': '2024-01-15 19:15:00',
            'author_id': 'user10',
            'retweet_count': 6,
            'like_count': 34,
            'reply_count': 8,
            'quote_count': 3,
            'lang': 'pt'
        }
    ]
    
    df = pd.DataFrame(sample_tweets)
    print(f"✅ Dados de exemplo criados com {len(df)} tweets")
    return df
