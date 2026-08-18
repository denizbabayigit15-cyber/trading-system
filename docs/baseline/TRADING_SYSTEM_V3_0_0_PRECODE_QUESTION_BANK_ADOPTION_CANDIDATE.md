# TRADING SYSTEM — V3.0.0 PRE-CODE QUESTION BANK ADOPTION CANDIDATE

**Adoption change request:** `CR-V3.0.0-PRECODE-001`  
**Status:** `REVIEW CANDIDATE / 900 REQUIREMENTS / NOT EXECUTED`  
**Rule:** The source questions below are retained. Their authoritative requirement, owner, policy, test and fail-action mappings are in `contracts/questions/question_registry.json`. Runtime PASS count is zero.

---
# TRADING SYSTEM — V2.3.1 ADAPTIVE SURVIVAL MASTER QUESTION BANK

**Durum:** `CHANGE_REQUEST_CANDIDATE / NON-NORMATIVE / NOT_EXECUTED`
**Kaynak çekirdek:** Master Implementation Contract V2.2.5 + Developer Constitution V1.1 + Implementation Readiness Matrix V2.2.5
**Aday değişiklik:** `CR-V2.3.1-ASQ-001`
**Toplam soru:** 900 (237 mevcut zorunlu + 663 önerilen genişletme)
**Araştırma kesim tarihi:** 2026-08-18

## 0. Kullanım ve bağlayıcılık notu
Bu dosya iki katmanlıdır. İlk 237 soru Master Contract'ın mevcut bağlayıcı çekirdeğidir. Sonraki 663 soru dış araştırma, gerçek piyasa kontrolleri ve uzun dönemli sistem tasarımı temelinde önerilen genişletme setidir. Önerilen sorular, Master Contract'a sessizce eklenmiş yeni üretim kuralları değildir; uygulanacak her maddi kural için `STOP → CHANGE REQUEST → IMPACT ANALYSIS → CONTRACT VERSION → TEST → APPROVAL → IMPLEMENT → RECERTIFICATION` süreci gerekir.

Üretim-kritik sorular için mevcut sözleşmenin temel cevap durumları `PASS / FAIL / UNKNOWN / NOT_APPLICABLE` olarak korunmalıdır. `UNKNOWN`, üretim-kritik kapsamda FAIL olarak değerlendirilir.

Bu bankada soru sayısı tek başına güvenlik veya kârlılık kanıtı değildir. Bir soru yalnızca tekil kimlik, uygulanabilir kapsam, bağlayıcı sözleşme/politika, çalıştırılmış test, değişmez kanıt ve açık fail action ile denetlenebilir hale gelir. Bu dosyada yeni soruların mevcut cevabı varsayılan olarak `UNKNOWN / NOT_EXECUTED`'dır; hiçbir yeni soru yalnızca yazıldığı için `PASS` sayılamaz.

Rakip algoritma veya piyasa katılımcısı niyeti doğrudan gözlenemiyorsa sonuç `OBSERVED` olarak sunulamaz. Böyle iddialar `DERIVED`, `INFERRED` veya `UNKNOWN` sınıfında; belirsizlik, alternatif açıklamalar ve yanlış-pozitif maliyetiyle tutulur. Sistem, gözlenemeyen bir rakip hakkında kesin bilgi varmış gibi işlem yetkisi üretemez.

Varlık sınıfına ve yargı alanına özel sorular yalnızca bağlanmış `MarketProfile`, broker/venue sözleşmesi ve uygulanabilir hukuk envanteriyle etkinleşir. Uygulanmayan soru ancak kanıtlı `NOT_APPLICABLE` olabilir; sessizce atlanamaz.

## 1. Soru formatı
| Alan | Açıklama |
|---|---|
| Soru ID | Makine tarafından izlenecek benzersiz kimlik |
| Alan | Soru ailesi / risk alanı |
| Soru | Sistem tarafından cevaplanması gereken denetim sorusu |
| Statü | Mevcut zorunlu çekirdek veya önerilen genişletme |
| Kritikliği | `PRODUCTION_BLOCKING / CONDITIONAL_BLOCKING / ADVISORY` |
| Bilgi sınıfı | `OBSERVED / DERIVED / INFERRED / VENDOR_MODEL / UNKNOWN / UNAVAILABLE` |
| Kanıt | `EVIDENCE_ID`, zaman aralığı, kapsam hash'i ve üretici |
| Bağ | `CONTRACT_ID / POLICY_ID / TEST_ID / SCENARIO_ID` |
| Başarısızlık eylemi | Bloklama, risk azaltma, izolasyon, geri alma veya change request |

---
## 2. Mevcut V2.2.5 zorunlu çekirdek — 237 soru

Bu 237 soru bağlayıcı Master Contract'tan semantik kayma olmaması için **kanonik İngilizce ifadeleriyle** aynen korunmuştur. Türkçe açıklama üretim kuralı sayılmaz; çelişkide aşağıdaki kanonik ifade ve V2.2.5 Master Contract geçerlidir.

### DATA SUFFICIENCY — DS

1. `DS-001` Does the strategy have an explicit minimum data tier?
2. `DS-002` Does every required feature map to its raw source data?
3. `DS-003` Is the required source available at decision time?
4. `DS-004` Is the required source quality above policy?
5. `DS-005` Is data coverage above policy?
6. `DS-006` Is data missingness below policy?
7. `DS-007` Is staleness below policy?
8. `DS-008` Is sequence-gap rate below policy?
9. `DS-009` Is out-of-order rate below policy?
10. `DS-010` Is clock error below policy?
11. `DS-011` Is every strategy-specific L1/L2/L3/MBO dependency explicitly declared?
12. `DS-012` Is every options-data dependency explicitly declared?
13. `DS-013` Is every futures-data dependency explicitly declared?
14. `DS-014` Is every macro vintage dependency explicitly declared?
15. `DS-015` Is every fundamental vintage dependency explicitly declared?
16. `DS-016` Does fallback preserve required data quality?
17. `DS-017` Does missing critical data veto the strategy?
18. `DS-018` Does proxy substitution require explicit certification?
19. `DS-019` Is the fallback activation rate measured?
20. `DS-020` Is the strategy's data sufficiency report versioned?

### TEMPORAL TRUTH — TT

21. `TT-001` Was every decision-bearing input actually available before decision time?
22. `TT-002` Is first-available time distinct from persistence time?
23. `TT-003` Is revision history preserved?
24. `TT-004` Is historical replay using the version known then?
25. `TT-005` Is macro vintage preserved?
26. `TT-006` Is fundamental vintage preserved?
27. `TT-007` Are news first-seen and publication timestamps distinct?
28. `TT-008` Are corrections and retractions versioned?
29. `TT-009` Are corporate actions point-in-time correct?
30. `TT-010` Is historical universe reconstruction deterministic?

### ORDER BOOK — OB

31. `OB-001` Is the book reconstructed deterministically?
32. `OB-002` Are sequence gaps detected?
33. `OB-003` Are duplicate events detected?
34. `OB-004` Are out-of-order events handled?
35. `OB-005` Are book resets detected?
36. `OB-006` Are corrections handled?
37. `OB-007` Are trade/book timestamps reconciled?
38. `OB-008` Is queue state explicitly classified as observed or inferred?
39. `OB-009` Does incomplete book state disable dependent strategies?
40. `OB-010` Is reconstruction recovery independently certified?

### LABEL — LB

41. `LB-001` Is the target explicitly defined?
42. `LB-002` Is horizon explicitly defined?
43. `LB-003` Is entry price rule explicit?
44. `LB-004` Is exit rule explicit?
45. `LB-005` Is stop rule explicit?
46. `LB-006` Is timeout rule explicit?
47. `LB-007` Is partial fill handled?
48. `LB-008` Is partial exit handled?
49. `LB-009` Is same-bar stop/target ambiguity handled conservatively?
50. `LB-010` Is label construction cost-aware where required?
51. `LB-011` Is overlapping observation dependence handled?
52. `LB-012` Is censoring handled?

### ALPHA — AL

53. `AL-001` Does every production alpha have a hypothesis?
54. `AL-002` Does it have an economic mechanism?
55. `AL-003` Is expected direction documented?
56. `AL-004` Is target label linked?
57. `AL-005` Is required data linked?
58. `AL-006` Is expected regime linked?
59. `AL-007` Is excluded regime linked?
60. `AL-008` Is gross expectancy measured?
61. `AL-009` Is net expectancy measured?
62. `AL-010` Is uncertainty measured?
63. `AL-011` Is half-life measured?
64. `AL-012` Is capacity measured?
65. `AL-013` Is dependency measured?
66. `AL-014` Is stability measured?
67. `AL-015` Is decay measured?
68. `AL-016` Is the alpha validated out-of-sample?
69. `AL-017` Is the alpha stable across required regimes?
70. `AL-018` Does reverse-direction testing contradict the claimed mechanism?
71. `AL-019` Does removing the largest winner destroy the result?
72. `AL-020` Does the edge survive realistic execution?

### PROBABILITY — PB

73. `PB-001` Is probability distinct from confidence?
74. `PB-002` Is probability calibrated?
75. `PB-003` Is Brier score within policy?
76. `PB-004` Is calibration error within policy?
77. `PB-005` Is regime calibration within policy?
78. `PB-006` Is minimum effective sample met?
79. `PB-007` Are confidence intervals acceptable?
80. `PB-008` Is probability drift monitored?
81. `PB-009` Does calibration failure block production?

### EXPECTANCY / COST — EV

82. `EV-001` Is gross EV calculated?
83. `EV-002` Is commission included?
84. `EV-003` Is spread cost included?
85. `EV-004` Is slippage included?
86. `EV-005` Is market impact included?
87. `EV-006` Is funding included where applicable?
88. `EV-007` Is borrow included where applicable?
89. `EV-008` Is financing included where applicable?
90. `EV-009` Is roll/holding cost included where applicable?
91. `EV-010` Is adverse selection included where applicable?
92. `EV-011` Is latency cost modeled where material?
93. `EV-012` Is EV uncertainty measured?
94. `EV-013` Is EV lower bound calculated?
95. `EV-014` Does lower-bound EV exceed the edge floor?
96. `EV-015` Does cost uncertainty remain below the certified edge buffer?

### EXECUTION — EX

97. `EX-001` Is order submission latency modeled?
98. `EX-002` Is acknowledgement latency modeled?
99. `EX-003` Is queue position modeled when required?
100. `EX-004` Is limit-fill probability modeled?
101. `EX-005` Are partial fills modeled?
102. `EX-006` Are cancel/replace delays modeled?
103. `EX-007` Is adverse selection modeled?
104. `EX-008` Are order rejections modeled?
105. `EX-009` Are spread expansions modeled?
106. `EX-010` Are liquidity collapses modeled?
107. `EX-011` Are gap-through-stop conditions modeled?
108. `EX-012` Is fill realism calibrated to shadow/paper/live evidence?
109. `EX-013` Is expected-vs-realized slippage monitored?
110. `EX-014` Is expected-vs-realized fill probability monitored?
111. `EX-015` Is expected-vs-realized impact monitored?
112. `EX-016` Does execution stop when edge half-life is exceeded?

### RISK — RK

113. `RK-001` Is risk deterministic?
114. `RK-002` Is trade risk below strategy risk?
115. `RK-003` Is strategy risk below factor risk?
116. `RK-004` Is factor risk below asset risk?
117. `RK-005` Is asset risk below portfolio risk?
118. `RK-006` Is drawdown response active?
119. `RK-007` Is risk-of-ruin within policy?
120. `RK-008` Is expected shortfall within policy?
121. `RK-009` Is gap risk modeled?
122. `RK-010` Is spread expansion modeled?
123. `RK-011` Is liquidity-adjusted loss modeled?
124. `RK-012` Is forced liquidation modeled?
125. `RK-013` Does positive EV fail to override unacceptable tail risk?

### PORTFOLIO / CAPITAL — PC

126. `PC-001` Is the trade evaluated against current portfolio state?
127. `PC-002` Is marginal portfolio risk measured?
128. `PC-003` Is factor concentration measured?
129. `PC-004` Is alpha-factor concentration measured?
130. `PC-005` Is venue concentration measured?
131. `PC-006` Is event concentration measured?
132. `PC-007` Is model concentration measured?
133. `PC-008` Is correlation regime-aware where required?
134. `PC-009` Are tail dependencies measured?
135. `PC-010` Is capital competition deterministic?
136. `PC-011` Is capacity respected?
137. `PC-012` Is capital-size dependence of EV measured?

### EXIT / POSITION — PX

138. `PX-001` Is hard-stop behavior defined?
139. `PX-002` Is thesis invalidation defined?
140. `PX-003` Is time-stop defined?
141. `PX-004` Is target behavior defined?
142. `PX-005` Is partial exit behavior defined?
143. `PX-006` Is emergency exit defined?
144. `PX-007` Is exit capacity validated?
145. `PX-008` Is gap risk handled?
146. `PX-009` Is event-risk exit handled?
147. `PX-010` Is regime invalidation handled?

### REGIME / ADAPTATION — RG

148. `RG-001` Is current regime classified?
149. `RG-002` Is regime confidence measured?
150. `RG-003` Is transition state measurable?
151. `RG-004` Is transition confirmation defined?
152. `RG-005` Is unknown regime handled safely?
153. `RG-006` Is strategy-specific transition response defined?
154. `RG-007` Is regime drift monitored?
155. `RG-008` Is new-regime discovery possible?
156. `RG-009` Is regime detection latency within strategy half-life?

### DECAY / DRIFT — DR

157. `DR-001` Is rolling expectancy monitored?
158. `DR-002` Is lower-bound EV monitored?
159. `DR-003` Is probability calibration drift monitored?
160. `DR-004` Is feature drift monitored?
161. `DR-005` Is data-quality drift monitored?
162. `DR-006` Is execution drift monitored?
163. `DR-007` Is cost drift monitored?
164. `DR-008` Is latency drift monitored?
165. `DR-009` Is capacity drift monitored?
166. `DR-010` Are state transitions thresholded?
167. `DR-011` Does strategy degradation block or reduce trading?

### CAPACITY — CP

168. `CP-001` Is capacity measured?
169. `CP-002` Is capacity a function of liquidity?
170. `CP-003` Is impact size-dependent?
171. `CP-004` Is fill probability size-dependent?
172. `CP-005` Is exit liquidity size-dependent?
173. `CP-006` Is stress liquidity included?
174. `CP-007` Is a capital-to-edge curve produced?
175. `CP-008` Is production allocation inside certified capacity?

### RESEARCH / OVERFITTING — RS

176. `RS-001` Is every trial registered?
177. `RS-002` Are failed trials recorded?
178. `RS-003` Is trial count tracked?
179. `RS-004` Is selection rule explicit?
180. `RS-005` Is stopping rule explicit?
181. `RS-006` Is search-space exposure measured?
182. `RS-007` Is validation reuse tracked?
183. `RS-008` Is test-set exposure controlled?
184. `RS-009` Are multiple-testing risks evaluated?
185. `RS-010` Is PBO evaluated where applicable?
186. `RS-011` Is DSR evaluated where applicable?
187. `RS-012` Is parameter instability evaluated?
188. `RS-013` Is regime robustness evaluated?
189. `RS-014` Is stationarity evaluated where relevant?
190. `RS-015` Is serial dependence handled?

### REPLAY / CERTIFICATION — RP

191. `RP-001` Is replay deterministic?
192. `RP-002` Does replay reproduce decision-time data availability?
193. `RP-003` Does replay reproduce source state?
194. `RP-004` Does replay reproduce risk policy?
195. `RP-005` Does replay reproduce capital state?
196. `RP-006` Does replay reproduce execution assumptions?
197. `RP-007` Does replay reproduce cost assumptions?
198. `RP-008` Does replay reproduce strategy version?
199. `RP-009` Does replay reproduce model/feature versions?
200. `RP-010` Does replay preserve decision lineage?

### FAILURE / RECOVERY — FR

201. `FR-001` Does stale data enter safe mode?
202. `FR-002` Does sequence failure block dependent trades?
203. `FR-003` Does clock failure block critical decisions?
204. `FR-004` Does broker/internal mismatch block new orders?
205. `FR-005` Does unknown position state block new orders?
206. `FR-006` Does database loss preserve safe authority?
207. `FR-007` Does event-bus failure preserve safe authority?
208. `FR-008` Does process restart require reconciliation?
209. `FR-009` Does recovery require risk revalidation?
210. `FR-010` Does restore keep trading disabled until certification?

### LEARNING — LG

