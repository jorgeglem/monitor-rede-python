import subprocess
import platform
import time
import os
from datetime import datetime

def testar_ping(host):
    parametro = '-n' if platform.system().lower() == 'windows' else '-c'
    comando = ['ping', parametro, '1', host]
    try:
        res = subprocess.run(comando, stdout=subprocess.PIPE, text=True, timeout=2)
        if res.returncode == 0:
            for chave in ["tempo=", "time=", "tempo<", "time<"]:
                if chave in res.stdout.lower():
                    return float(res.stdout.lower().split(chave)[1].split("ms")[0].strip())
        return None
    except:
        return None

def exibir_barra_status(ms):
    """Cria uma barra visual: [#####     ] 50ms"""
    if ms is None: return "[OFFLINE] 🔴"
    
    # Define a 'saúde' da conexão
    limite = 200 # Consideramos 200ms como conexão lenta
    blocos = int((ms / limite) * 10)
    if blocos > 10: blocos = 10
    
    cor = "🟢" if ms < 80 else "🟡" if ms < 150 else "🔴"
    barra = "█" * blocos + "-" * (10 - blocos)
    return f"[{barra}] {ms}ms {cor}"

if __name__ == "__main__":
    alvo = "8.8.8.8" # DNS do Google
    historico = []
    
    print(f"--- MONITOR DE REDE PROFISSIONAL ---")
    print(f"Monitorando {alvo}... Pressione Ctrl+C para parar.\n")

    try:
        while True:
            ms = testar_ping(alvo)
            agora = datetime.now().strftime('%H:%M:%S')
            status_visual = exibir_barra_status(ms)
            
            if ms:
                historico.append(ms)
                # Mantém apenas os últimos 10 testes para a média
                if len(historico) > 10: historico.pop(0)
                media = sum(historico) / len(historico)
                
                print(f"[{agora}] {status_visual} | Média(10p): {media:.1f}ms", end='\r')
            else:
                print(f"[{agora}] {status_visual} | ALERTA: FALHA DE CONEXÃO!", end='\r')
            
            time.sleep(2) # Intervalo entre os testes
            
    except KeyboardInterrupt:
        print(f"\n\n--- Monitoramento Encerrado ---")
        if historico:
            print(f"Latência Máxima: {max(historico)}ms")
            print(f"Latência Mínima: {min(historico)}ms")