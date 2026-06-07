# 贡献指南 | Contributing Guide

## 🇨🇳 中文

### 如何贡献

1. **Fork** 本仓库
2. 创建特性分支 (`git checkout -b feature/your-feature`)
3. 提交修改 (`git commit -m 'feat: 添加XXX功能'`)
4. 推送到分支 (`git push origin feature/your-feature`)
5. 创建 **Pull Request**

### 数据贡献规范

- 所有设备参数库必须使用 `dict[str, dict]` 格式
- 型号名作为 key，参数作为 value
- 必须引用正确的国标/行标编号（最新版本）
- 新增设备必须包含 `standard` 和 `source_note` 字段
- 运行 `python verify_fixes.py` 确保所有验证通过

### 提交信息规范

```
feat: 新增功能
fix: 修复BUG
docs: 文档更新
refactor: 代码重构
test: 测试相关
chore: 构建/工具变更
```

### 国标版本要求

新增设备参数必须引用最新版国标，常见标准版本：

| 标准号 | 最新版本 |
|--------|---------|
| GB/T 6451 | 2023 |
| GB/T 10228 | 2023 |
| GB/T 12706 | 2020 |
| GB/T 1984 | 2024 |
| GB/T 17467 | 2020 |

---

## 🇬🇧 English

### How to Contribute

1. **Fork** this repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'feat: add XXX feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a **Pull Request**

### Data Contribution Guidelines

- All equipment parameter libraries must use `dict[str, dict]` format
- Model name as key, parameters as value
- Must reference correct national/industry standard numbers (latest version)
- New equipment must include `standard` and `source_note` fields
- Operating, planning, life-cycle, and dynamic-limit fields must include a
  `source_type` or `field_source_types` marker. Use `derived_formula` for
  calculated values, `standard_reference` for standards-backed methods, and
  `engineering_policy` for planning defaults.
- See [docs/cnpower_project_guide.md](docs/cnpower_project_guide.md) before
  adding transformer loading, ampacity, endurance, protection-curve, or
  life-cycle data.
- Run `python verify_fixes.py` to ensure all validations pass

### Commit Message Convention

```
feat: new feature
fix: bug fix
docs: documentation update
refactor: code refactoring
test: test related
chore: build/tool changes
```

### National Standard Version Requirements

New equipment parameters must reference the latest version of national standards:

| Standard | Latest Version |
|----------|---------------|
| GB/T 6451 | 2023 |
| GB/T 10228 | 2023 |
| GB/T 1094.7 | 2024 |
| GB/T 1094.11 | 2022 |
| GB/T 12706 | 2020 |
| GB/T 1984 | 2024 |
| GB/T 17467 | 2020 |
| GB 20052 | 2024 |