211. `LG-001` Can learning write production policy directly? (Must be NO.)
212. `LG-002` Is feedback evidence-linked?
213. `LG-003` Is every learning proposal versioned?
214. `LG-004` Is every candidate validated before promotion?
215. `LG-005` Is champion/challenger state explicit?
216. `LG-006` Is rollback available?
217. `LG-007` Are negative outcomes retained?
218. `LG-008` Can a failed challenger displace a champion? (Must be NO.)

### SECURITY / AUTHORITY — SC

219. `SC-001` Can AI alter risk ceilings? (Must be NO.)
220. `SC-002` Can AI alter kill switches? (Must be NO.)
221. `SC-003` Can research alter production directly? (Must be NO.)
222. `SC-004` Can notification failure create trading authority? (Must be NO.)
223. `SC-005` Is release state versioned?
224. `SC-006` Are secrets separated by environment?
225. `SC-007` Is high-impact control capability-scoped?

### FUTURE MARKET — FM

226. `FM-001` Can the system detect feature-distribution change?
227. `FM-002` Can it detect target-distribution change?
228. `FM-003` Can it detect market-structure change?
229. `FM-004` Can it detect liquidity-structure change?
230. `FM-005` Can it detect execution-latency change?
231. `FM-006` Can it detect cost-model change?
232. `FM-007` Can it detect strategy crowding/decay?
233. `FM-008` Can it detect vendor methodology change?
234. `FM-009` Can it discover previously unseen regimes?
235. `FM-010` Can it isolate an affected strategy without disabling unrelated certified strategies?
236. `FM-011` Does adaptation require governed research/certification?
237. `FM-012` Can the system return to the last certified champion?

---

## 3. V2.3 Adaptive Survival genişletmesi — 450 yeni soru
Bu bölüm, mevcut 237 sorunun üzerine uzun dönemli adaptasyon, piyasa ekolojisi, rakip algoritmalar, bilinmeyen durumlar, online öğrenme, execution ekolojisi, strateji yaşam döngüsü, sermaye hayatta kalması ve meta-overfitting gibi alanları ekler.

### Piyasa Ekolojisi ve Rakip Davranışı
| ID | Soru | Statü |
|---|---|---|
| `ME-001` | Sistemin alpha'sının başka piyasa katılımcıları tarafından keşfedildiğini tespit edebiliyor mu? | YENİ / ÖNERİLEN |
| `ME-002` | Edge yaygınlaştığında beklenen getiri erozyonu ölçülüyor mu? | YENİ / ÖNERİLEN |
| `ME-003` | Aynı mekanizmayı kullanan stratejilerin toplam yoğunluğu ölçülüyor mu? | YENİ / ÖNERİLEN |
| `ME-004` | Strateji crowding ile likidite crowding birbirinden ayrıştırılıyor mu? | YENİ / ÖNERİLEN |
| `ME-005` | Rakip stratejilerdeki değişim bizim execution maliyetimizi etkiliyor mu? | YENİ / ÖNERİLEN |
| `ME-006` | Alpha yarı ömrünün piyasa katılımcısı sayısına bağlı değişimi ölçülüyor mu? | YENİ / ÖNERİLEN |
| `ME-007` | Stratejinin başarısının daha fazla rakip çekerek kendi edge'ini zayıflatabileceği modelleniyor mu? | YENİ / ÖNERİLEN |
| `ME-008` | Piyasadaki algo yoğunluğu artınca edge'in istatistiksel yapısı yeniden ölçülüyor mu? | YENİ / ÖNERİLEN |
| `ME-009` | Piyasa ekolojisinin değişmesiyle aynı sinyalin farklı fiyat etkisi oluşturduğu tespit ediliyor mu? | YENİ / ÖNERİLEN |
| `ME-010` | Sistem kendi başarısının piyasa davranışını değiştirme riskini ölçüyor mu? | YENİ / ÖNERİLEN |
| `ME-011` | Piyasa katılımcılarının heterojen davranışlarının strateji performansına katkısı ayrıştırılıyor mu? | YENİ / ÖNERİLEN |
| `ME-012` | Likidite sağlayıcı davranışı ile alpha performansı arasındaki nedensel ilişki test ediliyor mu? | YENİ / ÖNERİLEN |
| `ME-013` | Rakip strateji kümeleri ile ortak risk faktörleri arasında ilişki ölçülüyor mu? | YENİ / ÖNERİLEN |
| `ME-014` | Piyasa yoğunluğu arttığında kapasite eğrisi yeniden hesaplanıyor mu? | YENİ / ÖNERİLEN |
| `ME-015` | Crowding artışında no-trade bölgesi otomatik genişletiliyor mu? | YENİ / ÖNERİLEN |
| `ME-016` | Stratejinin başarısı piyasa tarafından arbitraj edilerek ortadan kaldırılabiliyor mu? | YENİ / ÖNERİLEN |
| `ME-017` | Edge kaybının rakip adaptasyonundan mı yoksa rejim değişiminden mi geldiği ayrıştırılıyor mu? | YENİ / ÖNERİLEN |
| `ME-018` | Sistemin rakip davranışı için gözlemleyebildiği doğrudan ve dolaylı kanıtlar ayrıştırılıyor mu? | YENİ / ÖNERİLEN |
| `ME-019` | Piyasa ekolojisi için gözlemlenemeyen aktörlerin etkisi ayrıca belirsizlik olarak temsil ediliyor mu? | YENİ / ÖNERİLEN |
| `ME-020` | Rakip davranış tahmini yanlışlandığında strateji riski azaltılıyor mu? | YENİ / ÖNERİLEN |
| `ME-021` | Ekosistem değişimlerinin detection latency maliyeti ölçülüyor mu? | YENİ / ÖNERİLEN |
| `ME-022` | Rakip strateji kümelerinin aynı venue içindeki etkileşimi stres altında test ediliyor mu? | YENİ / ÖNERİLEN |
| `ME-023` | Bir edge'in kalıcı olabilmesi için piyasa yapısında hangi koşulların korunması gerektiği kayıtlı mı? | YENİ / ÖNERİLEN |
| `ME-024` | Strateji crowding metriği sertifikasyon kapsamına bağlanmış mı? | YENİ / ÖNERİLEN |
| `ME-025` | Piyasa ekolojisi değişimi bir sertifikasyon revocation tetikleyicisi olabiliyor mu? | YENİ / ÖNERİLEN |

### Rakip Algoritmalar ve Adversarial Piyasa
| ID | Soru | Statü |
|---|---|---|
| `AA-001` | Rakip bir algoritmanın giriş tetikleyicimizi keşfettiğini gösteren işaretler tespit ediliyor mu? | YENİ / ÖNERİLEN |
| `AA-002` | Emir zamanlamamızın tahmin edilebilirliği ölçülüyor mu? | YENİ / ÖNERİLEN |
| `AA-003` | Emir büyüklük dağılımımızın benzersiz bir parmak izi oluşturup oluşturmadığı ölçülüyor mu? | YENİ / ÖNERİLEN |
| `AA-004` | Order-flow pattern'ımızın dışarıdan sınıflandırılabilirliği test ediliyor mu? | YENİ / ÖNERİLEN |
| `AA-005` | Venue veya piyasa yapıcıların bizim işlem stilimize tepki verdiği ölçülüyor mu? | YENİ / ÖNERİLEN |
| `AA-006` | Rakiplerin adverse selection davranışının execution kaybımıza katkısı ölçülüyor mu? | YENİ / ÖNERİLEN |
| `AA-007` | Rakiplerin bizim strategy signal'ımızdan bağımsız olarak benzer bir sinyal üretme olasılığı modelleniyor mu? | YENİ / ÖNERİLEN |
| `AA-008` | Bir rakibin bizi izlediği varsayımı altında execution simulator adversarial senaryo çalıştırabiliyor mu? | YENİ / ÖNERİLEN |
| `AA-009` | Latency avantajı olan rakiplere karşı edge dayanıklılığı test ediliyor mu? | YENİ / ÖNERİLEN |
| `AA-010` | Rakiplerin önden konumlanması veya front-running benzeri etkiler için sinyaller izleniyor mu? | YENİ / ÖNERİLEN |
| `AA-011` | Rakiplerin piyasa likiditesini bizim lehimize veya aleyhimize değiştirmesi modelleniyor mu? | YENİ / ÖNERİLEN |
| `AA-012` | Market maker quote davranışının bizim order pattern'ımıza koşullu değişimi ölçülüyor mu? | YENİ / ÖNERİLEN |
| `AA-013` | Rakip stratejilerin aynı ekonomik mekanizmayı farklı ifade biçimleriyle kullanması tespit ediliyor mu? | YENİ / ÖNERİLEN |
| `AA-014` | Rakip davranışındaki değişim ile execution model drift arasında ayrım yapılıyor mu? | YENİ / ÖNERİLEN |
| `AA-015` | Adversarial market response yanlış alarm verdiğinde sistem gereksiz yere stratejiyi kapatıyor mu? | YENİ / ÖNERİLEN |
| `AA-016` | Adversarial response kaçırıldığında zarar potansiyeli ölçülüyor mu? | YENİ / ÖNERİLEN |
| `AA-017` | Rakip davranışının bilinmediği durumda güvenlik payı otomatik artırılıyor mu? | YENİ / ÖNERİLEN |
| `AA-018` | Rakiplerin farklı venue'lerdeki davranışları arasında bağlantı kuruluyor mu? | YENİ / ÖNERİLEN |
| `AA-019` | Rakip algoritmaların öğrenme hızı ile bizim adaptasyon hızımız karşılaştırılıyor mu? | YENİ / ÖNERİLEN |
| `AA-020` | Rakiplerin performansımıza verdiği tepki için gecikmeli nedensellik testi uygulanıyor mu? | YENİ / ÖNERİLEN |
| `AA-021` | Sistemin savunma mekanizması rakibe karşı aşırı adaptasyon yaparak kendi alpha'sını bozuyor mu? | YENİ / ÖNERİLEN |
| `AA-022` | Rakip davranışına uyum amacıyla yapılan değişiklikler ayrı certification scope oluşturuyor mu? | YENİ / ÖNERİLEN |
| `AA-023` | Adversarial testler canlı veriden bağımsız kontrollü replay ile tekrarlanabiliyor mu? | YENİ / ÖNERİLEN |
| `AA-024` | Rakip strateji ortamı değiştiğinde son sağlam champion'a geri dönüş mümkün mü? | YENİ / ÖNERİLEN |
| `AA-025` | Rakip ekosisteminin ölçülemeyen kısmı UNKNOWN olarak authority'yi etkileyebiliyor mu? | YENİ / ÖNERİLEN |

### Edge Evrimi ve Edge Ömrü
| ID | Soru | Statü |
|---|---|---|
| `EE-001` | Her alpha için keşif, büyüme, olgunluk, crowding, doygunluk, bozulma ve ölüm durumları ayrı izleniyor mu? | YENİ / ÖNERİLEN |
| `EE-002` | Edge'in olgunluk aşaması istatistiksel olarak sınıflandırılabiliyor mu? | YENİ / ÖNERİLEN |
| `EE-003` | Edge saturation noktası tahmin ediliyor mu? | YENİ / ÖNERİLEN |
| `EE-004` | Edge half-life ile piyasa yaygınlığı arasında ilişki ölçülüyor mu? | YENİ / ÖNERİLEN |
| `EE-005` | Edge ölümünün geçici mi kalıcı mı olduğu test ediliyor mu? | YENİ / ÖNERİLEN |
| `EE-006` | Ölmüş görünen alpha yeniden ortaya çıktığında bunun eski mekanizmanın geri dönüşü mü yoksa yeni alpha mı olduğu ayrıştırılıyor mu? | YENİ / ÖNERİLEN |
| `EE-007` | Aynı ekonomik mekanizmanın farklı feature setleriyle yeniden ortaya çıkması tespit ediliyor mu? | YENİ / ÖNERİLEN |
| `EE-008` | Edge yaşlanması execution maliyetinden bağımsız ölçülebiliyor mu? | YENİ / ÖNERİLEN |
| `EE-009` | Edge decay ile data drift birlikte gerçekleştiğinde hangisinin baskın olduğu ayrıştırılıyor mu? | YENİ / ÖNERİLEN |
| `EE-010` | Edge bozulması yalnızca performans düşüşünden değil beklenti alt sınırından da izleniyor mu? | YENİ / ÖNERİLEN |
| `EE-011` | Edge decay detection için minimum gözlem penceresi tanımlı mı? | YENİ / ÖNERİLEN |
| `EE-012` | Edge revival için yeni certification gerekiyor mu? | YENİ / ÖNERİLEN |
| `EE-013` | Bir alpha'nın beklenen ömrü capital allocation kararında kullanılıyor mu? | YENİ / ÖNERİLEN |
| `EE-014` | Edge half-life execution latency'den kısa hale gelince pozisyon açılması engelleniyor mu? | YENİ / ÖNERİLEN |
| `EE-015` | Edge strength belirsizliği arttığında risk otomatik azalıyor mu? | YENİ / ÖNERİLEN |
| `EE-016` | Edge deterioration öncesinde öncü göstergeler izleniyor mu? | YENİ / ÖNERİLEN |
| `EE-017` | Edge ölümünün ardından sistem aynı fikri tekrar tekrar test ederek selection bias yaratıyor mu? | YENİ / ÖNERİLEN |
| `EE-018` | Ölen alpha'ların nedenleri araştırma hafızasında kalıcı tutuluyor mu? | YENİ / ÖNERİLEN |
| `EE-019` | Edge decay nedeniyle azaltılan risk sonradan hangi kanıtla geri artırılabilir? | YENİ / ÖNERİLEN |
| `EE-020` | Edge'in farklı piyasa rejimlerindeki yaşam döngüsü ayrı ayrı ölçülüyor mu? | YENİ / ÖNERİLEN |
| `EE-021` | Edge'in venue bazlı ömrü karşılaştırılıyor mu? | YENİ / ÖNERİLEN |
| `EE-022` | Edge'in strateji family'leri arasında paylaşımı ölçülüyor mu? | YENİ / ÖNERİLEN |
| `EE-023` | Edge'in yalnızca belirli zaman aralıklarında hayatta kalması sertifikasyon kapsamına yansıyor mu? | YENİ / ÖNERİLEN |
| `EE-024` | Bir alpha'nın kalıcı olduğunu söylemek için hangi minimum bağımsız kanıt gerekir? | YENİ / ÖNERİLEN |
| `EE-025` | Edge ömrü tahmin modeli yanlışlandığında sistem güvenli tarafta kalıyor mu? | YENİ / ÖNERİLEN |

### Rejim Geçişi ve Yapısal Kırılma
| ID | Soru | Statü |
|---|---|---|
| `RGX-001` | Rejim ile yapısal kırılma birbirinden ayrı sınıflandırılıyor mu? | YENİ / ÖNERİLEN |
| `RGX-002` | Geçiş başlamadan önce öncü değişim göstergeleri ölçülüyor mu? | YENİ / ÖNERİLEN |
| `RGX-003` | False regime change ile gerçek regime change ayrıştırılıyor mu? | YENİ / ÖNERİLEN |
| `RGX-004` | Rejim tespit gecikmesinin P&L maliyeti ölçülüyor mu? | YENİ / ÖNERİLEN |
| `RGX-005` | Rejim detection yanlış pozitif ürettiğinde gereksiz risk azaltma maliyeti ölçülüyor mu? | YENİ / ÖNERİLEN |
| `RGX-006` | Yeni rejimin daha önce sertifikalanmış rejimlere benzerliği ölçülüyor mu? | YENİ / ÖNERİLEN |
| `RGX-007` | Tamamen yeni rejim için UNKNOWN state gerçekten çalışıyor mu? | YENİ / ÖNERİLEN |
| `RGX-008` | Rejim bilinmiyorsa strategy'nin işlem izni nasıl sınırlandırılıyor? | YENİ / ÖNERİLEN |
| `RGX-009` | Bir rejim geçişinin feature distribution mı yoksa target relationship mi değiştirdiği ayrıştırılıyor mu? | YENİ / ÖNERİLEN |
| `RGX-010` | Rejim değişikliği execution maliyetlerini de değiştirdiğinde bu iki drift ayrı ölçülüyor mu? | YENİ / ÖNERİLEN |
| `RGX-011` | Rejim değişiminin farklı asset'lerde aynı anda olup olmadığı ölçülüyor mu? | YENİ / ÖNERİLEN |
| `RGX-012` | Rejim değişimi correlation yapısını değiştirdiğinde portfolio risk yeniden hesaplanıyor mu? | YENİ / ÖNERİLEN |
| `RGX-013` | Rejim geçişi sırasında strategy alpha ve probability calibration birlikte yeniden değerlendiriliyor mu? | YENİ / ÖNERİLEN |
| `RGX-014` | Rejim geçişi sırasında capacity eğrisi otomatik yeniden hesaplanıyor mu? | YENİ / ÖNERİLEN |
| `RGX-015` | Rejim geçişinde shadow validation yapılmadan production adaptation engelleniyor mu? | YENİ / ÖNERİLEN |
| `RGX-016` | Yeni rejim için yeterli örnek oluşmadan strategy promotion engelleniyor mu? | YENİ / ÖNERİLEN |
| `RGX-017` | Rejim geri döndüğünde eski champion'ın güvenli şekilde tekrar kullanılabilmesi mümkün mü? | YENİ / ÖNERİLEN |
| `RGX-018` | Rejim tespit modeli kendi geçmiş hatalarından dolayı gecikmeyi artırıyor mu? | YENİ / ÖNERİLEN |
| `RGX-019` | Rejim değişimlerinde kalibrasyon drift'i ayrı bir veto oluşturabiliyor mu? | YENİ / ÖNERİLEN |
| `RGX-020` | Rejim sınıflandırması farklı modeller arasında anlaşmazlığa yol açıyorsa uncertainty büyütülüyor mu? | YENİ / ÖNERİLEN |
| `RGX-021` | Rejimlerin birbirine geçiş olasılıkları ve geçiş maliyetleri ölçülüyor mu? | YENİ / ÖNERİLEN |
| `RGX-022` | Rejim modeli yeni piyasa mekanizmasını var olan bir rejime yanlış eşliyorsa bunu tespit eden test var mı? | YENİ / ÖNERİLEN |
| `RGX-023` | Rejim etiketi için insan veya dış uzman müdahalesi gerekiyorsa bu süreç reproducible mı? | YENİ / ÖNERİLEN |
| `RGX-024` | Rejim detection için aynı verinin farklı preprocessing biçimlerinin sonuçları karşılaştırılıyor mu? | YENİ / ÖNERİLEN |
| `RGX-025` | Yeni rejimde ilk güvenli sermaye tahsisi için ayrı risk bütçesi var mı? | YENİ / ÖNERİLEN |

