import solverCan
import math

y = [24.0, 26.5858, 31.2679, 38.0, 46.7639, 57.5505, 70.3542, 85.1716, 102.0, 120.8377]

# Parçalı
r1 = solverCan.irrational(y)
print("=== irrational (parcali) ===")
print(r1['equation'])
solverCan.table(y, r1['compute'])

# Tek denklem
r2 = solverCan.irrationalOneEq(y)
print("\n=== irrationalOneEq (tek denklem) ===")
print(r2['equation'])
solverCan.table(y, r2['compute'])

# Karşılaştırma
print("\nGercek vs Tahmin (x=90):")
gercek = 90**2 + 24 - math.sqrt(90)
print(f"  irrational:      {r1['compute'](90):>10.4f}  sapma=%{abs(r1['compute'](90)-gercek)/gercek*100:.4f}")
print(f"  irrationalOneEq: {r2['compute'](90):>10.4f}  sapma=%{abs(r2['compute'](90)-gercek)/gercek*100:.4f}")
print(f"  gercek:          {gercek:>10.4f}")