# Fesing
Program for reading out data from Fesing batteries. Tested on FCIFP48100A with Fesing logo

## Protokol
Program se ptá dvěma způsoby, ke každému je jedna odpověď. Je to znásilněný ModBus

### Krátký dotaz
```
> 01 1d 00 00 00 00 ed c8
< 01 1d 00 22 5d 5d 01 f5 01 01 f5 01 75 30 00 02 01 00 02 01 0d 0a 01 0d 08 01 02 bf 01 02 bd 01 00 00 08 27 eb 64 70 b6
```

Dekódování odpovědi
 - 01 1d - zopakování dotazu
 - 00 22 - délka odpovědi v bajtech
 - 5d - max SOC
 - 5d - min SOC
 - 01 f5 01 - max TV, v dV, big endian
 - 01 f5 01 - min TV, v dV, big endian
 - 75 30 - proud v dA?
 - 00 02 01 - rozbalancovanost?
 - 00 02 01 - rodíl teplot?
 - 0d 0a 01 - napětí nejnabitějšího článku
 - 0d 08 01 - napětí nejvybitějšího článku
 - 02 bf 01 - teplota nejchladnějšího článku?
 - 02 bd 01 - teplota nejteplejšího článku?
 - 00 00 08 27 eb 64 
 - 70 b6 - checksum


### Dlouhý dotaz

```
> 01 18 00 00 00 01 e0 08
< 01 18 00 7e 5d 03 a2 01 f5 75 30 2b 64 30 8e 00 63 ff ff ff ff 00 08 34 00 10 01 10 08 04 00 01 01 00 64 00 04 00 02 00 02 0d 09 02 be 0d 0a 01 0d 08 0f 02 bf 02 bd 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 bd 02 be 02 be 02 bf 02 d6 03 0e 0d 0a 0d 0a 0d 0a 0d 0a 0d 0a 0d 0a 0d 0a 0d 0a 0d 0a 0d 0a 0d 0a 0d 0a 0d 0a 0d 0a 0d 08 00 00 ff f4 03 e8 03 e8 00 00 00 62 09
```

Dekódování odpovědi
 - 01 18 - zopakování příkazu
 - 00 7e - počet bajtů odpovědi
 - 5d - SOC v %
 - 03 a2 - rate capacity v dAh
 - 01 f5 - napětí baterie v dV, big endian
 - 75 30 - proud v dA
 - 2b 64 30 8e 
 - 00 63 
 - ff ff ff ff 
 - 00 08 34 00 10 01 10 08 
 - 04 - BMS Work status? (0x04 standby, 0x02 charging)
 - 00 - Relay1Status?
 - 01 - Relay2Status?
 - 01 - Relay3Status?
 - 00 - Relay4Status?
 - 64 - SOH?
 - 00 04 - Cycles?
 - 00 02 - VoltDiff?
 - 00 02 - TempDiff?
 - 0d 09 - průměrné napětí článku
 - 02 be - průměrná teplota 
 - 0d 0a 01 - napětí nejnabitějšího článku a který to je
 - 0d 08 0f - napětí nejvybitějšího článku a který to je
 - 02 bf - teplota nejteplejšího článku
 - 02 bd - teplota nejstudenějšího článku
 - 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 - Alarmy 
 - 02 bd - teplota článku 1 v dC + 500
 - 02 be - teplota článků 2
 - 02 be - teplota článků 3
 - 02 bf - teplota článků 4
 - 02 d6 - teplota MOS
 - 03 0e - teplota TA
 - 0d 0a - napětí 1. článku, v mV, int16 big endian 
 - 0d 0a - napětí 2. článku
 - 0d 0a  - napětí 3. článku
 - 0d 0a  - napětí 4. článku
 - 0d 0a  - napětí 5. článku
 - 0d 0a  - napětí 6. článku
 - 0d 0a  - napětí 7. článku
 - 0d 0a - napětí 8. článku
 - 0d 0a  - napětí 9. článku
 - 0d 0a  - napětí 10. článku
 - 0d 0a  - napětí 11. článku
 - 0d 0a  - napětí 12. článku
 - 0d 0a  - napětí 13. článku
 - 0d 0a  - napětí 14. článku
 - 0d 08  - napětí 15. článku
 - 00 00 - napětí 16. článku 
 - ff f4 - current AD value (asi proud v ADU)
 - 03 e8 - Max charge current? 
 - 03 e8 - Max discharge current?
 - 00 00 00 
 - 62 09 - checksum