### Bilinmeyen-Bilinmeyenler ve OOD
| ID | Soru | Statü |
|---|---|---|
| `UU-001` | Sistem mevcut feature uzayının açıklayamadığı yeni davranışları tespit edebiliyor mu? | YENİ / ÖNERİLEN |
| `UU-002` | Model residual'larının yeni bir piyasa mekanizmasına işaret edip etmediği ölçülüyor mu? | YENİ / ÖNERİLEN |
| `UU-003` | Tekrarlayan anomaliler otomatik araştırma adayı oluşturuyor mu? | YENİ / ÖNERİLEN |
| `UU-004` | Unknown unknown ile veri kalitesi hatası birbirinden ayrıştırılıyor mu? | YENİ / ÖNERİLEN |
| `UU-005` | Unknown durumun süresi risk bütçesine yansıtılıyor mu? | YENİ / ÖNERİLEN |
| `UU-006` | Model high-confidence üretse bile OOD durumunda işlem bloklanabiliyor mu? | YENİ / ÖNERİLEN |
| `UU-007` | OOD detection false-negative oranı ölçülüyor mu? | YENİ / ÖNERİLEN |
| `UU-008` | OOD detection false-positive maliyeti ölçülüyor mu? | YENİ / ÖNERİLEN |
| `UU-009` | OOD detection gecikmesinin ekonomik maliyeti hesaplanıyor mu? | YENİ / ÖNERİLEN |
| `UU-010` | Yeni bir anomali daha önce görülen anomalilerle karşılaştırılıyor mu? | YENİ / ÖNERİLEN |
| `UU-011` | Sistem bilmediği bir durumu “normal” kabul etmeyi reddediyor mu? | YENİ / ÖNERİLEN |
| `UU-012` | Unknown state içinde execution ve risk tarafı daha muhafazakâr hale geliyor mu? | YENİ / ÖNERİLEN |
| `UU-013` | Unknown state recovery için hangi kanıtların gerektiği tanımlı mı? | YENİ / ÖNERİLEN |
| `UU-014` | Anomali detection sistemi kendi eğitim verisine aşırı uyum sağlamış olabilir mi? | YENİ / ÖNERİLEN |
| `UU-015` | Anomali modeli yeni piyasa rejimini veri bozukluğu sanıyor olabilir mi? | YENİ / ÖNERİLEN |
| `UU-016` | Unknown olaylar ayrı bir research dataset olarak tutuluyor mu? | YENİ / ÖNERİLEN |
| `UU-017` | Her unknown olayın sonradan açıklanıp açıklanmadığı izleniyor mu? | YENİ / ÖNERİLEN |
| `UU-018` | Açıklanan unknown olayın neden daha önce tespit edilmediği postmortem ile belirleniyor mu? | YENİ / ÖNERİLEN |
| `UU-019` | Unknown event ile strategy decay arasındaki ilişki ölçülüyor mu? | YENİ / ÖNERİLEN |
| `UU-020` | Unknown event ile execution failure arasındaki ilişki ölçülüyor mu? | YENİ / ÖNERİLEN |
| `UU-021` | Birden fazla bağımsız detector aynı unknown olayı gösteriyorsa confidence artırılabiliyor mu? | YENİ / ÖNERİLEN |
| `UU-022` | Detector'lar çelişiyorsa sistem belirsizliği artırıyor mu? | YENİ / ÖNERİLEN |
| `UU-023` | Unknown event kritikse otomatik certification review açılıyor mu? | YENİ / ÖNERİLEN |
| `UU-024` | Unknown event sonrası eski certification scope'u korumak için hangi koşullar gerekiyor? | YENİ / ÖNERİLEN |
| `UU-025` | Yeni keşfedilen mekanizma soru bankasına kontrollü olarak eklenebiliyor mu? | YENİ / ÖNERİLEN |

### Model Rekabeti ve Model Ekosistemi
| ID | Soru | Statü |
|---|---|---|
| `MC-001` | Champion ve challenger aynı kapsamda hangi ekonomik koşullarda karşılaştırılıyor? | YENİ / ÖNERİLEN |
| `MC-002` | Challenger avantajı yalnızca başka bir regime'deyse promotion engelleniyor mu? | YENİ / ÖNERİLEN |
| `MC-003` | Yeni model daha iyi performansı daha yüksek tail risk ile mi elde ediyor? | YENİ / ÖNERİLEN |
| `MC-004` | Model değişiminin probability calibration üzerindeki etkisi ölçülüyor mu? | YENİ / ÖNERİLEN |
| `MC-005` | Model değişiminin execution timing üzerindeki etkisi ölçülüyor mu? | YENİ / ÖNERİLEN |
| `MC-006` | Modeller arasındaki disagreement ölçülüyor mu? | YENİ / ÖNERİLEN |
| `MC-007` | Model disagreement artışı risk azaltma tetikleyebiliyor mu? | YENİ / ÖNERİLEN |
| `MC-008` | Modellerin ortak hata bölgeleri tespit ediliyor mu? | YENİ / ÖNERİLEN |
| `MC-009` | Tüm modeller aynı veri kaynağı kusuruna bağımlı mı? | YENİ / ÖNERİLEN |
| `MC-010` | Model diversity gerçek bağımsızlık mı yoksa sadece farklı mimari görünümü mü? | YENİ / ÖNERİLEN |
| `MC-011` | Yeni modelin feature dependency yapısı eski modelden ayrışıyor mu? | YENİ / ÖNERİLEN |
| `MC-012` | Model promotion sonrası drift detector hassasiyeti değişiyor mu? | YENİ / ÖNERİLEN |
| `MC-013` | Yeni model aynı regime içinde daha kırılgan mı? | YENİ / ÖNERİLEN |
| `MC-014` | Model ensemble kullanılıyorsa ortak bias ölçülüyor mu? | YENİ / ÖNERİLEN |
| `MC-015` | Bir modelin kaldırılması portföy alpha dependency'sini değiştiriyor mu? | YENİ / ÖNERİLEN |
| `MC-016` | Model geri alma kararı önceden tanımlı mı? | YENİ / ÖNERİLEN |
| `MC-017` | Model rollback sırasında açık pozisyonların işleyişi tanımlı mı? | YENİ / ÖNERİLEN |
| `MC-018` | Model versiyon değişiminin sertifikasyon scope hash'ine etkisi doğru uygulanıyor mu? | YENİ / ÖNERİLEN |
| `MC-019` | Model performansının yalnızca en son dönemde yükselmesi promotion için yeterli mi? | YENİ / ÖNERİLEN |
| `MC-020` | Model stabilitesi için uzun dönem test penceresi tanımlı mı? | YENİ / ÖNERİLEN |
| `MC-021` | Model değişiminin computational cost'u risk/latency bütçesine yansıyor mu? | YENİ / ÖNERİLEN |
| `MC-022` | Model complexity artışı gerçekten incremental edge sağlıyor mu? | YENİ / ÖNERİLEN |
| `MC-023` | Modelin explainability kaybı authority'yi etkiliyor mu? | YENİ / ÖNERİLEN |
| `MC-024` | Model selection sürecinde başarısız modeller korunuyor mu? | YENİ / ÖNERİLEN |
| `MC-025` | Model ecosystem değiştiğinde champion seçim kriteri yeniden sertifikalandırılıyor mu? | YENİ / ÖNERİLEN |

### Adaptasyon Yönetimi ve Adaptasyon Hızı
| ID | Soru | Statü |
|---|---|---|
| `AG-001` | Sistem her drift olayında otomatik model değiştiriyor mu? | YENİ / ÖNERİLEN |
| `AG-002` | Drift algılanması ile adaptation arasında minimum doğrulama süresi var mı? | YENİ / ÖNERİLEN |
| `AG-003` | Değişimin geçici mi kalıcı mı olduğu test ediliyor mu? | YENİ / ÖNERİLEN |
| `AG-004` | Adaptasyonun yanlış olmasının maliyeti ölçülüyor mu? | YENİ / ÖNERİLEN |
| `AG-005` | Adaptasyon yapmamanın maliyeti ile yanlış adaptasyonun maliyeti karşılaştırılıyor mu? | YENİ / ÖNERİLEN |
| `AG-006` | Adaptasyon sıklığı model churn üretiyor mu? | YENİ / ÖNERİLEN |
| `AG-007` | Model churn execution kalitesini bozuyor mu? | YENİ / ÖNERİLEN |
| `AG-008` | Model churn probability calibration'ı bozuyor mu? | YENİ / ÖNERİLEN |
| `AG-009` | Adaptasyon için minimum independent evidence şartı var mı? | YENİ / ÖNERİLEN |
| `AG-010` | Adaptasyon öncesi ve sonrası davranış difference report üretiliyor mu? | YENİ / ÖNERİLEN |
| `AG-011` | Adaptasyon sonrası rollback penceresi tanımlı mı? | YENİ / ÖNERİLEN |
| `AG-012` | Adaptasyon kendi yarattığı feedback loop'un etkisini ölçüyor mu? | YENİ / ÖNERİLEN |
| `AG-013` | Adaptasyonun performans artışı regime-specific ise genelleme engelleniyor mu? | YENİ / ÖNERİLEN |
| `AG-014` | Adaptasyon search budget tarafından sınırlandırılıyor mu? | YENİ / ÖNERİLEN |
| `AG-015` | Online değişiklikler test setine tekrar tekrar maruz kalıyor mu? | YENİ / ÖNERİLEN |
| `AG-016` | Adaptasyon süreci ayrı bir certification scope oluşturuyor mu? | YENİ / ÖNERİLEN |
| `AG-017` | Adaptasyonun güvenlik sınırları hard policy ile korunuyor mu? | YENİ / ÖNERİLEN |
| `AG-018` | Adaptasyon başarısız olduğunda son sertifikalı modele dönülüyor mu? | YENİ / ÖNERİLEN |
| `AG-019` | Adaptasyon sırasında sermaye otomatik azaltılabiliyor mu? | YENİ / ÖNERİLEN |
| `AG-020` | Adaptasyonun kaynak tüketimi trading critical path'i etkiliyor mu? | YENİ / ÖNERİLEN |
| `AG-021` | Adaptasyonun kendi gecikmesi edge half-life'ı aşabiliyor mu? | YENİ / ÖNERİLEN |
| `AG-022` | Adaptasyon threshold'ları zamanla sessizce değişebiliyor mu? | YENİ / ÖNERİLEN |
| `AG-023` | Adaptasyon threshold değişiklikleri change request gerektiriyor mu? | YENİ / ÖNERİLEN |
| `AG-024` | Adaptasyonun etkisi farklı market profile'larda ayrı ölçülüyor mu? | YENİ / ÖNERİLEN |
| `AG-025` | Adaptasyon sonucunun gerçek ekonomiye katkısı attribution ile doğrulanıyor mu? | YENİ / ÖNERİLEN |

### Çevrim İçi Öğrenme ve Online Güvenlik
| ID | Soru | Statü |
|---|---|---|
| `OL-001` | Online learner hangi verileri anında kullanmaya yetkili? | YENİ / ÖNERİLEN |
| `OL-002` | Outcome kapanmadan online learner etiketi kullanabiliyor mu? | YENİ / ÖNERİLEN |
| `OL-003` | Label delay doğru şekilde modelleniyor mu? | YENİ / ÖNERİLEN |
| `OL-004` | Online pipeline içinde future leakage tespit ediliyor mu? | YENİ / ÖNERİLEN |
| `OL-005` | Online learner kendi ürettiği kararların sonuçlarından circular feedback alıyor mu? | YENİ / ÖNERİLEN |
| `OL-006` | Online update sonrası modelin davranış farkı ölçülüyor mu? | YENİ / ÖNERİLEN |
| `OL-007` | Online learning performans artışını yalnızca son rejimde mi gösteriyor? | YENİ / ÖNERİLEN |
| `OL-008` | Online update başarısız olduğunda rollback mümkün mü? | YENİ / ÖNERİLEN |
| `OL-009` | Her online update yeniden üretilebilir mi? | YENİ / ÖNERİLEN |
| `OL-010` | Random seed ve environment version online update ile saklanıyor mu? | YENİ / ÖNERİLEN |
| `OL-011` | Online learner için update cadence sertifikalı mı? | YENİ / ÖNERİLEN |
| `OL-012` | Update sırasında model ve feature drift birlikte kontrol ediliyor mu? | YENİ / ÖNERİLEN |
| `OL-013` | Online learning nedeniyle confidence artışı gerçek calibration iyileşmesiyle doğrulanıyor mu? | YENİ / ÖNERİLEN |
| `OL-014` | Online learner risk limitlerini dolaylı biçimde genişletebiliyor mu? | YENİ / ÖNERİLEN |
| `OL-015` | Online learning update'leri champion/challenger kurallarını bypass edebiliyor mu? | YENİ / ÖNERİLEN |
| `OL-016` | Online learner data vendor drift karşısında kendini yanlış uyarlıyor mu? | YENİ / ÖNERİLEN |
| `OL-017` | Online update sıklığı execution latency'yi etkiliyor mu? | YENİ / ÖNERİLEN |
| `OL-018` | Online learning kullanımı certification scope'u değiştirdiğinde sistem bunu zorunlu tutuyor mu? | YENİ / ÖNERİLEN |
| `OL-019` | Online learner farklı asset'ler arasında kirli bilgi paylaşabiliyor mu? | YENİ / ÖNERİLEN |
| `OL-020` | Cross-asset transfer öğrenmesi veri bağımlılığını doğru taşıyor mu? | YENİ / ÖNERİLEN |
| `OL-021` | Online learner failure durumunda statik güvenli model kullanılabiliyor mu? | YENİ / ÖNERİLEN |
| `OL-022` | Online modelin eski davranışı immutable olarak saklanıyor mu? | YENİ / ÖNERİLEN |
| `OL-023` | Her update için hypothesis ve reason kaydediliyor mu? | YENİ / ÖNERİLEN |
| `OL-024` | Online update sonrası adversarial exam yeniden çalıştırılıyor mu? | YENİ / ÖNERİLEN |
| `OL-025` | Online learner üretime geçmeden önce shadow/paper validation gerektiriyor mu? | YENİ / ÖNERİLEN |

