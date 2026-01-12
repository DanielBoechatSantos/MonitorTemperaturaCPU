import os
import time
import clr  # Pacote pythonnet

# 1. Localiza a DLL
dll_path = os.path.join(os.path.dirname(__file__), "OpenHardwareMonitorLib.dll")

if not os.path.exists(dll_path):
    print(f"ERRO: O arquivo OpenHardwareMonitorLib.dll não foi encontrado em: {dll_path}")
else:
    try:
        # 2. Carrega a biblioteca .NET
        clr.AddReference(dll_path)
        from OpenHardwareMonitor.Hardware import Computer

        # 3. Inicializa o objeto Computer
        pc = Computer()
        pc.CPUEnabled = True  # Habilita monitoramento do processador
        pc.Open()

        print("=== MONITOR DE TEMPERATURA REAL (OHM) ===")
        print("Pressione Ctrl+C para encerrar\n")

        while True:
            for hardware in pc.Hardware:
                hardware.Update()  # Solicita novos dados ao driver
                
                # Procura por sensores dentro de cada peça de hardware
                for sensor in hardware.Sensors:
                    if str(sensor.SensorType) == 'Temperature':
                        # Exibe o nome do núcleo e o valor atual
                        print(f"[{hardware.Name}] {sensor.Name}: {sensor.Value:.1f}°C")
            
            time.sleep(1)
            print("-" * 35)

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        print("\nIMPORTANTE: Verifique se você abriu o VS Code como ADMINISTRADOR.")
    finally:
        try:
            pc.Close()
        except:
            pass