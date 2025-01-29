import yfinance as yf
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, Dense, Flatten
import time

# Fonction pour récupérer les prix historiques
def get_historical_prices(symbol='AAPL', period='6mo', interval='1d'):
    data = yf.download(symbol, period=period, interval=interval)
    return data['Close'].values  # Retourne les prix de clôture

# Fonction pour récupérer le prix actuel en temps réel
def get_live_price(symbol='AAPL'):
    ticker = yf.Ticker(symbol)
    try:
        price = ticker.history(period="1d", interval="1m")['Close'].iloc[-1]
        return float(price)
    except Exception as e:
        print(f"Erreur lors de la récupération du prix en temps réel : {e}")
        return None

# Fonction pour préparer les données
def prepare_data(data, lookback=60):
    X, y = [], []
    for i in range(len(data) - lookback - 1):
        X_seq = data[i:i + lookback]
        y_value = data[i + lookback]  # Le prix suivant à prédire
        X.append(X_seq)
        y.append(y_value)
    return np.array(X), np.array(y)

# Construire le modèle Conv1D
def create_model(input_shape):
    model = Sequential([
        LSTM(128, return_sequences=True, input_shape=(60, 1)),
        Dropout(0.2),
        LSTM(64, return_sequences=False),
        Dropout(0.2),
        Dense(32, activation='relu'),
        Dense(1, activation='linear')
    ])
    model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
    return model

# Simulation de trading en temps réel
def simulate_live_trading(model, symbol, initial_balance=1000, lookback=60):
    balance = initial_balance
    position = 0
    historical_prices = get_historical_prices(symbol=symbol, period='6mo', interval='1d')
    prices = historical_prices.tolist()  # Convertir en liste pour ajouter de nouvelles valeurs

    print("\n-- Début de la simulation de trading en temps réel ---")
    while True:
        try:
            live_price = get_live_price(symbol)

            if live_price is not None:
                prices.append(live_price)  # Ajouter le prix en direct à la liste

            # Vérifier si assez de données pour une prédiction
            if len(prices) >= lookback:
                prices[-1] = [prices[-1]]
                recent_data = np.array(prices[-lookback:]).reshape(1, lookback, 1)
                predicted_price = model.predict(recent_data/100000, verbose=0)[0][0]*100000

                print(f"Prix actuel : {live_price:.2f}, Prédiction : {predicted_price:.2f}")

                # Décisions d'achat ou de vente
                if predicted_price > live_price and balance > 0:  # Acheter
                    position = balance / live_price
                    print(f"Achat à {live_price:.2f}. Position : {position:.4f} unités")
                    balance = 0
                elif predicted_price < live_price and position > 0:  # Vendre
                    balance += position * live_price
                    print(f"Vente à {live_price:.2f}. Nouveau solde : {balance:.2f}")
                    position = 0

            # Pause avant la prochaine mise à jour
            time.sleep(60)  # Met à jour toutes les minutes
        except KeyboardInterrupt:
            # Calcul du solde final si l'utilisateur interrompt la simulation
            if position > 0:
                balance += position * live_price
                print(f"\nVente finale à {live_price:.2f}. Solde final : {balance:.2f}")
            print("\n-- Fin de la simulation de trading en temps réel ---")
            break
        except Exception as e:
            print(f"Erreur : {e}")
            time.sleep(60)  # Attente avant une nouvelle tentative

# Main
def main():
    symbol = 'BTC-EUR'
    lookback = 60

    print(f"Chargement des données pour {symbol}...")
    prices = get_historical_prices(symbol=symbol)
    X, y = prepare_data(prices, lookback=lookback)

    print(f"Nombre d'exemples générés : {len(X)}")
    if len(X) == 0:
        print("Pas assez de données pour entraîner le modèle.")
        return

    X = X.reshape(X.shape[0], X.shape[1], 1)

    model = create_model(input_shape=(X.shape[1], X.shape[2]))
    print("Entraînement du modèle...")
    model.fit(X/100000, y/100000, epochs=25, batch_size=32, verbose=1)
    model.summary()

    simulate_live_trading(model, symbol, initial_balance=1000, lookback=lookback)

if __name__ == "__main__":
    main()
