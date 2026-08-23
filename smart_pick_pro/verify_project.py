import sys
import py_compile
from pathlib import Path

project_dir = Path(__file__).parent

files_to_check = [
    "config.py",
    "auth.py",
    "api_client.py",
    "analytics.py",
    "progol.py",
    "app.py"
]

print("=== VERIFICACIÓN DE SINTAXIS DE ARCHIVOS DE PROYECTO ===")
errors = 0
for filename in files_to_check:
    filepath = project_dir / filename
    try:
        py_compile.compile(str(filepath), doraise=True)
        print(f"✅ {filename}: Sintaxis Correcta")
    except Exception as e:
        print(f"❌ {filename}: ERROR de sintaxis -> {e}")
        errors += 1

print("\n=== VERIFICACIÓN DE MÓDULOS DEL SISTEMA ===")
sys.path.insert(0, str(project_dir))

try:
    import auth
    print("✅ auth.py importado correctamente.")
    exito, role = auth.verificar_credenciales("admin", "SmartVIP2026!")
    print(f"✅ Verificación de credenciales admin iniciales: exito={exito}, role='{role}'")
except Exception as e:
    print(f"❌ Error en prueba de auth.py: {e}")
    errors += 1

try:
    import analytics
    print("✅ analytics.py importado correctamente.")
    res_p = analytics.calcular_matriz_poisson("45%", "30%", "25%")
    print(f"✅ Matriz de Poisson probada: Home={res_p['p_home_win']}%, Over1.5={res_p['p_over_15']}%")
    val_b, ev = analytics.calcular_valor("45%", 2.40)
    print(f"✅ Calculadora de Valor EV probada: EsValor={val_b}, EV={ev}%")
except Exception as e:
    print(f"❌ Error en prueba de analytics.py: {e}")
    errors += 1

try:
    import progol
    print("✅ progol.py importado correctamente.")
    q = progol.generar_quiniela_progol(4, 3)
    print(f"✅ Generador de Quiniela probado: {len(q)} casilleros generados.")
except Exception as e:
    print(f"❌ Error en prueba de progol.py: {e}")
    errors += 1

if errors == 0:
    print("\n🎉🎉🎉 ¡TODAS LAS PRUEBAS AUTOMATIZADAS PASARON EXITOSAMENTE! 🎉🎉🎉")
else:
    print(f"\n⚠️ Se encontraron {errors} errores durante la verificación.")
