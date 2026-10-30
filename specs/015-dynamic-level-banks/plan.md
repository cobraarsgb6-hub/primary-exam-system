# Architectural Plan: 015-dynamic-level-banks
## Phase P14: تعميق بنك الأسئلة وتوسيع مستويات L1 / L2 / L3

### 1. Approach & Design Strategy
لتحقيق كثافة 45 سؤالاً لكل درس دون تحميل مساحة تخزين متضخمة أو إبطاء الأداء:
1. **Hybrid Architecture (Curated Bank + Algorithmic Level Stratification):**
   - الجمع بين الأسئلة المعتمدة التأسيسية عالية الجودة والمدققة بيداغوجياً، ومولدات الأسئلة الديناميكية لمستويات الصعوبة L1/L2/L3.
   - تضمين مصفوفات الأسئلة المعيارية الموسعة في `Code.gs` و `sampleBankWithLevels()` و `tests/e2e/mock_bridge.js`.
2. **Pedagogical Layering:**
   - **Level 1 (Easy / Foundational):** direct definition, standard formula, 1-step logic.
   - **Level 2 (Medium / Application):** multi-step computation, real-world context, rule application.
   - **Level 3 (Hard / Cambridge Challenge):** synthesis, inverse thinking, common misconception traps, experimental data analysis.

### 2. Integration Points
- `Code.gs`: توسيع مصفوفة `sampleBankWithLevels()` وإضافة مولدات التفكير العليا للدروس التي لا تزال دون الـ 45 سؤالاً.
- `mock_bridge.js`: توسيع `serverCatalog` ليدعم التدفق الكامل لجميع المواد بمستوياتها الثلاثة.
- `Index.bundle.html`: إعادة التجميع عبر `bundle.py` لضمان تزامن كافة الأسطح.

### 3. Verification Strategy
- اختبار Node.js مخصص: `tests/dynamicLevelBanks.test.js`
- اختبارات التكامل: `npm test`
