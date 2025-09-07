"""
Arquivo de configuração do projeto
"""
import os

# Configurações da API do Twitter
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN', '')

# Configurações de análise
DEFAULT_MAX_RESULTS = 100
DEFAULT_DAYS_BACK = 7
DEFAULT_LANGUAGE = 'portuguese'

# Configurações de pré-processamento
REMOVE_STOPWORDS = True
APPLY_STEMMING = False
MIN_TEXT_LENGTH = 3

# Configurações de visualização
FIGURE_SIZE = (12, 8)
DPI = 300
CHART_STYLE = 'seaborn-v0_8'

# Configurações de saída
OUTPUT_DIR = 'output'
REPORT_FORMAT = 'html'

# Palavras personalizadas para análise de sentimento
CUSTOM_POSITIVE_WORDS = {
    'bom', 'boa', 'ótimo', 'ótima', 'excelente', 'fantástico', 'fantástica',
    'incrível', 'maravilhoso', 'maravilhosa', 'perfeito', 'perfeita',
    'adoro', 'amo', 'gosto', 'recomendo', 'satisfeito', 'satisfeita',
    'feliz', 'alegre', 'contente', 'impressionado', 'impressionada',
    'surpreendente', 'genial', 'brilhante', 'espetacular', 'magnífico',
    'delicioso', 'deliciosa', 'saboroso', 'saborosa', 'gostoso', 'gostosa',
    'top', 'show', 'demais', 'sensacional', 'incrível', 'fantástico'
}

CUSTOM_NEGATIVE_WORDS = {
    'ruim', 'péssimo', 'péssima', 'horrível', 'terrível', 'odioso',
    'detesto', 'odeio', 'desgosto', 'desapontado', 'desapontada',
    'frustrado', 'frustrada', 'irritado', 'irritada', 'bravo', 'brava',
    'furioso', 'furiosa', 'chateado', 'chateada', 'triste', 'deprimido',
    'deprimida', 'angustiado', 'angustiada', 'preocupado', 'preocupada',
    'nervoso', 'nervosa', 'ansioso', 'ansiosa', 'medo', 'assustado',
    'assustada', 'decepcionado', 'decepcionada', 'chocado', 'chocada',
    'lixo', 'porcaria', 'merda', 'droga', 'inferno', 'desastre'
}

# Configurações de cores para visualização
SENTIMENT_COLORS = {
    'positivo': '#2E8B57',  # Verde
    'negativo': '#DC143C',  # Vermelho
    'neutro': '#4682B4'     # Azul
}