### Execution Ekolojisi ve Kendi Piyasa Etkimiz
| ID | Soru | Statü |
|---|---|---|
| `XE-001` | Sistemin kendi emirlerinin piyasa state'ini değiştirmesi modelleniyor mu? | YENİ / ÖNERİLEN |
| `XE-002` | Kendi market impact'imiz ile dış market impact ayrıştırılıyor mu? | YENİ / ÖNERİLEN |
| `XE-003` | Aynı strategy'nin art arda işlemlerinin execution kalitesini bozması ölçülüyor mu? | YENİ / ÖNERİLEN |
| `XE-004` | Kendi order flow fingerprint'imiz detect ediliyor mu? | YENİ / ÖNERİLEN |
| `XE-005` | Kendi işlemimiz nedeniyle sonraki fırsatların EV'si değişiyor mu? | YENİ / ÖNERİLEN |
| `XE-006` | Self-induced slippage ölçülüyor mu? | YENİ / ÖNERİLEN |
| `XE-007` | Self-induced spread widening ölçülüyor mu? | YENİ / ÖNERİLEN |
| `XE-008` | Kendi pozisyon büyüklüğümüzün sonraki exit liquidity'yi azaltması modelleniyor mu? | YENİ / ÖNERİLEN |
| `XE-009` | Execution optimization predictive alpha'yı bozuyor mu? | YENİ / ÖNERİLEN |
| `XE-010` | Execution optimizer ile strategy signal arasındaki feedback kontrol ediliyor mu? | YENİ / ÖNERİLEN |
| `XE-011` | Venue selection kendi order flow'umuz nedeniyle endojen hale geliyor mu? | YENİ / ÖNERİLEN |
| `XE-012` | Kendi işlemlerimizin farklı venue'lerde cross-impact etkisi ölçülüyor mu? | YENİ / ÖNERİLEN |
| `XE-013` | Execution path dependency replay ile yeniden üretilebiliyor mu? | YENİ / ÖNERİLEN |
| `XE-014` | Gerçekleşen execution sonrasında aynı strategy'nin sonraki kararları güncelleniyorsa bu adaptation kontrollü mü? | YENİ / ÖNERİLEN |
| `XE-015` | Execution cost model kendi davranışımıza göre drift edebiliyor mu? | YENİ / ÖNERİLEN |
| `XE-016` | Kendi işlem yoğunluğumuz arttığında capacity otomatik düşürülebiliyor mu? | YENİ / ÖNERİLEN |
| `XE-017` | Kendi işlemlerimizin likidite replenishment üzerindeki etkisi ölçülüyor mu? | YENİ / ÖNERİLEN |
| `XE-018` | Kendi cancellation davranışımızın adverse selection etkisi ölçülüyor mu? | YENİ / ÖNERİLEN |
| `XE-019` | Execution kararlarının piyasa tarafından öğrenilebilirliği ölçülüyor mu? | YENİ / ÖNERİLEN |
| `XE-020` | Execution randomness kullanılıyorsa bunun faydası ve maliyeti kanıtlanmış mı? | YENİ / ÖNERİLEN |
| `XE-021` | Execution policy değişimi certification scope'a bağlanmış mı? | YENİ / ÖNERİLEN |
| `XE-022` | Execution model yanlışlandığında risk ve capital otomatik düşüyor mu? | YENİ / ÖNERİLEN |
| `XE-023` | Execution latency dağılımının regime değişimlerine duyarlılığı ölçülüyor mu? | YENİ / ÖNERİLEN |
| `XE-024` | Acil çıkışta self-impact kapasitesi ayrıca test ediliyor mu? | YENİ / ÖNERİLEN |
| `XE-025` | Kendi execution davranışımızın strategy alpha'sını uzun vadede tüketip tüketmediği ölçülüyor mu? | YENİ / ÖNERİLEN |

### Strateji Emekliliği ve Yeniden Doğuş
| ID | Soru | Statü |
|---|---|---|
| `SR-001` | Bir strategy'nin “ölü” olduğuna karar veren objektif koşullar var mı? | YENİ / ÖNERİLEN |
| `SR-002` | Strategy ölümünün kalıcı mı geçici mi olduğu ayrıştırılıyor mu? | YENİ / ÖNERİLEN |
| `SR-003` | Strategy geçici olarak WATCH/PROBATION durumuna alınabiliyor mu? | YENİ / ÖNERİLEN |
| `SR-004` | Strategy yeniden aktive edilmeden önce yeni evidence gerekiyor mu? | YENİ / ÖNERİLEN |
| `SR-005` | Öldürülen strategy'nin ölüm nedeni kalıcı research memory'de tutuluyor mu? | YENİ / ÖNERİLEN |
| `SR-006` | Strategy retirement reason aynı mekanizmayı kullanan başka strategy'lere aktarılıyor mu? | YENİ / ÖNERİLEN |
| `SR-007` | Strategy replacement adayları sistematik olarak aranıyor mu? | YENİ / ÖNERİLEN |
| `SR-008` | Replacement strategy aynı mekanizmanın sadece parametre değiştirilmiş kopyası mı? | YENİ / ÖNERİLEN |
| `SR-009` | Retired strategy'nin yeniden keşfi selection bias yaratıyor mu? | YENİ / ÖNERİLEN |
| `SR-010` | Strategy revival için yeni certification scope oluşturuluyor mu? | YENİ / ÖNERİLEN |
| `SR-011` | Bir strategy'nin risk bütçesi azaltılarak yaşatılması hangi koşullarda mümkün? | YENİ / ÖNERİLEN |
| `SR-012` | Strategy retirement kararının false-positive maliyeti ölçülüyor mu? | YENİ / ÖNERİLEN |
| `SR-013` | Strategy retirement kararının false-negative maliyeti ölçülüyor mu? | YENİ / ÖNERİLEN |
| `SR-014` | Retirement detection window istatistiksel olarak yeterli mi? | YENİ / ÖNERİLEN |
| `SR-015` | Strategy retirement sonrası açık pozisyonların yönetimi tanımlı mı? | YENİ / ÖNERİLEN |
| `SR-016` | Retired strategy'nin historical results'u korunuyor mu? | YENİ / ÖNERİLEN |
| `SR-017` | Strategy versionları arasındaki davranış farkı replay ile ispatlanabiliyor mu? | YENİ / ÖNERİLEN |
| `SR-018` | Strategy family bazında retirement pattern'leri izleniyor mu? | YENİ / ÖNERİLEN |
| `SR-019` | Bir strategy'nin sadece belirli venue'lerde ölmesi ayrı işleniyor mu? | YENİ / ÖNERİLEN |
| `SR-020` | Bir strategy'nin sadece belirli regime'lerde ölmesi ayrı işleniyor mu? | YENİ / ÖNERİLEN |
| `SR-021` | Strategy death event bir model drift göstergesi olabilir mi? | YENİ / ÖNERİLEN |
| `SR-022` | Strategy death ile market structure change arasında bağlantı aranıyor mu? | YENİ / ÖNERİLEN |
| `SR-023` | Strategy retirement süreci kendisi overfit ediliyor mu? | YENİ / ÖNERİLEN |
| `SR-024` | Retirement rule değiştiğinde eski decision evidence yeniden yorumlanıyor mu? | YENİ / ÖNERİLEN |
| `SR-025` | Strategy resurrection için hangi bağımsız kanıtlar zorunlu? | YENİ / ÖNERİLEN |

### Sermaye Hayatta Kalması ve Ruin Dayanıklılığı
| ID | Soru | Statü |
|---|---|---|
| `CS-001` | Sistemin hayatta kalma sermayesi açıkça hesaplanıyor mu? | YENİ / ÖNERİLEN |
| `CS-002` | En kötü doğrulanmış rejimde beklenen sermaye kaybı ölçülüyor mu? | YENİ / ÖNERİLEN |
| `CS-003` | Birden fazla strategy aynı anda başarısız olursa portfolio ne yapıyor? | YENİ / ÖNERİLEN |
| `CS-004` | Correlation 1'e yaklaştığında risk bütçesi yeniden hesaplanıyor mu? | YENİ / ÖNERİLEN |
| `CS-005` | Tail risk engine'leri birlikte başarısız olduğunda güvenli fallback var mı? | YENİ / ÖNERİLEN |
| `CS-006` | Likidite yokluğu sırasında liquidation path modelleniyor mu? | YENİ / ÖNERİLEN |
| `CS-007` | Uzun süre fırsat çıkmadığında sermaye nasıl korunuyor? | YENİ / ÖNERİLEN |
| `CS-008` | No-trade veya cash-like durum explicit strategy/policy olarak tanımlı mı? | YENİ / ÖNERİLEN |
| `CS-009` | Recovery time sermaye planlamasına dahil mi? | YENİ / ÖNERİLEN |
| `CS-010` | Survival capital altında kalan kaynak ile risk capital ayrıştırılıyor mu? | YENİ / ÖNERİLEN |
| `CS-011` | Daily loss, weekly loss ve drawdown limitlerinin etkileşimi test ediliyor mu? | YENİ / ÖNERİLEN |
| `CS-012` | Seri kayıplarda risk azaltma gecikmesi ölçülüyor mu? | YENİ / ÖNERİLEN |
| `CS-013` | Ruin probability modelinin parametre belirsizliği hesaba katılıyor mu? | YENİ / ÖNERİLEN |
| `CS-014` | Tail correlation yanlış tahmin edildiğinde worst-case sonuç ölçülüyor mu? | YENİ / ÖNERİLEN |
| `CS-015` | Emergency liquidity ihtiyacı portfolio sizing'e yansıyor mu? | YENİ / ÖNERİLEN |
| `CS-016` | Sistemin operational downtime riski ekonomik survival analizine dahil mi? | YENİ / ÖNERİLEN |
| `CS-017` | Broker/venue erişim kaybında sermaye koruma planı test ediliyor mu? | YENİ / ÖNERİLEN |
| `CS-018` | Bir strategy family çökerken diğerlerinin sermaye payı otomatik artırılmadan önce yeni kanıt gerekiyor mu? | YENİ / ÖNERİLEN |
| `CS-019` | Capital preservation hedefi nominal return hedefini üstünlükle bastırıyor mu? | YENİ / ÖNERİLEN |
| `CS-020` | Uzun drawdown döneminde model churn otomatik sınırlandırılıyor mu? | YENİ / ÖNERİLEN |
| `CS-021` | Survival planı farklı account size'lar için ayrı ölçülüyor mu? | YENİ / ÖNERİLEN |
| `CS-022` | Leverage artışının survival probability üzerindeki etkisi ölçülüyor mu? | YENİ / ÖNERİLEN |
| `CS-023` | Recovery sırasında açık pozisyon ve nakit durumu tekrar doğrulanıyor mu? | YENİ / ÖNERİLEN |
| `CS-024` | Ruin metric ile gerçek historical drawdown davranışı düzenli karşılaştırılıyor mu? | YENİ / ÖNERİLEN |
| `CS-025` | Survival assumptions değiştiğinde R4 yeniden değerlendirme tetikleniyor mu? | YENİ / ÖNERİLEN |

### Fırsat Tükenmesi ve Opportunity Scarcity
| ID | Soru | Statü |
|---|---|---|
| `OD-001` | Aynı fırsat türünün çok sık işlem görmesi kaliteyi düşürüyor mu? | YENİ / ÖNERİLEN |
| `OD-002` | İlk fırsatlarla sonraki fırsatlar arasında EV farkı ölçülüyor mu? | YENİ / ÖNERİLEN |
| `OD-003` | Strategy kendi opportunity set'ini tüketebiliyor mu? | YENİ / ÖNERİLEN |
| `OD-004` | Opportunity scarcity capital allocation kararına dahil mi? | YENİ / ÖNERİLEN |
| `OD-005` | Aynı market event sonrası oluşan çoklu sinyaller bağımsız fırsatlar mı? | YENİ / ÖNERİLEN |
| `OD-006` | Fırsatların kümelenmesi tek bir ekonomik olay olarak ele alınıyor mu? | YENİ / ÖNERİLEN |
| `OD-007` | Aşırı trade frequency edge erosion yaratıyorsa no-trade eşiği sıkılaşıyor mu? | YENİ / ÖNERİLEN |
| `OD-008` | Bir fırsatın sonraki fırsatları etkileyip etkilemediği ölçülüyor mu? | YENİ / ÖNERİLEN |
| `OD-009` | Opportunity decay ile alpha decay ayrıştırılıyor mu? | YENİ / ÖNERİLEN |
| `OD-010` | Opportunity capacity strategy capacity ile aynı kavram olarak yanlış kullanılmıyor mu? | YENİ / ÖNERİLEN |
| `OD-011` | Bir market event için aynı anda kaç strategy fırsat üretebilir? | YENİ / ÖNERİLEN |
| `OD-012` | Capital competition opportunity similarity'yi hesaba katıyor mu? | YENİ / ÖNERİLEN |
| `OD-013` | Opportunity duplication nedeniyle nominal sample size şişiriliyor mu? | YENİ / ÖNERİLEN |
| `OD-014` | Aynı signal ailesindeki fırsatlar effective sample size hesabında bağımlı kabul ediliyor mu? | YENİ / ÖNERİLEN |
| `OD-015` | Opportunity scarcity regime'ler arasında değişiyor mu? | YENİ / ÖNERİLEN |
| `OD-016` | Rare opportunity stratejilerinde küçük sample nedeniyle uncertainty artışı risk kararına yansıyor mu? | YENİ / ÖNERİLEN |
| `OD-017` | Fırsatların oluşmadığı dönemde strategy performansı “başarısızlık” olarak yanlış yorumlanıyor mu? | YENİ / ÖNERİLEN |
| `OD-018` | Opportunity absence veri arızasından ayırt ediliyor mu? | YENİ / ÖNERİLEN |
| `OD-019` | Opportunity generation latency ölçülüyor mu? | YENİ / ÖNERİLEN |
| `OD-020` | Opportunity expiry sonrası sinyalin execution'a gitmesi engelleniyor mu? | YENİ / ÖNERİLEN |
| `OD-021` | Opportunity re-entry kuralları bağımsız mı? | YENİ / ÖNERİLEN |
| `OD-022` | Bir fırsatın tekrar kullanılması market impact nedeniyle değerini değiştiriyor mu? | YENİ / ÖNERİLEN |
| `OD-023` | Opportunity ranking ile capital ranking ayrıştırılıyor mu? | YENİ / ÖNERİLEN |
| `OD-024` | Opportunity scarcity için ayrı observability metriği var mı? | YENİ / ÖNERİLEN |
| `OD-025` | Opportunity depletion yeni research sorusu üretebiliyor mu? | YENİ / ÖNERİLEN |

### Veri Ekolojisi ve Sağlayıcı Drift’i
| ID | Soru | Statü |
|---|---|---|
| `DE-001` | Veri sağlayıcısının metodoloji değişimi otomatik olarak tespit ediliyor mu? | YENİ / ÖNERİLEN |
| `DE-002` | Sağlayıcı bir alanın semantiğini değiştirdiğinde sistem bunu fark ediyor mu? | YENİ / ÖNERİLEN |
| `DE-003` | Kaynak değişiminde historical comparability korunuyor mu? | YENİ / ÖNERİLEN |
| `DE-004` | İki sağlayıcı aynı olayı farklı temsil ettiğinde fark analizi yapılıyor mu? | YENİ / ÖNERİLEN |
| `DE-005` | Vendor drift ile market drift ayrıştırılıyor mu? | YENİ / ÖNERİLEN |
| `DE-006` | Vendor bağımlılığı strategy risk profile içinde ölçülüyor mu? | YENİ / ÖNERİLEN |
| `DE-007` | Tek vendor arızasında fallback source point-in-time özelliklerini koruyor mu? | YENİ / ÖNERİLEN |
| `DE-008` | Vendor değişimi feature distribution drift oluşturuyorsa tespit ediliyor mu? | YENİ / ÖNERİLEN |
| `DE-009` | Vendor revision behavior değişimi certification scope'a yansıyor mu? | YENİ / ÖNERİLEN |
| `DE-010` | Vendor data latency değişimi edge half-life açısından kontrol ediliyor mu? | YENİ / ÖNERİLEN |
| `DE-011` | Vendor field quality düşüşünde strategy eligibility otomatik değişiyor mu? | YENİ / ÖNERİLEN |
| `DE-012` | Vendor pricing/funding/fee verilerindeki değişiklikler economic model ile eşleştiriliyor mu? | YENİ / ÖNERİLEN |
| `DE-013` | Vendor outage sonrası recovery historical continuity'yi koruyor mu? | YENİ / ÖNERİLEN |
| `DE-014` | Vendor contract/entitlement değişikliği canlı authority'yi revocation edebiliyor mu? | YENİ / ÖNERİLEN |
| `DE-015` | Vendor methodology change için backfill ve no-backfill ayrımı yapılıyor mu? | YENİ / ÖNERİLEN |
| `DE-016` | Vendor versionları manifest ve lineage içinde tutuluyor mu? | YENİ / ÖNERİLEN |
| `DE-017` | Vendor değişiminin alpha sonuçlarına etkisi attribution ile ölçülüyor mu? | YENİ / ÖNERİLEN |
| `DE-018` | Vendor drift ile model drift birlikte gerçekleştiğinde ayrıştırma mekanizması var mı? | YENİ / ÖNERİLEN |
| `DE-019` | Yeni vendor verisinin eski vendor ile eşdeğerliği kanıtlanmadan production use engelleniyor mu? | YENİ / ÖNERİLEN |
| `DE-020` | Vendor fallback activation rate strategy certificate içine giriyor mu? | YENİ / ÖNERİLEN |
| `DE-021` | Vendor seçimi cost-performance-latency açısından ölçülüyor mu? | YENİ / ÖNERİLEN |
| `DE-022` | Bir vendor'ın tahsisli kapasitesi dolduğunda data quality politikası ne yapıyor? | YENİ / ÖNERİLEN |
| `DE-023` | Vendor dependency kritikse multi-source diversity gerçekten bağımsız mı? | YENİ / ÖNERİLEN |
| `DE-024` | Vendor source status bilinmiyorsa authority fail-closed oluyor mu? | YENİ / ÖNERİLEN |
| `DE-025` | Vendor değişiklikleri question bank sınavına otomatik yeni senaryo üretebiliyor mu? | YENİ / ÖNERİLEN |

