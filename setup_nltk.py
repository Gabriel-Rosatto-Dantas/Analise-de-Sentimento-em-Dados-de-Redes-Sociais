"""
Script para configurar dados do NLTK
"""
import ssl
import nltk

def setup_nltk():
    """Configura dados necessários do NLTK"""
    try:
        # Configura SSL para evitar problemas de certificado
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
        
        print("📥 Baixando dados do NLTK...")
        
        # Baixa dados necessários
        nltk.download('punkt', quiet=True)
        nltk.download('punkt_tab', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('rslp', quiet=True)
        
        # Tenta baixar VADER, mas continua se falhar
        try:
            nltk.download('vader_lexicon', quiet=True)
        except:
            print("⚠️ VADER lexicon não disponível, usando análise básica")
        
        print("✅ Dados do NLTK configurados com sucesso!")
        
    except Exception as e:
        print(f"⚠️ Erro ao configurar NLTK: {str(e)}")
        print("   O sistema ainda funcionará, mas com funcionalidades limitadas.")

if __name__ == "__main__":
    setup_nltk()
