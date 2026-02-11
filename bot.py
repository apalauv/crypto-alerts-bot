import requests
import time
import os
from datetime import datetime

# Configuración desde variables de entorno
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Configuración de Alertas
ALERTAS = {
    "BTC": {
        "symbol": "BTCUSDT",
        "niveles": {
            "P1": {"precio": 70000, "descripcion": "Menos Agresiva", "activada": True},
            "P2": {"precio": 65000, "descripcion": "", "activada": True},
            "P3": {"precio": 60000, "descripcion": "", "activada": True},
            "P4": {"precio": 55000, "descripcion": "", "activada": True},
            "P5": {"precio": 50000, "descripcion": "Más Agresiva", "activada": True}
        }
    },
    "ETH": {
        "symbol": "ETHUSDT",
        "niveles": {
            "P1": {"precio": 2120, "descripcion": "Menos Agresiva", "activada": True},
            "P2": {"precio": 1800, "descripcion": "", "activada": True},
            "P3": {"precio": 1520, "descripcion": "", "activada": True},
            "P4": {"precio": 1300, "descripcion": "", "activada": True},
            "P5": {"precio": 1100, "descripcion": "Más Agresiva", "activada": True}
        }
    },
    "BNB": {
        "symbol": "BNBUSDT",
        "niveles": {
            "P1": {"precio": 700, "descripcion": "Menos Agresiva", "activada": True},
            "P2": {"precio": 550, "descripcion": "", "activada": True},
            "P3": {"precio": 420, "descripcion": "", "activada": True},
            "P4": {"precio": 340, "descripcion": "", "activada": True},
            "P5": {"precio": 250, "descripcion": "", "activada": True},
            "P6": {"precio": 190, "descripcion": "Más Agresiva", "activada": True}
        }
    },
    "SOL": {
        "symbol": "SOLUSDT",
        "niveles": {
            "P1": {"precio": 62, "descripcion": "Menos Agresiva", "activada": True},
            "P2": {"precio": 52, "descripcion": "", "activada": True},
            "P3": {"precio": 42, "descripcion": "", "activada": True},
            "P4": {"precio": 32, "descripcion": "Más Agresiva", "activada": True}
        }
    },
    "LINK": {
        "symbol": "LINKUSDT",
        "niveles": {
            "P1": {"precio": 10.50, "descripcion": "Menos Agresiva", "activada": True},
            "P2": {"precio": 8.50, "descripcion": "", "activada": True},
            "P3": {"precio": 6.50, "descripcion": "", "activada": True},
            "P4": {"precio": 5.50, "descripcion": "", "activada": True},
            "P5": {"precio": 4.50, "descripcion": "Más Agresiva", "activada": True}
        }
    },
    "SUI": {
        "symbol": "SUIUSDT",
        "niveles": {
            "P1": {"precio": 1.15, "descripcion": "Menos Agresiva", "activada": True},
            "P2": {"precio": 0.90, "descripcion": "", "activada": True},
            "P3": {"precio": 0.58, "descripcion": "", "activada": True},
            "P4": {"precio": 0.40, "descripcion": "Más Agresiva", "activada": True}
        }
    },
    "AAVE": {
        "symbol": "AAVEUSDT",
        "niveles": {
            "P1": {"precio": 131, "descripcion": "Menos Agresiva", "activada": True},
            "P2": {"precio": 92, "descripcion": "", "activada": True},
            "P3": {"precio": 64.04, "descripcion": "Más Agresiva", "activada": True}
        }
    },
    "MSTR": {
        "symbol": "MSTR",
        "niveles": {
            "P1": {"precio": 130, "descripcion": "Menos Agresiva", "activada": True},
            "P2": {"precio": 120, "descripcion": "", "activada": True},
            "P3": {"precio": 110, "descripcion": "", "activada": True},
            "P4": {"precio": 105, "descripcion": "", "activada": True},
            "P5": {"precio": 100, "descripcion": "", "activada": True},
            "P6": {"precio": 80, "descripcion": "Más Agresiva", "activada": True}
        }
    }
}

def obtener_precio_crypto(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return float(response.json()["price"])
    except:
        pass
    return None

def obtener_precio_stock(symbol):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            precio = response.json()["chart"]["result"][0]["meta"]["regularMarketPrice"]
            return float(precio)
    except:
        pass
    return None

def enviar_alerta_telegram(mensaje):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        params = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "HTML"}
        response = requests.post(url, params=params, timeout=10)
        return response.status_code == 200
    except:
        return False

def monitorear_precios():
    print(f"🤖 Bot Iniciado - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    while True:
        try:
            for activo, config in ALERTAS.items():
                symbol = config["symbol"]
                
                if "USDT" in symbol:
                    precio_actual = obtener_precio_crypto(symbol)
                else:
                    precio_actual = obtener_precio_stock(symbol)
                
                if precio_actual is None:
                    continue
                
                print(f"{activo}: ${precio_actual:,.2f}")
                
                for nivel, datos in config["niveles"].items():
                    precio_alerta = datos["precio"]
                    
                    if precio_actual <= precio_alerta and datos["activada"]:
                        emoji = {"P1": "🟢", "P2": "🟢", "P3": "🟡", "P4": "🟠"}.get(nivel, "🔴")
                        descripcion = f"⚠️ <i>{datos['descripcion']}</i>\n" if datos["descripcion"] else ""
                        
                        mensaje = f"{emoji} <b>ALERTA {nivel}</b> - {activo}\n"
                        mensaje += f"💰 Precio: <b>${precio_actual:,.2f}</b>\n"
                        mensaje += f"📍 Nivel: ${precio_alerta:,.2f}\n{descripcion}"
                        mensaje += f"🕐 {datetime.now().strftime('%H:%M:%S')}"
                        
                        if enviar_alerta_telegram(mensaje):
                            ALERTAS[activo]["niveles"][nivel]["activada"] = False
            
            print(f"\n⏳ Próxima verificación en 60 segundos...\n")
            time.sleep(60)
            
        except KeyboardInterrupt:
            print("\n🛑 Bot detenido")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("ERROR: Configurar TELEGRAM_TOKEN y CHAT_ID")
    else:
        monitorear_precios()