### Nedensellik, Counterfactual ve Mekanizma Testleri
| ID | Soru | Statü |
|---|---|---|
| `CA-001` | Alpha'nın yalnızca korelasyon değil ekonomik mekanizma temeli var mı? | YENİ / ÖNERİLEN |
| `CA-002` | Mekanizmanın gerekli koşulları açıkça tanımlı mı? | YENİ / ÖNERİLEN |
| `CA-003` | Mekanizmanın yeterli koşulları açıkça tanımlı mı? | YENİ / ÖNERİLEN |
| `CA-004` | Feature çıkarıldığında economic mechanism gerçekten bozuluyor mu? | YENİ / ÖNERİLEN |
| `CA-005` | Alternatif veri ile aynı mekanizma gözlenebiliyor mu? | YENİ / ÖNERİLEN |
| `CA-006` | Reverse-direction testi mekanizma varsayımını güçlendiriyor mu? | YENİ / ÖNERİLEN |
| `CA-007` | Counterfactual olarak trade yapılmasaydı sonuç ne olurdu? | YENİ / ÖNERİLEN |
| `CA-008` | Fırsat başka execution mode ile alındığında sonuç değişiyor mu? | YENİ / ÖNERİLEN |
| `CA-009` | Daha küçük size ile risk-adjusted sonuç iyileşiyor mu? | YENİ / ÖNERİLEN |
| `CA-010` | Beklemek ile hemen işlem yapmak karşılaştırılıyor mu? | YENİ / ÖNERİLEN |
| `CA-011` | Ters yön senaryosu sistematik olarak test ediliyor mu? | YENİ / ÖNERİLEN |
| `CA-012` | P&L içinde alpha, beta, selection, sizing ve execution katkıları ayrıştırılıyor mu? | YENİ / ÖNERİLEN |
| `CA-013` | Attribution residual büyükse causal inference güvenilmez olarak işaretleniyor mu? | YENİ / ÖNERİLEN |
| `CA-014` | Causal conclusion ile predictive correlation birbirinden ayrılıyor mu? | YENİ / ÖNERİLEN |
| `CA-015` | Yeni bir feature yalnızca performans artırıyor diye mekanizma kanıtı sayılmıyor mu? | YENİ / ÖNERİLEN |
| `CA-016` | Feature importance ile economic causality birbirine karıştırılmıyor mu? | YENİ / ÖNERİLEN |
| `CA-017` | Regime değişiminde causal relationship yeniden doğrulanıyor mu? | YENİ / ÖNERİLEN |
| `CA-018` | Mekanizma market participant behavior değişince de geçerli mi? | YENİ / ÖNERİLEN |
| `CA-019` | Mekanizmanın uygulanabilirliğini bozacak execution cost threshold'ları ölçülüyor mu? | YENİ / ÖNERİLEN |
| `CA-020` | Mekanizma crowding altında dayanıyor mu? | YENİ / ÖNERİLEN |
| `CA-021` | Mekanizma farklı venue'lerde aynı yönü gösteriyor mu? | YENİ / ÖNERİLEN |
| `CA-022` | Mekanizma farklı time horizon'larda tutarlı mı? | YENİ / ÖNERİLEN |
| `CA-023` | Mekanizma için bağımsız veri kaynakları aynı sonuca ulaşıyor mu? | YENİ / ÖNERİLEN |
| `CA-024` | Mekanizma başarısının önemli bir kısmı tek bir gözlem dönemine dayanıyorsa bu risk ölçülüyor mu? | YENİ / ÖNERİLEN |
| `CA-025` | Mekanizmanın yanlışlanacağı koşullar açıkça kayıtlı mı? | YENİ / ÖNERİLEN |

### Stratejiler Arası Etkileşim
| ID | Soru | Statü |
|---|---|---|
| `SI-001` | İki strategy aynı anda çalıştığında birbirlerinin fill kalitesini bozuyor mu? | YENİ / ÖNERİLEN |
| `SI-002` | Bir strategy'nin order flow'u diğer strategy'nin alpha'sını etkiliyor mu? | YENİ / ÖNERİLEN |
| `SI-003` | Strategy'ler aynı likidite havuzunu tüketiyor mu? | YENİ / ÖNERİLEN |
| `SI-004` | Aynı instrument üzerinde eşzamanlı strategy sayısı sınırlandırılıyor mu? | YENİ / ÖNERİLEN |
| `SI-005` | Strategy portfolio'sunun toplam execution footprint'i ölçülüyor mu? | YENİ / ÖNERİLEN |
| `SI-006` | Strategy interaction nedeniyle correlation sadece returns üzerinden değil order flow üzerinden de ölçülüyor mu? | YENİ / ÖNERİLEN |
| `SI-007` | Bir strategy'nin boyutu diğerinin edge half-life'ını değiştiriyor mu? | YENİ / ÖNERİLEN |
| `SI-008` | Capital allocation strategy interaction maliyetini içeriyor mu? | YENİ / ÖNERİLEN |
| `SI-009` | Strategy combination backtest overfitting yaratıyor mu? | YENİ / ÖNERİLEN |
| `SI-010` | Strategy ensemble gerçek incremental information sağlıyor mu? | YENİ / ÖNERİLEN |
| `SI-011` | Stratejilerin ortak feature dependency'si ölçülüyor mu? | YENİ / ÖNERİLEN |
| `SI-012` | Strateji çakışması alpha factor riskine yansıtılıyor mu? | YENİ / ÖNERİLEN |
| `SI-013` | Stratejiler aynı tail event altında birlikte zarar görüyor mu? | YENİ / ÖNERİLEN |
| `SI-014` | Bir strategy disable edildiğinde diğer strategy'lerin execution behavior'ı değişiyor mu? | YENİ / ÖNERİLEN |
| `SI-015` | Strategy interaction replay ile deterministik ölçülebiliyor mu? | YENİ / ÖNERİLEN |
| `SI-016` | Yeni strategy promotion mevcut portfolio'nun kapasitesini düşürüyorsa promotion buna göre sınırlandırılıyor mu? | YENİ / ÖNERİLEN |
| `SI-017` | Strategy conflict durumunda higher-safety outcome uygulanıyor mu? | YENİ / ÖNERİLEN |
| `SI-018` | Strategy interaction evidence certification scope'a dahil mi? | YENİ / ÖNERİLEN |
| `SI-019` | Strategy pairwise correlation dışında yüksek-order dependency ölçülüyor mu? | YENİ / ÖNERİLEN |
| `SI-020` | Strategy aynı ekonomik mekanizmayı farklı labels ile gizli biçimde çoğaltıyor mu? | YENİ / ÖNERİLEN |
| `SI-021` | Strategy family diversification bağımsız ekonomik mechanism'e dayanıyor mu? | YENİ / ÖNERİLEN |
| `SI-022` | Bir strategy kendi sibling strategy'lerinin fırsatlarını tüketiyor mu? | YENİ / ÖNERİLEN |
| `SI-023` | Strategy shutdown risklerini diğer strategy'lere taşıyor mu? | YENİ / ÖNERİLEN |
| `SI-024` | Strategy interaction nedeniyle portfolio optimizer yanlış leverage artışı üretebilir mi? | YENİ / ÖNERİLEN |
| `SI-025` | Strategy ecosystem değişimi için ayrı kill/disable scope var mı? | YENİ / ÖNERİLEN |

### Derin Mikro Yapı ve Emir Defteri Ekonomisi
| ID | Soru | Statü |
|---|---|---|
| `OBX-001` | Kuyruk pozisyonu için gözlenen ve çıkarımsal durum ayrımı korunuyor mu? | YENİ / ÖNERİLEN |
| `OBX-002` | Order lifetime dağılımı stratejiye özel izleniyor mu? | YENİ / ÖNERİLEN |
| `OBX-003` | Cancel/add/modify/execute oranları regime bazında ölçülüyor mu? | YENİ / ÖNERİLEN |
| `OBX-004` | Queue depletion hızı execution modeline dahil mi? | YENİ / ÖNERİLEN |
| `OBX-005` | Hidden/iceberg likidite olasılığı modelleniyor mu? | YENİ / ÖNERİLEN |
| `OBX-006` | Trade-through olayları tespit ediliyor mu? | YENİ / ÖNERİLEN |
| `OBX-007` | Locked/crossed book durumları ayrı risk durumu yaratıyor mu? | YENİ / ÖNERİLEN |
| `OBX-008` | Tick-size regime değişimleri microstructure alpha'sını etkiliyor mu? | YENİ / ÖNERİLEN |
| `OBX-009` | Auction davranışı strategy scope'una dahil edildiğinde doğru modelleniyor mu? | YENİ / ÖNERİLEN |
| `OBX-010` | Venue fragmentation nedeniyle aynı order flow olayının farklı venue'lerdeki karşılığı eşleştiriliyor mu? | YENİ / ÖNERİLEN |
| `OBX-011` | Cross-venue latency farkları execution modeline yansıyor mu? | YENİ / ÖNERİLEN |
| `OBX-012` | Microstructure state reconstruction deterministic mi? | YENİ / ÖNERİLEN |
| `OBX-013` | Book corruption detection ile data vendor drift ayrıştırılıyor mu? | YENİ / ÖNERİLEN |
| `OBX-014` | Queue model yanlışlandığında dependent strategy otomatik kapanıyor mu? | YENİ / ÖNERİLEN |
| `OBX-015` | Order book liquidity replenishment pattern'i zamanla drift ediyor mu? | YENİ / ÖNERİLEN |
| `OBX-016` | Adverse selection order lifetime ve spread birlikte kullanılarak ölçülüyor mu? | YENİ / ÖNERİLEN |
| `OBX-017` | Microstructure alpha'sının capacity'si order book depth ile ilişkilendiriliyor mu? | YENİ / ÖNERİLEN |
| `OBX-018` | Bir venue'de gözlenen queue davranışı diğer venue'ye taşınmadan önce sertifikalandırılıyor mu? | YENİ / ÖNERİLEN |
| `OBX-019` | MBO olmayan yerde queue-position iddiası açıkça INFERRED olarak işaretleniyor mu? | YENİ / ÖNERİLEN |
| `OBX-020` | Order book reset sonrasında yeniden certification gerekiyor mu? | YENİ / ÖNERİLEN |
| `OBX-021` | Sequence gap sonrası historical reconstruction ile live reconstruction aynı sonucu üretiyor mu? | YENİ / ÖNERİLEN |
| `OBX-022` | Book event timestamps ile trade timestamps arasında tutarsızlık detection var mı? | YENİ / ÖNERİLEN |
| `OBX-023` | Market impact modeli depth consumption ile uyumlu mu? | YENİ / ÖNERİLEN |
| `OBX-024` | Microstructure feature'larının gecikmesi edge half-life içinde mi? | YENİ / ÖNERİLEN |
| `OBX-025` | Order book signal predictive edge'inin execution feasibility ile birlikte ölçülmesi zorunlu mu? | YENİ / ÖNERİLEN |

### Uzun Vadeli Hayatta Kalma
| ID | Soru | Statü |
|---|---|---|
| `LH-001` | Sistem 1, 3, 5 ve 10 yıllık ufuklarda strateji hayatta kalmasını değerlendirebiliyor mu? | YENİ / ÖNERİLEN |
| `LH-002` | Kısa dönem noise ile uzun dönem edge decay ayrıştırılıyor mu? | YENİ / ÖNERİLEN |
| `LH-003` | Sistem yaşlandıkça model complexity azaltılabiliyor mu? | YENİ / ÖNERİLEN |
| `LH-004` | Eski feature'ların artık geçersiz olduğu tespit ediliyor mu? | YENİ / ÖNERİLEN |
| `LH-005` | Yeni nesil strategy'ler eski neslin hatalarını yeniden öğreniyor mu? | YENİ / ÖNERİLEN |
| `LH-006` | Uzun dönem performans farklı market profile'larda karşılaştırılıyor mu? | YENİ / ÖNERİLEN |
| `LH-007` | Uzun dönem capacity decay ölçülüyor mu? | YENİ / ÖNERİLEN |
| `LH-008` | Uzun dönem execution cost drift ölçülüyor mu? | YENİ / ÖNERİLEN |
| `LH-009` | Uzun dönem vendor drift geçmiş kararları etkilemeden geleceği etkiliyor mu? | YENİ / ÖNERİLEN |
| `LH-010` | Uzun dönem certification evidence immutable biçimde saklanıyor mu? | YENİ / ÖNERİLEN |
| `LH-011` | Uzun süre kullanılmayan strategy'nin sertifikası otomatik geçerli kabul ediliyor mu? | YENİ / ÖNERİLEN |
| `LH-012` | Piyasa yapısında nesiller arası değişim ölçülüyor mu? | YENİ / ÖNERİLEN |
| `LH-013` | Uzun dönem strategy family diversity korunuyor mu? | YENİ / ÖNERİLEN |
| `LH-014` | Research pipeline yıllar boyunca aynı selection bias'ı üretmiyor mu? | YENİ / ÖNERİLEN |
| `LH-015` | Question bank zaman içinde genişletilirken meta-overfitting kontrol ediliyor mu? | YENİ / ÖNERİLEN |
| `LH-016` | Uzun dönem model replacement sıklığı ile economic durability karşılaştırılıyor mu? | YENİ / ÖNERİLEN |
| `LH-017` | Sistem yeni technology/venue değişikliklerini önden test edebiliyor mu? | YENİ / ÖNERİLEN |
| `LH-018` | Uzun dönem regulatory veya market structure değişiklikleri için ayrı scenario setleri var mı? | YENİ / ÖNERİLEN |
| `LH-019` | Uzun drawdown dönemi strategy confidence'ını yapay olarak artırmıyor mu? | YENİ / ÖNERİLEN |
| `LH-020` | Uzun dönem success ile tek bir historic bull/bear period arasındaki ayrım korunuyor mu? | YENİ / ÖNERİLEN |
| `LH-021` | Uzun dönem portfolio survival bağımsız market shocks ile test ediliyor mu? | YENİ / ÖNERİLEN |
| `LH-022` | Strategy retirement/revival kayıtları nesiller boyunca korunuyor mu? | YENİ / ÖNERİLEN |
| `LH-023` | Long-horizon validation windows test-set contamination yaratmadan korunuyor mu? | YENİ / ÖNERİLEN |
| `LH-024` | Sistem yıllar sonra aynı kararın nedenini yeniden oluşturabiliyor mu? | YENİ / ÖNERİLEN |
| `LH-025` | 10 yıllık hedefte “kârlılık” yerine survival ve evidence kalitesi de ölçülüyor mu? | YENİ / ÖNERİLEN |

### Meta-Overfitting ve Sınavın Kendisine Uyum
| ID | Soru | Statü |
|---|---|---|
| `MO-001` | Sistem kendi sertifikasyon kriterlerine overfit olmuş olabilir mi? | YENİ / ÖNERİLEN |
| `MO-002` | Question bank değişiklikleri seçim yanlılığı yaratıyor mu? | YENİ / ÖNERİLEN |
| `MO-003` | Yeni sorular eklendikçe geçmiş sonuçların anlamı değişiyor mu? | YENİ / ÖNERİLEN |
| `MO-004` | Certification threshold'ları geçmiş performansa göre optimize edilmiş mi? | YENİ / ÖNERİLEN |
| `MO-005` | Question wording değişikliği model davranışını bilinçsizce etkiliyor mu? | YENİ / ÖNERİLEN |
| `MO-006` | Aynı dataset ile çok sayıda farklı certification rule deneniyor mu? | YENİ / ÖNERİLEN |
| `MO-007` | En iyi rule set seçildikten sonra selection pressure kaydediliyor mu? | YENİ / ÖNERİLEN |
| `MO-008` | Question bank tuning ayrı bir research trial olarak kayıtlı mı? | YENİ / ÖNERİLEN |
| `MO-009` | Certification process'inin kendisi bağımsız test setinde sınanıyor mu? | YENİ / ÖNERİLEN |
| `MO-010` | Model certification workflow'u “sınavı geçmeyi” öğrenebiliyor mu? | YENİ / ÖNERİLEN |
| `MO-011` | Certification evidence ile research evidence ayrılıyor mu? | YENİ / ÖNERİLEN |
| `MO-012` | Bir rule yalnızca bir strategy'yi kurtarmak için gevşetilmiş olabilir mi? | YENİ / ÖNERİLEN |
| `MO-013` | Sık threshold değişiklikleri hidden parameter tuning oluşturuyor mu? | YENİ / ÖNERİLEN |
| `MO-014` | Question bank coverage artışı gerçek risk coverage artışı ile doğrulanıyor mu? | YENİ / ÖNERİLEN |
| `MO-015` | Aynı failure scenario farklı adlarla tekrar edilip sahte coverage yaratıyor mu? | YENİ / ÖNERİLEN |
| `MO-016` | Question similarity ve redundancy ölçülüyor mu? | YENİ / ÖNERİLEN |
| `MO-017` | 100 benzer soru tek bir bağımsız kanıt gibi yanlış sayılıyor mu? | YENİ / ÖNERİLEN |
| `MO-018` | Question family sonuçları evidence independence açısından gruplanıyor mu? | YENİ / ÖNERİLEN |
| `MO-019` | Certification test seti question bank tarafından zamanla “öğrenilebilir” hale geliyor mu? | YENİ / ÖNERİLEN |
| `MO-020` | Adversarial scenarios hidden test setinde tutulabiliyor mu? | YENİ / ÖNERİLEN |
| `MO-021` | Question bank için ayrı train/validation/test split uygulanıyor mu? | YENİ / ÖNERİLEN |
| `MO-022` | Yeni question üretiminde geçmiş failure evidence kullanılırken leakage engelleniyor mu? | YENİ / ÖNERİLEN |
| `MO-023` | Question bank kendi başarısını measured economic outcome ile doğruluyor mu? | YENİ / ÖNERİLEN |
| `MO-024` | Question bank değişiklikleri için versioned impact analysis var mı? | YENİ / ÖNERİLEN |
| `MO-025` | Meta-overfitting tespit edilirse certification derhal duruyor mu? | YENİ / ÖNERİLEN |

---
## 4. V2.3.1 kurumsal-düzey hardening genişletmesi — 213 yeni soru

Bu bölüm; ilk V2.3 taslağında eksik kalan seçim-ayarlı istatistik, execution gizliliği, piyasa bütünlüğü, venue/broker/counterparty, siber ve adversarial ML, operasyonel dayanıklılık, varlık-sınıfı koşulları ve yönetişim alanlarını tamamlar.

### İstatistiksel Geçerlilik ve Ardışık Çıkarım — SV
| ID | Soru | Statü |
|---|---|---|
| SV-001 | Araştırmada denenmiş tüm strateji, özellik, hedef, ufuk ve parametrelerin birleşik trial evreni değişmez biçimde kaydediliyor mu? | YENİ / ÖNERİLEN |
| SV-002 | İnsan tarafından manuel elenen denemeler de search budget ve selection pressure hesabına giriyor mu? | YENİ / ÖNERİLEN |
| SV-003 | White Reality Check veya eşdeğer veri-snooping düzeltmesinin uygulanabilirliği politika ile belirlenmiş mi? | YENİ / ÖNERİLEN |
| SV-004 | Hansen SPA veya eşdeğer üstün tahmin testi, çok sayıdaki zayıf alternatifin etkisini ele alıyor mu? | YENİ / ÖNERİLEN |
| SV-005 | DSR hesabı deneme sayısı, çarpıklık, basıklık ve seri bağımlılık girdilerini eksiksiz kullanıyor mu? | YENİ / ÖNERİLEN |
| SV-006 | PBO/CSCV tasarımı zamansal bağımlılığı ve strateji seçim sürecini bozmayacak şekilde uygulanıyor mu? | YENİ / ÖNERİLEN |
| SV-007 | Bootstrap veya yeniden örnekleme blok uzunluğu önceden tanımlı ve bağımlılık yapısına uygun mu? | YENİ / ÖNERİLEN |
| SV-008 | Çapraz varlık, çapraz strateji ve ortak olay bağımlılığı etkin örnek büyüklüğünde hesaba katılıyor mu? | YENİ / ÖNERİLEN |
| SV-009 | Örtüşen label ve pozisyon süreleri bağımsız gözlemmiş gibi sayılmıyor mu? | YENİ / ÖNERİLEN |
| SV-010 | Canlı performansın sürekli izlenmesi optional stopping ve repeated testing yanlılığına karşı düzeltiliyor mu? | YENİ / ÖNERİLEN |
| SV-011 | Birden fazla hedef, zaman ufku, rejim ve metriğin birlikte test edilmesi çoklu test ailesine dahil mi? | YENİ / ÖNERİLEN |
| SV-012 | Kazanan stratejinin güven aralığı seçim yapıldıktan sonra selection-adjusted olarak yeniden hesaplanıyor mu? | YENİ / ÖNERİLEN |
| SV-013 | Benchmark testten önce dondurulmuş, uygulanabilir ve aynı maliyet/kapasite varsayımlarına tabi mi? | YENİ / ÖNERİLEN |
| SV-014 | Strateji nakit, basit beta, eşit ağırlık ve uygun pasif/naif bazlarla karşılaştırılıyor mu? | YENİ / ÖNERİLEN |
| SV-015 | Sonuçların birkaç uç kazanç, tek dönem veya tek enstrümana bağımlılığı raporlanıyor mu? | YENİ / ÖNERİLEN |
| SV-016 | Leave-one-regime-out ve leave-one-event-cluster-out dayanıklılık testleri uygulanabilir olduğunda çalıştırılıyor mu? | YENİ / ÖNERİLEN |
| SV-017 | Parametre optimumu dar bir tepe yerine ekonomik olarak açıklanabilir bir plato oluşturuyor mu? | YENİ / ÖNERİLEN |
| SV-018 | Küçük veri, maliyet, gecikme ve parametre değişiklikleri edge işaretini veya büyüklüğünü tersine çeviriyor mu? | YENİ / ÖNERİLEN |
| SV-019 | Non-stationarity altında güven aralıklarının geçerliliği ayrıca sınanıyor mu? | YENİ / ÖNERİLEN |
| SV-020 | İstatistiksel anlamlılık ile gerçek maliyet sonrası ekonomik anlamlılık ayrı kapılar mı? | YENİ / ÖNERİLEN |
| SV-021 | İddia edilen Sharpe/EV için gereken minimum track record seçimden önce belirleniyor mu? | YENİ / ÖNERİLEN |
| SV-022 | Birincil performans metriği sonuçlar görülmeden önce kayıt altına alınıyor mu? | YENİ / ÖNERİLEN |
| SV-023 | Sıfır-edge, ters yön, gecikmeli sinyal ve rastgeleleştirilmiş sinyal null modelleri birlikte sınanıyor mu? | YENİ / ÖNERİLEN |
| SV-024 | Sayısal kütüphane, seed, donanım ve paralellik değişiminde sonuçların tolerans dahilinde yeniden üretilebilirliği kanıtlanıyor mu? | YENİ / ÖNERİLEN |
| SV-025 | Üretici ekipten bağımsız bir doğrulayıcı model, veri, backtest ve sonuç yorumunu gerçekten challenge ediyor mu? | YENİ / ÖNERİLEN |

### Execution Gizliliği, Routing ve Venue Gaming — EP
| ID | Soru | Statü |
|---|---|---|
| EP-001 | Child-order zamanlamasının tahmin edilebilirliği ölçülüyor mu? | YENİ / ÖNERİLEN |
| EP-002 | Emir büyüklüğü, fiyat adımı ve bekleme süresi dağılımı strateji parmak izi oluşturuyor mu? | YENİ / ÖNERİLEN |
| EP-003 | Cancel/replace paterni gelecekteki işlem niyetini dışarı sızdırıyor mu? | YENİ / ÖNERİLEN |
| EP-004 | Venue-routing tercihleri büyük emrin kalan yönü ve büyüklüğü hakkında sinyal üretiyor mu? | YENİ / ÖNERİLEN |
| EP-005 | Pasif/agresif mod geçişleri rakiplerce sınıflandırılabilecek kadar düzenli mi? | YENİ / ÖNERİLEN |
| EP-006 | Dolum sonrası kısa ve orta ufuk fiyat hareketi information leakage ve adverse selection için ölçülüyor mu? | YENİ / ÖNERİLEN |
| EP-007 | Gerçek execution, aynı piyasa koşullarındaki sertifikalı counterfactual schedule ile karşılaştırılıyor mu? | YENİ / ÖNERİLEN |
| EP-008 | Zamanlama veya boyut randomizasyonu kullanılırsa yalnızca sertifikalı risk, fiyat ve tamamlanma sınırları içinde mi kalıyor? | YENİ / ÖNERİLEN |
| EP-009 | Router sonucu görülen en iyi fiyata değil, o anda uygulanabilir en iyi net execution sonucuna göre değerlendiriliyor mu? | YENİ / ÖNERİLEN |
| EP-010 | Ücret, rebate, maker-taker teşviki ve order-type davranışı net routing kararına dahil mi? | YENİ / ÖNERİLEN |
| EP-011 | Dark/hidden venue dolumları fill oranıyla birlikte toxicity ve post-trade reversion açısından ölçülüyor mu? | YENİ / ÖNERİLEN |
| EP-012 | Venue, broker, zaman, boyut ve order type bazında koşullu adverse selection izleniyor mu? | YENİ / ÖNERİLEN |
| EP-013 | Last-look veya reject yeteneği olan venue'lerde kabul/red asimetrisi ve gecikmesi ölçülüyor mu? | YENİ / KOŞULLU |
| EP-014 | Kısmi dolumun kalan emir üzerindeki bilgi sızıntısı ve maliyeti modelleniyor mu? | YENİ / ÖNERİLEN |
| EP-015 | Kendi execution'ımızın ilişkili enstrüman, hedge ve diğer stratejiler üzerindeki çapraz etkisi ölçülüyor mu? | YENİ / ÖNERİLEN |
| EP-016 | Aynı enstrümanda çalışan stratejilerin emirleri birbirini front-run ediyor veya queue position bozuyor mu? | YENİ / ÖNERİLEN |
| EP-017 | Self-match prevention kapsamı hesap, strateji, session ve venue kimlikleri arasında doğrulanıyor mu? | YENİ / ÖNERİLEN |
| EP-018 | Cancel-on-disconnect ve venue kill araçlarının gerçek kapsamı, gecikmesi ve hata modu test ediliyor mu? | YENİ / ÖNERİLEN |
| EP-019 | Mesaj oranı, order-to-trade oranı ve venue throttle sınırları stres altında ihlal edilmeden korunuyor mu? | YENİ / ÖNERİLEN |
| EP-020 | Auction, halt reopen ve price-band durumlarında router ayrı ve sertifikalı davranış kullanıyor mu? | YENİ / KOŞULLU |
| EP-021 | Strateji edge'i düşük gecikmeli rakiplere rağmen kalıyor mu, yoksa sonuç yalnızca erişilemeyen latency avantajına mı dayanıyor? | YENİ / ÖNERİLEN |
| EP-022 | Stale quote, stale route veya venue-state gecikmesi yanlış venue seçimini otomatik veto ediyor mu? | YENİ / ÖNERİLEN |
| EP-023 | Dış broker execution algosu kullanılıyorsa karar, sürüm, parametre ve gerçekleşen davranış denetlenebilir mi? | YENİ / KOŞULLU |
| EP-024 | Router veya fill model drift'i venue kural değişikliği, piyasa değişimi ve kendi footprint'imizden ayrıştırılıyor mu? | YENİ / ÖNERİLEN |
| EP-025 | Gerçek zamanlı ve post-trade TCA bağımsız kaynaklarla mutabakatlı ve decision→order→fill lineage'ına bağlı mı? | YENİ / ÖNERİLEN |

### Piyasa Bütünlüğü ve Manipülasyona Dayanıklılık — MI
| ID | Soru | Statü |
|---|---|---|
| MI-001 | Sistem kendi emirlerinin spoofing veya layering benzeri görünmesine ya da davranmasına yol açabilecek paterni izliyor mu? | YENİ / ÖNERİLEN |
| MI-002 | Wash trade ve ekonomik sahiplik bazlı self-trade riski venue'ler ve hesaplar arasında ölçülüyor mu? | YENİ / ÖNERİLEN |
| MI-003 | Momentum ignition, marking-the-close/open ve fiyatı etkileme riski için davranışsal kontroller var mı? | YENİ / ÖNERİLEN |
| MI-004 | Gözetim tüm yeni emirleri, düzeltmeleri, iptalleri, redleri ve işlemleri kapsıyor mu? | YENİ / ÖNERİLEN |
| MI-005 | Cross-venue ve cross-product manipülasyon paternleri ilişkili enstrümanlar üzerinden değerlendiriliyor mu? | YENİ / ÖNERİLEN |
| MI-006 | Gözetim yalnızca gerçekleşen trade'lere değil, gerçekleşmeyen emir niyetinin davranışsal kanıtlarına da bakıyor mu? | YENİ / ÖNERİLEN |
| MI-007 | Alert eşiği değişiklikleri versiyonlu, onaylı ve geçmiş alert seti üzerinde yeniden doğrulanmış mı? | YENİ / ÖNERİLEN |
| MI-008 | Yanlış pozitif alert maliyeti ile kaçırılan kötüye kullanım riski ayrı ölçülüyor mu? | YENİ / ÖNERİLEN |
| MI-009 | Manipülasyon sinyali oluştuğunda yeni emir yetkisi ile mevcut risk azaltma yetkisi doğru ayrılıyor mu? | YENİ / ÖNERİLEN |
| MI-010 | Model veya AI, P&L amacıyla gözetim eşiğini gevşetemiyor mu? | YENİ / ÖNERİLEN |
| MI-011 | Araştırma optimizasyonu farkında olmadan yasa dışı veya düzensiz piyasa davranışını ödüllendiriyor mu? | YENİ / ÖNERİLEN |
| MI-012 | Quote stuffing veya mesaj fırtınası sahte likidite/yanlış sinyal ürettiğinde dependent strateji korunuyor mu? | YENİ / ÖNERİLEN |
| MI-013 | Hızlı ekle-iptal, iceberg, replenishment ve gerçek likidite birbirinden belirsizlikle ayrıştırılıyor mu? | YENİ / ÖNERİLEN |
| MI-014 | Pump-and-dump veya koordine sosyal medya akışı veri kaynağını ve alpha'yı karantinaya alabiliyor mu? | YENİ / KOŞULLU |
| MI-015 | Sahte haber, düzeltilmiş haber ve kaynak taklidi event engine tarafından tespit edilebiliyor mu? | YENİ / KOŞULLU |
| MI-016 | Anormal fiyat/volume olayı otomatik olarak trade sinyali sayılmadan önce bütünlük kontrollerinden geçiyor mu? | YENİ / ÖNERİLEN |
| MI-017 | Manipülasyon şüphesinde kullanılan order-book kanıtı tam, sıralı ve zaman senkronlu mu? | YENİ / ÖNERİLEN |
| MI-018 | Venue veya veri kaynağı eksikliği gözetimde kör nokta oluşturduğunda kapsam açıkça UNKNOWN oluyor mu? | YENİ / ÖNERİLEN |
| MI-019 | Gözetim alert'leri yetkin kişi tarafından zamanında ele alınıyor ve kapanış gerekçesi kanıtlanıyor mu? | YENİ / ÖNERİLEN |
| MI-020 | Manipülasyon kontrolü backtest, replay, shadow ve canlı loglarda aynı semantiği kullanıyor mu? | YENİ / ÖNERİLEN |
| MI-021 | Sistem, rakip manipülasyonuna tepki verirken kendisi düzensiz piyasa koşuluna katkıda bulunuyor mu? | YENİ / ÖNERİLEN |
| MI-022 | Piyasa bütünlüğü ihlali olasılığı strateji, hesap, venue ve global kapsamda ayrı izolasyon tetikleyebiliyor mu? | YENİ / ÖNERİLEN |
| MI-023 | Tüm gözetim istisnaları süreli, sahipli ve otomatik sona eren şekilde yönetiliyor mu? | YENİ / ÖNERİLEN |
| MI-024 | Regulatory inquiry veya venue talebi için order lifecycle ve karar gerekçesi eksiksiz yeniden üretilebiliyor mu? | YENİ / KOŞULLU |
| MI-025 | Uygulanabilir piyasa suistimali kuralları MarketProfile ve yargı alanı değiştiğinde yeniden değerlendiriliyor mu? | YENİ / KOŞULLU |

### Venue, Broker, Counterparty ve Saklama — VC
| ID | Soru | Statü |
|---|---|---|
| VC-001 | Broker, venue, clearing üyesi, custodian ve settlement bankası bağımlılıkları ayrı counterparty olarak kayıtlı mı? | YENİ / ÖNERİLEN |
| VC-002 | Counterparty exposure nakit, teminat, açık pozisyon, açık emir ve bekleyen settlement dahil ölçülüyor mu? | YENİ / ÖNERİLEN |
| VC-003 | Tek broker/venue/custodian yoğunluğu ve correlated failure riski politika ile sınırlandırılabilir mi? | YENİ / ÖNERİLEN |
| VC-004 | Broker API alanları ile ekonomik pozisyon, cash, margin ve order state semantiği birebir doğrulanmış mı? | YENİ / ÖNERİLEN |
| VC-005 | Broker/venue kural, API, fee, margin veya liquidation değişikliği otomatik recertification review açıyor mu? | YENİ / ÖNERİLEN |
| VC-006 | Intraday margin değişikliği ve house-margin artışı risk/capital yetkisini anında yeniden hesaplatıyor mu? | YENİ / ÖNERİLEN |
| VC-007 | Counterparty temerrüdü veya işlem kısıtı altında pozisyon kapatma, hedge ve transfer seçenekleri önceden modellenmiş mi? | YENİ / ÖNERİLEN |
| VC-008 | Müşteri varlıklarının segregation durumu kanıta dayalı mı; yalnızca broker beyanına güvenilmiyor mu? | YENİ / KOŞULLU |
| VC-009 | Custody anahtar, yetki, withdrawal ve recovery süreci least-privilege ve çoklu kontrol altında mı? | YENİ / KOŞULLU |
| VC-010 | Deposit/withdrawal/settlement gecikmesi likidite ve yeniden dengeleme riskine dahil mi? | YENİ / ÖNERİLEN |
| VC-011 | Failover broker'a geçiş duplicate order veya iki tarafta açık risk yaratmadan çalışıyor mu? | YENİ / ÖNERİLEN |
| VC-012 | Primary broker erişilemezken external truth kaynağıyla position/open-order reconciliation yapılabiliyor mu? | YENİ / ÖNERİLEN |
| VC-013 | Close-only, reduce-only, cancel-only ve maintenance modları ayrı yetki durumları olarak modelleniyor mu? | YENİ / ÖNERİLEN |
| VC-014 | Venue fiyatının referans piyasalardan sapması veri hatası, lokal likidite ve solvency riski açısından ayrıştırılıyor mu? | YENİ / ÖNERİLEN |
| VC-015 | Mark, index, settlement ve liquidation fiyatlarının kaynakları ile fallback hiyerarşisi doğrulanmış mı? | YENİ / KOŞULLU |
| VC-016 | Teminatın para birimi, haircut'ı, yeniden kullanım ve rehypothecation riski biliniyor mu? | YENİ / KOŞULLU |
| VC-017 | Stablecoin veya tokenized collateral depeg ve redemption riski sermaye hesabına giriyor mu? | YENİ / KOŞULLU |
| VC-018 | Broker/venue sağlık metriği finansal, operasyonel ve piyasa davranışı sinyallerini birbirine karıştırmadan izliyor mu? | YENİ / ÖNERİLEN |
| VC-019 | Counterparty sağlık sinyali UNKNOWN olduğunda yeni exposure fail-closed oluyor mu? | YENİ / ÖNERİLEN |
| VC-020 | Broker tarafından sunulan sigorta veya garanti kapsamı doğrulanmadan risk azaltıcı sayılmıyor mu? | YENİ / KOŞULLU |
| VC-021 | Settlement fail, trade bust, give-up ve allocation hataları accounting/reconciliation içinde ele alınıyor mu? | YENİ / KOŞULLU |
| VC-022 | Venue liquidation engine davranışı gap, illiquidity ve partial liquidation altında replay edilebiliyor mu? | YENİ / KOŞULLU |
| VC-023 | Bağlı counterparty'ler veya ortak altyapı nedeniyle görünmeyen yoğunlaşma tespit ediliyor mu? | YENİ / ÖNERİLEN |
| VC-024 | Counterparty çıkış planı veri, pozisyon, nakit ve kayıt taşınabilirliğini içeriyor mu? | YENİ / ÖNERİLEN |
| VC-025 | Counterparty risk kararı P&L veya daha iyi görünen fiyat nedeniyle aşılamıyor mu? | YENİ / ÖNERİLEN |

### Siber Güvenlik, Tedarik Zinciri ve Adversarial ML — CY
| ID | Soru | Statü |
|---|---|---|
| CY-001 | Üretim bağımlılıkları için sürüm kilidi, provenance ve SBOM benzeri envanter tutuluyor mu? | YENİ / ÖNERİLEN |
| CY-002 | Build ve deployment artefaktları imzalı ve doğrulanmış kaynaktan mı geliyor? | YENİ / ÖNERİLEN |
| CY-003 | Secret, API key ve signing key'ler ortam, rol ve yetenek bazında ayrılmış mı? | YENİ / ÖNERİLEN |
| CY-004 | Kritik erişimlerde MFA, least privilege, kısa ömürlü kimlik ve düzenli erişim incelemesi uygulanıyor mu? | YENİ / ÖNERİLEN |
| CY-005 | Anahtar rotasyonu açık emirler ve recovery yetkisini bozmadan test edilmiş mi? | YENİ / ÖNERİLEN |
| CY-006 | Güvenlik açığı bulunan dependency'nin etkilediği engine, veri ve sertifika scope'u çıkarılabiliyor mu? | YENİ / ÖNERİLEN |
| CY-007 | Development, research, test ve production ağları ile kimlikleri gerçekten ayrılmış mı? | YENİ / ÖNERİLEN |
| CY-008 | Market-data poisoning veya sahte feed enjeksiyonu bağımsız kaynak ve imza/transport kanıtıyla tespit ediliyor mu? | YENİ / ÖNERİLEN |
| CY-009 | Training data poisoning, label corruption ve backdoor örüntüleri için testler var mı? | YENİ / ÖNERİLEN |
| CY-010 | Adversarial input veya evasion, modelin yüksek güvenli yanlış karar üretmesine karşı sınanıyor mu? | YENİ / ÖNERİLEN |
| CY-011 | Model extraction veya strateji çalma riski log, API ve erişim düzeyinde izleniyor mu? | YENİ / ÖNERİLEN |
| CY-012 | Model/feature artefakt hash'i decision snapshot ve certification scope'a bağlı mı? | YENİ / ÖNERİLEN |
| CY-013 | Dış haber, belge veya web metni AI bileşenine prompt injection taşıdığında yetki yolu kapalı mı? | YENİ / KOŞULLU |
| CY-014 | LLM veya AI çıktısı veri, politika, risk, order ve reconciliation gerçeği yerine geçemiyor mu? | YENİ / KOŞULLU |
| CY-015 | AI context freshness, source provenance ve tool sonucu imza/kayıt zinciriyle doğrulanıyor mu? | YENİ / KOŞULLU |
| CY-016 | Broker callback, webhook ve execution report sahteciliği kimlik doğrulama ve replay protection ile engelleniyor mu? | YENİ / ÖNERİLEN |
| CY-017 | Zaman kaynağına saldırı veya clock manipulation kritik kararları fail-closed duruma geçiriyor mu? | YENİ / ÖNERİLEN |
| CY-018 | Audit log, karar defteri ve kanıt deposu silme/değiştirmeye karşı korumalı mı? | YENİ / ÖNERİLEN |
| CY-019 | Backup'lar ransomware, credential compromise ve sessiz veri bozulmasına karşı bağımsız doğrulanıyor mu? | YENİ / ÖNERİLEN |
| CY-020 | Güvenlik incident'i hangi scope'ların authorization lease'ini iptal edeceğini deterministik belirliyor mu? | YENİ / ÖNERİLEN |
| CY-021 | Güvenlik taraması yalnızca source code'u değil container, dependency, config ve infrastructure tanımını kapsıyor mu? | YENİ / ÖNERİLEN |
| CY-022 | Kritik güvenlik kontrolünün kendisi bypass, race condition ve fail-open davranışına karşı test ediliyor mu? | YENİ / ÖNERİLEN |
| CY-023 | Third-party model, veri, paket veya broker SDK güncellemesi doğrulanmadan production'a giremiyor mu? | YENİ / ÖNERİLEN |
| CY-024 | Incident recovery sonrasında tüm secret, artefakt ve state doğrulanmadan trading yetkisi geri gelmiyor mu? | YENİ / ÖNERİLEN |
| CY-025 | Adversarial ML tehdit modeli saldırganın amacı, bilgisi, erişimi, yaşam-döngüsü aşaması ve beklenen etkisini açıkça kaydediyor mu? | YENİ / ÖNERİLEN |

### Operasyonel Dayanıklılık ve İnsan Faktörleri — OR
| ID | Soru | Statü |
|---|---|---|
| OR-001 | Kritik işlevler ve bunların kabul edilebilir kesinti toleransları politika ile tanımlı mı? | YENİ / ÖNERİLEN |
| OR-002 | Her kritik işlev için RTO/RPO ve veri kaybı etkisi bağlanmış mı? | YENİ / ÖNERİLEN |
| OR-003 | Tek kişi, tek cihaz, tek ISP, tek bölge veya tek cloud bağımlılığı haritalanmış mı? | YENİ / ÖNERİLEN |
| OR-004 | Birincil ve yedek sistemlerin aynı güç, ağ, DNS, kimlik veya vendor arızasına bağlı olmadığı kanıtlanıyor mu? | YENİ / ÖNERİLEN |
| OR-005 | Runbook'lar son incident ve sistem sürümüyle uyumlu ve gerçek tatbikatta çalıştırılmış mı? | YENİ / ÖNERİLEN |
| OR-006 | On-call ve eskalasyon zinciri ilgili piyasa saatlerinde erişilebilir ve yetkin mi? | YENİ / ÖNERİLEN |
| OR-007 | Startup, shutdown, restart ve failover state machine'leri açık emir ve pozisyonlarla birlikte test edilmiş mi? | YENİ / ÖNERİLEN |
| OR-008 | Disk, bellek, CPU, ağ, connection pool ve event backlog tükenmesi güvenli degradasyona yol açıyor mu? | YENİ / ÖNERİLEN |
| OR-009 | Backpressure altında kritik risk/reconciliation olayları düşük öncelikli telemetry tarafından engellenmiyor mu? | YENİ / ÖNERİLEN |
| OR-010 | Daylight-saving, leap second, takvim ve tatil değişiklikleri MarketProfile bazında test edilmiş mi? | YENİ / ÖNERİLEN |
| OR-011 | Elektrik, UPS, workstation, işletim sistemi ve yerel ağ kesintileri için gerçekçi recovery kanıtı var mı? | YENİ / ÖNERİLEN |
| OR-012 | Beklenen yüksek volatilite/event pencerelerinde change-freeze veya daha sıkı deployment politikası tanımlı mı? | YENİ / ÖNERİLEN |
| OR-013 | Canary veya kontrollü deployment, sermaye ve enstrüman kapsamını gerçekten sınırlandırıyor mu? | YENİ / ÖNERİLEN |
| OR-014 | Rollback yalnızca kodu değil schema, config, policy, model ve açık pozisyon etkisini kapsıyor mu? | YENİ / ÖNERİLEN |
| OR-015 | Chaos/failure injection üretim yetkisi vermeden gerçek dependency graph üzerinde tekrarlanabiliyor mu? | YENİ / ÖNERİLEN |
| OR-016 | Alert fırtınası ve alert fatigue kritik alarmın görülmesini engelliyor mu? | YENİ / ÖNERİLEN |
| OR-017 | Her alarmın sahibi, zaman bütçesi, otomatik eylemi ve kapanış kanıtı tanımlı mı? | YENİ / ÖNERİLEN |
| OR-018 | Manual input veya override yanlış format, stale context ve yanlış hesap seçimine karşı doğrulanıyor mu? | YENİ / ÖNERİLEN |
| OR-019 | Yüksek etkili değişiklik veya kurtarma eylemi için gerekli bağımsız kontrol/iki kişi kuralı uygulanabilir mi? | YENİ / ÖNERİLEN |
| OR-020 | Operatör yorgunluğu, saat dilimi, eğitim eksikliği ve erişilemezlik incident senaryolarında ele alınıyor mu? | YENİ / ÖNERİLEN |
| OR-021 | Incident severity ekonomik zarar, veri bütünlüğü, yetki kaybı ve piyasa bütünlüğünü birlikte değerlendiriyor mu? | YENİ / ÖNERİLEN |
| OR-022 | Postmortem suçlama yerine kök neden, kaçan kontrol, kanıt ve tekrar önleme eylemini kaydediyor mu? | YENİ / ÖNERİLEN |
| OR-023 | Recovery'nin tamamlandığını söyleyen bileşen, recovery'yi gerçekleştiren bileşenden bağımsız doğrulanıyor mu? | YENİ / ÖNERİLEN |
| OR-024 | Uzun kesinti sonrası veri backfill ve state rebuild sırasında yeni trading yetkisi kapalı kalıyor mu? | YENİ / ÖNERİLEN |
| OR-025 | Dayanıklılık testi yalnızca sistemin ayağa kalkmasını değil doğru ekonomik ve dış durumla uzlaşmasını kanıtlıyor mu? | YENİ / ÖNERİLEN |

### MarketProfile-Koşullu Varlık Sınıfı Ekleri — 45 soru

Bu sorular yalnızca ilgili varlık sınıfı MarketProfile kapsamındaysa etkinleşir. Kapsam dışı olmak, kanıtsız atlama değil NOT_APPLICABLE + EVIDENCE gerektirir.

#### Hisse / ETF — EQX
| ID | Soru | Statü |
|---|---|---|
| EQX-001 | Split, reverse split, temettü, rights, spin-off ve merger ayarlamaları point-in-time doğru mu? | YENİ / KOŞULLU |
| EQX-002 | Symbol, listing venue ve kalıcı instrument identity tarihsel olarak doğru eşleniyor mu? | YENİ / KOŞULLU |
| EQX-003 | Delist edilmiş ve iflas etmiş enstrümanlar universe'den geriye dönük silinmeden korunuyor mu? | YENİ / KOŞULLU |
| EQX-004 | Halt, LULD/price-band ve reopen auction davranışları veri, risk ve execution katmanında modelleniyor mu? | YENİ / KOŞULLU |
| EQX-005 | Short locate, borrow availability, borrow fee ve recall riski decision-time gerçeğiyle bağlı mı? | YENİ / KOŞULLU |
| EQX-006 | Primary listing, ADR, cross-listing ve currency dönüşümü aynı ekonomik exposure olarak doğru ilişkilendiriliyor mu? | YENİ / KOŞULLU |
| EQX-007 | Open/close auction imbalance ve fill kuralları venue sürümüne göre replay ediliyor mu? | YENİ / KOŞULLU |
| EQX-008 | ETF NAV/iNAV, basket, creation-redemption ve underlying market saat farkı basis riskine dahil mi? | YENİ / KOŞULLU |
| EQX-009 | Corporate action veya symbol değişiminde açık emir, stop ve position semantics yeniden doğrulanıyor mu? | YENİ / KOŞULLU |

#### Vadeli İşlem — FTX
| ID | Soru | Statü |
|---|---|---|
| FTX-001 | Expiry, first-notice, last-trade ve delivery takvimi instrument master'da bağlayıcı mı? | YENİ / KOŞULLU |
| FTX-002 | Fiziksel teslim ve cash settlement riski yanlışlıkla açık pozisyonda bırakılamıyor mu? | YENİ / KOŞULLU |
| FTX-003 | Continuous contract serisi gerçek trade edilebilir kontrat ve roll maliyetinden ayrılıyor mu? | YENİ / KOŞULLU |
| FTX-004 | Roll kuralı karar anında bilinen likidite, basis ve calendar spread'e dayanıyor mu? | YENİ / KOŞULLU |
| FTX-005 | Contract multiplier, tick value, currency ve fiyatlama convention değişiklikleri deterministik mi? | YENİ / KOŞULLU |
| FTX-006 | Limit-up/down, velocity logic ve exchange emergency action altında risk ve exit davranışı test edilmiş mi? | YENİ / KOŞULLU |
| FTX-007 | Initial/maintenance/house margin ve intraday değişiklikleri liquidation riskine giriyor mu? | YENİ / KOŞULLU |
| FTX-008 | Calendar/inter-commodity spread bacak riski ve legging maliyeti modelleniyor mu? | YENİ / KOŞULLU |
| FTX-009 | Position/accountability limit ve aggregation kuralları uygulanabilir scope'a bağlı mı? | YENİ / KOŞULLU |

#### Opsiyon — OPX
| ID | Soru | Statü |
|---|---|---|
| OPX-001 | Option symbology, expiry, strike, multiplier ve adjustment history kalıcı identity ile bağlı mı? | YENİ / KOŞULLU |
| OPX-002 | Surface verisi no-arbitrage, stale quote ve crossed-market kontrollerinden geçiyor mu? | YENİ / KOŞULLU |
| OPX-003 | Rate, dividend, borrow ve forward girdileri decision-time vintage ile fiyatlamaya giriyor mu? | YENİ / KOŞULLU |
| OPX-004 | Exercise, assignment ve early-exercise riski pozisyon/sermaye hesabında ele alınıyor mu? | YENİ / KOŞULLU |
| OPX-005 | Pin risk ve expiry yakınında gamma/likidite sıçraması stres ediliyor mu? | YENİ / KOŞULLU |
| OPX-006 | Volatility jump, skew shift ve correlation break altında Greeks/model risk yeniden hesaplanıyor mu? | YENİ / KOŞULLU |
| OPX-007 | Multi-leg emirlerde legging, partial fill ve cancel sonrası artık exposure modelleniyor mu? | YENİ / KOŞULLU |
| OPX-008 | American/European style, settlement type ve exercise cutoff venue/contract bazında doğru mu? | YENİ / KOŞULLU |
| OPX-009 | Vendor Greeks veya GEX doğrudan gözlem değil VENDOR_MODEL/INFERRED olarak kaynak ve belirsizliğiyle tutuluyor mu? | YENİ / KOŞULLU |

#### FX / NDF — FXX
| ID | Soru | Statü |
|---|---|---|
| FXX-001 | Merkezi olmayan venue yapısında piyasa fiyatı ve likidite kapsamı açıkça tanımlı mı? | YENİ / KOŞULLU |
| FXX-002 | Last-look, reject, requote ve asymmetric hold time execution kalitesine dahil mi? | YENİ / KOŞULLU |
| FXX-003 | Settlement/Herstatt riski, value date ve cut-off saatleri sermaye ve counterparty riskine giriyor mu? | YENİ / KOŞULLU |
| FXX-004 | Tom-next, swap, rollover ve holiday carry maliyetleri point-in-time doğru mu? | YENİ / KOŞULLU |
| FXX-005 | Base/quote orientation, pip/tick precision ve currency conversion deterministik mi? | YENİ / KOŞULLU |
| FXX-006 | Bölgesel tatiller ve session overlap likidite/cost modeline bağlanmış mı? | YENİ / KOŞULLU |
| FXX-007 | NDF fixing source, fixing window ve settlement currency riski doğrulanmış mı? | YENİ / KOŞULLU |
| FXX-008 | Prime broker credit line ve venue-specific limit değişikliği execution authority'yi etkiliyor mu? | YENİ / KOŞULLU |
| FXX-009 | Dealer/venue fiyat farklılıkları stale quote, toxicity ve gerçek fragmentasyon olarak ayrıştırılıyor mu? | YENİ / KOŞULLU |

#### Kripto / Dijital Varlık — CRX
| ID | Soru | Statü |
|---|---|---|
| CRX-001 | Exchange, custodian, stablecoin issuer ve blockchain ağ riski birbirinden ayrı ölçülüyor mu? | YENİ / KOŞULLU |
| CRX-002 | Stablecoin depeg, redemption gecikmesi ve quote-currency solvency riski tüm P&L/sermaye hesabına giriyor mu? | YENİ / KOŞULLU |
| CRX-003 | Mark/index/oracle bileşenleri, ağırlıkları ve fallback'leri sürüm ve kaynakla doğrulanıyor mu? | YENİ / KOŞULLU |
| CRX-004 | 24/7 piyasada bakım, upgrade ve düşük personel kapsaması güvenli operasyon planına bağlı mı? | YENİ / KOŞULLU |
| CRX-005 | Chain reorg, fork, finality ve network congestion deposit/withdrawal/settlement riskine giriyor mu? | YENİ / KOŞULLU |
| CRX-006 | Funding, auto-deleveraging ve liquidation cascade birlikte stres ediliyor mu? | YENİ / KOŞULLU |
| CRX-007 | Withdrawal halt veya transfer kısıtı oluştuğunda venue içi kâr kullanılabilir nakit sayılmıyor mu? | YENİ / KOŞULLU |
| CRX-008 | Token migration, airdrop, redenomination ve contract change instrument lifecycle içinde yönetiliyor mu? | YENİ / KOŞULLU |
| CRX-009 | Venue insolvency, müşteri varlığı segregation belirsizliği ve hukuki yetki alanı counterparty limitine giriyor mu? | YENİ / KOŞULLU |

### Yönetişim, Hukuk, Muhasebe ve Teşvikler — GV
| ID | Soru | Statü |
|---|---|---|
| GV-001 | Her MarketProfile için geçerli yargı alanı, hesap türü, venue ve ürün kapsamı açık mı? | YENİ / ÖNERİLEN |
| GV-002 | Uygulanabilir düzenleme, venue rulebook, broker sözleşmesi ve veri lisansı envanteri sürümleniyor mu? | YENİ / ÖNERİLEN |
| GV-003 | Düzenleyici veya sözleşmesel değişiklik ilgili strategy/certification scope'u otomatik review'a alıyor mu? | YENİ / ÖNERİLEN |
| GV-004 | Veri entitlement ve yeniden kullanım hakkı araştırma, replay ve production için ayrı doğrulanıyor mu? | YENİ / ÖNERİLEN |
| GV-005 | Yasaklı/kısıtlı enstrüman, hesap, bölge ve işlem türü emirden önce veto ediliyor mu? | YENİ / KOŞULLU |
| GV-006 | Kayıt saklama süresi ve içeriği karar, emir, iletişim, model ve policy kanıtını kapsıyor mu? | YENİ / KOŞULLU |
| GV-007 | Model owner, validation owner, risk owner ve production approver sorumlulukları ayrılmış mı? | YENİ / ÖNERİLEN |
| GV-008 | Aynı kişi maddi kuralı yazıp doğrulayıp canlıya alma yetkisini tek başına kullanamıyor mu? | YENİ / ÖNERİLEN |
| GV-009 | Vendor, broker, rebate ve fee teşvikleri karar kalitesini çarpıtan conflict olarak kaydediliyor mu? | YENİ / ÖNERİLEN |
| GV-010 | Performans teşviki drawdown, tail risk veya kontrol ihlalini gizlemeyi ödüllendirmiyor mu? | YENİ / ÖNERİLEN |
| GV-011 | Muhasebe para birimi, realized/unrealized P&L, fee, funding, tax lot ve settlement politikası deterministik mi? | YENİ / ÖNERİLEN |
| GV-012 | Vergi ve raporlama sonucu ekonomik başarı hesabından ayrıştırılmadan doğru şekilde dahil ediliyor mu? | YENİ / KOŞULLU |
| GV-013 | Question bank değişiklikleri trial/search budget ve certification history içinde kaydediliyor mu? | YENİ / ÖNERİLEN |
| GV-014 | İstisna/waiver yalnızca süreli, kapsamlı, sahipli ve risk azaltıcı koşullarla verilebiliyor mu? | YENİ / ÖNERİLEN |
| GV-015 | İstisna süresi dolduğunda yetki otomatik olarak daha güvenli duruma dönüyor mu? | YENİ / ÖNERİLEN |
| GV-016 | Dış denetim veya bağımsız review gerekli kanıt paketini yeniden üretebiliyor mu? | YENİ / ÖNERİLEN |
| GV-017 | Uygulanabilir hukuk belirsizse sistem bunu UNKNOWN olarak ele alıp ilgili yeni riski blokluyor mu? | YENİ / KOŞULLU |
| GV-018 | Kâr hedefi, performans baskısı veya fırsat kaçırma korkusu risk, bütünlük, hukuk ve reconciliation veto'larını aşamıyor mu? | YENİ / ÖNERİLEN |

---
## 5. Genişletme ilkeleri
- Bir soru yalnızca ölçülebilir bir cevap ve kayıtlı evidence ile anlamlıdır.
- Aynı riski farklı kelimelerle tekrar eden sorular bağımsız kanıt sayılamaz.
- Bir sorunun cevabı bilinmiyorsa belirsizlik gizlenemez.
- Yeni sorular trading davranışı icat etmek için değil, eksik davranışları görünür kılmak için kullanılır.
- Yeni bir hard rule gerekiyorsa Change Request → Impact Analysis → Contract Version → Test → Approval → Implementation → Recertification yolu izlenir.
- Question bank kendisi de meta-overfitting testine tabi tutulmalıdır.
- Uzun dönem adaptasyon, her drift olayında değişmek değil; değişimin gerçek, kalıcı ve ekonomik olarak anlamlı olduğunu kanıtlamak demektir.

## 6. Doğrulanmış araştırma ve standart dayanakları

Bu kaynaklar soru üretme ve kontrol kapsamını genişletme dayanağıdır; tek başına projeye yeni trading yetkisi veya sayısal eşik vermez. Düzenleyici kaynakların uygulanabilirliği MarketProfile, hesap/broker türü ve yargı alanına göre hukuk incelemesi gerektirir.

### Resmî ve gözetim kaynakları
- [EU RTS 6 — algorithmic trading systems, testing, controlled deployment, kill function, surveillance ve business continuity](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX%3A32017R0589) — OR, MI, EP, GV.
- [FCA 2025 multi-firm review of algorithmic trading controls](https://www.fca.org.uk/publications/multi-firm-reviews/algorithmic-trading-controls-high-level-observations) — governance, development/testing, risk controls ve market-abuse surveillance.
- [SEC Rule 15c3-5 — Market Access Risk Controls](https://www.sec.gov/files/rules/final/2010/34-63241-secg.htm) — pre-trade financial/regulatory controls ve düzenli etkinlik incelemesi.
- [FINRA Regulatory Notice 15-09 — Algorithmic Trading Supervision](https://www.finra.org/rules-guidance/notices/15-09) — geliştirme, test, doğrulama, supervision ve control practices.
- [SEC Report to Congress on Algorithmic Trading](https://www.sec.gov/files/algo_trading_report_2020.pdf) — fragmentasyon, order types, latency ve piyasa yapısı.
- [FINRA Manipulative Trading](https://www.finra.org/rules-guidance/guidance/reports/2025-finra-annual-regulatory-oversight-report/manipulative-trading) — layering, spoofing, momentum ignition, wash sales ve cross-product surveillance.
- [SEC Regulation SCI](https://www.sec.gov/files/rules/final/2014/34-73639.pdf) — capacity, integrity, resiliency, availability, security, stress ve BC/DR.
- [CME risk tools and safeguards](https://www.cmegroup.com/clearing/files/financialsafeguards.pdf) — kill switch ve venue-side risk controls.
- [Federal Reserve SR 26-2 — Revised Guidance on Model Risk Management](https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm) — risk-bazlı model yönetişimi; 17 Nisan 2026 itibarıyla SR 11-7'nin yerini almıştır.
- [NIST AI 100-2e2025 — Adversarial Machine Learning Taxonomy](https://csrc.nist.gov/pubs/ai/100/2/e2025/final) — poisoning, evasion, model/AI lifecycle tehdit modeli.
- [NIST SP 800-218 — Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final) — güvenli yazılım yaşam döngüsü ve tedarik zinciri.
- [Basel Committee Principles for Operational Resilience](https://www.bis.org/bcbs/publ/d516.htm) — kritik operasyonların kesinti boyunca sürdürülebilmesi.
- [Basel Committee Counterparty Credit Risk Guidelines](https://www.bis.org/bcbs/publ/d588.htm) — counterparty risk ölçüm, yönetişim ve kontrol ilkeleri.
- [IOSCO Crypto and Digital Asset Markets Recommendations](https://www.iosco.org/library/pubdocs/pdf/IOSCOPD747.pdf) — custody, conflict, market integrity ve operasyonel risk.
- [FSB Global Regulatory Framework for Crypto-asset Activities](https://www.fsb.org/2023/07/fsb-global-regulatory-framework-for-crypto-asset-activities/) — crypto activity, stablecoin ve cross-border risk çerçevesi.

### Birincil araştırma kaynakları
- [Bailey et al. — The Probability of Backtest Overfitting](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253) — PBO ve selection risk.
- [Bailey & López de Prado — The Deflated Sharpe Ratio](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551) — multiple testing, non-normality ve selection-adjusted Sharpe.
- [White — A Reality Check for Data Snooping](https://onlinelibrary.wiley.com/doi/abs/10.1111/1468-0262.00152) — data-snooping düzeltmesi.
- [Hansen — A Test for Superior Predictive Ability](https://www.tandfonline.com/doi/abs/10.1198/073500105000000063) — çoklu model karşılaştırmasında SPA.
- [Almgren & Chriss — Optimal Execution of Portfolio Transactions](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=53501) — market impact, execution cost ve risk dengesi.
- [Cabral et al. — Non-stationarity in Financial Time Series](https://www.sciencedirect.com/science/article/pii/S092523122602045X) — drift, structural break ve adaptif değerlendirme taksonomisi.
- [Colliard et al. — Algorithmic Pricing and Liquidity in Securities Markets](https://academic.oup.com/rfs/advance-article/doi/10.1093/rfs/hhag010/8489056) — öğrenen market maker'ların adverse selection ve rekabetçi fiyatlamaya adaptasyonu.

## 7. Zorunlu sınav kayıt şeması

Her soru sonucu en az şu alanları taşımalıdır:

| Alan | Zorunlu anlam |
|---|---|
| QUESTION_ID | Bu bankadaki benzersiz kimlik |
| QUESTION_VERSION | İfadenin ve semantiğin sürümü |
| SCOPE_HASH | MarketProfile + strategy + model + data + venue + account + policy kapsamı |
| APPLICABILITY | APPLICABLE veya kanıtlı NOT_APPLICABLE |
| CRITICALITY | PRODUCTION_BLOCKING / CONDITIONAL_BLOCKING / ADVISORY |
| STATUS | PASS / FAIL / UNKNOWN / NOT_APPLICABLE |
| INFORMATION_CLASS | OBSERVED / DERIVED / INFERRED / VENDOR_MODEL / UNKNOWN / UNAVAILABLE |
| EVIDENCE_ID | Değişmez kanıt kimliği; PASS için zorunlu |
| CONTRACT_ID | Bağlayıcı gereksinim |
| POLICY_ID | Sayısal eşik ve karar semantiği |
| TEST_ID | Çalıştırılmış test |
| SCENARIO_ID | Varsa failure/adversarial senaryo |
| OBSERVATION_WINDOW | Başlangıç, bitiş ve decision-time cut-off |
| FAIL_ACTION | Bloklama, azaltma, izolasyon, rollback veya change request |
| OWNER / APPROVER | Üreten ve bağımsız onaylayan taraf |
| RECERTIFICATION_STATUS | Kapsam değişimi sonrası güncel durum |

PASS ancak uygulanabilir scope için gerekli contract/policy/test bağları mevcutsa, test gerçekten çalıştırılmışsa, kanıt değişmezse ve scope hash tam eşleşiyorsa geçerlidir. Dashboard rengi, belge varlığı, test skeleton'ı veya niyet beyanı PASS değildir.

## 8. Kabul ve hazır oluş kararı

- İlk 237 soru V2.2.5 bağlayıcı çekirdeği olarak kalır.
- Sonraki 663 soru CR-V2.3.1-ASQ-001 kapsamında öneridir; onaysız biçimde üretim yetkisi veya sayısal politika yaratmaz.
- Bu bankanın yayınlanması R1/R2/R3/R4 statülerini yükseltmez.
- Yeni soruların mevcut sonucu UNKNOWN / NOT_EXECUTED'tır.
- İlk uygulama dalgası; SV, EP, MI, VC, CY ve OR ailelerinin scope/criticality ataması ile başlamalıdır.
- Ardından her aktif MarketProfile için EQX/FTX/OPX/FXX/CRX uygulanabilirlik matrisi üretilmelidir.
- R4 için soru sayısı değil, gerçek maliyetler altında bağımsız ve scope-exact ekonomik kanıt belirleyicidir.

**Son söz:** Bu dosya 900 soruluk denetim yüzeyidir; kârlılık sertifikası değildir.
